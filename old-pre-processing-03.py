# ================================
# PREPROCESSING PIPELINE USING ACTIONABLE CSV
# ================================

import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.colab import files
from google.colab import drive

# -------------------------------
# 1️⃣ CONFIGURATION
# -------------------------------
PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_KEY_PATH = "/content/va-sdh-adl-staging.json"
SAMPLE_SIZE = 100000

# GitHub raw URL for actionable CSV
ACTIONS_CSV_URL = "https://raw.githubusercontent.com/vieuxcolon/Data-Challenge-Master-Minds/main/actionable_columns.csv"

# Google Drive save path
drive_save_path = "/content/drive/MyDrive/processed_dataset.csv"

# -------------------------------
# 2️⃣ AUTHENTICATION
# -------------------------------
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_PATH
client = bigquery.Client(project=PROJECT_ID)

# Mount Google Drive
drive.mount('/content/drive')

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
# 5️⃣ PREPROCESSING LOOP
# -------------------------------
for idx, row in actions_df.iterrows():
    col = row['Column']
    action = row['Action']

    if col not in df.columns:
        print(f"⚠️ Column '{col}' not found in dataset, skipping")
        continue

    # Fill missing values if action requires it
    if "Missing Flag" in action:
        flag_col = col + "_missing_flag"
        df[flag_col] = df[col].isnull().astype(int)

    # Encode categorical features
    if "Encode" in action:
        if df[col].dtype == "object" or df[col].dtype.name == "category":
            df[col] = df[col].astype("category").cat.codes

    # Transform datetime/date/time to numeric features
    if "Transform" in action:
        # Handle datetime64
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col + "_year"] = df[col].dt.year
            df[col + "_month"] = df[col].dt.month
            df[col + "_day"] = df[col].dt.day
            df[col + "_weekday"] = df[col].dt.weekday
            df[col + "_hour"] = df[col].dt.hour
            df[col + "_minute"] = df[col].dt.minute
        # Handle time columns (BigQuery TIME)
        elif str(df[col].dtype) == "time":
            df[col + "_seconds"] = df[col].apply(lambda x: x.hour*3600 + x.minute*60 + x.second)
        # Handle date columns (BigQuery DATE)
        elif str(df[col].dtype) == "date":
            df[col + "_year"] = df[col].dt.year
            df[col + "_month"] = df[col].dt.month
            df[col + "_day"] = df[col].dt.day

# -------------------------------
# 6️⃣ SAVE PROCESSED DATA
# -------------------------------
# Save to Google Drive
df.to_csv(drive_save_path, index=False)
print(f"✅ Processed dataset saved to Google Drive at '{drive_save_path}'")

# Optional: download from Colab
files.download(drive_save_path)
