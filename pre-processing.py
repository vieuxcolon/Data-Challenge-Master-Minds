# ================================
# PREPROCESSING PIPELINE (FROM GOOGLE DRIVE)
# ================================

# ============================================
print("\n STEP 1: IMPORT LIBRARIES")
print("What: Import required libraries")
print("Why: Enable data processing and transformations")
print("How: Using pandas, numpy\n")

import pandas as pd
import numpy as np
import time
from google.colab import drive


# ============================================
print("\n STEP 2: LOAD DATA FROM GOOGLE DRIVE")
print("What: Load full raw dataset")
print("Why: Avoid BigQuery and improve speed")
print("How: Mount Drive and read CSV\n")

drive.mount('/content/drive', force_remount=True)

RAW_PATH = "/content/drive/MyDrive/raw_dataset.csv"
OUTPUT_PATH = "/content/drive/MyDrive/processed_dataset_full.csv"

print(" Loading dataset...")
df = pd.read_csv(RAW_PATH)

print(f" Dataset loaded: {df.shape}")


# ============================================
print("\n STEP 3: LOAD PREPROCESSING RULES")
print("What: Load actionable columns configuration")
print("Why: Drive transformation logic")
print("How: Read CSV from GitHub\n")

ACTIONS_CSV_URL = "https://raw.githubusercontent.com/vieuxcolon/Data-Challenge-Master-Minds/main/actionable_columns.csv"

actions_df = pd.read_csv(ACTIONS_CSV_URL)

print(f" Rules loaded: {len(actions_df)}")


# ============================================
print("\n STEP 4: INITIALIZE PROCESSING")
print("What: Prepare variables for transformation")
print("Why: Track progress and results")
print("How: Initialize counters and containers\n")

start_time = time.time()

new_cols = pd.DataFrame(index=df.index)
encoded_count = 0
transformed_count = 0
skipped_columns = []


# ============================================
print("\n STEP 5: APPLY TRANSFORMATIONS")
print("What: Apply encoding and datetime transformations")
print("Why: Convert data into ML-compatible format")
print("How: Loop through actionable rules\n")

for _, row in actions_df.iterrows():

    col = row["Column"]
    action = row["Action"]

    if col not in df.columns:
        skipped_columns.append(col)
        continue

    # ENCODING
    if "Encode" in action:
        if df[col].dtype in ["object", "category"]:
            df[col] = df[col].astype("category").cat.codes
            encoded_count += 1

    # DATETIME
    if "Transform" in action:
        if pd.api.types.is_datetime64_any_dtype(df[col]):

            new_cols[col + "_year"] = df[col].dt.year
            new_cols[col + "_month"] = df[col].dt.month
            new_cols[col + "_day"] = df[col].dt.day
            new_cols[col + "_weekday"] = df[col].dt.weekday
            new_cols[col + "_hour"] = df[col].dt.hour

            transformed_count += 1


# ============================================
print("\n STEP 6: MERGE NEW FEATURES")
print("What: Add transformed features")
print("Why: Enrich dataset for modeling")
print("How: Concatenate dataframes\n")

if not new_cols.empty:
    df = pd.concat([df, new_cols], axis=1)


# ============================================
print("\n STEP 7: FINAL REPORT")
print("What: Summarize preprocessing")
print("Why: Validate transformations")
print("How: Print metrics\n")

elapsed = round(time.time() - start_time, 2)

print(f" Encoded columns: {encoded_count}")
print(f" Datetime transformed: {transformed_count}")
print(f" Skipped columns: {len(skipped_columns)}")
print(f" Execution time: {elapsed}s")
print(f" Final shape: {df.shape}")


# ============================================
print("\n STEP 8: SAVE PROCESSED DATASET")
print("What: Save processed dataset")
print("Why: Enable modeling and reuse")
print("How: Export CSV\n")

df.to_csv(OUTPUT_PATH, index=False)

print(f" Dataset saved at: {OUTPUT_PATH}")
