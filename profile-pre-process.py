# ================================
#  BULLETPROOF DATA PIPELINE (CSV)
# ================================

print("\n STEP 1: MOUNT GOOGLE DRIVE", flush=True)
from google.colab import drive
drive.mount('/content/drive')

DRIVE_PATH = "/content/drive/MyDrive/"

print("\n STEP 2: IMPORT LIBRARIES", flush=True)
import pandas as pd
import numpy as np
from IPython.display import display
import time

print("\n STEP 3: LOAD PROCESSED DATASET", flush=True)
PROCESSED_PATH = DRIVE_PATH + "processed_dataset_full.csv"
df = pd.read_csv(PROCESSED_PATH)
print(f"Dataset loaded: {df.shape}", flush=True)

# ============================================
print("\n STEP 4: BASIC OVERVIEW", flush=True)
print(f"Shape: {df.shape}", flush=True)
print(f"Memory: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB", flush=True)
display(df.head(5))

# ============================================
print("\n STEP 5: TYPE DETECTION", flush=True)
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
print(f"Numerical: {len(num_cols)}", flush=True)
print(f"Categorical: {len(cat_cols)}", flush=True)
print(f"Datetime: {len(datetime_cols)}", flush=True)

# ============================================
print("\n STEP 6: MISSING VALUES", flush=True)
missing_df = pd.DataFrame({
    "missing_count": df.isnull().sum(),
    "missing_pct": df.isnull().mean() * 100
}).sort_values(by="missing_pct", ascending=False)
display(missing_df.head(20))

# ============================================
print("\n STEP 7: DUPLICATES", flush=True)
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates}", flush=True)

# ============================================
print("\n STEP 8: COLUMN SUMMARY", flush=True)
summary_df = pd.DataFrame({
    "column": df.columns,
    "dtype": df.dtypes.astype(str),
    "missing_pct": df.isnull().mean().values * 100,
    "n_unique": df.nunique().values
})
display(summary_df.head(20))

# ============================================
print("\n STEP 9: SAVE PROFILING OUTPUTS", flush=True)
summary_df.to_csv(DRIVE_PATH + "column_summary_processed.csv", index=False)
missing_df.to_csv(DRIVE_PATH + "missing_summary_processed.csv", index=False)

dataset_summary = pd.DataFrame({
    "metric": ["rows", "columns", "duplicates"],
    "value": [len(df), df.shape[1], duplicates]
})
dataset_summary.to_csv(DRIVE_PATH + "dataset_summary_processed.csv", index=False)
print(" Profiling outputs saved to Google Drive", flush=True)
