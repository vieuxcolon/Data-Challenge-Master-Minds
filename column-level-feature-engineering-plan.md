## **1. Numeric Features**

**Goals:** Handle outliers, skew, missing values, and scaling.

| Column Example / Group                                                                           | Issue / Flag                                | Recommended Strategy                                                                                                                   |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `TurnsBlockTimeMinutes`, `DeskDurationMinutes`, `DelayMainReasonDuration`, `PxAvgTimeInTerminal` | Outliers, negative values, high missingness | Cap extreme values (winsorization), replace negatives with NaN if invalid, scale using robust scaler or log-transform skewed variables |
| `InvoiceNbPaxTotal`, `InvoiceNbPaxHTransit`, `FarmsNbPaxPHMR`                                    | High correlation & outliers                 | Consider aggregation (sum/mean), normalization; optionally create per-flight ratios                                                    |
| PAX scan metrics (`PxScansPIF`, `PxAvgTimeBetweenPIFCtG`, `PxScansGAT`)                          | Sparse, negative, and skewed                | Impute missing with median or 0 if meaningful; log-transform; create “scanned / total PAX” ratio                                       |
| Low variance numeric (e.g., `NbFlight`)                                                          | Almost constant                             | Drop unless categorical encoding is meaningful                                                                                         |

**General Actions:**

* Impute missing numeric values using **median or domain-informed value**.
* Flag missing values with indicator columns to preserve information.
* Standardize or scale as needed for models sensitive to magnitude (e.g., neural networks).

---

## **2. Categorical Features**

**Goals:** Encode high-cardinality features, handle sparse and missing categories.

| Column Example / Group                                                            | Issue / Flag                        | Recommended Strategy                                                                      |
| --------------------------------------------------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------- |
| `IdMovementVinci`, `IdFarms`, `IdAircraftType`, `flightNumber`, `airlineOACICode` | High cardinality (>100)             | Use **target encoding**, **frequency encoding**, or embeddings (for deep learning models) |
| `IdTerminalType`, `NbFlight`, `AirportCode`                                       | Low variance (≤2 unique)            | Likely drop or treat as binary flags if meaningful                                        |
| `DelayMainReason`, `DelayMainReasonSubcode`                                       | Sparse with few frequent categories | One-hot encode frequent categories, group rare categories under “Other”                   |
| `ResponsableModifCtG`, `BusCauseModif`                                            | High missing                        | Fill with “Missing” category, optionally create missing indicator                         |
| Airports (`AirportOrigin`, `AirportPrevious`)                                     | High cardinality                    | Frequency or embedding encoding; optionally group by hub/region                           |

**General Actions:**

* Always **encode missing as a separate category** when missingness is high (>30%).
* Consider **hierarchical encoding**: e.g., airline → aircraft type → flight number.

---

## **3. Datetime Features**

**Goals:** Derive temporal patterns, handle missing values, and calculate intervals.

| Column Example / Group                                             | Issue / Flag        | Recommended Strategy                                                                           |
| ------------------------------------------------------------------ | ------------------- | ---------------------------------------------------------------------------------------------- |
| `LTDeskOpenScheduledDatetime`, `LTDeskCloseScheduledDatetime`      | 73–74% missing      | Impute missing as NaT; create **duration features** (close-open)                               |
| `LTCtGDynamicDatetime`, `LTCtGInitialDatetime`, `LTRunwayDatetime` | 89–98% missing      | Compute **intervals**: e.g., “arrival to check-in”, “check-in to PIF”, “bag delivery duration” |
| `InvoiceDate`, `LTExternalDate`                                    | Some missing        | Extract **year, month, day, weekday, hour** as features                                        |
| `PxAvgTimeBetween*`                                                | Negative and sparse | Treat negative as missing; compute derived ratios with other time columns                      |

**Derived Features Examples:**

* Flight durations, bag processing durations, check-in to boarding intervals
* Day-of-week, month, holiday/weekend flags
* Lag/rolling features for operational efficiency or congestion prediction

---

## **4. High Missing Columns (>90%)**

* Columns like `LTCancellationDatetime`, `BusCauseModif`, `BusRotationSchedule`, `InvoiceRevenue`
  **Strategy:**
* Drop unless domain-specific imputation is possible
* Alternatively, create **binary missingness flag** if missing itself is informative

---

## **5. Operational & Aggregate Features**

* Combine related columns for robustness:

  * `PxScans*` → total scans per passenger or flight
  * `Turns*` → total turnaround time, taxi time ratios
  * Desk durations → average per flight or per terminal

* Consider **ratios**: e.g., PAX scanned / total PAX, delayed PAX / total PAX, bag delivered / total bag

---

## **6. Outlier & Error Handling**

* Negative times and durations → replace with NaN or domain-imputed value
* Extremely high values → winsorize at 99th percentile or cap based on domain knowledge
* Keep missing indicators to capture **operational anomalies**

---

## **7. Feature Flags Recap**

* **High missing (>30%)**: Create flags
* **Low variance (≤2 unique)**: Drop or keep as binary flag
* **High cardinality (>100)**: Use embedding/frequency/target encoding

---

## **8. Suggested Preprocessing Pipeline**

1. **Numeric:** Impute → Cap outliers → Scale/log-transform
2. **Categorical:** Impute → Encode (target/frequency/one-hot)
3. **Datetime:** Impute → Extract features → Compute intervals
4. **Missing Flags:** Add indicator columns
5. **Derived Aggregates:** Operational totals, ratios, durations

---

## **Model-Ready Dataset Blueprint**

### **1. Numeric Features**

| Column                                                                                                             | Action                                                  | Reasoning                                                            |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- | -------------------------------------------------------------------- |
| `TurnsBlockTimeMinutes`, `DeskDurationMinutes`, `DelayMainReasonDuration`, `PxAvgTimeInTerminal`, `PxAvgDwellTime` | Keep, impute missing, cap outliers, scale/log-transform | Important operational metrics; some have negative/outlier values     |
| `TurnsBlockDays`, `TurnsRealTaxiTimeMinutes`                                                                       | Keep, impute missing, scale                             | Low outliers, operational durations                                  |
| `PxScans*` (`PxScansPIF`, `PxScansGAT`, `PxScansCKN`, etc.)                                                        | Keep, impute missing as 0, optionally create ratios     | Passenger scan counts; negatives replaced as missing                 |
| `NbFlight`, `NbCounter`, `NbConveyor`, `FarmsNbPaxConnecting`                                                      | Keep, impute missing, optionally log-transform          | Low variance may exist but operational relevance justifies inclusion |
| Low variance numerics (`DeskDurationMinutes` negative extreme, `TurnsBlockDays`)                                   | Keep if domain important; else drop                     | Rare but may indicate outliers/errors                                |

**Notes:**

* Missing values → median or domain-informed
* Outliers → winsorize or clip at 1st/99th percentile

---

### **2. Categorical Features**

| Column                                                                                                                                   | Action                                                        | Reasoning                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------- |
| High cardinality (`IdMovementVinci`, `IdFarms`, `IdAircraftType`, `flightNumber`, `airlineOACICode`, `AirportOrigin`, `AirportPrevious`) | Encode: target/frequency/embedding                            | Preserve info without exploding dimensionality |
| Low cardinality / binary (`IdTerminalType`, `NbFlight`)                                                                                  | One-hot or leave as-is                                        | No scaling needed                              |
| Sparse / missing (`DelayMainReason`, `DelayMainReasonSubcode`, `ResponsableModifCtG`)                                                    | Fill missing as `"Missing"`, optionally group rare categories | Missingness may be informative                 |
| Medium cardinality (`ServiceCode`, `IdBusContactType`)                                                                                   | One-hot encode frequent categories                            | Avoid high-dimensional sparse encoding         |

**Notes:**

* Keep missing indicators for features with >30% missing
* Consider hierarchical encoding for airports → airline → flight numbers

---

### **3. Datetime Features**

| Column                                                                                                                                                                                  | Action                                                                | Reasoning                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------- |
| Scheduled/Actual times (`LTDeskOpenScheduledDatetime`, `LTDeskCloseScheduledDatetime`, `LTRunwayDatetime`, `LTCtG*Datetime`, `LTFirstBagDeliveryDatetime`, `LTLastBagDeliveryDatetime`) | Keep → compute derived intervals: durations, delays, time differences | Most have high missing; intervals more informative |
| Time-only features (`LTScheduledTime`, `LTExternalTime`)                                                                                                                                | Extract hour, minute, AM/PM flags                                     | Capture operational patterns                       |
| Date-only features (`LTDeskOpenScheduledDate`, `LTDeskCloseScheduledDate`)                                                                                                              | Extract day-of-week, month, weekend/holiday                           | Temporal patterns for delays, throughput           |

**Derived Feature Examples:**

* Bag delivery duration: `LTLastBagDeliveryDatetime - LTFirstBagDeliveryDatetime`
* Turnaround times: `TurnsBlockTimeMinutes` / `TurnsBlockDays`
* Check-in to boarding duration: `PxAvgTimeBetweenPIFCtG`

---

### **4. Columns to Drop or Use Cautiously**

| Column                                                             | Reasoning                                                          |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `BusCauseModif`, `BusRotationSchedule`, `BusRotationActual`        | High missingness (~98%)                                            |
| `InvoiceRevenue`, `InvoiceNbPax*`                                  | If target modeling unrelated to financials, optional; high missing |
| Extremely low variance numeric (`NbFlight` with 1–2 unique values) | Minimal predictive value                                           |
| Some text/object columns (`DelayMainReasonComment`)                | Sparse, unstructured; requires NLP if used                         |

---

### **5. Missing Value Handling Strategy**

* **>30% missing** → create missing flag + optional imputation
* **Numeric** → median or domain-informed value
* **Categorical** → fill `"Missing"` or group rare categories

---

### **6. Feature Engineering Recommendations**

* **Numeric ratios:** PAX scanned / total PAX, bag delivered / total bag
* **Time intervals:** Turnaround times, bag processing duration, check-in to boarding times
* **Temporal flags:** Day-of-week, weekend/weekday, hour-of-day, month, holidays
* **Aggregates per flight/terminal:** Sum/average of PAX, durations, scans

---

### **7. Column-Level Summary**

**Keep with transformation:**

* `TurnsBlockTimeMinutes`, `DeskDurationMinutes`, `PxAvg*`, `PxScans*`, `LT*Datetime`

**Encode / Transform:**

* `Id*`, `flightNumber`, `airlineOACICode`, `AirportOrigin/Previous`

**Drop / Optional:**

* `BusCauseModif`, `InvoiceRevenue`, `DelayMainReasonComment`

**Missing flags:**

* Columns >30% missing like `LTCancellationDatetime`, `LTFirstBagDeliveryDatetime`

---

**Summary:**
Prepares for a **clean, model-ready dataset**, balances missing values, encodes categorical and datetime features properly, and ensures numeric outliers are addressed. It also preserves operational and temporal patterns essential for predicting delays, bag handling, or PAX flow.

---





Do you want me to create that next?
