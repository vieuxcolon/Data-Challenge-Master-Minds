# =============================================
# PRODUCTION-PROOF PREPROCESSING PIPELINE
# Full Dataset — Actionable Columns
# Fully Annotated with Semantics
# =============================================

# -------------------------------
# 0️. IMPORTS
# -------------------------------
import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.colab import drive, files

print(" Libraries imported: pandas, numpy, BigQuery, Google Drive")

# -------------------------------
# 1️. CONFIGURATION
# -------------------------------
PROJECT_ID = "va-sdh-adl-staging"  # GCP Project
DATASET_ID = "aero_insa"           # BigQuery Dataset
TABLE_ID = "mouvements_aero_insa"  # BigQuery Table
SERVICE_ACCOUNT_LOCAL_PATH = "/content/va-sdh-adl-staging.json"  # Colab service account key path
ACTIONS_CSV_URL = "https://raw.githubusercontent.com/vieuxcolon/Data-Challenge-Master-Minds/main/actionable_columns.csv"
CHUNK_SIZE = 50000                 # Load in manageable chunks to avoid RAM overflow
DRIVE_SAVE_PATH = "/content/drive/MyDrive/processed_dataset_full.csv"  # Output path

print(f"🔧 Configuration set: Project={PROJECT_ID}, Dataset={DATASET_ID}, Table={TABLE_ID}")

# -------------------------------
# 2️. AUTHENTICATION
# -------------------------------

# Step 1: Upload the JSON key if not already in Colab
if not os.path.exists(SERVICE_ACCOUNT_LOCAL_PATH):
    from google.colab import files
    print("⚠️ Service account key not found. Please upload va-sdh-adl-staging.json")
    files.upload()  # User manually uploads

# Step 2: Set environment variable for Google authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_LOCAL_PATH
print(f" GOOGLE_APPLICATION_CREDENTIALS set to {SERVICE_ACCOUNT_LOCAL_PATH}")

# Step 3: Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)
print(" BigQuery client initialized successfully")

# Step 4: Mount Google Drive to save processed dataset
drive.mount('/content/drive', force_remount=True)
print(" Google Drive mounted at /content/drive")

# -------------------------------
# 3️. LOAD ACTIONABLE CSV
# -------------------------------

# Load actionable columns which specify the preprocessing strategy per column
actions_df = pd.read_csv(ACTIONS_CSV_URL)
print(f"📄 Loaded actionable columns CSV with {len(actions_df)} rows")
display(actions_df.head(5))

# -------------------------------
# 4️. DEFINE BIGQUERY TABLE REFERENCE
# -------------------------------
table_ref = f"`{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
print(f"📌 Table reference defined: {table_ref}")

# -------------------------------
# 5️. INITIALIZE AGGREGATES
# -------------------------------

df_final = pd.DataFrame()  # Will accumulate processed chunks
skipped_columns = []       # Track columns in CSV but not in BigQuery table
print("🛠 Initialized empty dataframe for final processed dataset")

# -------------------------------
# 6️. ITERATE OVER BIGQUERY TABLE IN CHUNKS
# -------------------------------
query = f"SELECT * FROM {table_ref}"
query_job = client.query(query)

print(f" Querying full table in chunks of {CHUNK_SIZE} rows")

for df_chunk in query_job.result(page_size=CHUNK_SIZE).to_dataframe_iterable(create_bqstorage_client=False):

    print(f"\n Processing new chunk: {df_chunk.shape[0]} rows, {df_chunk.shape[1]} columns")

    new_cols = pd.DataFrame(index=df_chunk.index)  # Collect new features per chunk

    # -------------------------------
    # 6a️⃣ APPLY ACTIONS TO EACH COLUMN
    # -------------------------------
    for idx, row in actions_df.iterrows():
        col = row['Column']
        action = row['Action']

        # Skip columns not in dataset
        if col not in df_chunk.columns:
            skipped_columns.append(col)
            continue

        # Categorical encoding: convert text to integer codes
        if "Encode" in action:
            if df_chunk[col].dtype == "object" or df_chunk[col].dtype.name == "category":
                df_chunk[col] = df_chunk[col].astype("category").cat.codes
                print(f" Encoded categorical column: {col}")

        # Datetime transformation: extract numeric components
        if "Transform" in action:
            if pd.api.types.is_datetime64_any_dtype(df_chunk[col]):
                new_cols[col + "_year"] = df_chunk[col].dt.year
                new_cols[col + "_month"] = df_chunk[col].dt.month
                new_cols[col + "_day"] = df_chunk[col].dt.day
                new_cols[col + "_weekday"] = df_chunk[col].dt.weekday
                new_cols[col + "_hour"] = df_chunk[col].dt.hour
                new_cols[col + "_minute"] = df_chunk[col].dt.minute
                print(f" Transformed datetime column: {col}")
            elif str(df_chunk[col].dtype) == "time":
                new_cols[col + "_seconds"] = df_chunk[col].apply(lambda x: x.hour*3600 + x.minute*60 + x.second)
                print(f"⏱ Transformed TIME column: {col}")
            elif str(df_chunk[col].dtype) == "date":
                new_cols[col + "_year"] = df_chunk[col].dt.year
                new_cols[col + "_month"] = df_chunk[col].dt.month
                new_cols[col + "_day"] = df_chunk[col].dt.day
                print(f" Transformed DATE column: {col}")

    # -------------------------------
    # 6b️⃣ CONCATENATE NEW FEATURES
    # -------------------------------
    if not new_cols.empty:
        df_chunk = pd.concat([df_chunk, new_cols], axis=1)
        print(f" Added {new_cols.shape[1]} new features from datetime transformations")

    # -------------------------------
    # 6c️⃣ APPEND CHUNK TO FINAL DATAFRAME
    # -------------------------------
    df_final = pd.concat([df_final, df_chunk], ignore_index=True)
    print(f" Chunk processed. Accumulated dataset shape: {df_final.shape[0]} rows, {df_final.shape[1]} columns")

# -------------------------------
#  REPORT SKIPPED COLUMNS
# -------------------------------
if skipped_columns:
    print(f"\n Skipped {len(skipped_columns)} columns not found in dataset:")
    print(skipped_columns)
else:
    print("\n All columns from actionable CSV found in dataset")

# -------------------------------
# 8️ SAVE FINAL PROCESSED DATA
# -------------------------------
df_final.to_csv(DRIVE_SAVE_PATH, index=False)
print(f" Full dataset preprocessing completed successfully!")
print(f" Final dataset shape: {df_final.shape[0]} rows, {df_final.shape[1]} columns")
print(f" Dataset saved to Google Drive at: {DRIVE_SAVE_PATH}")

# Optional: download to local machine
files.download(DRIVE_SAVE_PATH)
