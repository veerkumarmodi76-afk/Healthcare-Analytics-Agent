# Data Quality Report

## Project

AI-Powered Health Insurance Actuarial Intelligence Platform (AI-AIP)

Prepared By: Veer Kumar Modi

Date: June 2026

---

# 1. Dataset Overview

Dataset Type: Health Insurance Portfolio Dataset

Rows: 228,711

Columns: 42

Observation Level:
One insured individual within one policy during one calendar year.

Years Covered:

* 2017
* 2018
* 2019

---

# 2. Data Completeness Assessment

## Missing Values Identified

| Variable           | Missing Count | Action Taken                       |
| ------------------ | ------------- | ---------------------------------- |
| date_lapse_insured | 167,181       | Retained (Active policy indicator) |
| date_lapse_policy  | 174,568       | Retained (Active policy indicator) |
| year_lapse_insured | 167,181       | Retained                           |
| year_lapse_policy  | 174,568       | Retained                           |
| IICIMUN            | 10,886        | Median Imputation                  |
| IICIPROV           | 5,701         | Median Imputation                  |
| C_H                | 10,886        | Unknown Category                   |
| C_GI               | 13,213        | Median Imputation                  |
| C_II               | 13,213        | Median Imputation                  |
| C_IE_P             | 13,213        | Median Imputation                  |
| C_IE_S             | 13,213        | Median Imputation                  |
| C_IE_T             | 13,213        | Median Imputation                  |
| C_GE_P             | 13,213        | Median Imputation                  |
| C_GE_S             | 13,213        | Median Imputation                  |
| C_GE_T             | 13,213        | Median Imputation                  |
| C_C                | 10,556        | Unknown Category                   |

---

# 3. Duplicate Assessment

Duplicate Records Found:
0

Action Taken:
No duplicate records removed.

---

# 4. Target Variable Assessment

## Lapse Variable

Distribution:

| Status              | Count   |
| ------------------- | ------- |
| Active (2)          | 187,271 |
| Lapse at Expiry (3) | 25,092  |
| Early Lapse (1)     | 16,348  |

Binary Target Created:

* 0 = Active
* 1 = Lapsed

Feature Name:

lapse_binary

---

# 5. Feature Engineering

The following derived variables were created:

| Feature              | Description                            |
| -------------------- | -------------------------------------- |
| insured_duration     | Years insured with company             |
| policy_duration      | Policy age                             |
| family_size          | Number of insured members under policy |
| claim_frequency      | Medical services per exposure          |
| claim_severity       | Average claim cost per service         |
| loss_ratio           | Claims cost divided by premium         |
| premium_per_exposure | Exposure-adjusted premium              |
| claims_per_exposure  | Exposure-adjusted claims               |
| age_band             | Age segmentation                       |
| seniority_band       | Seniority segmentation                 |
| insured_lapsed_flag  | Insured lapse indicator                |
| policy_lapsed_flag   | Policy lapse indicator                 |
| risk_score           | Composite actuarial risk measure       |
| risk_class           | Low / Medium / High / Very High        |

---

# 6. Risk Class Construction

Risk Score Components:

* Loss Ratio (50%)
* Claim Frequency (30%)
* Age (20%)

Risk Classes:

* Low
* Medium
* High
* VeryHigh

Risk classes were generated using quartile segmentation.

---

# 7. Data Quality Conclusion

Dataset passed preprocessing checks.

No critical integrity issues were identified.

Processed dataset is suitable for:

* Underwriting Risk Modelling
* Premium Prediction
* Portfolio Analytics
* Lapse Prediction
* Dashboard Integration
* AI Copilot Analytics

Final Output:

data/processed/processed_data.csv

Status:

APPROVED FOR MODEL DEVELOPMENT
