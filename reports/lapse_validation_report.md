# Lapse Engine Validation Report

## Module

Phase 4B – Lapse Prediction Engine

## Model

XGBoost Classifier

## Dataset

Processed Health Insurance Dataset

Rows: 228,711

Target Variable:
lapse_binary

Class Distribution:

Active (0): 187,271 (81.9%)

Lapsed (1): 41,440 (18.1%)

## Features Used

### Categorical Features

* gender
* type_policy
* type_product
* distribution_channel
* age_band

### Numerical Features

* age
* premium
* family_size
* seniority_insured
* seniority_policy
* risk_score
* claim_frequency
* loss_ratio

## Imbalance Handling

scale_pos_weight = 4.52

## Model Performance

Accuracy: 72%

AUC-ROC: 0.7879

### Classification Report

Class 0

Precision: 0.91

Recall: 0.73

F1: 0.81

Class 1

Precision: 0.36

Recall: 0.69

F1: 0.47

## Retention Segmentation

### At-Risk

Probability > 0.70

Action:
Agent Call + Discount

### Watch

Probability 0.40–0.70

Action:
Loyalty Email

### Stable

Probability < 0.40

Action:
No Action

## Segment Distribution

Stable: 110,699

Watch: 91,124

At-Risk: 26,888

## Outputs Generated

* models/lapse/lapse_model.pkl
* outputs/lapse/lapse_predictions.csv
* outputs/lapse/lapse_risk_scores.csv

## Validation Status

PASS

The lapse model successfully identifies customers with elevated lapse risk and supports targeted retention interventions.
