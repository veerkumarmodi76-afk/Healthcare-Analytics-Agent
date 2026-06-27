"""
streamlit_app.py

Healthcare Insurance Decision Intelligence Platform

Main Entry Point
"""

from __future__ import annotations

import streamlit as st

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Healthcare Insurance Decision Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------
# Session Initialization
# ----------------------------------------------------------

def initialize_session():

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


initialize_session()
