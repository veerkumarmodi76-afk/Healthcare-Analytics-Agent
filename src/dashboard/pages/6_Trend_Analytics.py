"""
6_Trend_Analytics.py

Trend Analytics Dashboard

Responsibilities
----------------
- Premium Trend
- Claims Trend
- Loss Ratio Trend
- Lapse Trend
- Portfolio Growth
- Risk Mix Trend

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
    page_title="Trend Analytics",
    page_icon="📈",
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

    premium_trend = loader.load_premium_trend()

    claims_trend = loader.load_claims_trend()

    loss_ratio_trend = loader.load_loss_ratio_trend()

    lapse_trend = loader.load_lapse_trend()

    growth_trend = loader.load_growth_trend()

    risk_mix = loader.load_risk_mix_trend()

except Exception as e:

    st.error(str(e))

    st.stop()

# ==========================================================
# Header
# ==========================================================

st.title("📈 Trend Analytics")

st.caption(
    "Portfolio trends and business performance over time"
)

st.divider()

# ==========================================================
# Helper
# ==========================================================

def line_chart(df, title):

    if len(df.columns) >= 2:

        fig = px.line(
            df,
            x=df.columns[0],
            y=df.columns[1],
            markers=True,
            title=title,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.dataframe(
            df,
            use_container_width=True,
        )

# ==========================================================
# Premium Trend
# ==========================================================

st.subheader("Premium Trend")

line_chart(
    premium_trend,
    "Premium Trend",
)

st.divider()

# ==========================================================
# Claims Trend
# ==========================================================

st.subheader("Claims Trend")

line_chart(
    claims_trend,
    "Claims Trend",
)

st.divider()

# ==========================================================
# Loss Ratio Trend
# ==========================================================

st.subheader("Loss Ratio Trend")

line_chart(
    loss_ratio_trend,
    "Loss Ratio Trend",
)

st.divider()

# ==========================================================
# Lapse Trend
# ==========================================================

st.subheader("Lapse Trend")

line_chart(
    lapse_trend,
    "Lapse Trend",
)

st.divider()

# ==========================================================
# Portfolio Growth
# ==========================================================

st.subheader("Portfolio Growth")

line_chart(
    growth_trend,
    "Portfolio Growth",
)

st.divider()

# ==========================================================
# Risk Mix Trend
# ==========================================================

st.subheader("Risk Mix Trend")

if len(risk_mix.columns) >= 2:

    fig = px.bar(
        risk_mix,
        x=risk_mix.columns[0],
        y=risk_mix.columns[1],
        title="Risk Mix",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:

    st.dataframe(
        risk_mix,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# Trend Insights
# ==========================================================

st.subheader("Business Insights")

left, right = st.columns(2)

with left:

    st.info(
        """
Monitor premium and claims trends to
evaluate portfolio profitability and
pricing adequacy over time.
"""
    )

with right:

    st.info(
        """
Loss ratio and lapse trends help identify
changing portfolio risk and customer
retention behaviour.
"""
    )

st.divider()

# ==========================================================
# Raw Data
# ==========================================================

with st.expander("View Raw Trend Data"):

    tabs = st.tabs(
        [
            "Premium",
            "Claims",
            "Loss Ratio",
            "Lapse",
            "Growth",
            "Risk Mix",
        ]
    )

    datasets = [
        premium_trend,
        claims_trend,
        loss_ratio_trend,
        lapse_trend,
        growth_trend,
        risk_mix,
    ]

    for tab, df in zip(tabs, datasets):

        with tab:

            st.dataframe(
                df,
                use_container_width=True,
            )