from google.cloud import bigquery
import pandas as pd
import numpy as np
import os

# -------------------------
# Configuration
# -------------------------
PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_KEY_PATH = "/content/va-sdh-adl-staging.json"

CHUNK_SIZE = 50000  # rows per chunk

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_PATH
client = bigquery.Client(project=PROJECT_ID)

table_ref = f"`{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"

# -------------------------
# Initialize aggregators
# -------------------------
numeric_stats = {}
categorical_counts = {}
missing_counts = {}
datetime_coverage = {}
total_rows = 0

# -------------------------
# BigQuery iterator
# -------------------------
query = f"SELECT * FROM {table_ref}"
query_job = client.query(query)

for page in query_job.result(page_size=CHUNK_SIZE).pages:
    df_chunk = page.to_dataframe()  # no extra arguments
    total_rows += len(df_chunk)

    # -----------------
    # Missing values
    # -----------------
    for col in df_chunk.columns:
        missing_counts[col] = missing_counts.get(col, 0) + df_chunk[col].isnull().sum()

    # -----------------
    # Numeric stats
    # -----------------
    num_cols = df_chunk.select_dtypes(include=[np.number]).columns.tolist()
    for col in num_cols:
        if col not in numeric_stats:
            numeric_stats[col] = {"sum":0, "sum_sq":0, "min":np.inf, "max":-np.inf, "count":0}
        col_data = df_chunk[col].dropna()
        numeric_stats[col]["sum"] += col_data.sum()
        numeric_stats[col]["sum_sq"] += (col_data**2).sum()
        numeric_stats[col]["min"] = min(numeric_stats[col]["min"], col_data.min())
        numeric_stats[col]["max"] = max(numeric_stats[col]["max"], col_data.max())
        numeric_stats[col]["count"] += col_data.count()

    # -----------------
    # Categorical stats
    # -----------------
    cat_cols = df_chunk.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in cat_cols:
        if col not in categorical_counts:
            categorical_counts[col] = {}
        for val, cnt in df_chunk[col].value_counts(dropna=False).items():
            categorical_counts[col][val] = categorical_counts[col].get(val, 0) + cnt

    # -----------------
    # Datetime coverage
    # -----------------
    datetime_cols = df_chunk.select_dtypes(include=["datetime64"]).columns.tolist()
    for col in datetime_cols:
        if col not in datetime_coverage:
            datetime_coverage[col] = {"min": pd.Timestamp.max, "max": pd.Timestamp.min}
        datetime_coverage[col]["min"] = min(datetime_coverage[col]["min"], df_chunk[col].min())
        datetime_coverage[col]["max"] = max(datetime_coverage[col]["max"], df_chunk[col].max())

# -------------------------
# Compile numeric summary
# -------------------------
numeric_summary = []
for col, stats in numeric_stats.items():
    mean = stats["sum"] / stats["count"] if stats["count"] > 0 else None
    variance = (stats["sum_sq"] / stats["count"] - mean**2) if stats["count"] > 0 else None
    std = np.sqrt(variance) if variance is not None else None
    numeric_summary.append({
        "column": col,
        "count": stats["count"],
        "mean": mean,
        "std": std,
        "min": stats["min"],
        "max": stats["max"]
    })
numeric_summary_df = pd.DataFrame(numeric_summary)

# -------------------------
# Compile categorical summary
# -------------------------
categorical_summary = []
for col, counts in categorical_counts.items():
    top_values = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3])
    categorical_summary.append({
        "column": col,
        "unique_count": len(counts),
        "top_values": top_values
    })
categorical_summary_df = pd.DataFrame(categorical_summary)

# -------------------------
# Compile missing value summary
# -------------------------
missing_summary_df = pd.DataFrame({
    "column": list(missing_counts.keys()),
    "missing_count": list(missing_counts.values()),
    "missing_pct": [v/total_rows*100 for v in missing_counts.values()]
}).sort_values(by="missing_pct", ascending=False)

# -------------------------
# Compile datetime coverage summary
# -------------------------
datetime_summary = []
for col, val in datetime_coverage.items():
    datetime_summary.append({
        "column": col,
        "min": val["min"],
        "max": val["max"]
    })
datetime_summary_df = pd.DataFrame(datetime_summary)

# -------------------------
# Save to CSV
# -------------------------
numeric_summary_df.to_csv("numeric_summary_full.csv", index=False)
categorical_summary_df.to_csv("categorical_summary_full.csv", index=False)
missing_summary_df.to_csv("missing_summary_full.csv", index=False)
datetime_summary_df.to_csv("datetime_summary_full.csv", index=False)

print(f"✅ Full dataset profiling completed. Total rows processed: {total_rows}")
