# ================================
#  BULLETPROOF DATA PIPELINE
# ================================

# ============================================
print("\n STEP 1: MOUNT GOOGLE DRIVE", flush=True)
print("What: Connect Colab to Google Drive", flush=True)
print("Why: Persist dataset and avoid re-downloading", flush=True)
print("How: Using drive.mount()\n", flush=True)

from google.colab import drive
drive.mount('/content/drive')

DRIVE_PATH = "/content/drive/MyDrive/"


# ============================================
print("\n STEP 2: IMPORT LIBRARIES", flush=True)
print("What: Import required libraries", flush=True)
print("Why: Enable data processing and BigQuery access", flush=True)
print("How: Using pandas, numpy, BigQuery client\n", flush=True)

import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from IPython.display import display
import time


# ============================================
print("\n STEP 3: CONFIGURATION", flush=True)
print("What: Define project parameters", flush=True)
print("Why: Centralize pipeline configuration", flush=True)
print("How: Set project, dataset, table, credentials\n", flush=True)

PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_KEY_PATH = "/content/va-sdh-adl-staging.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_PATH

table_ref = f"`{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"


# ============================================
print("\n STEP 4: CONNECT TO BIGQUERY", flush=True)
print("What: Initialize BigQuery client", flush=True)
print("Why: Required to execute queries", flush=True)
print("How: Using google.cloud.bigquery.Client\n", flush=True)

client = bigquery.Client(project=PROJECT_ID)


# ============================================
print("\n STEP 5: EXECUTE QUERY (SAFE MODE)", flush=True)
print("What: Run full dataset query", flush=True)
print("Why: Load dataset once for full pipeline", flush=True)
print("How: Submit job → wait → download\n", flush=True)

query = f"SELECT * FROM {table_ref}"

start_time = time.time()

query_job = client.query(query)

print(" Query submitted to BigQuery. Waiting for execution...", flush=True)

query_job.result()  # wait for completion

print(" Query finished. Downloading data...", flush=True)

df = query_job.to_dataframe(create_bqstorage_client=False)

print(f" Dataset loaded: {df.shape}", flush=True)
print(f" Load time: {time.time() - start_time:.2f} seconds", flush=True)


# ============================================
print("\n STEP 6: SAVE RAW DATASET", flush=True)
print("What: Save full dataset to Google Drive", flush=True)
print("Why: Avoid future BigQuery calls", flush=True)
print("How: Using pandas to_csv()\n", flush=True)

RAW_PATH = DRIVE_PATH + "raw_dataset.csv"
df.to_csv(RAW_PATH, index=False)

print(f" Dataset saved at: {RAW_PATH}", flush=True)


# ============================================
print("\n STEP 7: BASIC OVERVIEW", flush=True)

print(f"Shape: {df.shape}", flush=True)
print(f"Memory: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB", flush=True)

display(df.head(5))


# ============================================
print("\n STEP 8: TYPE DETECTION", flush=True)

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

print(f"Numerical: {len(num_cols)}", flush=True)
print(f"Categorical: {len(cat_cols)}", flush=True)
print(f"Datetime: {len(datetime_cols)}", flush=True)


# ============================================
print("\n STEP 9: MISSING VALUES", flush=True)

missing_df = pd.DataFrame({
    "missing_count": df.isnull().sum(),
    "missing_pct": df.isnull().mean() * 100
}).sort_values(by="missing_pct", ascending=False)

display(missing_df.head(20))


# ============================================
print("\n STEP 10: DUPLICATES", flush=True)

duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates}", flush=True)


# ============================================
print("\n STEP 11: COLUMN SUMMARY", flush=True)

summary_df = pd.DataFrame({
    "column": df.columns,
    "dtype": df.dtypes.astype(str),
    "missing_pct": df.isnull().mean().values * 100,
    "n_unique": df.nunique().values
})

display(summary_df.head(20))


# ============================================
print("\n STEP 12: SAVE PROFILING OUTPUTS", flush=True)

summary_df.to_csv(DRIVE_PATH + "column_summary.csv", index=False)
missing_df.to_csv(DRIVE_PATH + "missing_summary.csv", index=False)

dataset_summary = pd.DataFrame({
    "metric": ["rows", "columns", "duplicates"],
    "value": [len(df), df.shape[1], duplicates]
})

dataset_summary.to_csv(DRIVE_PATH + "dataset_summary.csv", index=False)



print(" Profiling outputs saved to Google Drive", flush=True)
