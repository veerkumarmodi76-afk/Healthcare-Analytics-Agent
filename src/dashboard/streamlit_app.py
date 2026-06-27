"""
streamlit_app.py

Healthcare Insurance Decision Intelligence Platform

Main Streamlit Entry Point

Responsibilities
----------------
- Configure Streamlit
- Initialize application state
- Render sidebar
- Render landing page

Analytics, pipeline execution and dashboard logic
live in dedicated components.
"""

from __future__ import annotations

import streamlit as st

from src.dashboard.components.sidebar import render_sidebar
from src.dashboard.components.landing import render_landing

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Healthcare Insurance Decision Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# Session Initialization
# ==========================================================

def initialize_session():
    """
    Initialize global application session state.
    """

    defaults = {

        "pipeline_running": False,

        "pipeline_finished": False,

        "pipeline_success": False,

        "pipeline_state": None,

        "messages": [],

        "copilot": None,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ==========================================================
# Main Application
# ==========================================================

def main():

    initialize_session()

    render_sidebar()

    render_landing()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()