"""
2_Risk_Analytics.py

Risk Analytics Dashboard

Responsibilities
----------------
- Portfolio Risk Distribution
- Risk by Age Band
- Risk by Policy Type
- Risk by Distribution Channel
- Risk Profitability
- Risk Premium Summary
- Risk Claims Summary

No analytics logic lives here.
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils.dashboard_loader import DashboardLoader

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Risk Analytics",
    page_icon="⚠️",
    layout="wide",
)

loader = DashboardLoader()

# ==========================================================
# Portfolio Validation
# ==========================================================

if not loader.portfolio_exists():

    st.warning(
        """
No processed portfolio found.

Please upload a dataset and execute the
master pipeline first.
"""
    )

    st.stop()

# ==========================================================
# Load Data
# ==========================================================

try:

    risk_distribution = loader.load_risk_distribution()

    risk_by_age = loader.load_risk_by_age()

    risk_by_channel = loader.load_risk_by_channel()

    risk_by_policy = loader.load_risk_by_policy()

    risk_profitability = loader.load_risk_profitability()

except Exception as e:

    st.error(e)

    st.stop()

# ==========================================================
# Header
# ==========================================================

st.title("⚠️ Risk Analytics")

st.caption(
    "Portfolio risk distribution and segmentation"
)

st.divider()

# ==========================================================
# Portfolio Risk Distribution
# ==========================================================

st.subheader("Portfolio Risk Distribution")

if len(risk_distribution.columns) >= 2:

    fig = px.pie(
        risk_distribution,
        names=risk_distribution.columns[0],
        values=risk_distribution.columns[1],
        hole=0.45,
        title="Risk Class Distribution",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.dataframe(
        risk_distribution,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# Risk by Age Band
# ==========================================================

st.subheader("Risk by Age Band")

if len(risk_by_age.columns) >= 2:

    fig = px.bar(
        risk_by_age,
        x=risk_by_age.columns[0],
        y=risk_by_age.columns[1],
        title="Risk by Age Band",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.dataframe(
        risk_by_age,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# Risk by Policy Type
# ==========================================================

st.subheader("Risk by Policy Type")

if len(risk_by_policy.columns) >= 2:

    fig = px.bar(
        risk_by_policy,
        x=risk_by_policy.columns[0],
        y=risk_by_policy.columns[1],
        title="Risk by Policy Type",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.dataframe(
        risk_by_policy,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# Risk by Distribution Channel
# ==========================================================

st.subheader("Risk by Distribution Channel")

if len(risk_by_channel.columns) >= 2:

    fig = px.bar(
        risk_by_channel,
        x=risk_by_channel.columns[0],
        y=risk_by_channel.columns[1],
        title="Risk by Distribution Channel",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.dataframe(
        risk_by_channel,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# Risk Profitability
# ==========================================================

st.subheader("Risk Profitability")

st.dataframe(
    risk_profitability,
    use_container_width=True,
)

st.divider()

# ==========================================================
# Portfolio Insights
# ==========================================================

st.subheader("Risk Insights")

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
Review the distribution of policyholders
across risk classes to identify segments
requiring enhanced underwriting attention.
"""
    )

with col2:

    st.info(
        """
Compare age, policy type, and distribution
channel to identify concentrations of
higher-risk business.
"""
    )

st.divider()

# ==========================================================
# Raw Data
# ==========================================================

with st.expander(
    "View Raw Risk Data",
    expanded=False,
):

    tabs = st.tabs(
        [
            "Distribution",
            "Age",
            "Policy",
            "Channel",
            "Profitability",
        ]
    )

    with tabs[0]:
        st.dataframe(
            risk_distribution,
            use_container_width=True,
        )

    with tabs[1]:
        st.dataframe(
            risk_by_age,
            use_container_width=True,
        )

    with tabs[2]:
        st.dataframe(
            risk_by_policy,
            use_container_width=True,
        )

    with tabs[3]:
        st.dataframe(
            risk_by_channel,
            use_container_width=True,
        )

    with tabs[4]:
        st.dataframe(
            risk_profitability,
            use_container_width=True,
        )
