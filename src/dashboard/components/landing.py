"""
landing.py

Upload & Run Component

Responsibilities
----------------
- Upload healthcare datasets
- Configure execution mode
- Execute analytics pipeline
- Display pipeline progress
- Show portfolio status

No analytics logic lives here.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

import streamlit as st

from .uploader import upload_dataset
from .pipeline_status import (
    run_pipeline,
    render_pipeline_status,
)

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

OUTPUTS = PROJECT_ROOT / "outputs"

REQUIRED_FILES = [
    OUTPUTS / "portfolio" / "executive_kpis.csv",
    OUTPUTS / "portfolio" / "portfolio_metrics.csv",
    OUTPUTS / "pricing" / "premium_quotes.csv",
    OUTPUTS / "underwriting" / "underwriting_predictions.csv",
    OUTPUTS / "lapse" / "lapse_predictions.csv",
]


# ==========================================================
# Helpers
# ==========================================================

def portfolio_exists() -> bool:
    """Return True if pipeline outputs exist."""

    return all(file.exists() for file in REQUIRED_FILES)


def last_pipeline_run() -> str:
    """Return last pipeline execution time."""

    log_file = OUTPUTS / "pipeline_log.txt"

    if not log_file.exists():
        return "Never"

    modified = datetime.fromtimestamp(
        log_file.stat().st_mtime
    )

    return modified.strftime("%d %b %Y  %I:%M %p")


# ==========================================================
# Existing Portfolio
# ==========================================================

def existing_portfolio_card():

    st.success("A processed healthcare portfolio is available.")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Status", "Ready")
    c2.metric("Outputs", "Available")
    c3.metric("Last Run", last_pipeline_run())
    c4.metric("Dashboards", "Ready")

    st.info(
        """
The analytics outputs have already been generated.

You can immediately explore the dashboard pages from the navigation menu,
or upload a new portfolio below to perform another analysis.
"""
    )


# ==========================================================
# Upload Section
# ==========================================================

def upload_section():

    st.subheader("📁 Upload Dataset")

    upload_dataset()

    if not st.session_state.get("dataset_ready", False):
        return

    st.success("Dataset uploaded successfully.")

    st.divider()

    st.subheader("⚙ Execution Mode")

    execution_mode = st.radio(
        "Choose how the analytics pipeline should run.",
        [
            "Production (Use Pretrained Models)",
            "Developer (Retrain Models)",
        ],
        index=0,
    )

    st.session_state["execution_mode"] = execution_mode

    if execution_mode.startswith("Production"):

        st.info(
            """
Recommended for most users.

Uses pretrained machine learning models for fast and consistent analytics.
"""
        )

    else:

        st.warning(
            """
Retrains every machine learning model before generating predictions.

Recommended only when updating models or experimenting with new datasets.
"""
        )

    st.divider()

    st.success("Configuration complete. Ready to execute.")

    if st.button(
        "🚀 Run Analytics Pipeline",
        type="primary",
        use_container_width=True,
    ):

        render_pipeline_status()

        success = run_pipeline()

        render_pipeline_status()

        if success:

            st.success(
                """
Analytics pipeline completed successfully.

Generated outputs include:

• Underwriting Predictions

• Premium Quotes

• Lapse Predictions

• Portfolio Analytics

• Executive KPIs

Dashboard pages are now ready to use.
"""
            )

            st.balloons()


# ==========================================================
# Main Page
# ==========================================================

def render_landing():

    st.title("📤 Upload & Run")

    st.caption(
        "Upload a healthcare insurance portfolio and execute the analytics pipeline."
    )

    st.info(
        """
### Pipeline Workflow

Upload Dataset

↓

Configure Execution Mode

↓

Run Analytics Pipeline

↓

Generate Outputs

↓

Explore Dashboards
"""
    )

    st.divider()

    if portfolio_exists():

        existing_portfolio_card()

        st.divider()

        with st.expander(
            "Upload a New Portfolio",
            expanded=False,
        ):

            upload_section()

    else:

        st.warning("No processed portfolio is currently available.")

        st.info(
            """
Upload a healthcare insurance dataset to begin analysis.

The platform will automatically:

• Validate the dataset

• Preprocess the portfolio

• Execute the analytics pipeline

• Generate machine learning predictions

• Produce dashboard-ready outputs
"""
        )

        upload_section()
