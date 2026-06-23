from pathlib import Path
import pandas as pd

BASE = Path("outputs/portfolio")


def build_context() -> str:

    metrics = pd.read_csv(BASE / "portfolio_metrics.csv")

    risk = pd.read_csv(BASE / "risk_profitability.csv")

    retention = pd.read_csv(BASE / "retention_summary.csv")

    leakage = pd.read_csv(BASE / "premium_leakage.csv")

    return f"""
PORTFOLIO METRICS

{metrics.to_string(index=False)}

RISK PROFITABILITY

{risk.to_string(index=False)}

RETENTION SUMMARY

{retention.to_string(index=False)}

PREMIUM LEAKAGE

{leakage.to_string(index=False)}
"""
