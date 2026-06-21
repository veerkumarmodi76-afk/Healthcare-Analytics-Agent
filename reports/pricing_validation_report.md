# Pricing Engine Validation Report

## Module

Phase 4A – Claim Cost Prediction & Pricing Engine

## Model

XGBoost Regressor

## Dataset

Processed Health Insurance Dataset

Rows: 228,711

Target Variable:
cost_claims_year

## Features Used

### Categorical Features

* gender
* type_policy
* type_product
* distribution_channel

### Numerical Features

* age
* family_size
* seniority_insured
* seniority_policy
* exposure_time
* n_medical_services
* claim_frequency
* claim_severity
* risk_score
* IICIMUN
* IICIPROV
* C_GI
* C_II

## Model Performance

Mean Absolute Error (MAE): 21.73

R² Score: 0.9473

## Pricing Logic

Loading Factors:

| Risk Class | Loading |
| ---------- | ------- |
| Low        | 1.15    |
| Medium     | 1.25    |
| High       | 1.45    |
| VeryHigh   | 1.65    |

Premium Formula:

Recommended Premium =
Predicted Claim Cost × Loading Factor

Safety Constraint:

Recommended Premium ≥ Predicted Claim Cost × 1.10

## Outputs Generated

* models/pricing/pricing_model.pkl
* outputs/pricing/predicted_claim_cost.csv
* outputs/pricing/premium_quotes.csv
* outputs/pricing/feature_importance.csv

## Validation Status

PASS

The pricing engine achieved strong predictive performance and generated actuarially adjusted premium recommendations.
