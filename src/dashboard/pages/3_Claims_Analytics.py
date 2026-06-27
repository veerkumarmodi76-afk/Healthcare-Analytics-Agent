"""
3_Claims_Analytics.py

Claims Analytics Dashboard

Responsibilities
----------------
- Claim Frequency Analysis
- Claim Severity Analysis
- Portfolio Claims Summary
- Top Loss Segments
- Loss Performance

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
    page_title="Claims Analytics",
    page_icon="🏥",
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

Run the Healthcare Analytics Pipeline first.
"""
    )
    st.stop()

# ==========================================================
# Load Data
# ==========================================================

try:

    claim_frequency = loader.load_claim_frequency()

    claim_severity = loader.load_claim_severity()

    claim_summary = loader.load_claim_summary()

    top_loss_segments = loader.load_top_loss_segments()

except Exception as e:

    st.error(str(e))
    st.stop()

# ==========================================================
# Header
# ==========================================================

st.title("🏥 Claims Analytics")

st.caption(
    "Claims behaviour, severity and loss performance"
)

st.divider()

# ==========================================================
# Claim Frequency
# ==========================================================

st.subheader("Claim Frequency")

if len(claim_frequency.columns) >= 2:

    fig = px.bar(
        claim_frequency,
        x=claim_frequency.columns[0],
        y=claim_frequency.columns[1],
        title="Claim Frequency by Age",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.dataframe(
        claim_frequency,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# Claim Severity
# ==========================================================

st.subheader("Claim Severity")

if len(claim_severity.columns) >= 2:

    fig = px.bar(
        claim_severity,
        x=claim_severity.columns[0],
        y=claim_severity.columns[1],
        title="Average Claim Severity",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.dataframe(
        claim_severity,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# Claims Summary
# ==========================================================

st.subheader("Claims Summary")

st.dataframe(
    claim_summary,
    use_container_width=True,
)

st.divider()

# ==========================================================
# Top Loss Segments
# ==========================================================

st.subheader("Top Loss Segments")

st.dataframe(
    top_loss_segments,
    use_container_width=True,
)

st.divider()

# ==========================================================
# Business Insights
# ==========================================================

st.subheader("Claims Insights")

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
Claim frequency indicates how often claims occur
across different portfolio segments.
Higher frequency may require underwriting review.
"""
    )

with col2:

    st.info(
        """
Claim severity measures the financial impact
of each claim and helps identify high-cost
customer groups.
"""
    )

st.divider()

# ==========================================================
# Raw Data
# ==========================================================

with st.expander("View Raw Claims Data"):

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Frequency",
            "Severity",
            "Summary",
            "Loss Segments",
        ]
    )

    with tab1:
        st.dataframe(
            claim_frequency,
            use_container_width=True,
        )

    with tab2:
        st.dataframe(
            claim_severity,
            use_container_width=True,
        )

    with tab3:
        st.dataframe(
            claim_summary,
            use_container_width=True,
        )

    with tab4:
        st.dataframe(
            top_loss_segments,
            use_container_width=True,
        )