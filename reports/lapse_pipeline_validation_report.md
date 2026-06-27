# Lapse Pipeline Validation Report

## Project

**AI-AIP – Healthcare Analytics Agent**

---

# Objective

The Lapse Prediction Pipeline is responsible for identifying insurance policyholders who are most likely to discontinue or fail to renew their policies. It combines machine learning with business-oriented retention analytics to estimate lapse probability, prioritize high-risk customers, recommend retention actions, and quantify the potential financial impact of customer attrition.

The pipeline transforms the processed insurance portfolio into actionable retention intelligence that supports portfolio management, executive reporting, dashboard analytics, and AI-powered business insights.

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
Model Evaluation
        │
        ▼
Portfolio Prediction
        │
        ▼
Risk Segmentation
        │
        ▼
Retention Analytics
        │
        ▼
Business Report Generation
```

Each stage completes successfully before the next stage begins.

---

# Pipeline Execution Summary

Execution Status

**SUCCESS**

Input Dataset

* Rows: **228,711**
* Columns: **52**

Selected Model

* Algorithm: **XGBoost Classifier**
* Target Variable: **Lapse Binary**

Candidate Models Evaluated

* Random Forest Classifier
* XGBoost Classifier

Cross Validation

* Random Forest ROC-AUC: **0.8125**
* XGBoost ROC-AUC: **0.8401**

Best Model

**XGBoost Classifier**

Final Model Performance

| Metric    |      Value |
| --------- | ---------: |
| Accuracy  | **0.8372** |
| Precision | **0.5441** |
| Recall    | **0.6239** |
| F1 Score  | **0.5813** |
| ROC-AUC   | **0.8432** |

Training Dataset

* Training Rows: **182,968**
* Testing Rows: **45,743**

The lapse prediction pipeline completed successfully without runtime errors and generated all expected analytical artifacts.

---

# Stage 1 — Model Training

## Purpose

Train a supervised classification model capable of estimating the probability of policy lapse.

### Input

* Processed insurance portfolio
* Engineered actuarial features
* Customer demographic variables
* Portfolio segmentation features

### Feature Categories

Categorical Features

* Gender
* Policy Type
* Product Type
* Distribution Channel
* Age Band
* Seniority Band
* Portfolio Segment

Numerical Features

* Age
* Premium
* Family Size
* Seniority
* Premium per Exposure
* Claims per Exposure
* Segment Score
* Portfolio Segment Encoding
* Age Band Score

### Candidate Models

* Random Forest Classifier
* XGBoost Classifier

The pipeline evaluates multiple candidate models using 5-fold stratified cross-validation and automatically selects the model with the highest ROC-AUC score.

Outputs Generated

```text
models/lapse/
    lapse_model.pkl
    feature_importance.csv
    model_metrics.json
    shap_summary.csv
```

---

# Stage 2 — Model Evaluation

## Purpose

Evaluate predictive performance using multiple classification metrics.

Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix
* Classification Report
* ROC Curve

### Results

| Metric    |      Value |
| --------- | ---------: |
| Accuracy  | **0.8372** |
| Precision | **0.5441** |
| Recall    | **0.6239** |
| F1 Score  | **0.5813** |
| ROC-AUC   | **0.8432** |

The evaluation indicates strong discriminatory performance with a ROC-AUC of **0.8432**, demonstrating effective identification of customers at risk of lapse.

Outputs Generated

```text
outputs/lapse/
    classification_report.txt
    confusion_matrix.csv
    roc_curve.csv
```

---

# Stage 3 — Portfolio Prediction

## Purpose

Generate lapse probabilities for the complete insurance portfolio.

Prediction Outputs

* Predicted Lapse
* Lapse Probability
* Prediction Confidence
* Risk Segment
* Primary Decision Driver
* Secondary Decision Driver

Portfolio Size

**228,711 policyholders**

Average Lapse Probability

**0.3767**

Outputs Generated

```text
outputs/lapse/
    lapse_predictions.csv
```

---

# Stage 4 — Retention Analytics

## Purpose

Transform machine learning predictions into actionable business recommendations.

Each customer is assigned:

* Retention Priority
* Estimated Revenue Loss
* Estimated Retention Cost
* Expected ROI
* Recommended Retention Action

### Risk Segments

| Segment  |   Policies |
| -------- | ---------: |
| Very Low | **57,676** |
| Low      | **76,174** |
| Medium   | **69,252** |
| High     |  **5,259** |
| Critical | **20,350** |

### Recommended Actions

* No Action Required
* Automated Reminder Email
* Personalized Renewal Offer
* Agent Call + Loyalty Discount
* Immediate Relationship Manager Call + Premium Review

Portfolio Summary

* Estimated Revenue at Risk: **₹4,307,400,750.00**
* Estimated Retention Campaign Cost: **₹207,001,700.00**

Outputs Generated

```text
outputs/lapse/
    lapse_retention_actions.csv
```

---

# Stage 5 — Business Report Generation

## Purpose

Generate business-ready reports for dashboards, executives, and the AI Copilot.

The reporting module consolidates:

* Model Performance
* Portfolio Summary
* Risk Distribution
* Feature Importance
* Financial Impact
* Retention Recommendations

Outputs Generated

```text
outputs/lapse/
    lapse_summary.md
    lapse_summary.json
```

---

# Generated Artifacts

## Model

```text
models/lapse/
    lapse_model.pkl
```

## Training Outputs

```text
models/lapse/
    feature_importance.csv
    model_metrics.json
    shap_summary.csv
```

## Evaluation Outputs

```text
outputs/lapse/
    classification_report.txt
    confusion_matrix.csv
    roc_curve.csv
```

## Prediction Outputs

```text
outputs/lapse/
    lapse_predictions.csv
```

## Retention Outputs

```text
outputs/lapse/
    lapse_retention_actions.csv
```

## Reporting Outputs

```text
outputs/lapse/
    lapse_summary.md
    lapse_summary.json
```

---

# Validation Summary

| Validation Item           | Status |
| ------------------------- | ------ |
| Processed Dataset Loading | Passed |
| Dataset Validation        | Passed |
| Feature Validation        | Passed |
| Candidate Model Training  | Passed |
| Cross Validation          | Passed |
| Model Selection           | Passed |
| Model Evaluation          | Passed |
| Portfolio Prediction      | Passed |
| Risk Segmentation         | Passed |
| Retention Analytics       | Passed |
| Report Generation         | Passed |

Overall Status

**PASSED**

---

# Integration within AI-AIP

The Lapse Prediction Pipeline represents the third machine learning stage within the Healthcare Analytics Agent.

It consumes outputs from:

* Preprocessing Pipeline

Its outputs are subsequently consumed by:

* Portfolio Analytics
* Retention Analytics Dashboard
* Executive Dashboard
* AI Copilot
* Executive Reports
* Download Center

The modular architecture allows the lapse pipeline to operate independently while integrating seamlessly with downstream analytical components.

---

# Technical Highlights

The lapse prediction module incorporates several production-oriented practices:

* Modular architecture
* Automated candidate model selection
* Stratified cross-validation
* XGBoost classification
* Feature preprocessing pipeline
* SHAP-based explainability
* Model persistence using Joblib
* Comprehensive evaluation metrics
* Risk segmentation
* Business-oriented retention analytics
* Revenue-at-risk estimation
* ROI estimation
* Structured JSON outputs
* Markdown reporting

---

# Conclusion

The Lapse Prediction Pipeline has been successfully implemented as a modular, production-style customer retention analytics engine within the AI-AIP Healthcare Analytics Agent.

The pipeline performs automated lapse probability prediction, customer risk segmentation, retention prioritization, financial impact estimation, business recommendation generation, explainable analytics, and executive reporting within a single integrated workflow.

All expected artifacts are generated successfully, validation confirms that every processing stage completed successfully, and the pipeline is fully integrated with the Portfolio Analytics module, Executive Dashboard, AI Copilot, and enterprise reporting framework.

The Lapse Prediction module is considered **complete, validated, and production-ready** for the current scope of the AI-AIP Healthcare Analytics Agent.
