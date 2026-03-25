# ================================
#  FULL DATA PROFILING PIPELINE (PRODUCTION VERSION)
# ================================

# ============================================
print("\n STEP 1: IMPORTING LIBRARIES")
print("What: Import required Python libraries")
print("Why: Needed for data processing and BigQuery access")
print("How: Using pandas, numpy, BigQuery client\n")

import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from IPython.display import display
from google.colab import drive


# ============================================
print("\n STEP 2: CONFIGURATION")
print("What: Define project and dataset parameters")
print("Why: Centralize pipeline configuration")
print("How: Set project ID, dataset, table, credentials\n")

PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_KEY_PATH = "/content/va-sdh-adl-staging.json"

DRIVE_PATH = "/content/drive/MyDrive/"


# ============================================
print("\n STEP 3: AUTHENTICATION & CONNECTION")
print("What: Authenticate and connect to BigQuery")
print("Why: Required to access remote dataset")
print("How: Using service account credentials\n")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_PATH
client = bigquery.Client(project=PROJECT_ID)

table_ref = f"`{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"


# ============================================
print("\n STEP 4: LOAD FULL DATASET")
print("What: Load entire dataset from BigQuery")
print("Why: Use once for profiling + save locally")
print("How: SQL SELECT without LIMIT\n")

query = f"""
SELECT *
FROM {table_ref}
"""

print(" Querying full dataset (this may take a few minutes)...")

df = client.query(query).to_dataframe(create_bqstorage_client=False)

print(f" Full dataset loaded: {df.shape}")


# ============================================
print("\n STEP 5: MOUNT GOOGLE DRIVE")
print("What: Mount Google Drive")
print("Why: Save dataset and outputs for reuse")
print("How: Using drive.mount()\n")

drive.mount('/content/drive', force_remount=True)


# ============================================
print("\n STEP 6: SAVE RAW DATASET")
print("What: Save full raw dataset")
print("Why: Avoid future BigQuery queries")
print("How: Export CSV to Google Drive\n")

RAW_PATH = DRIVE_PATH + "raw_dataset.csv"

df.to_csv(RAW_PATH, index=False)

print(f" Raw dataset saved at: {RAW_PATH}")


# ============================================
print("\n STEP 7: BASIC DATA OVERVIEW")
print("What: Inspect dataset shape and memory usage")
print("Why: Understand dataset size and cost")
print("How: Using pandas methods\n")

print(f"Shape: {df.shape}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")

display(df.dtypes.value_counts())


# ============================================
print("\n STEP 8: COLUMN TYPE DETECTION")

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

print(f"Numerical: {len(num_cols)}")
print(f"Categorical: {len(cat_cols)}")
print(f"Datetime: {len(datetime_cols)}")


# ============================================
print("\n STEP 9: MISSING VALUES")

missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100

missing_df = pd.DataFrame({
    "missing_count": missing,
    "missing_pct": missing_pct
}).sort_values(by="missing_pct", ascending=False)

display(missing_df.head(30))


# ============================================
print("\n STEP 10: CORRELATION ANALYSIS")

if len(num_cols) > 1:
    corr_matrix = df[num_cols].corr()
    corr_unstacked = corr_matrix.abs().unstack().sort_values(ascending=False)
    corr_unstacked = corr_unstacked[corr_unstacked < 1]
    display(corr_unstacked.head(20))


# ============================================
print("\n STEP 11: DUPLICATES")

duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates}")


# ============================================
print("\n STEP 12: COLUMN SUMMARY")

summary_data = []

for col in df.columns:
    summary_data.append({
        "column": col,
        "dtype": str(df[col].dtype),
        "n_unique": df[col].nunique(),
        "missing_pct": df[col].isnull().mean() * 100,
    })

summary_df = pd.DataFrame(summary_data)
display(summary_df.head(30))


# ============================================
print("\n STEP 13: SAVE PROFILING OUTPUTS")

summary_df.to_csv(DRIVE_PATH + "column_summary.csv", index=False)
missing_df.to_csv(DRIVE_PATH + "missing_summary.csv", index=False)

dataset_summary = pd.DataFrame({
    "metric": ["rows", "columns", "duplicates"],
    "value": [len(df), df.shape[1], duplicates]
})

dataset_summary.to_csv(DRIVE_PATH + "dataset_summary.csv", index=False)

print(" Profiling outputs saved to Google Drive:")
print("  - column_summary.csv")
print("  - missing_summary.csv")
print("  - dataset_summary.csv")
