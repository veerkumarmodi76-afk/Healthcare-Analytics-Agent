# Preprocessing Pipeline Validation Report

## Project

**AI-AIP – Healthcare Analytics Agent**

---

# Objective

The objective of the preprocessing pipeline is to transform the raw healthcare insurance dataset into a clean, validated, feature-engineered dataset that can be consumed by all downstream analytical modules including:

* Underwriting
* Pricing
* Lapse Prediction
* Portfolio Analytics
* Executive Dashboard
* AI Copilot

The preprocessing pipeline serves as the foundation of the entire AI-AIP system.

---

# Pipeline Workflow

The preprocessing pipeline executes the following stages sequentially:

```text
Raw Dataset
      │
      ▼
Data Ingestion
      │
      ▼
Data Quality Assessment
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Portfolio Segmentation
      │
      ▼
Processed Dataset
```

Each stage completes before the next stage begins.

---

# Pipeline Execution Summary

Execution Status

**SUCCESS**

Input Dataset

* Rows: **228,711**
* Columns: **42**

Final Processed Dataset

* Rows: **228,711**
* Columns: **52**

New engineered features added:

* Family Size
* Age Band
* Seniority Band
* Premium per Exposure
* Claims per Exposure
* Lapse Binary
* Portfolio Segment
* Portfolio Segment Encoded
* Segment Score
* Age Band Score

The pipeline completed successfully without runtime errors.

---

# Stage 1 — Data Ingestion

Purpose

* Load the raw dataset.
* Validate required schema.
* Verify required columns.
* Generate dataset metadata.

Results

* Dataset loaded successfully.
* Schema validation passed.
* Dataset memory usage calculated.
* Dataset metadata generated.

No missing mandatory columns were detected.

---

# Stage 2 — Data Quality Assessment

Purpose

Evaluate the overall health of the incoming dataset before cleaning.

Checks Performed

* Missing values
* Duplicate records
* Data types
* Outlier detection
* Negative value detection
* Constant column detection
* High missing-value columns

Results

* Quality report generated successfully.
* Four columns exceeded the configured missing-value threshold (>50%).
* No critical validation failures occurred.

Outputs Generated

```text
outputs/preprocessing/
    data_quality_report.csv
```

---

# Stage 3 — Data Cleaning

Purpose

Prepare the dataset for modelling.

Operations Performed

* Duplicate removal
* Date parsing
* Numerical missing-value imputation
* Categorical missing-value imputation
* Text standardization
* Negative value validation

Results

* Duplicate rows removed: **0**
* Missing numerical values successfully imputed.
* Missing categorical values successfully imputed.
* Text values standardized.
* Cleaning completed successfully.

Output Dataset Shape

```text
228711 × 42
```

---

# Stage 4 — Feature Engineering

Purpose

Generate business-oriented features for downstream machine learning models.

Features Created

* Family Size
* Age Band
* Seniority Band
* Premium per Exposure
* Claims per Exposure
* Lapse Binary

Special Handling

Rows with an exposure time of zero were temporarily converted to `NaN` before ratio calculations to prevent divide-by-zero errors.

After feature creation, resulting missing values were replaced with zero to maintain numerical consistency.

Results

* 8,645 zero exposure values handled safely.
* Feature dictionary generated successfully.

Output Dataset Shape

```text
228711 × 48
```

Outputs Generated

```text
outputs/preprocessing/
    feature_dictionary.csv
```

---

# Stage 5 — Portfolio Segmentation

Purpose

Generate business-oriented customer portfolio segments for analytics and reporting.

Segmentation Variables

* Claims per Exposure
* Premium per Exposure
* Age Band
* Family Size

Outputs Created

* Segment Score
* Portfolio Segment
* Portfolio Segment Encoded
* Age Band Score

Portfolio Distribution

| Segment           | Policies |
| ----------------- | -------: |
| Low Exposure      |   57,178 |
| Moderate Exposure |   57,178 |
| High Exposure     |   57,177 |
| Critical Exposure |   57,178 |

The segmentation process produced a balanced portfolio distribution suitable for analytics and visualization.

Output Dataset Shape

```text
228711 × 52
```

Outputs Generated

```text
outputs/preprocessing/
    segmentation_summary.csv
```

---

# Final Outputs

Processed Dataset

```text
data/processed/
    processed_data.csv
```

Supporting Outputs

```text
outputs/preprocessing/
    data_quality_report.csv
    feature_dictionary.csv
    segmentation_summary.csv
```

Pipeline Log

```text
outputs/
    pipeline_log.txt
```

---

# Validation Summary

| Validation Item          | Status |
| ------------------------ | ------ |
| Dataset Loading          | Passed |
| Schema Validation        | Passed |
| Data Quality Assessment  | Passed |
| Duplicate Removal        | Passed |
| Missing Value Handling   | Passed |
| Feature Engineering      | Passed |
| Portfolio Segmentation   | Passed |
| Processed Dataset Export | Passed |

Overall Status

**PASSED**

---

# Logging Improvements

During validation, duplicate informational log messages were observed because both the orchestration module (`preprocess.py`) and individual processing modules logged the same high-level events (for example, dataset loading and feature engineering).

To improve readability, duplicate stage-level log statements were removed from the orchestration layer. Individual modules continue to log their own internal operations, resulting in cleaner and more concise execution logs while preserving detailed processing information.

No functional changes were made to the preprocessing logic; this modification affected logging only.

---

# Conclusion

The preprocessing pipeline successfully transforms the raw healthcare insurance dataset into a validated, standardized, and feature-enriched dataset suitable for all downstream AI-AIP modules.

The pipeline completed without errors, generated all expected intermediate reports, exported the processed dataset successfully, and produced balanced portfolio segmentation. Following the removal of duplicate orchestration log messages, the execution logs are cleaner while maintaining comprehensive operational visibility.

The preprocessing layer is considered stable and ready to support the subsequent Underwriting, Pricing, Lapse Prediction, Portfolio Analytics, Dashboard, and AI Copilot pipelines.
