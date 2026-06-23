from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import streamlit as st
import plotly.express as px

from src.utils.dashboard_loader import service


st.title("Trend Analytics")

# ==========================================
# Premium Trend
# ==========================================

st.subheader("Premium Trend")

premium = service.get_premium_trend()

fig = px.line(
    premium,
    x="period",
    y="total_premium",
    markers=True,
    title="Total Premium by Period",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.dataframe(
    premium,
    use_container_width=True,
)

# ==========================================
# Claims Trend
# ==========================================

st.subheader("Claims Trend")

claims = service.get_claims_trend()

fig = px.line(
    claims,
    x="period",
    y="total_claims",
    markers=True,
    title="Total Claims by Period",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.dataframe(
    claims,
    use_container_width=True,
)

# ==========================================
# Loss Ratio Trend
# ==========================================

st.subheader("Loss Ratio Trend")

loss_ratio = service.get_loss_ratio_trend()

fig = px.line(
    loss_ratio,
    x="period",
    y="avg_loss_ratio_pct",
    markers=True,
    title="Average Loss Ratio %",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# Lapse Trend
# ==========================================

st.subheader("Lapse Trend")

lapse = service.get_lapse_trend()

fig = px.line(
    lapse,
    x="period",
    y="lapse_rate_pct",
    markers=True,
    title="Lapse Rate %",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# Risk Mix Trend
# ==========================================

st.subheader("Risk Mix Trend")

risk_mix = service.get_risk_mix_trend()

fig = px.area(
    risk_mix,
    x="period",
    y="percentage",
    color="risk_class",
    title="Risk Mix Evolution",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================
# Portfolio Growth Summary
# ==========================================

st.subheader("Portfolio Growth Summary")

growth = service.get_portfolio_growth_summary()

st.dataframe(
    growth,
    use_container_width=True,
)
