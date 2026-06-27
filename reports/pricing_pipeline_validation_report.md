# Pricing Pipeline Validation Report

## Project

**AI-AIP – Healthcare Analytics Agent**

---

# Objective

The Pricing Pipeline estimates the expected healthcare claim cost for every policyholder and converts those estimates into business-ready premium recommendations. It integrates machine learning with underwriting decisions to support actuarial pricing, portfolio management, dashboard analytics, reporting, and AI-powered business insights.

The pricing module consumes the processed insurance dataset and underwriting outputs, applies a trained regression model to estimate future claim costs, and then calculates recommended premiums using configurable business loading factors, expense loadings, and profit margins.

---

# Pipeline Workflow

```text
Processed Dataset
        │
        ▼
Feature Validation
        │
        ▼
Model Training
        │
        ▼
Expected Claim Cost Prediction
        │
        ▼
Merge with Underwriting Decisions
        │
        ▼
Premium Calculation
        │
        ▼
Business Rule Validation
        │
        ▼
Portfolio Summary
        │
        ▼
Pricing Report Generation
```

Each stage completes successfully before the next stage begins.

---

# Pipeline Execution Summary

Execution Status

**SUCCESS**

Input Dataset

* Rows: **228,711**
* Columns: **52**

Model

* Algorithm: **XGBoost Regressor**
* Version: **2.0.0**
* Target Variable: **Annual Claim Cost**

Performance

* MAE: **94.22**
* RMSE: **760.88**
* R² Score: **0.8002**

Training Dataset

* Training Rows: **182,968**
* Testing Rows: **45,743**

The pricing pipeline completed successfully without runtime errors and generated all expected analytical artifacts.

---

# Stage 1 — Pricing Model Training

## Purpose

Train a supervised regression model capable of predicting expected annual healthcare claim costs.

### Input

* Processed insurance portfolio
* Engineered actuarial features
* Portfolio segmentation variables

### Feature Categories

Categorical Features

* Gender
* Policy Type
* Product Type
* Distribution Channel
* Reimbursement
* New Business
* Age Band
* Seniority Band
* Portfolio Segment
* Insurance category indicators

Numerical Features

* Age
* Premium
* Exposure Time
* Family Size
* Premium per Exposure
* Seniority
* Geographic indicators
* Portfolio scores

### Model

* XGBoost Regressor

The target variable is transformed using a logarithmic transformation during training to improve stability and reduce the influence of highly skewed claim costs.

Outputs Generated

* pricing_model.pkl
* metrics.json
* training_metadata.json
* feature_importance.csv

---

# Stage 2 — Claim Cost Prediction

## Purpose

Generate expected annual healthcare claim costs for every policy in the portfolio.

### Processing Steps

* Load trained pricing model
* Validate processed dataset
* Apply preprocessing pipeline
* Generate predictions
* Reverse logarithmic transformation
* Prevent negative claim costs
* Validate prediction quality

Outputs Generated

* predicted_claim_cost.csv
* prediction_summary.json
* prediction_metadata.json

Portfolio Prediction

* Policies Processed: **228,711**

Prediction statistics include:

* Average expected claim cost
* Minimum prediction
* Maximum prediction
* Standard deviation
* Total expected portfolio claim cost

---

# Stage 3 — Premium Generation

## Purpose

Convert predicted claim costs into actuarially recommended premiums.

Premium calculation integrates machine learning outputs with underwriting risk classifications.

### Pricing Formula

```text
Recommended Premium

=

(Pure Premium × Loading Factor)

+ Expense Loading

+ Profit Margin
```

### Business Components

Pure Premium

* Expected claim cost

Risk Loading

Applied according to underwriting risk class:

| Risk Class | Loading Factor |
| ---------- | -------------: |
| Low        |           1.15 |
| Medium     |           1.25 |
| High       |           1.45 |
| Very High  |           1.65 |

Expense Loading

* Fixed administrative expense
* Variable expense percentage

Profit Margin

* Percentage of expected claim cost

Business validation rules ensure:

* No negative premiums
* Minimum loading applied
* Minimum premium floor
* Missing values handled safely

Outputs Generated

* premium_quotes.csv
* premium_summary.json
* premium_metadata.json

---

# Stage 4 — Pricing Report Generation

## Purpose

Produce business-ready pricing reports suitable for dashboards, executives, and AI Copilot.

The reporting module consolidates:

* Model performance
* Prediction statistics
* Premium portfolio summary
* Feature importance
* Model metadata

Outputs Generated

* pricing_report.md
* pricing_report.json

---

# Generated Artifacts

## Model

```text
models/pricing/
    pricing_model.pkl
```

## Training Outputs

```text
outputs/pricing/
    metrics.json
    feature_importance.csv
    training_metadata.json
```

## Prediction Outputs

```text
outputs/pricing/
    predicted_claim_cost.csv
    prediction_summary.json
    prediction_metadata.json
```

## Premium Outputs

```text
outputs/pricing/
    premium_quotes.csv
    premium_summary.json
    premium_metadata.json
```

## Reporting Outputs

```text
outputs/pricing/
    pricing_report.md
    pricing_report.json
```

---

# Validation Summary

| Validation Item              | Status |
| ---------------------------- | ------ |
| Processed Dataset Loading    | Passed |
| Dataset Validation           | Passed |
| Feature Validation           | Passed |
| Model Training               | Passed |
| Model Performance Validation | Passed |
| Portfolio Prediction         | Passed |
| Prediction Validation        | Passed |
| Premium Generation           | Passed |
| Business Rule Validation     | Passed |
| Report Generation            | Passed |

Overall Status

**PASSED**

---

# Integration within AI-AIP

The Pricing Pipeline operates as the second machine learning stage within the Healthcare Analytics Agent.

It consumes outputs from:

* Preprocessing Pipeline
* Underwriting Pipeline

Its outputs are subsequently consumed by:

* Portfolio Analytics
* Executive Dashboard
* Pricing Analytics Dashboard
* AI Copilot
* Executive Reports
* Download Center

The modular design allows the pricing pipeline to operate independently while remaining fully integrated with downstream analytical components.

---

# Technical Highlights

The pricing module incorporates several production-oriented practices:

* Modular architecture
* Dedicated validation layer
* Feature preprocessing pipeline
* Log-transformed regression target
* Model persistence using Joblib
* Comprehensive metadata generation
* Business rule enforcement
* Structured JSON outputs
* Markdown reporting
* Configurable premium loading factors

---

# Conclusion

The Pricing Pipeline has been successfully implemented as a modular, production-style actuarial pricing engine within the AI-AIP Healthcare Analytics Agent.

The pipeline performs automated claim cost prediction, premium recommendation generation, portfolio-wide pricing analysis, business rule validation, metadata generation, and executive reporting within a single integrated workflow. All expected artifacts are generated successfully, and validation confirms that the pricing stage is stable, reproducible, and ready for integration with the Portfolio Analytics module, Executive Dashboard, AI Copilot, and enterprise reporting framework.

The Pricing module is considered **complete and validated** for the current scope of the AI-AIP project.
