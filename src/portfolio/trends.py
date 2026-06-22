from __future__ import annotations

import logging
from dataclasses import dataclass

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "period",
    "premium",
    "cost_claims_year",
    "loss_ratio",
    "lapse_binary",
    "risk_class",
]


@dataclass(slots=True)
class TrendsAnalyticsResult:
    """
    Container for trend analytics outputs.
    """

    premium_trend: pd.DataFrame
    claims_trend: pd.DataFrame
    loss_ratio_trend: pd.DataFrame
    lapse_trend: pd.DataFrame
    risk_mix_trend: pd.DataFrame
    portfolio_growth_summary: pd.DataFrame


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
) -> None:
    """
    Validate required columns.
    """

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def get_premium_trend(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Premium trend by year.
    """

    result = (
        df
        .groupby("period", dropna=False)
        .agg(
            total_premium=("premium", "sum"),
            policy_count=("period", "count"),
        )
        .reset_index()
        .sort_values("period")
    )

    result["premium_growth_pct"] = (
        result["total_premium"].pct_change().mul(100).round(2)
    )

    result["total_premium"] = result["total_premium"].round(2)

    return result


def get_claims_trend(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Claims trend by year.
    """

    result = (
        df
        .groupby("period", dropna=False)
        .agg(
            total_claims=(
                "cost_claims_year",
                "sum",
            )
        )
        .reset_index()
        .sort_values("period")
    )

    result["claims_growth_pct"] = result["total_claims"].pct_change().mul(100).round(2)

    result["total_claims"] = result["total_claims"].round(2)

    return result


def get_loss_ratio_trend(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Loss ratio trend by year.
    """

    result = (
        df
        .groupby("period", dropna=False)
        .agg(
            avg_loss_ratio=(
                "loss_ratio",
                "mean",
            )
        )
        .reset_index()
        .sort_values("period")
    )

    result["avg_loss_ratio_pct"] = (result["avg_loss_ratio"] * 100).round(2)

    result.drop(
        columns=["avg_loss_ratio"],
        inplace=True,
    )

    return result


def get_lapse_trend(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Lapse rate trend by year.
    """

    result = (
        df
        .groupby("period", dropna=False)
        .agg(
            lapse_rate=(
                "lapse_binary",
                "mean",
            ),
            total_policies=(
                "period",
                "count",
            ),
        )
        .reset_index()
        .sort_values("period")
    )

    result["lapse_rate_pct"] = (result["lapse_rate"] * 100).round(2)

    result.drop(
        columns=["lapse_rate"],
        inplace=True,
    )

    return result


def get_risk_mix_trend(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Risk class mix by year.
    Useful for stacked area charts.
    """

    result = (
        df
        .groupby(
            ["period", "risk_class"],
            dropna=False,
        )
        .size()
        .reset_index(name="policy_count")
    )

    totals = (
        result.groupby("period")["policy_count"].sum().rename("total").reset_index()
    )

    result = result.merge(
        totals,
        on="period",
        how="left",
    )

    result["percentage"] = (result["policy_count"] / result["total"] * 100).round(2)

    result.drop(
        columns=["total"],
        inplace=True,
    )

    return result.sort_values(["period", "risk_class"])


def get_portfolio_growth_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Executive trend summary.
    """

    yearly = (
        df
        .groupby("period")
        .agg(
            premium=("premium", "sum"),
            claims=("cost_claims_year", "sum"),
        )
        .sort_index()
    )

    first_year = yearly.iloc[0]
    last_year = yearly.iloc[-1]

    premium_growth = (
        (last_year["premium"] - first_year["premium"]) / first_year["premium"] * 100
    )

    claims_growth = (
        (last_year["claims"] - first_year["claims"]) / first_year["claims"] * 100
    )

    return pd.DataFrame({
        "metric": [
            "premium_growth_pct",
            "claims_growth_pct",
        ],
        "value": [
            round(premium_growth, 2),
            round(claims_growth, 2),
        ],
    })


def generate_trend_analytics(
    df: pd.DataFrame,
) -> TrendsAnalyticsResult:
    """
    Generate all portfolio trend analytics.

    Parameters
    ----------
    df : pd.DataFrame
        Master portfolio dataframe.

    Returns
    -------
    TrendsAnalyticsResult
    """

    logger.info("Starting trend analytics generation...")

    validate_columns(
        df,
        REQUIRED_COLUMNS,
    )

    result = TrendsAnalyticsResult(
        premium_trend=get_premium_trend(df),
        claims_trend=get_claims_trend(df),
        loss_ratio_trend=get_loss_ratio_trend(df),
        lapse_trend=get_lapse_trend(df),
        risk_mix_trend=get_risk_mix_trend(df),
        portfolio_growth_summary=get_portfolio_growth_summary(df),
    )

    logger.info("Trend analytics completed successfully.")

    return result
