# ================================
# PREPROCESSING PIPELINE USING ACTIONABLE CSV (Optimized)
# ================================

import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.colab import files, drive
import os

# -------------------------------
# 1️⃣ CONFIGURATION
# -------------------------------
PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_KEY_PATH = "/content/va-sdh-adl-staging.json"
SAMPLE_SIZE = 100000
ACTIONS_CSV_URL = "https://raw.githubusercontent.com/vieuxcolon/Data-Challenge-Master-Minds/main/actionable_columns.csv"
drive_save_path = "/content/drive/MyDrive/processed_dataset.csv"

# -------------------------------
# 2️⃣ AUTHENTICATION
# -------------------------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_PATH
client = bigquery.Client(project=PROJECT_ID)

# Mount Google Drive
drive.mount('/content/drive', force_remount=True)

# -------------------------------
# 3️⃣ LOAD DATA SAMPLE FROM BIGQUERY
# -------------------------------
query = f"""
SELECT *
FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
LIMIT {SAMPLE_SIZE}
"""
df = client.query(query).to_dataframe(create_bqstorage_client=False)
print(f"Loaded sample: {df.shape[0]} rows, {df.shape[1]} columns")

# -------------------------------
# 4️⃣ LOAD ACTIONABLE CSV
# -------------------------------
actions_df = pd.read_csv(ACTIONS_CSV_URL)
print(f"Loaded actionable CSV with {len(actions_df)} rows")
display(actions_df.head(5))

# -------------------------------
# 5️⃣ PREPROCESSING LOOP (Optimized)
# -------------------------------
new_cols = pd.DataFrame(index=df.index)  # Collect new columns here
skipped_cols = []

for idx, row in actions_df.iterrows():
    col = row['Column']
    action = row['Action']

    if col not in df.columns:
        skipped_cols.append(col)
        continue

    # Fill missing values if action requires it
    if "Missing Flag" in action:
        new_cols[col + "_missing_flag"] = df[col].isnull().astype(int)

    # Encode categorical features
    if "Encode" in action:
        if df[col].dtype == "object" or df[col].dtype.name == "category":
            df[col] = df[col].astype("category").cat.codes

    # Transform datetime/date/time to numeric features
    if "Transform" in action:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            new_cols[col + "_year"] = df[col].dt.year
            new_cols[col + "_month"] = df[col].dt.month
            new_cols[col + "_day"] = df[col].dt.day
            new_cols[col + "_weekday"] = df[col].dt.weekday
            new_cols[col + "_hour"] = df[col].dt.hour
            new_cols[col + "_minute"] = df[col].dt.minute
        elif str(df[col].dtype) == "time":  # BigQuery TIME
            new_cols[col + "_seconds"] = df[col].apply(lambda x: x.hour*3600 + x.minute*60 + x.second)
        elif str(df[col].dtype) == "date":  # BigQuery DATE
            new_cols[col + "_year"] = df[col].dt.year
            new_cols[col + "_month"] = df[col].dt.month
            new_cols[col + "_day"] = df[col].dt.day

# Concatenate all new columns at once to prevent fragmentation
if not new_cols.empty:
    df = pd.concat([df, new_cols], axis=1).copy()
    print(f"✅ Added {new_cols.shape[1]} new columns. Total columns now: {df.shape[1]}")

# Report skipped columns
if skipped_cols:
    print(f" Skipped {len(skipped_cols)} columns not found in dataset.")
    print(skipped_cols)

# -------------------------------
# 6️⃣ SAVE PROCESSED DATA
# -------------------------------
df.to_csv(drive_save_path, index=False)
print(f"✅ Processed dataset saved to Google Drive at '{drive_save_path}'")
files.download(drive_save_path)
