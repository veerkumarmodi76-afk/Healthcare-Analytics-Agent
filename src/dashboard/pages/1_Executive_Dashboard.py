import streamlit as st
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from src.utils.dashboard_loader import service

st.title("Executive Dashboard")

summary = service.get_dashboard_summary()

c1, c2, c3 = st.columns(3)

c1.metric("Total Premium", f"{summary['total_premium']:,.0f}")

c2.metric("Total Claims", f"{summary['total_claims']:,.0f}")

c3.metric("Loss Ratio %", f"{summary['loss_ratio']:.2f}")

c4, c5, c6 = st.columns(3)

c4.metric("Policies", f"{summary['total_policies']:,.0f}")

c5.metric("Avg Risk Score", f"{summary['avg_risk_score']:.2f}")

c6.metric("Avg Lapse %", f"{summary['avg_lapse_probability']:.2f}")

st.divider()

st.subheader("Executive Insights")

for insight in service.generate_executive_insights():
    st.info(insight)
