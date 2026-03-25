# ============================================
# PRODUCTION-PROOF PREPROCESSING PIPELINE
# ============================================

import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.colab import drive, files
import os

# -------------------------------
# 1️⃣ CONFIGURATION
# -------------------------------
PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_KEY_PATH = "/content/va-sdh-adl-staging.json"
ACTIONS_CSV_URL = "https://raw.githubusercontent.com/vieuxcolon/Data-Challenge-Master-Minds/main/actionable_columns.csv"
DRIVE_SAVE_PATH = "/content/drive/MyDrive/processed_dataset.csv"

# -------------------------------
# 2️⃣ AUTHENTICATION
# -------------------------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_PATH
client = bigquery.Client(project=PROJECT_ID)

# Mount Google Drive
drive.mount('/content/drive', force_remount=True)

# -------------------------------
# 3️⃣ LOAD FULL DATA FROM BIGQUERY
# -------------------------------
query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
df = client.query(query).to_dataframe(create_bqstorage_client=False)
print(f"Loaded full dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# -------------------------------
# 4️⃣ LOAD ACTIONABLE CSV
# -------------------------------
actions_df = pd.read_csv(ACTIONS_CSV_URL)
print(f"Loaded actionable CSV with {len(actions_df)} rows")
display(actions_df.head(5))

# -------------------------------
# 5️⃣ PREPROCESSING LOOP
# -------------------------------
# Initialize storage for engineered features (replacing originals where appropriate)
for idx, row in actions_df.iterrows():
    col = row['Column']
    action = row['Action']

    if col not in df.columns:
        continue  # skip missing columns in dataset

    # ----------------------
    # 5a. Missing values imputation (in-place)
    # ----------------------
    if "Missing Flag" in action:
        # Instead of adding a new column, fill missing values directly
        if df[col].dtype in [np.float64, np.int64]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("UNKNOWN")

    # ----------------------
    # 5b. Categorical Encoding
    # ----------------------
    if "Encode" in action:
        if df[col].dtype == "object" or df[col].dtype.name == "category":
            # Label encoding in-place
            df[col] = df[col].astype("category").cat.codes

    # ----------------------
    # 5c. Datetime / Date / Time Transformation
    # ----------------------
    if "Transform" in action:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype('datetime64[ns]')
            df[col + "_year"] = df[col].dt.year
            df[col + "_month"] = df[col].dt.month
            df[col + "_day"] = df[col].dt.day
            df[col + "_weekday"] = df[col].dt.weekday
            df[col + "_hour"] = df[col].dt.hour
            df[col + "_minute"] = df[col].dt.minute
        elif str(df[col].dtype) == "time":  # TIME type
            df[col] = df[col].apply(lambda x: x.hour*3600 + x.minute*60 + x.second)
        elif str(df[col].dtype) == "date":  # DATE type
            df[col] = df[col].astype('datetime64[ns]')
            df[col + "_year"] = df[col].dt.year
            df[col + "_month"] = df[col].dt.month
            df[col + "_day"] = df[col].dt.day

# -------------------------------
# 6️⃣ REMOVE HIGHLY CORRELATED / LOW VARIANCE COLUMNS
# -------------------------------
# Example thresholds, adjust based on prior profiling
HIGH_CORR_THRESHOLD = 0.95
LOW_VARIANCE_THRESHOLD = 1  # single-valued columns

# Remove low variance
low_var_cols = [col for col in df.columns if df[col].nunique() <= LOW_VARIANCE_THRESHOLD]
df.drop(columns=low_var_cols, inplace=True)

# Remove high correlation columns (pairwise)
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr_matrix = df[numeric_cols].corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
high_corr_cols = [col for col in upper.columns if any(upper[col] > HIGH_CORR_THRESHOLD)]
df.drop(columns=high_corr_cols, inplace=True)

# -------------------------------
# 7️⃣ FINAL CHECKS
# -------------------------------
df.fillna(0, inplace=True)  # fill remaining missing values, if any
print(f"✅ Preprocessing completed. Final dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")

# -------------------------------
# 8️⃣ SAVE TO DRIVE
# -------------------------------
df.to_csv(DRIVE_SAVE_PATH, index=False)
print(f"✅ Processed dataset saved to Google Drive at '{DRIVE_SAVE_PATH}'")
files.download(DRIVE_SAVE_PATH)
