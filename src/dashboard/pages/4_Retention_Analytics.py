"""
4_Retention_Analytics.py

Retention Analytics Dashboard

Responsibilities
----------------
- Lapse Prediction Summary
- Lapse Probability
- Retention Summary
- Revenue at Risk
- Recommended Retention Actions

No analytics logic lives here.
"""

from __future__ import annotations

import streamlit as st
import plotly.express as px

from src.utils.dashboard_loader import DashboardLoader

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Retention Analytics",
    page_icon="🔄",
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

Please execute the Healthcare Analytics Pipeline first.
"""
    )

    st.stop()

# ==========================================================
# Load Data
# ==========================================================

try:

    lapse_predictions = loader.load_lapse_predictions()

    retention_summary = loader.load_retention_summary()

    lapse_summary = loader.load_lapse_summary()

except Exception as e:

    st.error(str(e))

    st.stop()

# ==========================================================
# Header
# ==========================================================

st.title("🔄 Retention Analytics")

st.caption(
    "Customer lapse prediction and retention intelligence"
)

st.divider()

# ==========================================================
# Retention Summary
# ==========================================================

st.subheader("Retention Summary")

st.dataframe(
    retention_summary,
    use_container_width=True,
)

st.divider()

# ==========================================================
# Risk Segment Distribution
# ==========================================================

st.subheader("Customer Risk Segments")

if (
    "risk_segment" in lapse_predictions.columns
):

    distribution = (
        lapse_predictions["risk_segment"]
        .value_counts()
        .reset_index()
    )

    distribution.columns = [
        "Risk Segment",
        "Policies",
    ]

    fig = px.pie(
        distribution,
        names="Risk Segment",
        values="Policies",
        hole=0.45,
        title="Portfolio Risk Segments",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.info(
        "Risk segment information unavailable."
    )

st.divider()

# ==========================================================
# Lapse Probability Distribution
# ==========================================================

st.subheader("Lapse Probability Distribution")

if (
    "lapse_probability"
    in lapse_predictions.columns
):

    fig = px.histogram(
        lapse_predictions,
        x="lapse_probability",
        nbins=30,
        title="Lapse Probability",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.info(
        "Lapse probability unavailable."
    )

st.divider()

# ==========================================================
# Sample Predictions
# ==========================================================

st.subheader("Sample Customer Predictions")

st.dataframe(
    lapse_predictions.head(25),
    use_container_width=True,
)

st.divider()

# ==========================================================
# Lapse Report
# ==========================================================

st.subheader("Lapse Summary")

if isinstance(lapse_summary, dict):

    st.json(lapse_summary)

else:

    st.write(lapse_summary)

st.divider()

# ==========================================================
# Business Insights
# ==========================================================

st.subheader("Business Insights")

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
High lapse probability customers should
be prioritized for proactive retention
campaigns and premium review.
"""
    )

with col2:

    st.info(
        """
Retention strategies should focus on
maximizing expected ROI while reducing
future premium leakage.
"""
    )

st.divider()

# ==========================================================
# Raw Data
# ==========================================================

with st.expander("View Raw Retention Data"):

    tab1, tab2, tab3 = st.tabs(
        [
            "Predictions",
            "Retention Summary",
            "Lapse Report",
        ]
    )

    with tab1:

        st.dataframe(
            lapse_predictions,
            use_container_width=True,
        )

    with tab2:

        st.dataframe(
            retention_summary,
            use_container_width=True,
        )

    with tab3:

        if isinstance(lapse_summary, dict):

            st.json(lapse_summary)

        else:

            st.write(lapse_summary)