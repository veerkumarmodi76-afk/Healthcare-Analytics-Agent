"""
landing.py

Landing Page Component

Responsibilities
----------------
- Display application welcome screen
- Detect existing portfolio
- Upload new datasets
- Execute the master pipeline
- Display pipeline progress
- Show execution summary

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
    """
    Check whether a processed portfolio already exists.
    """
    return all(file.exists() for file in REQUIRED_FILES)


def last_pipeline_run() -> str:
    """
    Return the timestamp of the latest pipeline execution.
    """

    log_file = OUTPUTS / "pipeline_log.txt"

    if not log_file.exists():
        return "Never"

    modified = datetime.fromtimestamp(
        log_file.stat().st_mtime
    )

    return modified.strftime("%d %b %Y  %I:%M %p")


# ==========================================================
# Existing Portfolio Section
# ==========================================================

def existing_portfolio_card():

    st.success("Existing portfolio detected.")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Status",
            "Ready",
        )

        st.metric(
            "Last Pipeline Run",
            last_pipeline_run(),
        )

    with col2:

        st.metric(
            "Outputs",
            "Available",
        )

        st.metric(
            "Analytics",
            "Ready",
        )

    st.info(
        """
Use the navigation menu on the left to access:

• Executive Dashboard

• Risk Analytics

• Pricing Analytics

• Claims Analytics

• Retention Analytics

• Trend Analytics

• AI Copilot
"""
    )


# ==========================================================
# Upload Section
# ==========================================================

def upload_section():

    st.subheader("Upload Healthcare Portfolio")

    upload_dataset()

    if st.session_state.get("dataset_ready", False):

        st.success("Dataset uploaded successfully.")

        st.write("")

        if st.button(
            "Run Analytics",
            type="primary",
            use_container_width=True,
        ):

            render_pipeline_status()

            success = run_pipeline()

            render_pipeline_status()

            if success:

                st.success(
                    "Analytics completed successfully."
                )

                st.balloons()

                st.info(
                    """
Dashboard pages are now available
from the navigation menu.
"""
                )


# ==========================================================
# Landing Page
# ==========================================================

def render_landing():

    st.title(
        "🏥 Healthcare Insurance Decision Intelligence Platform"
    )

    st.caption(
        "Enterprise AI Platform for Healthcare Insurance Analytics"
    )

    st.divider()

    if portfolio_exists():

        existing_portfolio_card()

        st.divider()

        with st.expander(
            "Upload New Portfolio",
            expanded=False,
        ):

            upload_section()

    else:

        st.warning(
            "No processed portfolio was found."
        )

        st.write(
            """
Upload a healthcare insurance dataset to
generate underwriting, pricing, lapse,
portfolio analytics, reports, and
dashboard-ready outputs.
"""
        )

        upload_section()

    st.divider()

    with st.expander(
        "Platform Overview",
        expanded=False,
    ):

        st.markdown(
            """
### Pipeline Modules

- Data Validation
- Data Preprocessing
- Underwriting Intelligence
- Pricing Intelligence
- Lapse Prediction
- Portfolio Analytics

---

### Dashboard Modules

- Executive Dashboard
- Risk Analytics
- Claims Analytics
- Pricing Analytics
- Retention Analytics
- Trend Analytics
- AI Copilot

---

### Supported Input Formats

- CSV
- XLSX

---

### Workflow

1. Upload Dataset
2. Execute Master Pipeline
3. Generate Reports
4. Open Dashboard
5. Explore AI Copilot
"""
        )