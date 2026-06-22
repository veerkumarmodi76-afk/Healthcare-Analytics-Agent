# AI-Powered Health Insurance Actuarial Intelligence Platform (AI-AIP)

## End-to-End Pipeline Validation Report

### Validation Date

June 2026

### Prepared By

Veer Kumar Modi

---

# Objective

Validate successful execution of the complete AI-AIP workflow from raw data ingestion through actuarial portfolio analytics and executive reporting.

---

# Pipeline Components Validated

## Phase 1 – Data Processing

Input Dataset:

* raw_data.csv

Results:

* Dataset Loaded Successfully
* Records Processed: 228,711
* Features Generated Successfully
* Risk Classes Generated Successfully

Output:

* data/processed/processed_data.csv

Status:

PASS

---

## Phase 2 – Underwriting Engine

Model:

XGBoost Classifier

Performance:

* Accuracy: 95.66%
* Macro F1 Score: 0.96

Outputs Generated:

* underwriting_model.pkl
* applicant_risk_scores.csv
* feature_importance.csv
* shap_summary.png
* applicant_0_waterfall.png

Status:

PASS

---

## Phase 3 – Pricing Engine

Model:

XGBoost Regressor

Performance:

* MAE: 21.73
* R²: 0.9473

Outputs Generated:

* pricing_model.pkl
* predicted_claim_cost.csv
* premium_quotes.csv

Status:

PASS

---

## Phase 4 – Lapse Prediction Engine

Model:

XGBoost Classifier

Performance:

* Accuracy: 72%
* AUC: 0.7879

Retention Segments:

* Stable: 110,699
* Watch: 91,124
* At-Risk: 26,888

Outputs Generated:

* lapse_model.pkl
* lapse_predictions.csv
* lapse_risk_scores.csv

Status:

PASS

---

## Phase 5 – Portfolio Analytics Engine

Portfolio Analytics Executed Successfully.

Outputs Generated:

### Executive KPIs

* executive_kpis.csv

### Portfolio Metrics

* portfolio_metrics.csv

### Risk Analytics

* risk_distribution.csv
* risk_by_age_band.csv
* risk_by_policy_type.csv
* risk_by_channel.csv
* risk_premium_summary.csv
* risk_claims_summary.csv
* risk_profitability.csv

### Claims Analytics

* frequency_by_age.csv
* severity_by_age.csv
* top_loss_segments.csv

### Trend Analytics

* premium_trend.csv
* claims_trend.csv
* loss_ratio_trend.csv
* lapse_trend.csv
* risk_mix_trend.csv
* portfolio_growth_summary.csv

### Pricing Analytics

* premium_leakage.csv

### Retention Analytics

* retention_summary.csv

Status:

PASS

---

## Phase 6 – Executive Summary

Output Generated:

* executive_summary.txt

Status:

PASS

---

# End-to-End Pipeline Validation

Pipeline Executed Successfully:

Raw Data
→ Preprocessing
→ Underwriting
→ Pricing
→ Lapse Prediction
→ Portfolio Analytics
→ Executive Reporting

No Runtime Errors Detected.

All Expected Outputs Generated Successfully.

---

# Conclusion

The AI-Powered Health Insurance Actuarial Intelligence Platform completed full end-to-end execution successfully.

The system is validated for:

* Underwriting Risk Assessment
* Premium Recommendation
* Customer Retention Analytics
* Portfolio Risk Monitoring
* Claims Analytics
* Pricing Adequacy Monitoring
* Executive Reporting

Validation Status:

APPROVED FOR STREAMLIT DASHBOARD DEVELOPMENT

Next Phase:

Phase 6 – Interactive Dashboard & AI Copilot
