"""
sidebar.py

Dashboard Sidebar Component

Responsibilities
----------------
- Display application information
- Display portfolio status
- Display pipeline status
- Display quick actions
- Display system information

No business logic lives here.
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
            "Healthcare Analytics Agent"
        )

        st.divider()

        # --------------------------------------------------
        # Portfolio Status
        # --------------------------------------------------

        st.subheader("Portfolio")

        if portfolio_available():

            st.success("Ready")

        else:

            st.warning("No Portfolio")

        st.caption(
            f"Last Run:\n{last_pipeline_run()}"
        )

        st.divider()

        # --------------------------------------------------
        # Pipeline
        # --------------------------------------------------

        st.subheader("Pipeline")

        if "pipeline_running" in st.session_state:

            if st.session_state.pipeline_running:

                st.info("Running")

            elif st.session_state.get(
                "pipeline_success",
                False,
            ):

                st.success("Completed")

            else:

                st.caption("Idle")

        else:

            st.caption("Idle")

        st.divider()

        # --------------------------------------------------
        # Modules
        # --------------------------------------------------

        st.subheader("Modules")

        modules = [
            "Validation",
            "Preprocessing",
            "Underwriting",
            "Pricing",
            "Lapse",
            "Portfolio",
        ]

        for module in modules:
            st.write(f"✓ {module}")

        st.divider()

        # --------------------------------------------------
        # Dashboard
        # --------------------------------------------------

        st.subheader("Dashboard")

        st.caption(
            """
Use the page navigation
above to access:

• Executive Dashboard

• Risk Analytics

• Claims Analytics

• Retention Analytics

• Pricing Analytics

• Trend Analytics

• Download Center

• AI Copilot
"""
        )

        st.divider()

        # --------------------------------------------------
        # System
        # --------------------------------------------------

        st.subheader("System")

        st.metric(
            "Version",
            "1.0.0",
        )

        st.metric(
            "Status",
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
            "Healthcare Insurance\nDecision Intelligence Platform"
        )