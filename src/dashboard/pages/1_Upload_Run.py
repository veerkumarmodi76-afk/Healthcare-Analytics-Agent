"""
1_Upload_Run.py

Upload & Run

Execute the Healthcare Insurance Analytics Pipeline.

Responsibilities
----------------
- Upload healthcare insurance datasets
- Configure execution mode
- Execute analytics pipeline
- Monitor pipeline progress
- Display execution summary

No analytics logic lives here.
"""

from __future__ import annotations

import streamlit as st

from src.dashboard.components.landing import render_landing


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Upload & Run",
    page_icon="📤",
    layout="wide",
)

# ==========================================================
# Render Page
# ==========================================================

render_landing()
