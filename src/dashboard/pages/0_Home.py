"""
0_Home.py

Healthcare Insurance Decision Intelligence Platform

Home / Welcome Page

Responsibilities
----------------
- Introduce the platform
- Guide first-time users
- Explain the workflow
- Explain execution modes
- Describe every module
- Provide quick start instructions

No analytics logic lives here.
"""

from __future__ import annotations

import streamlit as st

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🏥 Healthcare Insurance Decision Intelligence Platform")
st.caption("Enterprise AI Platform for Healthcare Insurance Analytics")

st.divider()

st.markdown(
    """
Welcome to the **Healthcare Insurance Decision Intelligence Platform**.

This platform transforms raw healthcare insurance portfolios into
business-ready insights using **Machine Learning**, **Explainable AI (XAI)**,
and **Business Intelligence**.

It assists healthcare insurers in making faster, more consistent,
and data-driven decisions across underwriting, pricing,
customer retention, and portfolio management.
"""
)

# ==========================================================
# PLATFORM WORKFLOW
# ==========================================================

st.header("🛣 Platform Workflow")

st.code(
    """
Upload Dataset
      │
      ▼
Validate Data
      │
      ▼
Preprocess Portfolio
      │
      ▼
Choose Execution Mode
      │
      ▼
Run Analytics Pipeline
      │
      ▼
Generate Reports
      │
      ▼
Explore Dashboards
      │
      ▼
Use AI Copilot
""",
    language="text",
)

st.divider()

# ==========================================================
# FIRST TIME USER GUIDE
# ==========================================================

st.header("🚀 First Time Setup")

steps = [
    "Open **Upload & Run** from the navigation menu.",
    "Upload your Healthcare Insurance dataset (CSV or XLSX).",
    "Choose an execution mode.",
    "Run the complete Healthcare Analytics Pipeline.",
    "Explore the generated dashboards and reports.",
    "Use the AI Copilot for interactive portfolio analysis.",
]

for i, step in enumerate(steps, start=1):
    st.success(f"Step {i}: {step}")

st.divider()

# ==========================================================
# EXECUTION MODES
# ==========================================================

st.header("⚙ Execution Modes")

prod, dev = st.columns(2)

with prod:

    st.success("🚀 Production Mode")

    st.markdown(
        """
### Recommended

Uses pretrained machine learning models.

**Best for**

- Daily business analysis
- Portfolio assessment
- Dashboard generation
- Fast execution
- Production deployment

No model retraining is performed.
"""
    )

with dev:

    st.warning("🛠 Developer Mode")

    st.markdown(
        """
### Advanced Users

Retrains all machine learning models before prediction.

**Best for**

- Model development
- Updated datasets
- Feature engineering
- Hyperparameter tuning
- Research experiments

Execution takes significantly longer.
"""
    )

st.divider()

# ==========================================================
# PLATFORM MODULES
# ==========================================================

st.header("📦 Platform Modules")

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("📊 Executive Dashboard")

    st.markdown(
        """
- Portfolio KPIs
- Business Summary
- Premium Overview
- Risk Distribution
"""
    )

    st.subheader("⚠ Underwriting")

    st.markdown(
        """
- Risk Classification
- Underwriting Decisions
- SHAP Explainability
- Individual Prediction Explanations
"""
    )

with col2:

    st.subheader("💰 Pricing")

    st.markdown(
        """
- Claim Cost Prediction
- Premium Recommendation
- Pricing Performance
- Portfolio Profitability
"""
    )

    st.subheader("🔄 Retention")

    st.markdown(
        """
- Lapse Prediction
- Revenue at Risk
- Customer Segmentation
- Retention Strategies
"""
    )

with col3:

    st.subheader("📈 Portfolio Analytics")

    st.markdown(
        """
- Exposure Analysis
- Claims Analysis
- Portfolio Trends
- Executive Reports
"""
    )

    st.subheader("🤖 AI Copilot")

    st.markdown(
        """
- Portfolio Question Answering
- Explain Predictions
- Business Insights
- Document Search (RAG)
"""
    )

st.divider()

# ==========================================================
# GENERATED OUTPUTS
# ==========================================================

st.header("📄 Generated Outputs")

left, right = st.columns(2)

with left:

    st.markdown(
        """
### Machine Learning Outputs

- Underwriting Predictions
- Premium Quotes
- Lapse Predictions
- SHAP Explainability Reports
"""
    )

with right:

    st.markdown(
        """
### Business Intelligence Outputs

- Executive KPIs
- Portfolio Analytics
- Pricing Reports
- Dashboard Visualizations
"""
    )

st.divider()

# ==========================================================
# SUPPORTED INPUTS
# ==========================================================

st.header("📁 Supported Input Formats")

st.info(
    """
Supported file types:

- CSV
- XLSX

Uploaded datasets are automatically validated and preprocessed before analytics are executed.
"""
)

st.divider()

# ==========================================================
# QUICK START
# ==========================================================

st.header("⚡ Quick Start")

st.markdown(
    """
1. Open **Upload & Run**
2. Upload your dataset
3. Select **Production Mode** *(recommended)*
4. Execute the Healthcare Analytics Pipeline
5. Explore dashboards and reports
6. Use the AI Copilot for deeper business insights
"""
)

st.divider()

# ==========================================================
# FAQ
# ==========================================================

st.header("❓ Frequently Asked Questions")

with st.expander("Which execution mode should I use?"):

    st.write(
        """
For almost all users, **Production Mode** is recommended.

Choose **Developer Mode** only when you need to retrain machine learning models using updated datasets.
"""
    )

with st.expander("Do I need to retrain models every time?"):

    st.write(
        """
No.

Once the machine learning models have been trained and saved,
Production Mode automatically reuses those trained models for future analyses.

Retraining is only required when new data or improved models are introduced.
"""
    )

with st.expander("What datasets are supported?"):

    st.write(
        """
Supported formats:

- CSV
- XLSX

The dataset should contain healthcare insurance portfolio information compatible with the platform's preprocessing pipeline.
"""
    )

with st.expander("What does the AI Copilot do?"):

    st.write(
        """
The AI Copilot can:

- Answer questions about your portfolio
- Explain model predictions
- Summarize business insights
- Search uploaded company documents using RAG
- Assist with insurance analytics
"""
    )

st.divider()

# ==========================================================
# PLATFORM SUMMARY
# ==========================================================

st.header("🎯 Platform Summary")

st.info(
    """
This platform integrates **Machine Learning**, **Explainable AI**, and
**Business Intelligence** into a unified decision support system for healthcare
insurance analytics.

Whether you are an underwriter, pricing analyst, portfolio manager, or business executive,
the platform provides actionable insights from a single workflow.
"""
)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "Healthcare Insurance Decision Intelligence Platform • Version 2.0"
)
