# ============================================
# Full Dataset Profiling in Chunks
# ============================================

from google.cloud import bigquery
import pandas as pd
import numpy as np

# Configuration
PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_KEY_PATH = "/content/va-sdh-adl-staging.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_PATH
client = bigquery.Client(project=PROJECT_ID)

table_ref = f"`{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"

# Batch size
CHUNK_SIZE = 50000  # adjust depending on your RAM

# Initialize aggregates
numeric_stats = {}
categorical_counts = {}
total_rows = 0

# BigQuery iterator
query = f"SELECT * FROM {table_ref}"
query_job = client.query(query)

# Iterate over rows in batches
for df_chunk in query_job.result(page_size=CHUNK_SIZE).to_dataframe_iterable(create_bqstorage_client=False):
    total_rows += len(df_chunk)

    # Numeric statistics
    num_cols = df_chunk.select_dtypes(include=[np.number]).columns.tolist()
    for col in num_cols:
        if col not in numeric_stats:
            numeric_stats[col] = {
                "sum": 0, "sum_sq": 0, "min": np.inf, "max": -np.inf, "count": 0
            }
        col_data = df_chunk[col].dropna()
        numeric_stats[col]["sum"] += col_data.sum()
        numeric_stats[col]["sum_sq"] += (col_data**2).sum()
        numeric_stats[col]["min"] = min(numeric_stats[col]["min"], col_data.min())
        numeric_stats[col]["max"] = max(numeric_stats[col]["max"], col_data.max())
        numeric_stats[col]["count"] += col_data.count()

    # Categorical counts (top values)
    cat_cols = df_chunk.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in cat_cols:
        if col not in categorical_counts:
            categorical_counts[col] = {}
        for val, cnt in df_chunk[col].value_counts(dropna=False).items():
            categorical_counts[col][val] = categorical_counts[col].get(val, 0) + cnt

# ============================================
# Compute final numeric stats
# ============================================
final_numeric_summary = []
for col, stats in numeric_stats.items():
    mean = stats["sum"] / stats["count"]
    variance = (stats["sum_sq"] / stats["count"]) - mean**2
    std = np.sqrt(variance)
    final_numeric_summary.append({
        "column": col,
        "mean": mean,
        "std": std,
        "min": stats["min"],
        "max": stats["max"],
        "count": stats["count"]
    })

numeric_summary_df = pd.DataFrame(final_numeric_summary)
print("Numeric summary computed for full dataset.")

# ============================================
# Compute categorical top values
# ============================================
final_cat_summary = []
for col, counts in categorical_counts.items():
    top_values = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3])
    final_cat_summary.append({
        "column": col,
        "top_values": top_values,
        "unique_count": len(counts)
    })

categorical_summary_df = pd.DataFrame(final_cat_summary)
print("Categorical summary computed for full dataset.")

# Save final profiling outputs
numeric_summary_df.to_csv("numeric_summary_full.csv", index=False)
categorical_summary_df.to_csv("categorical_summary_full.csv", index=False)

print(f"✅ Full dataset profiling completed. Total rows processed: {total_rows}")
