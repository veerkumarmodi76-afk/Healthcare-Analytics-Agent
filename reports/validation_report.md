# Validation Report

## Project

AI-Powered Health Insurance Actuarial Intelligence Platform (AI-AIP)

Prepared By: Veer Kumar Modi

Date: June 2026

---

# 1. Objective

The purpose of this validation exercise is to evaluate the performance of the Underwriting Risk Engine developed under Module 2 of the AI-AIP platform.

The model predicts applicant underwriting risk classes:

* Low Risk
* Medium Risk
* High Risk
* Very High Risk

The output supports underwriting decision-making and premium pricing workflows.

---

# 2. Dataset

Dataset Source: AI-AIP Processed Insurance Dataset

Total Records: 228,711

Features Used:

### Categorical Features

* gender
* type_policy
* type_policy_dg
* type_product
* reimbursement
* new_business
* distribution_channel
* age_band
* seniority_band

### Numerical Features

* age
* family_size
* seniority_insured
* seniority_policy
* exposure_time

Target Variable:

* risk_class_encoded

Class Mapping:

| Encoded Value | Risk Class |
| ------------- | ---------- |
| 0             | Low        |
| 1             | Medium     |
| 2             | High       |
| 3             | Very High  |

---

# 3. Train-Test Split

Training Set: 182,968 records (80%)

Testing Set: 45,743 records (20%)

Sampling Method:

* Stratified Train-Test Split
* Random State = 42

---

# 4. Model Specification

Algorithm:

XGBoost Classifier

Parameters:

* n_estimators = 300
* max_depth = 6
* learning_rate = 0.05
* subsample = 0.80
* colsample_bytree = 0.80

Evaluation Metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

---

# 5. Classification Performance

Overall Accuracy:

95.66%

Classification Report:

| Risk Class | Precision | Recall | F1 Score |
| ---------- | --------- | ------ | -------- |
| Low        | 0.97      | 0.99   | 0.98     |
| Medium     | 0.94      | 0.96   | 0.95     |
| High       | 0.93      | 0.94   | 0.93     |
| Very High  | 0.99      | 0.94   | 0.96     |

Macro Average F1:

0.96

Weighted Average F1:

0.96

---

# 6. Confusion Matrix

| Actual / Predicted | Low    | Medium | High   | Very High |
| ------------------ | ------ | ------ | ------ | --------- |
| Low                | 11,343 | 93     | 0      | 0         |
| Medium             | 333    | 10,945 | 158    | 0         |
| High               | 11     | 584    | 10,790 | 138       |
| Very High          | 3      | 34     | 633    | 10,678    |

---

# 7. Explainability Validation

Explainability was implemented using SHAP (SHapley Additive Explanations).

Generated Outputs:

* shap_summary.png
* applicant_0_waterfall.png
* feature_importance.csv

The SHAP summary plot provides global feature importance across the underwriting portfolio.

The waterfall plot provides local explainability for individual applicants.

---

# 8. Underwriting Output Validation

Generated Output File:

outputs/underwriting/applicant_risk_scores.csv

Output Fields:

* applicant_id
* risk_score
* risk_class
* risk_class_label
* underwriting_flag
* shap_top3_drivers

Underwriting Decision Mapping:

| Risk Class | Decision |
| ---------- | -------- |
| Low        | Standard |
| Medium     | Standard |
| High       | Rated    |
| Very High  | Decline  |

---

# 9. Deliverables Generated

Models:

* models/underwriting/underwriting_model.pkl

Outputs:

* outputs/underwriting/applicant_risk_scores.csv
* outputs/underwriting/feature_importance.csv
* outputs/underwriting/shap_summary.png
* outputs/underwriting/applicant_0_waterfall.png

---

# 10. Validation Conclusion

The underwriting risk engine completed training, prediction, and explainability generation successfully.

Key Results:

* Accuracy: 95.66%
* Macro F1 Score: 0.96
* All four risk classes predicted successfully.
* SHAP explainability generated successfully.
* Underwriting output files generated successfully.

Validation Status:

APPROVED FOR PHASE 4 DEVELOPMENT

Next Module:

Phase 4 – Claim Cost Prediction & Lapse Prediction Engine
