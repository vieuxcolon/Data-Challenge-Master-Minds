# ================================
#  LOAD RAW DATASET AND SHOW SAMPLE
# ================================

# ============================================
print("\n STEP 1: IMPORT LIBRARIES", flush=True)
import pandas as pd
from google.colab import drive

# ============================================
print("\n STEP 2: MOUNT GOOGLE DRIVE", flush=True)
drive.mount('/content/drive', force_remount=True)

# ============================================
print("\n STEP 3: LOAD RAW DATASET", flush=True)
RAW_PATH = "/content/drive/MyDrive/raw_dataset.csv"
print(f" Loading dataset from: {RAW_PATH}", flush=True)

df = pd.read_csv(RAW_PATH)
print(f" Dataset loaded: {df.shape}", flush=True)

# ============================================
print("\n STEP 4: SHOW FIRST 5 ROWS", flush=True)
display(df.head(5))
