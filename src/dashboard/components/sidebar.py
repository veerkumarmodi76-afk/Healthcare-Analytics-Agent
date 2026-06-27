"""
sidebar.py

Dashboard Sidebar Component

Responsibilities
----------------
- Display portfolio status
- Display pipeline status
- Display system information

Navigation is handled automatically by Streamlit.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

import streamlit as st

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

OUTPUT_DIR = PROJECT_ROOT / "outputs"

PIPELINE_LOG = OUTPUT_DIR / "pipeline_log.txt"

REQUIRED_OUTPUTS = [
    OUTPUT_DIR / "portfolio" / "executive_kpis.csv",
    OUTPUT_DIR / "portfolio" / "portfolio_metrics.csv",
    OUTPUT_DIR / "pricing" / "premium_quotes.csv",
    OUTPUT_DIR / "underwriting" / "underwriting_predictions.csv",
    OUTPUT_DIR / "lapse" / "lapse_predictions.csv",
]


# ==========================================================
# Helpers
# ==========================================================

def portfolio_available() -> bool:
    """Return True if analytics outputs exist."""
    return all(file.exists() for file in REQUIRED_OUTPUTS)


def last_pipeline_run() -> str:
    """Return last pipeline execution timestamp."""

    if not PIPELINE_LOG.exists():
        return "Never"

    modified = datetime.fromtimestamp(
        PIPELINE_LOG.stat().st_mtime
    )

    return modified.strftime("%d %b %Y\n%I:%M %p")


# ==========================================================
# Sidebar
# ==========================================================

def render_sidebar():

    with st.sidebar:

        st.title("🏥 AI-AIP")

        st.caption(
            "Healthcare Insurance Decision Intelligence Platform"
        )

        st.divider()

        # --------------------------------------------------
        # Portfolio Status
        # --------------------------------------------------

        st.subheader("📁 Portfolio")

        if portfolio_available():

            st.success("Ready")

        else:

            st.warning("Awaiting Dataset")

        st.caption(f"Last Pipeline Run\n{last_pipeline_run()}")

        st.divider()

        # --------------------------------------------------
        # Pipeline Status
        # --------------------------------------------------

        st.subheader("⚙ Pipeline")

        if st.session_state.get("pipeline_running", False):

            st.info("Running")

        elif st.session_state.get("pipeline_success", False):

            st.success("Completed")

        else:

            st.caption("Idle")

        st.divider()

        # --------------------------------------------------
        # System Information
        # --------------------------------------------------

        st.subheader("🖥 System")

        st.metric(
            "Version",
            "2.0.0",
        )

        st.metric(
            "Platform",
            "Operational",
        )

        st.metric(
            "Analytics",
            "Ready"
            if portfolio_available()
            else "Awaiting Data",
        )

        st.divider()

        st.caption(
            "Enterprise AI Platform for\nHealthcare Insurance Analytics"
        )
