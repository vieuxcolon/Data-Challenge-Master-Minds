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

table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# -------------------------
# Initialize aggregators
# -------------------------
numeric_stats = {}
categorical_counts = {}
missing_counts = {}
datetime_coverage = {}
total_rows = 0

# -------------------------
# Get total number of rows in table
# -------------------------
table = client.get_table(table_ref)
table_rows = table.num_rows
print(f"Total rows in table: {table_rows}")

# -------------------------
# Process in chunks using start_index + max_results
# -------------------------
for start_index in range(0, table_rows, CHUNK_SIZE):
    print(f"Processing rows {start_index} → {min(start_index + CHUNK_SIZE, table_rows)}")

    rows = client.list_rows(
        table_ref,
        start_index=start_index,
        max_results=CHUNK_SIZE
    )

    df_chunk = rows.to_dataframe()

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

print(f"✅ Finished processing {total_rows} rows")
