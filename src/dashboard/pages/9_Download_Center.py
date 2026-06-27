"""
9_Download_Center.py

Download Center

Responsibilities
----------------
- Download generated reports
- Download CSV outputs
- Download JSON outputs
- Download Markdown reports
- Browse generated artifacts

No analytics logic lives here.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.utils.dashboard_loader import DashboardLoader

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Download Center",
    page_icon="📥",
    layout="wide",
)

loader = DashboardLoader()

# ==========================================================
# Portfolio Validation
# ==========================================================

if not loader.portfolio_exists():

    st.warning(
        """
No processed portfolio found.

Run the Healthcare Analytics Pipeline first.
"""
    )

    st.stop()

# ==========================================================
# Header
# ==========================================================

st.title("📥 Download Center")

st.caption(
    "Download reports, datasets and analytical outputs."
)

st.divider()

# ==========================================================
# Load Available Files
# ==========================================================

reports = loader.available_reports()

if not reports:

    st.info("No downloadable files available.")

    st.stop()

# ==========================================================
# Statistics
# ==========================================================

csv_files = 0
json_files = 0
markdown_files = 0
other_files = 0

for file in reports.values():

    suffix = file.suffix.lower()

    if suffix == ".csv":
        csv_files += 1
    elif suffix == ".json":
        json_files += 1
    elif suffix in [".md", ".txt"]:
        markdown_files += 1
    else:
        other_files += 1

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("CSV Files", csv_files)

with col2:
    st.metric("JSON Files", json_files)

with col3:
    st.metric("Reports", markdown_files)

with col4:
    st.metric("Other", other_files)

st.divider()

# ==========================================================
# Downloads
# ==========================================================

st.subheader("Available Downloads")

for filename, filepath in sorted(reports.items()):

    suffix = filepath.suffix.lower()

    if suffix == ".csv":
        icon = "📊"
    elif suffix == ".json":
        icon = "📦"
    elif suffix == ".md":
        icon = "📝"
    elif suffix == ".txt":
        icon = "📄"
    elif suffix in [".png", ".jpg", ".jpeg"]:
        icon = "🖼️"
    else:
        icon = "📁"

    with st.expander(f"{icon} {filename}"):

        st.write(f"**Location:** `{filepath}`")

        st.write(
            f"**Size:** {filepath.stat().st_size / 1024:.2f} KB"
        )

        with open(filepath, "rb") as file:

            st.download_button(
                label=f"Download {filename}",
                data=file.read(),
                file_name=filename,
                mime="application/octet-stream",
                use_container_width=True,
            )

st.divider()

# ==========================================================
# Download Categories
# ==========================================================

st.subheader("Generated Output Categories")

st.markdown(
    """
### Dashboard Outputs

- Portfolio Analytics
- Executive KPIs
- Claims Analytics
- Risk Analytics
- Pricing Analytics
- Retention Analytics

---

### Machine Learning Outputs

- Underwriting Predictions
- Pricing Predictions
- Lapse Predictions
- SHAP Explainability

---

### Reports

- Executive Summary
- Pricing Report
- Lapse Report
- Pipeline Reports
- Validation Reports

---

### Metadata

- Model Metadata
- Feature Importance
- Training Metrics
- Prediction Metadata
"""
)

st.divider()

# ==========================================================
# Footer
# ==========================================================

st.success(
    f"{len(reports)} generated files are available for download."
)
