"""
1_Executive_Dashboard.py

Executive Dashboard

Enterprise overview of the Healthcare Insurance
Decision Intelligence Platform.

This page displays high-level portfolio KPIs,
portfolio health and executive insights.

No analytics logic lives here.
"""

from __future__ import annotations
import streamlit as st
import pandas as pd

from src.utils.dashboard_loader import DashboardLoader


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
)

loader = DashboardLoader()


# ==========================================================
# Portfolio Validation
# ==========================================================

if not loader.portfolio_exists():

    st.warning(
        """
No processed portfolio was found.

Upload a healthcare dataset and run the
master pipeline before opening dashboard pages.
"""
    )

    st.stop()


# ==========================================================
# Load Data
# ==========================================================

try:

    executive_kpis = loader.load_executive_kpis()

    portfolio_metrics = loader.load_portfolio_metrics()

    portfolio_health = loader.load_portfolio_health()

    executive_summary = loader.load_executive_summary()

except Exception as e:

    st.error(e)

    st.stop()


# ==========================================================
# Helper
# ==========================================================

def metric_value(df: pd.DataFrame, name: str):

    metric_col = df.columns[0]
    value_col = df.columns[1]

    row = df[
        df[metric_col].astype(str).str.lower()
        == name.lower()
    ]

    if row.empty:
        return "N/A"

    return row.iloc[0][value_col]


# ==========================================================
# Header
# ==========================================================

st.title("📊 Executive Dashboard")

st.caption(
    "Healthcare Insurance Decision Intelligence Platform"
)

st.divider()


# ==========================================================
# Portfolio Status
# ==========================================================

st.subheader("Portfolio Status")

col1, col2, col3 = st.columns(3)

with col1:

    st.success("Portfolio Ready")

with col2:

    st.info("Analytics Completed")

with col3:

    st.success("Pipeline Healthy")


st.divider()


# ==========================================================
# Executive KPIs
# ==========================================================

st.subheader("Executive KPIs")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Policies",
        f"{int(metric_value(executive_kpis, 'total_policies')):,}",
    )

    st.metric(
        "Insured Lives",
        f"{int(metric_value(executive_kpis, 'total_insured')):,}",
    )

    st.metric(
        "Total Premium",
        f"{float(metric_value(executive_kpis, 'total_premium')):,.2f}",
    )

with col2:

    st.metric(
        "Total Claims",
        f"{float(metric_value(executive_kpis, 'total_claims')):,.2f}",
    )

    st.metric(
        "Total Profit",
        f"{float(metric_value(executive_kpis, 'total_profit')):,.2f}",
    )

with col3:

    st.metric(
        "Loss Ratio",
        f"{float(metric_value(executive_kpis, 'loss_ratio_pct')):.2f}%",
    )

    st.metric(
        "Average Risk",
        f"{float(metric_value(portfolio_metrics, 'avg_risk_score')):.2f}",
    )


st.divider()


# ==========================================================
# Portfolio Health
# ==========================================================

st.subheader("Portfolio Health")

st.dataframe(
    portfolio_health,
    use_container_width=True,
)


st.divider()


# ==========================================================
# Executive Summary
# ==========================================================

st.subheader("Executive Summary")

st.text(executive_summary)


st.divider()


# ==========================================================
# Business Insights
# ==========================================================

st.subheader("Business Insights")

insight1, insight2 = st.columns(2)

with insight1:

    st.info(
        """
Review portfolio health, premium performance,
and loss ratio to assess overall business
performance.
"""
    )

with insight2:

    st.info(
        """
Use Risk, Pricing, Claims and Retention
Analytics pages for detailed operational
analysis.
"""
    )


st.divider()


# ==========================================================
# Quick Navigation
# ==========================================================

st.subheader("Available Dashboard Modules")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("Risk Analytics")

with col2:
    st.success("Claims Analytics")

with col3:
    st.success("Pricing Analytics")

with col4:
    st.success("AI Copilot")
