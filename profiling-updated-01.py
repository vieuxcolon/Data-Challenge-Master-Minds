# ============================================
# FULL DATA PROFILING PIPELINE WITH PRM METRICS + SUMMARY TABLES
# ============================================

import pandas as pd
import numpy as np

# ============================================
# STEP 0: CONFIGURATION
# ============================================

# Dataset path & chunk size
FILE_PATH = "/content/drive/MyDrive/raw_dataset.csv"
CHUNK_SIZE = 50000

# Column mapping (DO NOT CHANGE — works with your dataset)
PRM_COL = "FarmsNbPaxPHMR"     
CAPACITY_COL = "NbOfSeats"     
PAX_COL = "NbPaxTotal"         
TARGET_COL = "NbPaxTotal"      
DATE_COL = "LTScheduledDatetime"  
FLIGHT_TYPE_COL = "flight_type"   

# ============================================
# STEP 1: INITIALIZE STORAGE FOR CHUNKED PROCESSING
# ============================================

print(" Initializing storage structures...")
total_rows = 0
missing_counts = None
unique_counts = {}
numeric_cols = None
sample_chunks = []

# ============================================
# STEP 2: CHUNKED DATA LOADING + SAMPLING
# ============================================

print(" Reading dataset in chunks...")
reader = pd.read_csv(FILE_PATH, chunksize=CHUNK_SIZE, low_memory=False)

for i, chunk in enumerate(reader):
    print(f"➡ Processing chunk {i+1} (rows: {len(chunk)})...")
    total_rows += len(chunk)

    # Track missing counts
    if missing_counts is None:
        missing_counts = chunk.isnull().sum()
        numeric_cols = chunk.select_dtypes(include=np.number).columns.tolist()
    else:
        missing_counts += chunk.isnull().sum()

    # Track unique counts (approximate, memory-safe)
    for col in chunk.columns:
        unique_counts[col] = unique_counts.get(col, 0) + chunk[col].nunique()

    # Take 10% sample from each chunk for profiling
    sample_chunks.append(chunk.sample(frac=0.1))

# ============================================
# STEP 3: BUILD SAMPLE DATAFRAME
# ============================================

df_sample = pd.concat(sample_chunks, ignore_index=True)
print(f" Sample dataframe created: {df_sample.shape}")

# ============================================
# STEP 4: MISSINGNESS & UNIQUE COUNTS
# ============================================

print(" Computing missing values and unique counts...")

missing_pct = (missing_counts / total_rows) * 100
summary = pd.DataFrame({
    "column": missing_counts.index,
    "missing_pct": missing_pct.values,
    "n_unique": [unique_counts[col] for col in missing_counts.index]
})

summary.to_csv("/content/drive/MyDrive/summary.csv", index=False)
print(" summary.csv saved")

#  Additional summary: top 10 columns by missing %
missing_top10 = summary.sort_values("missing_pct", ascending=False).head(10)
missing_top10.to_csv("/content/drive/MyDrive/summary_top10_missing.csv", index=False)
print(" summary_top10_missing.csv saved")

# ============================================
# STEP 5: DATETIME & TEMPORAL PROFILING
# ============================================

print(" Profiling datetime columns...")

df_sample[DATE_COL] = pd.to_datetime(df_sample[DATE_COL], errors="coerce")
datetime_cols = [col for col in df_sample.columns if "Datetime" in col or "Date" in col]

temporal_summary = []
for col in datetime_cols:
    temp_series = pd.to_datetime(df_sample[col], errors="coerce")
    n_missing = temp_series.isna().sum()
    n_unique = temp_series.nunique()
    min_date = temp_series.min()
    max_date = temp_series.max()
    temporal_summary.append({
        "column": col,
        "n_missing": n_missing,
        "missing_pct": n_missing / len(df_sample) * 100,
        "n_unique": n_unique,
        "min_date": min_date,
        "max_date": max_date,
        "date_range_days": (max_date - min_date).days if pd.notnull(min_date) and pd.notnull(max_date) else None
    })

temporal_df = pd.DataFrame(temporal_summary).sort_values(by="missing_pct", ascending=False)
temporal_df.to_csv("/content/drive/MyDrive/temporal_summary.csv", index=False)
print(" temporal_summary.csv saved")

#  Additional summary: earliest and latest dates
temporal_top_dates = temporal_df[["column","min_date","max_date"]].sort_values("min_date")
temporal_top_dates.to_csv("/content/drive/MyDrive/temporal_top_dates.csv", index=False)
print(" temporal_top_dates.csv saved")

# ============================================
# STEP 6: TARGET CORRELATION
# ============================================

print(" Computing correlation with target...")

valid_num_cols = [col for col in numeric_cols if df_sample[col].nunique() > 10 and not col.lower().startswith("id")]
corr_matrix = df_sample[valid_num_cols].corr()

if TARGET_COL in df_sample.columns:
    target_corr = corr_matrix[TARGET_COL].sort_values(ascending=False)
    target_corr.to_csv("/content/drive/MyDrive/target_correlation.csv")
    print(" target_correlation.csv saved")

    #  Additional summary: top 10 correlations with target
    top10_corr = target_corr.head(10).reset_index()
    top10_corr.columns = ["feature", "corr_with_target"]
    top10_corr.to_csv("/content/drive/MyDrive/top10_target_corr.csv", index=False)
    print(" top10_target_corr.csv saved")
else:
    target_corr = None
    print(f" TARGET_COL '{TARGET_COL}' not found — skipping correlation")

# ============================================
# STEP 7: MULTI-COLLINEARITY
# ============================================

print("🔗 Checking multicollinearity (corr > 0.9)...")

high_corr_pairs = []
for i, col1 in enumerate(valid_num_cols):
    for col2 in valid_num_cols[i+1:]:
        corr = corr_matrix.loc[col1, col2]
        if abs(corr) > 0.9:
            high_corr_pairs.append((col1, col2, corr))

high_corr_df = pd.DataFrame(high_corr_pairs, columns=["f1", "f2", "corr"])
high_corr_df.to_csv("/content/drive/MyDrive/multicollinearity.csv", index=False)
print(" multicollinearity.csv saved")

#  Additional summary: number of highly correlated pairs
high_corr_summary = pd.DataFrame([{"num_high_corr_pairs": len(high_corr_df)}])
high_corr_summary.to_csv("/content/drive/MyDrive/high_corr_summary.csv", index=False)
print(" high_corr_summary.csv saved")

# ============================================
# STEP 8: OUTLIER DETECTION
# ============================================

print("⚠ Detecting outliers using IQR method...")

outlier_summary = {}
for col in valid_num_cols:
    q1 = df_sample[col].quantile(0.25)
    q3 = df_sample[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = ((df_sample[col] < lower) | (df_sample[col] > upper)).mean()
    outlier_summary[col] = outliers

outlier_df = pd.DataFrame.from_dict(outlier_summary, orient="index", columns=["outlier_pct"])
outlier_df.to_csv("/content/drive/MyDrive/outliers.csv")
print(" outliers.csv saved")

#  Additional summary: top 10 outlier columns
outlier_top10 = outlier_df.sort_values("outlier_pct", ascending=False).head(10)
outlier_top10.to_csv("/content/drive/MyDrive/outliers_top10.csv")
print(" outliers_top10.csv saved")

# ============================================
# STEP 9: FEATURE SCORING
# ============================================

print(" Computing feature scores...")

feature_scores = []
for col in summary["column"]:
    score = 0
    missing = summary.loc[summary["column"] == col, "missing_pct"].values[0]
    unique = summary.loc[summary["column"] == col, "n_unique"].values[0]

    if missing < 30: score += 1
    if unique < 1000: score += 1
    if col in valid_num_cols: score += 1
    if target_corr is not None and col in target_corr.index:
        if abs(target_corr[col]) > 0.3: score += 1
        if abs(target_corr[col]) > 0.9: score -= 2
    feature_scores.append((col, score))

feature_scores_df = pd.DataFrame(feature_scores, columns=["feature", "score"])
feature_scores_df.to_csv("/content/drive/MyDrive/feature_scores.csv", index=False)
print(" feature_scores.csv saved")

#  Additional summary: top 10 features by score
feature_top10 = feature_scores_df.sort_values("score", ascending=False).head(10)
feature_top10.to_csv("/content/drive/MyDrive/feature_scores_top10.csv", index=False)
print(" feature_scores_top10.csv saved")

# ============================================
# STEP 10: OPERATIONAL & PRM METRICS
# ============================================

print("✈️ Computing PRM metrics and load factors...")

# Safety check
for col in [PRM_COL, CAPACITY_COL, PAX_COL]:
    if col not in df_sample.columns:
        raise ValueError(f"Missing column: {col}")

df_sample[PRM_COL] = df_sample[PRM_COL].fillna(0)
df_sample[CAPACITY_COL] = df_sample[CAPACITY_COL].replace(0, np.nan)

df_sample["load_factor"] = df_sample[PAX_COL] / df_sample[CAPACITY_COL]
df_sample["PRM_load_factor"] = df_sample[PRM_COL] / df_sample[CAPACITY_COL]

def assign_season(date):
    if pd.isna(date): return "Unknown"
    m = date.month
    if m in [12,1,2]: return "Winter"
    if m in [3,4,5]: return "Spring"
    if m in [6,7,8]: return "Summer"
    if m in [9,10,11]: return "Fall"

df_sample["season"] = df_sample[DATE_COL].apply(assign_season)

# Holiday flag (empty, customize)
holidays = pd.to_datetime([])
df_sample["is_holiday"] = df_sample[DATE_COL].dt.normalize().isin(holidays)

agg_funcs = {
    TARGET_COL: ["mean","median","std"],
    PRM_COL: ["mean","median","std"],
    "load_factor": "mean",
    "PRM_load_factor": "mean",
    CAPACITY_COL: "mean",
}

# Season summary
season_summary = df_sample.groupby("season").agg(agg_funcs).reset_index()
season_summary.to_csv("/content/drive/MyDrive/season_summary.csv", index=False)
print(" season_summary.csv saved")

# Holiday summary
holiday_summary = df_sample.groupby("is_holiday").agg(agg_funcs).reset_index()
holiday_summary.to_csv("/content/drive/MyDrive/holiday_summary.csv", index=False)
print(" holiday_summary.csv saved")

# Flight type summary
if FLIGHT_TYPE_COL in df_sample.columns:
    flight_type_summary = df_sample.groupby(FLIGHT_TYPE_COL).agg(agg_funcs).reset_index()
    flight_type_summary.to_csv("/content/drive/MyDrive/flight_type_summary.csv", index=False)
    print(" flight_type_summary.csv saved")

# Combined summary
combined_group_cols = ["season","is_holiday"]
if FLIGHT_TYPE_COL in df_sample.columns:
    combined_group_cols.append(FLIGHT_TYPE_COL)

combined_summary = df_sample.groupby(combined_group_cols).agg(agg_funcs).reset_index()
combined_summary.to_csv("/content/drive/MyDrive/combined_summary.csv", index=False)
print(" combined_summary.csv saved")

#  Additional summary: mean load factor by season
season_load_summary = df_sample.groupby("season")[["load_factor","PRM_load_factor"]].mean().reset_index()
season_load_summary.to_csv("/content/drive/MyDrive/season_load_summary.csv", index=False)
print(" season_load_summary.csv saved")

print("✅ FULL PROFILING COMPLETE")
