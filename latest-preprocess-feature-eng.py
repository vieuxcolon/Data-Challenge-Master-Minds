# ================================
# BULLETPROOF DATA PIPELINE
# ================================

# ============================================
# STEP 1: MOUNT GOOGLE DRIVE
# ============================================
from google.colab import drive
drive.mount('/content/drive')
DRIVE_PATH = "/content/drive/MyDrive/"

# ============================================
# STEP 2: IMPORT LIBRARIES
# ============================================
import os
import pandas as pd
import numpy as np
import time
from IPython.display import display
from pandas_profiling import ProfileReport

# ============================================
# STEP 3: LOAD RAW DATASET
# ============================================
RAW_PATH = DRIVE_PATH + "raw_dataset.csv"
print("Loading raw dataset...")
start_time = time.time()
df = pd.read_csv(RAW_PATH, low_memory=False)
print(f"Raw dataset loaded: {df.shape}")
print(f"Load time: {time.time() - start_time:.2f}s")

# ============================================
# STEP 4: DROP HIGH-MISSING COLUMNS (>90%)
# ============================================
high_missing_cols = df.columns[df.isnull().mean() > 0.9].tolist()
df.drop(columns=high_missing_cols, inplace=True)
print(f"Dropped high-missing columns (>90%): {len(high_missing_cols)}")

# ============================================
# STEP 5: HANDLE MISSING VALUES
# ============================================
num_cols = df.select_dtypes(include=[np.number]).columns
cat_cols = df.select_dtypes(include=['object', 'category']).columns

# Fill numeric columns with median
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Fill categorical columns with 'UNKNOWN'
for col in cat_cols:
    df[col] = df[col].fillna("UNKNOWN")

# ============================================
# STEP 6: DATETIME TRANSFORMATION
# ============================================
datetime_cols = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
for col in datetime_cols:
    try:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    except Exception as e:
        print(f"Warning converting {col} to datetime: {e}")

# Convert datetime columns to numeric cyclic features
for col in datetime_cols:
    if df[col].dtype == 'datetime64[ns]':
        df[col + "_year"] = df[col].dt.year
        df[col + "_month"] = df[col].dt.month
        df[col + "_day"] = df[col].dt.day
        df[col + "_weekday"] = df[col].dt.weekday
        df[col + "_hour"] = df[col].dt.hour
        # cyclic transformations
        df[col + "_hour_sin"] = np.sin(2 * np.pi * df[col + "_hour"] / 24)
        df[col + "_hour_cos"] = np.cos(2 * np.pi * df[col + "_hour"] / 24)
        df[col + "_month_sin"] = np.sin(2 * np.pi * df[col + "_month"] / 12)
        df[col + "_month_cos"] = np.cos(2 * np.pi * df[col + "_month"] / 12)

# ============================================
# STEP 7: LOW-VARIANCE AND HIGHLY CORRELATED REMOVAL
# ============================================
# Remove low variance columns (<=1 unique value)
low_var_cols = [c for c in df.columns if df[c].nunique() <= 1]
df.drop(columns=low_var_cols, inplace=True)

# Remove highly correlated numeric columns (>0.95)
corr_matrix = df.corr().abs()
upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
high_corr_cols = [c for c in upper_tri.columns if any(upper_tri[c] > 0.95)]
df.drop(columns=high_corr_cols, inplace=True)

# ============================================
# STEP 8: FEATURE ENGINEERING
# ============================================
# Example: rolling mean of last 7 days passengers per flight (requires flight_id & datetime)
if 'IdFlight' in df.columns and 'FlightDate' in df.columns:
    df = df.sort_values(['IdFlight', 'FlightDate'])
    df['passengers_last_7'] = df.groupby('IdFlight')['Passengers'].rolling(7, min_periods=1).mean().reset_index(0, drop=True)

# Additional engineered features can be added here as needed

# ============================================
# STEP 9: SAVE PROCESSED + FEATURE ENGINEERED DATASET
# ============================================
PROCESSED_PATH = DRIVE_PATH + "processed_featured_dataset.csv"
df.to_csv(PROCESSED_PATH, index=False)
print(f"Processed dataset saved at: {PROCESSED_PATH}")

# ============================================
# STEP 10: DATA PROFILING (NEW)
# ============================================
print("Generating profiling report...")
profile = ProfileReport(df, title="Flight Passenger Dataset Profiling", explorative=True)
PROFILE_PATH = DRIVE_PATH + "processed_featured_dataset_profile.html"
profile.to_file(PROFILE_PATH)
print(f"Profiling report saved at: {PROFILE_PATH}")

# ============================================
# STEP 11: DISPLAY FIRST 5 ROWS
# ============================================
print("First 5 rows of preprocessed + feature engineered dataset:")
display(df.head())
print(f"Final dataset shape: {df.shape}")
