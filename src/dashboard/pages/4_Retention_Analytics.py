import streamlit as st
import plotly.express as px
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from src.utils.dashboard_loader import service

st.title("Retention Analytics")

retention = service.get_retention_summary()

fig = px.pie(
    retention,
    names="retention_segment",
    values="customers",
    title="Retention Segments",
)

st.plotly_chart(
    fig,
    width="stretch",
)

fig2 = px.bar(
    retention,
    x="retention_segment",
    y="premium_at_risk",
    title="Premium at Risk",
)

st.plotly_chart(
    fig2,
    width="stretch",
)

st.dataframe(
    retention,
    width="stretch",
)
