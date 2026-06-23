from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import streamlit as st


st.title("Download Center")

FILES = [
    "executive_summary.txt",
    "executive_kpis.csv",
    "portfolio_metrics.csv",
    "premium_leakage.csv",
    "retention_summary.csv",
]

BASE = ROOT / "outputs" / "portfolio"

for filename in FILES:
    path = BASE / filename

    if path.exists():
        with open(path, "rb") as f:
            st.download_button(
                label=f"Download {filename}",
                data=f,
                file_name=filename,
            )
