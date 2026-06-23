# AI-Powered Health Insurance Analytics Agent (AI-AIP)

## Final Project Report

### Author

Veer Kumar Modi

### Program

Integrated Programme in Management (IPM)

### Domain

Actuarial Analytics | Insurance Analytics | Machine Learning | Business Intelligence

---

# Executive Summary

The AI-Powered Health Insurance Analytics Agent (AI-AIP) is an end-to-end actuarial analytics platform developed to support insurance underwriting, pricing, retention management, portfolio monitoring, executive reporting, and AI-assisted decision-making.

The platform transforms raw policyholder data into actionable business intelligence through a combination of machine learning models, portfolio analytics, interactive dashboards, and an AI-powered copilot.

The system processes more than 228,000 policy records and provides insights across the insurance value chain.

---

# Business Problem

Insurance companies face several challenges:

* Inaccurate underwriting decisions
* Premium inadequacy
* High customer lapse rates
* Portfolio profitability deterioration
* Lack of centralized portfolio monitoring
* Slow executive reporting processes

Traditional reporting systems are often static and require manual intervention.

AI-AIP addresses these issues through automated analytics and intelligent decision support.

---

# Project Objectives

The project was designed to:

1. Automate underwriting risk assessment.
2. Predict expected claims cost.
3. Recommend risk-adjusted premiums.
4. Predict customer lapse behavior.
5. Generate retention recommendations.
6. Analyze portfolio profitability and claims experience.
7. Provide executive-level reporting.
8. Enable natural language portfolio exploration using an AI copilot.

---

# Dataset

Health Insurance Portfolio Dataset

Records:

228,711 policy observations

Input Variables:

* Demographics
* Policy Information
* Claims History
* Distribution Channel
* Premium Information
* Exposure Metrics
* Customer Tenure

Generated Features:

* claim_frequency
* claim_severity
* loss_ratio
* premium_per_exposure
* claims_per_exposure
* age_band
* seniority_band
* risk_score
* risk_class

Total Features After Engineering:

58

---

# System Architecture

Raw Data
↓
Data Ingestion
↓
Data Cleaning
↓
Feature Engineering
↓
Risk Segmentation
↓
Underwriting Model
↓
Pricing Model
↓
Lapse Model
↓
Portfolio Analytics Engine
↓
Executive Reporting
↓
Streamlit Dashboard
↓
AI Copilot

---

# Phase 1 – Data Processing Pipeline

Modules:

* ingest.py
* clean.py
* features.py
* risk.py
* preprocess.py

Responsibilities:

* Data ingestion
* Missing value handling
* Feature generation
* Risk segmentation
* Dataset preparation

Output:

processed_data.csv

Status:

Completed

---

# Phase 2 – Underwriting Engine

Objective:

Predict risk class of policyholders.

Model:

XGBoost Classifier

Outputs:

* risk_score
* risk_class_label
* underwriting_flag

Explainability:

SHAP Integration

Generated Artifacts:

* underwriting_model.pkl
* applicant_risk_scores.csv
* feature_importance.csv
* shap_summary.png
* applicant_0_waterfall.png

Performance:

Accuracy: 95.66%

Result:

Successfully segments policyholders into:

* Low Risk
* Medium Risk
* High Risk
* Very High Risk

Status:

Completed

---

# Phase 3 – Pricing Engine

Objective:

Predict future claims cost and recommend premiums.

Model:

XGBoost Regressor

Outputs:

* predicted_claim_cost
* recommended_premium

Generated Artifacts:

* pricing_model.pkl
* premium_quotes.csv

Performance:

MAE: 21.73

R²: 0.9473

Result:

Provides actuarially informed premium recommendations.

Status:

Completed

---

# Phase 4 – Lapse Prediction Engine

Objective:

Predict probability of customer lapse.

Model:

XGBoost Classifier

Outputs:

* lapse_probability
* retention_segment
* recommended_action

Retention Segments:

* Stable
* Watch
* At-Risk

Generated Artifacts:

* lapse_model.pkl
* lapse_risk_scores.csv

Performance:

Accuracy: 72%

AUC: 0.7879

Result:

Enables proactive customer retention strategies.

Status:

Completed

---

# Phase 5 – Portfolio Analytics Engine

Objective:

Provide enterprise-level portfolio monitoring.

Modules:

* risk.py
* claims.py
* trends.py
* metrics.py
* run.py

Capabilities:

## Risk Analytics

* Risk Distribution
* Risk by Age Band
* Risk by Policy Type
* Risk by Distribution Channel
* Risk Profitability Analysis

## Claims Analytics

* Claim Frequency Analysis
* Claim Severity Analysis
* Loss Ratio Analysis
* Top Loss Segments

## Trend Analytics

* Premium Trend
* Claims Trend
* Loss Ratio Trend
* Lapse Trend
* Risk Mix Trend
* Portfolio Growth Analysis

## Pricing Analytics

* Premium Leakage Analysis

## Retention Analytics

* Premium Exposure Analysis
* Retention Segment Monitoring

Generated Outputs:

20+ portfolio analytics datasets

Status:

Completed

---

# Phase 6 – Interactive Dashboard

Technology:

Streamlit

Dashboard Pages:

1. Executive Dashboard
2. Risk Analytics
3. Claims Analytics
4. Retention Analytics
5. Pricing Analytics
6. Trend Analytics
7. Download Center

Capabilities:

* KPI Monitoring
* Portfolio Visualization
* Trend Analysis
* Claims Monitoring
* Retention Monitoring
* Pricing Adequacy Monitoring
* Executive Insights

Status:

Completed

---

# Phase 7 – AI Copilot

Technology:

Google Gemini 2.5 Flash

Architecture:

Question
↓
Portfolio Context Builder
↓
Fact Extraction Layer
↓
Gemini
↓
Business Explanation

Anti-Hallucination Design:

The copilot is designed to:

* Use only portfolio-generated outputs
* Avoid creating unsupported numerical values
* Ground responses in analytical results
* Separate facts from recommendations
* Refuse unsupported questions

Capabilities:

* Portfolio Summarization
* Risk Assessment
* Pricing Analysis
* Retention Analysis
* Executive Decision Support

Status:

In Progress

---

# Technical Stack

Programming Language:

Python

Machine Learning:

* Scikit-Learn
* XGBoost

Analytics:

* Pandas
* NumPy

Visualization:

* Plotly
* Streamlit
* Matplotlib

Explainability:

* SHAP

AI Layer:

* Google Gemini 2.5 Flash

Development Environment:

* VS Code

Version Control:

* Git
* GitHub

---

# Key Achievements

Successfully developed:

✓ End-to-End Data Pipeline

✓ Automated Underwriting Engine

✓ Premium Recommendation Engine

✓ Lapse Prediction System

✓ Portfolio Analytics Framework

✓ Executive Reporting System

✓ Multi-Page Business Dashboard

✓ AI Copilot Architecture

✓ Explainable AI Integration

✓ Automated Pipeline Execution

---

# Business Value

The platform enables insurance organizations to:

* Improve underwriting consistency
* Detect unprofitable portfolio segments
* Optimize pricing decisions
* Reduce customer churn
* Monitor portfolio performance
* Accelerate executive reporting
* Improve decision-making through AI assistance

---

# Future Enhancements

Phase 8:

* Multi-turn conversational memory
* PDF report generation
* Scenario simulation engine
* Pricing stress testing
* What-if analysis
* Role-based dashboard access
* Cloud deployment

Phase 9:

* Real-time portfolio monitoring
* Agent performance analytics
* Customer lifetime value modeling
* Dynamic pricing optimization

---

# Conclusion

AI-AIP successfully demonstrates the integration of actuarial science, machine learning, portfolio analytics, business intelligence, and generative AI into a unified insurance analytics platform.

The project delivers a complete workflow from raw policyholder data to executive decision support and represents a production-style implementation of modern insurance analytics capabilities.
