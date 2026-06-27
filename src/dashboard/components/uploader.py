"""
Dataset Upload Component

Responsible for:

• Validating uploaded datasets
• Saving uploaded files
• Converting Excel to CSV
• Preparing data for the master pipeline
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
import streamlit as st


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_DATA_PATH = RAW_DATA_DIR / "raw_data.csv"

SUPPORTED_EXTENSIONS = ["csv", "xlsx"]


# ============================================================
# Validation
# ============================================================

def validate_extension(filename: str) -> bool:
    """
    Validate uploaded file extension.
    """
    extension = filename.split(".")[-1].lower()
    return extension in SUPPORTED_EXTENSIONS


# ============================================================
# Save Uploaded Dataset
# ============================================================

def save_uploaded_dataset(uploaded_file) -> Tuple[bool, str]:
    """
    Save uploaded dataset as data/raw/raw_data.csv

    Returns
    -------
    success : bool

    message : str
    """

    try:

        if uploaded_file is None:
            return False, "No dataset uploaded."

        if not validate_extension(uploaded_file.name):
            return (
                False,
                "Unsupported file format. Upload CSV or XLSX.",
            )

        extension = uploaded_file.name.split(".")[-1].lower()

        # ------------------------------------------
        # CSV
        # ------------------------------------------

        if extension == "csv":

            df = pd.read_csv(uploaded_file)

        # ------------------------------------------
        # Excel
        # ------------------------------------------

        elif extension == "xlsx":

            df = pd.read_excel(uploaded_file)

        else:

            return False, "Unsupported dataset."

        # ------------------------------------------
        # Basic validation
        # ------------------------------------------

        if df.empty:

            return False, "Dataset is empty."

        # ------------------------------------------
        # Save
        # ------------------------------------------

        df.to_csv(
            RAW_DATA_PATH,
            index=False,
        )

        return (
            True,
            f"Dataset saved successfully ({len(df):,} rows).",
        )

    except Exception as e:

        return False, str(e)


# ============================================================
# Streamlit Upload Widget
# ============================================================

def upload_dataset():
    """
    Render upload widget.

    Returns
    -------
    bool
        True if dataset saved successfully.

    """

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=SUPPORTED_EXTENSIONS,
    )

    if uploaded_file is None:
        return False

    st.success(f"Selected: {uploaded_file.name}")

    file_size = uploaded_file.size / (1024 * 1024)

    st.caption(f"File Size: {file_size:.2f} MB")

    if st.button(
        "Save Dataset",
        use_container_width=True,
    ):

        with st.spinner("Saving dataset..."):

            success, message = save_uploaded_dataset(uploaded_file)

        if success:

            st.session_state["dataset_ready"] = True

            st.success(message)

            st.info(
                "Dataset is ready for pipeline execution."
            )

            return True

        st.error(message)

    return False