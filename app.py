"""
app.py

Healthcare Insurance Decision Intelligence Platform

Application Entry Point
"""

from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================
# Global Configuration
# ==========================================================

st.set_page_config(
    page_title="Healthcare Insurance Decision Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# Session State
# ==========================================================

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
# Navigation
# ==========================================================

home = st.Page(
    "src/dashboard/pages/0_Home.py",
    title="Home",
    icon="🏠",
    default=True,
)

upload = st.Page(
    "src/dashboard/pages/1_Upload_Run.py",
    title="Upload & Run",
    icon="📤",
)

executive = st.Page(
    "src/dashboard/pages/2_Executive_Dashboard.py",
    title="Executive Dashboard",
    icon="📊",
)

risk = st.Page(
    "src/dashboard/pages/3_Risk_Analytics.py",
    title="Risk Analytics",
    icon="⚠️",
)

pricing = st.Page(
    "src/dashboard/pages/4_Pricing_Analytics.py",
    title="Pricing Analytics",
    icon="💰",
)

claims = st.Page(
    "src/dashboard/pages/5_Claims_Analytics.py",
    title="Claims Analytics",
    icon="📉",
)

retention = st.Page(
    "src/dashboard/pages/6_Retention_Analytics.py",
    title="Retention Analytics",
    icon="🔄",
)

portfolio = st.Page(
    "src/dashboard/pages/7_Trend_Analytics.py",
    title="Portfolio Analytics",
    icon="📈",
)

copilot = st.Page(
    "src/dashboard/pages/8_AI_Copilot.py",
    title="AI Copilot",
    icon="🤖",
)

navigation = st.navigation(
    {
        "Getting Started": [
            home,
            upload,
        ],
        "Analytics": [
            executive,
            risk,
            pricing,
            claims,
            retention,
            portfolio,
        ],
        "Artificial Intelligence": [
            copilot,
        ],
    }
)

navigation.run()
