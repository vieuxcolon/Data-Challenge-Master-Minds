# =============================================
# PRODUCTION-PROOF PREPROCESSING PIPELINE
# Full Dataset — Actionable Columns
# =============================================

# -------------------------------
# 0️⃣ IMPORTS
# -------------------------------
import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.colab import drive, files

# -------------------------------
# 1️⃣ CONFIGURATION
# -------------------------------
PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_LOCAL_PATH = "/content/va-sdh-adl-staging.json"  # Will upload in Colab
ACTIONS_CSV_URL = "https://raw.githubusercontent.com/vieuxcolon/Data-Challenge-Master-Minds/main/actionable_columns.csv"
CHUNK_SIZE = 50000  # Adjust depending on RAM
DRIVE_SAVE_PATH = "/content/drive/MyDrive/processed_dataset_full.csv"

# -------------------------------
# 2️⃣ AUTHENTICATION
# -------------------------------
# Step 1: Upload service account JSON key if not already in Colab
if not os.path.exists(SERVICE_ACCOUNT_LOCAL_PATH):
    from google.colab import files
    print("Upload the service account JSON key file:")
    files.upload()  # Upload va-sdh-adl-staging.json

# Step 2: Set environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_LOCAL_PATH

# Step 3: Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

# Mount Google Drive
drive.mount('/content/drive', force_remount=True)

# -------------------------------
# 3️⃣ LOAD ACTIONABLE CSV
# -------------------------------
actions_df = pd.read_csv(ACTIONS_CSV_URL)
print(f"Loaded actionable CSV with {len(actions_df)} rows")
display(actions_df.head(5))

# -------------------------------
# 4️⃣ DEFINE BIGQUERY TABLE REF
# -------------------------------
table_ref = f"`{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"

# -------------------------------
# 5️⃣ INITIALIZE DATA AGGREGATES
# -------------------------------
df_final = pd.DataFrame()  # Will collect all chunks
skipped_columns = []

# -------------------------------
# 6️⃣ ITERATE OVER DATA IN CHUNKS
# -------------------------------
query = f"SELECT * FROM {table_ref}"
query_job = client.query(query)

for df_chunk in query_job.result(page_size=CHUNK_SIZE).to_dataframe_iterable(create_bqstorage_client=False):
    # -------------------------------
    # Preprocessing: actionable columns
    # -------------------------------
    new_cols = pd.DataFrame(index=df_chunk.index)
    for idx, row in actions_df.iterrows():
        col = row['Column']
        action = row['Action']

        if col not in df_chunk.columns:
            skipped_columns.append(col)
            continue

        # Encode categorical features
        if "Encode" in action:
            if df_chunk[col].dtype == "object" or df_chunk[col].dtype.name == "category":
                df_chunk[col] = df_chunk[col].astype("category").cat.codes

        # Transform datetime/date/time to numeric features
        if "Transform" in action:
            if pd.api.types.is_datetime64_any_dtype(df_chunk[col]):
                new_cols[col + "_year"] = df_chunk[col].dt.year
                new_cols[col + "_month"] = df_chunk[col].dt.month
                new_cols[col + "_day"] = df_chunk[col].dt.day
                new_cols[col + "_weekday"] = df_chunk[col].dt.weekday
                new_cols[col + "_hour"] = df_chunk[col].dt.hour
                new_cols[col + "_minute"] = df_chunk[col].dt.minute
            elif str(df_chunk[col].dtype) == "time":  # BigQuery TIME
                new_cols[col + "_seconds"] = df_chunk[col].apply(lambda x: x.hour*3600 + x.minute*60 + x.second)
            elif str(df_chunk[col].dtype) == "date":  # BigQuery DATE
                new_cols[col + "_year"] = df_chunk[col].dt.year
                new_cols[col + "_month"] = df_chunk[col].dt.month
                new_cols[col + "_day"] = df_chunk[col].dt.day

    # Concatenate new features (if any)
    if not new_cols.empty:
        df_chunk = pd.concat([df_chunk, new_cols], axis=1)

    # Append chunk to final dataframe
    df_final = pd.concat([df_final, df_chunk], ignore_index=True)
    print(f"Processed chunk: {df_chunk.shape[0]} rows, {df_chunk.shape[1]} columns")

# -------------------------------
# 7️⃣ REPORT SKIPPED COLUMNS
# -------------------------------
if skipped_columns:
    print(f"Skipped {len(skipped_columns)} columns not found in dataset")
    print(skipped_columns)

# -------------------------------
# 8️⃣ SAVE FINAL PROCESSED DATA
# -------------------------------
df_final.to_csv(DRIVE_SAVE_PATH, index=False)
print(f"✅ Full dataset preprocessing completed: {df_final.shape[0]} rows, {df_final.shape[1]} columns")
print(f"Saved to Google Drive at: {DRIVE_SAVE_PATH}")
files.download(DRIVE_SAVE_PATH)
