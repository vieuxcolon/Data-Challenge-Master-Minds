# **Pre-processing Specification — Full Dataset**

**Dataset Shape (Full):**

* **Rows:** 364,545
* **Columns:** 195
* **Numeric columns:** 81
* **Categorical columns:** 86
* **Datetime columns:** 28
* **Total missing cells:** 29,428,590 (~41.4%)
* **Duplicate rows:** 0 (0%)

---

## **1. Columns Pre-processing Overview**

| Step              | Pre-processing Type                 | Columns Impacted                         | Number of Columns | Strategy                                                                   |
| ----------------- | ----------------------------------- | ---------------------------------------- | ----------------- | -------------------------------------------------------------------------- |
| 1                 | **Drop Unnecessary Columns**        | Columns with no information / irrelevant | 12                | Removed completely from dataset                                            |
| 2                 | **High-Correlation Removal**        | Numeric columns with correlation > 0.95  | 9                 | Remove to prevent multicollinearity                                        |
| 3                 | **Low-Variance Removal**            | Columns with ≤1 unique value             | 3                 | Remove non-informative features                                            |
| 4                 | **Missing Value Imputation**        | Columns with missing values              | 78                | Numeric → median; Categorical → “UNKNOWN”; **no new missing-flag columns** |
| 5                 | **Categorical Encoding**            | Categorical columns                      | 86                | In-place label encoding (no new columns)                                   |
| 6                 | **Datetime Feature Transformation** | Datetime/date/time columns               | 28                | Year, month, day, weekday, hour, minute; numeric features added in-place   |
| **Final Dataset** | —                                   | —                                        | **~171 columns**  | Compact, production-ready, fully engineered                                |

> ⚡ **Note:** No new missing-flag columns are added, keeping the feature matrix compact while still handling missing values robustly.

---

## **2. Detailed Pre-processing Strategy**

### **2.1 Drop Columns**

* Remove completely irrelevant or placeholder columns.
* Example: `LTCtGLastCallDatetime` (entirely missing), others with no operational value.
  **Columns dropped:** 12

### **2.2 Remove Highly Correlated Columns**

* Threshold: correlation > 0.95 (absolute value).
* Purpose: reduce multicollinearity for ML models.
  **Columns removed:** 9

### **2.3 Remove Low-Variance Columns**

* Threshold: ≤1 unique value.
* Purpose: remove non-informative features.
  **Columns removed:** 3

### **2.4 Missing Value Handling (In-place)**

* Numeric: impute missing values using **median**.
* Categorical: impute missing values using `"UNKNOWN"`.
* **No new columns are added**.
  **Columns impacted:** 78

### **2.5 Categorical Encoding**

* Convert categorical columns to **numeric codes** in-place.
* Enables tree-based and ML algorithms to process categorical features efficiently.
  **Columns impacted:** 86

### **2.6 Datetime / Date / Time Transformation**

* Extract numeric features: year, month, day, weekday, hour, minute.
* Numeric transformation is added **in-place**, no extra missing flags.
  **Columns impacted:** 28

---

## **3. Final Dataset Summary**

| Metric                                          | Value                                  |
| ----------------------------------------------- | -------------------------------------- |
| Total rows                                      | 364,545                                |
| Total columns before pre-processing             | 195                                    |
| Total columns dropped                           | 12 + 9 + 3 = 24                        |
| Total columns added via datetime transformation | 28 × ~5 numeric features = ~140?*      |
| Total columns after pre-processing              | ~171 (compact, no missing flags added) |
| Numeric columns                                 | 81                                     |
| Categorical columns                             | 86                                     |
| Datetime-derived numeric columns                | 28                                     |
| Missing values handled                          | 78 columns imputed in-place            |

*Datetime transformations are added **in-place**, replacing original datetime columns, so the total column count remains approximately 195. The dataset remains compact and fully engineered for production.

---

## **4. Key Benefits of the Updated Strategy**

1. **Compact Feature Matrix** – No redundant missing-flag columns.
2. **Robust Missing Handling** – All missing values are imputed in-place.
3. **ML-Ready** – Categorical encoding, numeric transformations, and datetime features handled.
4. **Low Risk of Multicollinearity** – High-correlation columns removed.
5. **Full Dataset Coverage** – Works on all 364,545 rows and 195 columns.
6. **Production-Ready** – Ready for pipelines feeding XGBoost, LightGBM, or neural networks.

---
