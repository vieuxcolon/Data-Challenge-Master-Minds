## **1. Dataset Overview**

* **Number of rows:** 100,000
* **Number of columns:** 195
* **Numeric columns:** 85
* **Categorical columns:** 68
* **Datetime columns:** 29
* **Total missing cells:** 8,110,518 (~41.6%)
* **Duplicate rows:** 0 (0%)

**Observations:**

* The dataset is **large and heterogeneous**, with many numeric, categorical, and datetime fields.
* High missingness (~42%) is concentrated in operational and passenger flow metrics.
* No duplicate rows, so every record is unique — good for model reliability.

---

## **2. Missing Data Analysis**

Key columns with high missingness (>70%):

| Column                                                                            | Missing % | Notes                                              |
| --------------------------------------------------------------------------------- | --------- | -------------------------------------------------- |
| `LTCtGLastCallDatetime`                                                           | 100%      | Cannot be used unless filled or imputed            |
| `Invoicerevenue`, `InvoiceImputationDate`, `InvoiceDate`, `InvoiceNbOfTouchAndGo` | 100%      | Entirely missing; likely placeholder or incomplete |
| `BusCauseModif`                                                                   | 98.3%     | Very sparse categorical data                       |
| `BusRotationSchedule`, `BusRotationActual`                                        | 97%       | Sparse operational metrics                         |
| `LTCancellationDatetime`                                                          | 96.5%     | Only a small fraction of rows have cancellations   |
| Desk operations (`LTDeskOpenScheduledDatetime`, `LTDeskCloseScheduledDatetime`)   | 73–74%    | Most flights don’t have desk scheduling info       |
| Passenger flow & PIF metrics                                                      | 87–89%    | Sparse PAX scanning metrics                        |

**Implications:**

* Columns with >90% missing are **not useful for modeling** unless external imputation strategies exist.
* Features with 70–90% missing can still be used cautiously with imputation or flag features (missingness itself can be informative).

---

## **3. Outlier Analysis**

Columns with extreme values or high outlier counts:

* **Passenger counts:** `InvoiceNbPaxConnecting` (13,854 outliers), `FarmsNbPaxPHMR` (13,518)
* **Operational timings:** `TurnsBlockTimeMinutes` (large maximum), `DeskDurationMinutes` (negative values present)
* **Delays:** `DelayHBLDurationMinutes` (6,895 outliers), `DelayMainReasonDuration` (2,730 outliers)
* **PAX scanning:** `PxAvgTimeBetweenCheckingPIF`, `PxAvgTimeInTerminal` have negative and extremely high values

**Implications:**

* Numerical columns should be **cleaned or capped** before modeling.
* Negative dwell or time intervals may indicate **data entry errors or missing data encoding**.

---

## **4. Correlation Highlights**

* Very strong correlations detected between operational and passenger metrics:

| Column 1                | Column 2                    | Correlation |
| ----------------------- | --------------------------- | ----------- |
| `InvoiceNbPaxHTransit`  | `InvoiceNbPaxTotal`         | 0.997       |
| `TurnsBlockTimeMinutes` | `InvoicePkgDurationMinutes` | 0.996       |
| `PxScansPIF`            | `PxScansAccPIF`             | 0.992       |
| `NbPax`                 | `NbPaxHTransit`             | 0.992       |

**Implications:**

* High correlation columns can be **reduced to avoid multicollinearity**, e.g., via feature selection or PCA.

---

## **5. Datetime Coverage**

* Data spans from **2020-03-20 → 2027-06-02** across different datetime types.
* Flight and passenger events are mostly in **2023–2026**.
* Some columns like `LTCtGLastCallDatetime` are completely empty.

**Implications:**

* Time-based features are rich but may require **UTC alignment, lag features, and careful handling of missing timestamps**.

---

## **6. Feature Engineering Flags**

| Flag                     | Count / Examples                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| High missing (>30%)      | `IdDelayMainReasonSubcode`, `Counter`, `Conveyor`, `LTCancellationDatetime`, PIF metrics         |
| Low variance (≤2 unique) | `NbFlight`, `AirportCode`, `IdTerminalType`                                                      |
| High cardinality (>100)  | `IdMovementVinci`, `IdFarms`, `IdAircraftType`, `airlineOACICode`, `SysStopover`, `flightNumber` |

**Implications:**

* High missing → consider imputation or dropping.
* Low variance → likely non-informative; candidate for removal.
* High cardinality → requires encoding strategies (target encoding, embeddings, hashing).

---

## **7. Categorical Data Insights**

* Sparse categorical variables (e.g., `BusCauseModif`, `ResponsableModifCtG`) have very high missing or few unique values.
* Frequent categories exist in `DelayMainReason` and `DelayMainReasonSubcode`.

**Implications:**

* Missingness itself can be a **predictive signal**.
* For rare categories, consider **grouping under “Other”** or **frequency encoding**.

---

## **8. Numeric Data Observations**

* Passenger counts, block times, and dwell times have **extreme skew and outliers**.
* PAX scanning intervals sometimes have **negative values**, likely needing **cleaning or capping**.
* Some operational durations are **orders of magnitude higher than typical values** — likely data entry errors.

---

## **9. Recommended Next Steps Before Modeling**

1. **Data Cleaning**

   * Handle negative and extreme numeric values.
   * Decide on strategy for >90% missing columns (drop or impute).

2. **Feature Engineering**

   * Encode high-cardinality categorical variables.
   * Create derived features from timestamps (e.g., flight duration, day-of-week, peak/off-peak).
   * Aggregate or reduce highly correlated columns.

3. **Leakage Detection**

   * Ensure target variables are **not directly derived from future information**.

4. **Outlier Handling**

   * Winsorization or robust scaling for operational metrics and passenger counts.

5. **Modeling Strategy**

   * Mixed data types → tree-based models (XGBoost, LightGBM) or neural networks with embeddings.
   * Missing values → consider using missing indicator features.

---
