import streamlit as st
import plotly.express as px
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from src.utils.dashboard_loader import service

st.title("Claims Analytics")

frequency = service.get_frequency_by_age()

fig = px.bar(
    frequency,
    x="age_band",
    y="avg_frequency",
    title="Claim Frequency by Age Band",
)

st.plotly_chart(
    fig,
    width="stretch",
)

severity = service.get_severity_by_age()

fig2 = px.bar(
    severity,
    x="age_band",
    y="avg_severity",
    title="Claim Severity by Age Band",
)

st.plotly_chart(
    fig2,
    width="stretch",
)

st.subheader("Top Loss Segments")

st.dataframe(
    service.get_top_loss_segments(),
    width="stretch",
)
