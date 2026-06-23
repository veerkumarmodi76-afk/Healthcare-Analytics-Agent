import streamlit as st
import plotly.express as px
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from src.utils.dashboard_loader import service

st.title("Pricing Analytics")

leakage = service.get_premium_leakage()

fig = px.bar(
    leakage,
    x="risk_class",
    y="premium_leakage",
    title="Premium Leakage",
)

st.plotly_chart(
    fig,
    width="stretch",
)

st.dataframe(
    leakage,
    width="stretch",
)
