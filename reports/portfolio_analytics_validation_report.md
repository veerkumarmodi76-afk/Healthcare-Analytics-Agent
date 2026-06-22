# Portfolio Analytics Engine Validation Report

## Project

AI-Powered Health Insurance Actuarial Intelligence Platform (AI-AIP)

Prepared By: Veer Kumar Modi

Date: June 2026

---

# 1. Module Overview

Module Name:

**Phase 5 – Portfolio Analytics Engine**

Purpose:

The Portfolio Analytics Engine consolidates outputs from the Underwriting, Pricing, and Lapse Prediction engines into a unified portfolio monitoring and decision-support framework.

The module provides:

* Risk Portfolio Analysis
* Claims Analytics
* Profitability Monitoring
* Trend Analysis
* Retention Analytics
* Pricing Adequacy Monitoring
* Executive Portfolio Reporting

---

# 2. Data Sources

The Portfolio Analytics Engine consumes the following validated datasets:

## Core Portfolio Dataset

Source:

```text
data/processed/processed_data.csv
```

Contains:

* Policy Information
* Demographics
* Claims Experience
* Premium Information
* Exposure Measures
* Lapse Indicators

---

## Underwriting Engine Outputs

Source:

```text
outputs/underwriting/applicant_risk_scores.csv
```

Fields Used:

* row_id
* risk_score
* risk_class
* underwriting_flag

---

## Pricing Engine Outputs

Source:

```text
outputs/pricing/premium_quotes.csv
```

Fields Used:

* row_id
* predicted_claim_cost
* recommended_premium

---

## Lapse Engine Outputs

Source:

```text
outputs/lapse/lapse_risk_scores.csv
```

Fields Used:

* row_id
* lapse_probability
* retention_segment
* recommended_action

---

# 3. Master Portfolio Dataset

The Portfolio Analytics Engine constructs a consolidated master dataset by joining all module outputs using:

```text
row_id
```

Result:

```text
master_df
```

The master dataframe includes:

| Category    | Variables                                         |
| ----------- | ------------------------------------------------- |
| Portfolio   | ID_policy, ID_insured, period                     |
| Demographic | age, gender, age_band                             |
| Claims      | cost_claims_year, claim_frequency, claim_severity |
| Premium     | premium, recommended_premium                      |
| Risk        | risk_score, risk_class                            |
| Retention   | lapse_probability, retention_segment              |
| Performance | loss_ratio                                        |

---

# 4. Risk Analytics

Implemented Module:

```text
src/portfolio/risk.py
```

Generated Outputs:

### Risk Distribution

Measures portfolio concentration by:

* Low Risk
* Medium Risk
* High Risk
* Very High Risk

---

### Risk by Age Band

Measures:

* Risk concentration by demographic segment

---

### Risk by Policy Type

Measures:

* Risk concentration across policy structures

---

### Risk by Distribution Channel

Measures:

* Risk concentration across acquisition channels

---

### Premium Summary

Metrics:

* Total Premium
* Average Premium
* Recommended Premium

Grouped By:

```text
risk_class
```

---

### Profitability Summary

Metrics:

* Total Premium
* Total Claims
* Profit
* Pricing Gap
* Loss Ratio

Grouped By:

```text
risk_class
```

---

# 5. Claims Analytics

Implemented Module:

```text
src/portfolio/claims.py
```

Generated Outputs:

### Portfolio Claims Summary

Metrics:

* Total Premium
* Total Claims
* Average Claim Frequency
* Average Claim Severity
* Portfolio Loss Ratio

---

### Claim Frequency Analysis

Grouped By:

```text
age_band
```

---

### Claim Severity Analysis

Grouped By:

```text
age_band
```

---

### Loss Ratio Analysis

Grouped By:

* Risk Class
* Policy Type

---

### Top Loss Segments

Identifies:

* Highest loss ratio portfolio segments
* Lowest profitability cohorts

---

# 6. Trend Analytics

Implemented Module:

```text
src/portfolio/trends.py
```

Observation Period:

```text
2017
2018
2019
```

Generated Outputs:

### Premium Trend

Measures:

* Annual Premium Growth

---

### Claims Trend

Measures:

* Annual Claims Growth

---

### Loss Ratio Trend

Measures:

* Portfolio Profitability Trend

---

### Lapse Trend

Measures:

* Annual Portfolio Retention Trend

---

### Risk Mix Trend

Measures:

* Evolution of Risk Distribution

---

### Portfolio Growth Summary

Measures:

* Premium Growth
* Claims Growth

---

# 7. Pricing Adequacy Analytics

Generated Output:

```text
premium_leakage.csv
```

Formula:

Premium Leakage =

```text
Recommended Premium
-
Actual Premium
```

Purpose:

* Detect underpriced segments
* Detect pricing opportunities
* Support actuarial pricing reviews

---

# 8. Retention Analytics

Generated Output:

```text
retention_summary.csv
```

Metrics:

* Customer Count
* Premium Exposure
* Retention Segment

Segments:

* Stable
* Watch
* At-Risk

Purpose:

* Quantify premium revenue at risk
* Support retention campaigns

---

# 9. Executive KPI Dashboard

Generated Output:

```text
executive_kpis.csv
```

Metrics:

| KPI                     |
| ----------------------- |
| Total Policies          |
| Total Insured           |
| Total Premium           |
| Total Claims            |
| Average Claim Frequency |
| Average Claim Severity  |
| Portfolio Loss Ratio    |
| Portfolio Lapse Rate    |

---

# 10. Portfolio Metrics Dashboard

Generated Output:

```text
portfolio_metrics.csv
```

Metrics:

| KPI                       |
| ------------------------- |
| Total Premium             |
| Total Claims              |
| Total Profit              |
| Portfolio Loss Ratio      |
| Average Risk Score        |
| Average Lapse Probability |

---

# 11. Executive Summary Engine

Implemented Module:

```text
src/portfolio/executive_summary.py
```

Generated Output:

```text
outputs/portfolio/executive_summary.txt
```

Capabilities:

* Portfolio Performance Commentary
* Risk Concentration Commentary
* Pricing Adequacy Commentary
* Retention Commentary
* Management Recommendations

---

# 12. Dashboard Integration

Implemented Module:

```text
src/portfolio/dashboard_data.py
```

Purpose:

Provide Streamlit-ready datasets for:

* KPI Cards
* Risk Charts
* Claims Charts
* Trend Charts
* Retention Analysis
* Pricing Analytics
* Executive Insights

---

# 13. Outputs Generated

```text
outputs/portfolio/

├── executive_kpis.csv
├── portfolio_metrics.csv
├── risk_distribution.csv
├── risk_profitability.csv
├── frequency_by_age.csv
├── severity_by_age.csv
├── top_loss_segments.csv
├── premium_trend.csv
├── claims_trend.csv
├── loss_ratio_trend.csv
├── lapse_trend.csv
├── premium_leakage.csv
├── retention_summary.csv
└── executive_summary.txt
```

---

# 14. Validation Status

Validation Checks Completed:

✓ Master Dataset Construction

✓ Risk Analytics Generation

✓ Claims Analytics Generation

✓ Trend Analytics Generation

✓ Premium Leakage Analytics

✓ Retention Analytics

✓ Executive KPI Generation

✓ Dashboard Data Service

✓ Executive Summary Generation

---

# 15. Conclusion

The Portfolio Analytics Engine successfully integrates outputs from the Underwriting, Pricing, and Lapse Prediction engines into a centralized actuarial intelligence framework.

The module provides:

* Portfolio Monitoring
* Profitability Analysis
* Risk Analytics
* Retention Analytics
* Pricing Adequacy Analysis
* Executive Reporting

The generated outputs are fully compatible with the Streamlit Dashboard and AI Copilot modules.

Validation Status:

## APPROVED FOR PHASE 6 DEVELOPMENT

Next Module:

### Phase 6 – Streamlit Dashboard & AI Copilot Integration
