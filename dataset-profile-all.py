# ================================
# FULL DATA PROFILING PIPELINE (FULL DATASET)
# ================================

# ============================================
# STEP 1: IMPORT LIBRARIES
# ============================================
import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from IPython.display import display
from google.colab import files

# ============================================
# STEP 2: CONFIGURATION
# ============================================
PROJECT_ID = "va-sdh-adl-staging"
DATASET_ID = "aero_insa"
TABLE_ID = "mouvements_aero_insa"
SERVICE_ACCOUNT_KEY_PATH = "/content/va-sdh-adl-staging.json"

CHUNK_SIZE = 50000  # rows per chunk, adjust for RAM

# ============================================
# STEP 3: AUTHENTICATION
# ============================================
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_PATH
client = bigquery.Client(project=PROJECT_ID)
table_ref = f"`{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"

# ============================================
# STEP 4: LOAD FULL DATA IN CHUNKS
# ============================================
print(f"Loading full dataset in chunks of {CHUNK_SIZE} rows...")
query = f"SELECT * FROM {table_ref}"  # no LIMIT
query_job = client.query(query)
row_iter = query_job.result()

dfs = []
total_rows = 0

for page in row_iter.pages:
    df_chunk = pd.DataFrame([dict(row) for row in page])
    dfs.append(df_chunk)
    total_rows += len(df_chunk)
    print(f"Processed {total_rows} rows so far...")

df = pd.concat(dfs, ignore_index=True)
print(f"\n✅ Finished loading full dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# ============================================
# STEP 5: BASIC DATA OVERVIEW
# ============================================
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
display(df.dtypes.value_counts())
display(df.head(10))

# ============================================
# STEP 6: COLUMN TYPE DETECTION
# ============================================
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
bool_cols = df.select_dtypes(include=["bool"]).columns.tolist()

print(f"Numerical: {len(num_cols)}, Categorical: {len(cat_cols)}, Datetime: {len(datetime_cols)}, Boolean: {len(bool_cols)}")

# ============================================
# STEP 7: MISSING VALUES ANALYSIS
# ============================================
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct}).sort_values(by="missing_pct", ascending=False)
display(missing_df.head(30))

# ============================================
# STEP 8: NUMERICAL STATISTICS
# ============================================
if len(num_cols) > 0:
    num_stats = df[num_cols].describe().T
    num_stats["skew"] = df[num_cols].skew()
    num_stats["kurtosis"] = df[num_cols].kurtosis()
    display(num_stats.head(30))

# ============================================
# STEP 9: CORRELATION ANALYSIS
# ============================================
if len(num_cols) > 1:
    corr_matrix = df[num_cols].corr()
    corr_unstacked = corr_matrix.abs().unstack().sort_values(ascending=False)
    corr_unstacked = corr_unstacked[corr_unstacked < 1]
    display(corr_unstacked.head(20))

# ============================================
# STEP 10: DUPLICATES
# ============================================
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates} ({duplicates/len(df)*100:.2f}%)")

# ============================================
# STEP 11: OUTLIER DETECTION (IQR)
# ============================================
outlier_summary = {}
for col in num_cols[:30]:  # limit to first 30 numerical columns
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
    outlier_summary[col] = len(outliers)

outlier_df = pd.DataFrame.from_dict(outlier_summary, orient='index', columns=["outlier_count"])
display(outlier_df.sort_values(by="outlier_count", ascending=False).head(20))

# ============================================
# STEP 12: DATETIME ANALYSIS
# ============================================
for col in datetime_cols:
    print(f"{col}: {df[col].min()} → {df[col].max()}")

# ============================================
# STEP 13: COLUMN SUMMARY
# ============================================
summary_data = []

for col in df.columns:
    col_data = df[col]
    summary = {
        "column": col,
        "dtype": str(col_data.dtype),
        "n_unique": col_data.nunique(),
        "missing_count": col_data.isnull().sum(),
        "missing_pct": col_data.isnull().mean() * 100,
    }
    is_numeric = pd.api.types.is_numeric_dtype(col_data)
    is_bool = pd.api.types.is_bool_dtype(col_data)

    if is_numeric and not is_bool:
        try:
            clean_col = pd.to_numeric(col_data, errors='coerce')
            summary.update({
                "mean": clean_col.mean(),
                "std": clean_col.std(),
                "min": clean_col.min(),
                "25%": clean_col.quantile(0.25),
                "50%": clean_col.quantile(0.5),
                "75%": clean_col.quantile(0.75),
                "max": clean_col.max(),
                "skew": clean_col.skew(),
            })
        except:
            summary.update({k: None for k in ["mean","std","min","25%","50%","75%","max","skew"]})
    else:
        summary.update({k: None for k in ["mean","std","min","25%","50%","75%","max","skew"]})

    try:
        if col_data.dtype == "object" or col_data.dtype.name == "category":
            summary["top_values"] = str(col_data.value_counts().head(3).to_dict())
        else:
            summary["top_values"] = None
    except:
        summary["top_values"] = None

    summary_data.append(summary)

summary_df = pd.DataFrame(summary_data).sort_values(by="missing_pct", ascending=False)
display(summary_df.head(50))

# ============================================
# STEP 14: DATASET SUMMARY
# ============================================
dataset_summary = {
    "n_rows": len(df),
    "n_columns": df.shape[1],
    "total_missing_cells": df.isnull().sum().sum(),
    "missing_percentage_total": df.isnull().sum().sum() / (df.shape[0]*df.shape[1]) * 100,
    "n_numeric_cols": len(num_cols),
    "n_categorical_cols": len(cat_cols),
    "n_datetime_cols": len(datetime_cols),
    "n_duplicate_rows": duplicates,
}
dataset_summary_df = pd.DataFrame(dataset_summary.items(), columns=["metric", "value"])
display(dataset_summary_df)

# ============================================
# STEP 15: FEATURE FLAGS
# ============================================
flags = []
for col in df.columns:
    n_unique = df[col].nunique()
    missing_pct = df[col].isnull().mean() * 100
    flags.append({
        "column": col,
        "high_missing (>30%)": missing_pct > 30,
        "low_variance (<=2 unique)": n_unique <= 2,
        "high_cardinality (>100)": n_unique > 100,
    })
flags_df = pd.DataFrame(flags)
display(flags_df.head(50))

# ============================================
# STEP 16: SAVE OUTPUTS
# ============================================
df.to_csv("raw_dataset_full.csv", index=False)
summary_df.to_csv("column_summary.csv", index=False)
dataset_summary_df.to_csv("dataset_summary.csv", index=False)
flags_df.to_csv("feature_flags.csv", index=False)
print("✅ All outputs saved locally")

# Optional: download files in Colab
files.download("raw_dataset_full.csv")
files.download("column_summary.csv")
files.download("dataset_summary.csv")
files.download("feature_flags.csv")
