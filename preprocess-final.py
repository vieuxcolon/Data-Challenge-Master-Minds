# ============================================
# FULL END-TO-END PREPROCESSING + FEATURE ENGINEERING PIPELINE
# ============================================

import pandas as pd
import numpy as np
import os
import hashlib

# -----------------------------
# CONFIGURATION
# -----------------------------
RAW_PATH = '/content/drive/MyDrive/raw_dataset.csv'
PREPROCESSED_PATH = '/content/drive/MyDrive/preprocessed_dataset.csv'
TEMP_DIR = '/content/temp_chunks/'
CHUNK_SIZE = 50000  # Adjust depending on Colab RAM

os.makedirs(TEMP_DIR, exist_ok=True)

# Columns of interest
PAX_COL = 'NbPaxTotal'
PRM_COL = 'FarmsNbPaxPHMR'
CAPACITY_COL = 'NbOfSeats'
DATE_COL = 'LTScheduledDatetime'

# High-cardinality categorical columns to hash
HIGH_CARD_COLS = ['flightNumber', 'CallSign', 'IdMovementVinci', 'IdFarms']

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------

def stable_hash(val):
    """
    What: Convert high-cardinality categorical values into reproducible numeric hashes.
    Why: Prevents memory explosion with one-hot encoding on large datasets.
    How: md5 hash mod 10^8 to produce stable integer.
    """
    return int(hashlib.md5(str(val).encode()).hexdigest(), 16) % (10**8)

def assign_season(date):
    """
    What: Assign seasonal label based on month.
    Why: Captures seasonal passenger patterns.
    How: Winter/ Spring/ Summer/ Fall; 'Unknown' if NaT.
    """
    if pd.isna(date): return "Unknown"
    m = date.month
    if m in [12,1,2]: return "Winter"
    if m in [3,4,5]: return "Spring"
    if m in [6,7,8]: return "Summer"
    if m in [9,10,11]: return "Fall"

# -----------------------------
# STEP 1: CHUNKED PREPROCESSING
# -----------------------------
print("🔹 STEP 1: CHUNKED PREPROCESSING STARTED")
temp_files = []

for i, chunk in enumerate(pd.read_csv(RAW_PATH, chunksize=CHUNK_SIZE)):
    print(f"\n Processing chunk {i} ({len(chunk)} rows)")

    # --- Missing Values ---
    cat_cols = chunk.select_dtypes(include='object').columns.tolist()
    chunk[cat_cols] = chunk[cat_cols].fillna('unknown')
    num_cols = chunk.select_dtypes(include=np.number).columns.tolist()
    chunk[num_cols] = chunk[num_cols].fillna(0)
    print(f" Missing values handled for categorical ({len(cat_cols)}) and numeric ({len(num_cols)}) columns")

    # --- Outlier Clipping ---
    if PAX_COL in chunk.columns and CAPACITY_COL in chunk.columns:
        chunk[PAX_COL] = chunk[PAX_COL].clip(0, chunk[CAPACITY_COL])
    if PRM_COL in chunk.columns:
        chunk[PRM_COL] = chunk[PRM_COL].clip(0, chunk[PAX_COL])
    print(" Outlier clipping applied to PAX and PRM columns")

    # --- Datetime Features ---
    datetime_cols = [col for col in chunk.columns if 'Datetime' in col or 'Date' in col]
    for dt_col in datetime_cols:
        chunk[dt_col] = pd.to_datetime(chunk[dt_col], errors='coerce')
    if DATE_COL in chunk.columns:
        chunk['hour'] = chunk[DATE_COL].dt.hour
        chunk['day_of_week'] = chunk[DATE_COL].dt.dayofweek
        chunk['season'] = chunk[DATE_COL].apply(assign_season)
        holidays = pd.to_datetime([])  # Update with actual holiday dates if available
        chunk['is_holiday'] = chunk[DATE_COL].dt.normalize().isin(holidays)
    print(f" Datetime features created: hour, day_of_week, season, is_holiday")

    # --- Load Factor & PRM Ratio ---
    chunk['load_factor'] = chunk[PAX_COL] / chunk[CAPACITY_COL].replace(0, np.nan)
    chunk['PRM_ratio'] = chunk[PRM_COL] / chunk[PAX_COL].replace(0, np.nan)
    print(" Load factor and PRM ratio calculated (division-by-zero safe)")

    # --- High-Cardinality Hashing ---
    for col in HIGH_CARD_COLS:
        if col in chunk.columns:
            chunk[col] = chunk[col].apply(stable_hash)
    print(f" High-cardinality hashing applied to: {HIGH_CARD_COLS}")

    # --- Save processed chunk ---
    temp_file = os.path.join(TEMP_DIR, f'preprocessing_chunk_{i}.csv')
    chunk.to_csv(temp_file, index=False)
    temp_files.append(temp_file)
    print(f" Chunk {i} saved to {temp_file}")

print("🔹 STEP 1 COMPLETE: All chunks processed and saved")

# -----------------------------
# STEP 2: MERGE CHUNKS
# -----------------------------
print("\n🔹 STEP 2: MERGING CHUNKS")
df_preprocessed = pd.concat([pd.read_csv(f) for f in temp_files], ignore_index=True)
print(f" Merged dataset shape: {df_preprocessed.shape}")

# Clean temp files
for f in temp_files:
    os.remove(f)
print(" Temporary chunk files removed")

# -----------------------------
# STEP 3: ROLLING / HISTORICAL FEATURES
# -----------------------------
print("\n STEP 3: ROLLING / HISTORICAL FEATURES")

df_preprocessed = df_preprocessed.sort_values(['IdMovement', DATE_COL])

# Flight-level rolling features
for window in [7, 30]:
    df_preprocessed[f'mean_pax_last_{window}_flights'] = (
        df_preprocessed.groupby('IdMovement')[PAX_COL]
        .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    )
    df_preprocessed[f'mean_prm_ratio_last_{window}_flights'] = (
        df_preprocessed.groupby('IdMovement')['PRM_ratio']
        .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    )
print(" Flight-level rolling features created (7 & 30 flights, leakage-free)")

# Route-level rolling features
if 'route' not in df_preprocessed.columns:
    df_preprocessed['route'] = df_preprocessed['AirportOrigin'].astype(str) + "_" + df_preprocessed['AirportCode'].astype(str)

for window in [7, 30]:
    df_preprocessed[f'mean_load_factor_route_weekday_last_{window}'] = (
        df_preprocessed.groupby(['route', 'day_of_week'])['load_factor']
        .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    )
print(" Route-level rolling features created (per route × weekday)")

# -----------------------------
# STEP 4: INTERACTION FEATURES
# -----------------------------
print("\n STEP 4: INTERACTION FEATURES")

df_preprocessed['airline_route'] = df_preprocessed['airlineOACICode'].astype(str) + "_" + df_preprocessed['route']
df_preprocessed['hour_terminal'] = df_preprocessed['hour'].astype(str) + "_" + df_preprocessed['Terminal'].astype(str)
df_preprocessed['holiday_destination'] = df_preprocessed['is_holiday'].astype(str) + "_" + df_preprocessed['AirportCode'].astype(str)
print(" Interaction features created: airline_route, hour_terminal, holiday_destination")

# -----------------------------
# STEP 5: TEMPORAL TRAIN/VAL/TEST SPLIT
# -----------------------------
print("\n STEP 5: TEMPORAL TRAIN/VAL/TEST SPLIT")
df_preprocessed = df_preprocessed.sort_values(DATE_COL)
train_end = '2022-12-31'
val_end = '2023-06-30'

train_df = df_preprocessed[df_preprocessed[DATE_COL] <= train_end]
val_df = df_preprocessed[(df_preprocessed[DATE_COL] > train_end) & (df_preprocessed[DATE_COL] <= val_end)]
test_df = df_preprocessed[df_preprocessed[DATE_COL] > val_end]

print(f" Dataset splits:")
print(f"   Train: {train_df.shape}")
print(f"   Validation: {val_df.shape}")
print(f"   Test: {test_df.shape}")

# -----------------------------
# STEP 6: SAVE FINAL DATASETS
# -----------------------------
train_df.to_csv('/content/drive/MyDrive/train_preprocessed.csv', index=False)
val_df.to_csv('/content/drive/MyDrive/val_preprocessed.csv', index=False)
test_df.to_csv('/content/drive/MyDrive/test_preprocessed.csv', index=False)
df_preprocessed.to_csv(PREPROCESSED_PATH, index=False)

print(f" Preprocessing complete. Full dataset saved at: {PREPROCESSED_PATH}")
print("✅ Pipeline finished successfully — all features included and modeling-ready")
