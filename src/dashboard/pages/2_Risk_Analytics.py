import streamlit as st
import plotly.express as px
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.utils.dashboard_loader import service

st.title("Risk Analytics")

risk_dist = service.get_risk_distribution()

fig = px.pie(
    risk_dist, names="risk_class", values="policy_count", title="Risk Distribution"
)

st.plotly_chart(
    fig,
    width="stretch",
)

risk_profit = service.get_risk_profitability()

fig2 = px.bar(
    risk_profit,
    x="risk_class",
    y="profit",
    title="Profit by Risk Class",
)

st.plotly_chart(
    fig2,
    width="stretch",
)

st.dataframe(
    risk_profit,
    width="stretch",
)
