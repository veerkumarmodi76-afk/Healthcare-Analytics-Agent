# Portfolio Analytics Pipeline Validation & Implementation Report

## Project

Healthcare Analytics Agent

---

# Module Overview

Portfolio Analytics is the final analytical layer of the Healthcare Analytics Agent. It consolidates outputs from the preprocessing, underwriting, pricing, and lapse prediction pipelines into a unified portfolio view, providing business intelligence, executive reporting, dashboard-ready datasets, and AI Copilot context.

Unlike previous modules that focus on individual predictive tasks, Portfolio Analytics evaluates the insurance portfolio as a whole and produces actionable insights for business decision-making.

---

# Objectives

The Portfolio Analytics module was designed to:

* Integrate outputs from all completed analytical pipelines.
* Build a unified portfolio dataset.
* Compute portfolio-wide KPIs.
* Perform risk, claims, pricing, retention, and trend analysis.
* Generate executive summaries.
* Export dashboard-ready datasets.
* Provide structured data for the AI Copilot.

---

# Pipeline Architecture

The Portfolio Analytics pipeline consumes outputs from previous modules.

```text
Processed Dataset
        │
        ▼
Underwriting Predictions
        │
        ▼
Pricing Outputs
        │
        ▼
Lapse Predictions
        │
        ▼
Portfolio Analytics
        │
        ├── Executive KPIs
        ├── Portfolio Metrics
        ├── Portfolio Health
        ├── Risk Analytics
        ├── Claims Analytics
        ├── Pricing Analytics
        ├── Retention Analytics
        ├── Trend Analytics
        ├── Executive Summary
        └── Dashboard Data
```

---

# Package Structure

```text
src/
└── portfolio/
    ├── __init__.py
    ├── run.py
    ├── metrics.py
    ├── claims.py
    ├── risk.py
    ├── trends.py
    ├── dashboard_data.py
    └── executive_summary.py
```

A dedicated PortfolioService orchestrates the complete execution of the module.

---

# Service Layer Implementation

A new `PortfolioService` was implemented following the same architecture as the preprocessing, underwriting, pricing, and lapse services.

The service performs the following tasks:

* Loads processed insurance data.
* Loads underwriting predictions.
* Loads premium recommendations.
* Loads lapse prediction outputs.
* Loads retention action outputs.
* Builds the unified master dataframe.
* Executes all portfolio analytics.
* Saves all generated reports.
* Generates the executive summary.

This preserves a consistent service-oriented architecture across the project.

---

# Master Portfolio Dataset

A unified master dataframe is created by combining:

* Processed customer information
* Underwriting decisions
* Pricing recommendations
* Lapse prediction probabilities
* Retention recommendations

The master dataset acts as the single analytical source for all portfolio calculations.

---

# Feature Engineering Enhancement

During implementation, portfolio validation identified that several actuarial metrics required by the analytics layer were missing from preprocessing.

Three new engineered features were added to the preprocessing pipeline.

## Claim Frequency

```
claim_frequency =
n_medical_services / exposure_time
```

Measures expected claim occurrence relative to policy exposure.

---

## Claim Severity

```
claim_severity =
cost_claims_year / n_medical_services
```

Measures the average financial impact of each medical claim.

---

## Loss Ratio

```
loss_ratio =
cost_claims_year / premium
```

Measures underwriting profitability by comparing annual claim costs with premium collected.

These features are now generated during preprocessing, ensuring they are available to every downstream analytical pipeline.

---

# Portfolio Analytics Generated

## Executive KPIs

The pipeline computes portfolio-level indicators including:

* Total Policies
* Total Insured
* Total Premium
* Total Claims
* Total Profit
* Portfolio Loss Ratio

---

## Portfolio Metrics

Additional analytical metrics include:

* Average Risk Score
* Average Lapse Probability
* Average Premium
* Average Claim Cost
* Pricing Margin
* Portfolio Exposure

---

## Portfolio Health

A composite portfolio health score is generated based on profitability, loss ratio, and lapse exposure.

The pipeline also classifies the overall portfolio status.

---

## Risk Analytics

Generated outputs include:

* Risk Distribution
* Risk Profitability
* Risk by Age Band
* Risk by Policy Type
* Risk by Distribution Channel
* Premium by Risk
* Claims by Risk

---

## Claims Analytics

Generated outputs include:

* Claim Frequency by Age
* Claim Severity by Age
* Loss Ratio by Risk
* Loss Ratio by Policy Type
* Highest Loss Segments
* Portfolio Claims Summary

---

## Pricing Analytics

Generated outputs include:

* Premium Leakage
* Pricing Adequacy
* Premium Summaries

---

## Retention Analytics

Generated outputs include:

* Premium at Risk
* Retention Segments
* Revenue Exposure
* Expected Retention ROI
* Recommended Retention Actions

---

## Trend Analytics

Generated outputs include:

* Premium Trend
* Claims Trend
* Loss Ratio Trend
* Lapse Trend
* Portfolio Growth
* Risk Mix Trend

---

# Dashboard Integration

A dedicated `DashboardDataService` was implemented to provide a clean abstraction layer between portfolio outputs and the Streamlit dashboard.

The service exposes methods to retrieve:

* Executive KPIs
* Portfolio Metrics
* Portfolio Health
* Risk Analytics
* Claims Analytics
* Trend Analytics
* Pricing Analytics
* Retention Analytics

This approach prevents dashboard pages from reading CSV files directly and centralizes all data access.

---

# Executive Summary Generation

An automated executive summary was implemented.

The summary reports:

* Portfolio premium
* Portfolio claims
* Portfolio profit
* Portfolio loss ratio
* Average portfolio risk
* Average lapse probability
* Highest claim burden
* Largest pricing leakage
* Highest premium exposure
* Business recommendations

---

# Integration Issues Identified & Resolved

## 1. Lapse Integration

The original PortfolioService attempted to load a non-existent file.

### Resolution

* Replaced obsolete lapse input.
* Loaded:

  * lapse_predictions.csv
  * lapse_retention_actions.csv
* Merged both datasets before portfolio processing.

---

## 2. Retention Segment Naming

Portfolio Analytics expected:

```
retention_segment
```

while the lapse pipeline generated:

```
risk_segment
```

### Resolution

Standardized the column name during data preparation.

---

## 3. Missing Portfolio Features

Portfolio Analytics required:

* claim_frequency
* claim_severity
* loss_ratio

These were absent from the processed dataset.

### Resolution

The preprocessing feature engineering pipeline was updated to generate all three metrics, ensuring a consistent feature set for downstream analytics.

---

## 4. Executive Summary KPI Mapping

Initial execution produced:

* Total Premium = 0
* Total Claims = 0
* Total Profit = 0

The analytics were correct, but the Executive Summary was reading these values from `portfolio_metrics.csv` instead of `executive_kpis.csv`.

### Resolution

The summary generator now reads:

**executive_kpis.csv**

* Total Premium
* Total Claims
* Total Profit
* Loss Ratio

and

**portfolio_metrics.csv**

* Average Risk Score
* Average Lapse Probability

The executive summary now reports the correct portfolio values.

---

## 5. Dashboard KPI Mapping

The DashboardDataService contained the same KPI mapping issue.

### Resolution

Dashboard summary and executive insight generation were updated to retrieve portfolio-level KPIs from `executive_kpis.csv` while continuing to use `portfolio_metrics.csv` for analytical metrics.

This ensures consistent values across reports, dashboard pages, and executive summaries.

---

# Output Files Generated

The Portfolio Analytics pipeline now generates:

* Executive KPIs
* Portfolio Metrics
* Portfolio Health
* Risk Distribution
* Risk Profitability
* Risk Premium Summary
* Risk Claims Summary
* Frequency by Age
* Severity by Age
* Top Loss Segments
* Premium Trend
* Claims Trend
* Loss Ratio Trend
* Lapse Trend
* Portfolio Growth Summary
* Risk Mix Trend
* Premium Leakage
* Retention Summary
* Executive Summary

These outputs are consumed directly by the dashboard and AI Copilot.

---

# Validation Result

| Component                   | Status |
| --------------------------- | ------ |
| Portfolio Service           | PASS   |
| Master Data Integration     | PASS   |
| Risk Analytics              | PASS   |
| Claims Analytics            | PASS   |
| Pricing Analytics           | PASS   |
| Retention Analytics         | PASS   |
| Trend Analytics             | PASS   |
| Executive KPI Generation    | PASS   |
| Portfolio Health Generation | PASS   |
| Executive Summary           | PASS   |
| Dashboard Data Service      | PASS   |

---

# Overall Assessment

The Portfolio Analytics module has been successfully implemented and integrated into the Healthcare Analytics Agent.

The pipeline now consolidates outputs from all predictive models into a unified analytical framework capable of producing portfolio-level KPIs, actuarial metrics, executive summaries, and dashboard-ready datasets.

The addition of Claim Frequency, Claim Severity, and Loss Ratio during preprocessing strengthened the analytical foundation of the project, while subsequent corrections to KPI mapping ensured consistency across generated reports, executive summaries, and dashboard services.

With these implementations complete, the backend analytics layer of the Healthcare Analytics Agent is fully operational and ready for Streamlit dashboard development and AI Copilot integration.
