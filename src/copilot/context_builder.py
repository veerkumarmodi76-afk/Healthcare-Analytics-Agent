"""
context_builder.py

Builds grounded context for the AI Copilot.

Responsibilities
----------------
- Load portfolio analytics
- Load executive summaries
- Load pricing outputs
- Load underwriting outputs
- Load lapse outputs
- Optionally append enterprise document context (Phase 11)
- Return one grounded context string for Gemini
"""

from __future__ import annotations

import json
from typing import Optional

import pandas as pd

from src.utils.dashboard_loader import DashboardLoader


loader = DashboardLoader()


# ==========================================================
# Helpers
# ==========================================================

def _df_to_text(df: pd.DataFrame, title: str) -> str:
    """
    Safely convert a dataframe into readable text.
    """

    if df is None or df.empty:
        return f"\n## {title}\nNo data available.\n"

    return f"\n## {title}\n\n{df.to_string(index=False)}\n"


def _json_to_text(data: dict, title: str) -> str:
    """
    Safely convert JSON into formatted text.
    """

    if not data:
        return f"\n## {title}\nNo data available.\n"

    return (
        f"\n## {title}\n\n"
        f"{json.dumps(data, indent=2)}\n"
    )


# ==========================================================
# Context Builder
# ==========================================================

def build_context(
    document_context: Optional[str] = None,
) -> str:
    """
    Build the complete grounded context supplied to Gemini.

    Parameters
    ----------
    document_context
        Optional retrieved enterprise documents
        (used in Phase 11).

    Returns
    -------
    str
        Complete context string.
    """

    sections = []

    # ======================================================
    # Executive
    # ======================================================

    sections.append(
        _df_to_text(
            loader.executive_kpis(),
            "Executive KPIs",
        )
    )

    sections.append(
        _df_to_text(
            loader.portfolio_metrics(),
            "Portfolio Metrics",
        )
    )

    sections.append(
        _df_to_text(
            loader.portfolio_health(),
            "Portfolio Health",
        )
    )

    summary = loader.executive_summary()

    if summary:
        sections.append(
            f"\n## Executive Summary\n\n{summary}\n"
        )

    # ======================================================
    # Risk
    # ======================================================

    sections.append(
        _df_to_text(
            loader.risk_distribution(),
            "Risk Distribution",
        )
    )

    sections.append(
        _df_to_text(
            loader.risk_profitability(),
            "Risk Profitability",
        )
    )

    # ======================================================
    # Claims
    # ======================================================

    sections.append(
        _df_to_text(
            loader.claim_summary(),
            "Claims Summary",
        )
    )

    # ======================================================
    # Pricing
    # ======================================================

    sections.append(
        _json_to_text(
            loader.pricing_report(),
            "Pricing Report",
        )
    )

    sections.append(
        _json_to_text(
            loader.premium_summary(),
            "Premium Summary",
        )
    )

    # ======================================================
    # Underwriting
    # ======================================================

    sections.append(
        _json_to_text(
            loader.underwriting_summary(),
            "Underwriting Summary",
        )
    )

    # ======================================================
    # Lapse
    # ======================================================

    sections.append(
        _json_to_text(
            loader.lapse_summary(),
            "Lapse Summary",
        )
    )

    sections.append(
        _df_to_text(
            loader.retention_summary(),
            "Retention Summary",
        )
    )

    # ======================================================
    # Trends
    # ======================================================

    sections.append(
        _df_to_text(
            loader.premium_trend(),
            "Premium Trend",
        )
    )

    sections.append(
        _df_to_text(
            loader.claims_trend(),
            "Claims Trend",
        )
    )

    sections.append(
        _df_to_text(
            loader.loss_ratio_trend(),
            "Loss Ratio Trend",
        )
    )

    # ======================================================
    # Enterprise Documents (Phase 11)
    # ======================================================

    if document_context:

        sections.append(
            "\n## Company Documents\n\n"
            + document_context
            + "\n"
        )

    return "\n".join(sections)