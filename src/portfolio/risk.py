from __future__ import annotations

import logging
from dataclasses import dataclass

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "risk_class",
    "age_band",
    "type_policy",
    "distribution_channel",
    "premium",
    "recommended_premium",
    "cost_claims_year",
    "loss_ratio",
]


@dataclass(slots=True)
class RiskAnalyticsResult:
    """
    Container for all risk analytics outputs.
    """

    risk_distribution: pd.DataFrame
    risk_by_age_band: pd.DataFrame
    risk_by_policy_type: pd.DataFrame
    risk_by_channel: pd.DataFrame
    risk_premium_summary: pd.DataFrame
    risk_claims_summary: pd.DataFrame
    risk_profitability_summary: pd.DataFrame


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
) -> None:
    """
    Validate required dataframe columns.
    """

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def get_risk_distribution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Portfolio distribution by risk class.
    """

    result = (
        df.groupby("risk_class", dropna=False).size().reset_index(name="policy_count")
    )

    total = result["policy_count"].sum()

    result["percentage"] = (result["policy_count"] / total * 100).round(2)

    return result.sort_values(
        "policy_count",
        ascending=False,
    )


def get_risk_by_age_band(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Risk class distribution across age bands.
    """

    return (
        df
        .groupby(
            ["age_band", "risk_class"],
            dropna=False,
        )
        .size()
        .reset_index(name="policy_count")
        .sort_values(
            ["age_band", "policy_count"],
            ascending=[True, False],
        )
    )


def get_risk_by_policy_type(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Risk class distribution across policy types.
    """

    return (
        df
        .groupby(
            ["type_policy", "risk_class"],
            dropna=False,
        )
        .size()
        .reset_index(name="policy_count")
        .sort_values(
            ["type_policy", "policy_count"],
            ascending=[True, False],
        )
    )


def get_risk_by_channel(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Risk class distribution across channels.
    """

    return (
        df
        .groupby(
            ["distribution_channel", "risk_class"],
            dropna=False,
        )
        .size()
        .reset_index(name="policy_count")
        .sort_values(
            ["distribution_channel", "policy_count"],
            ascending=[True, False],
        )
    )


def get_risk_premium_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Premium metrics by risk class.
    """

    result = (
        df
        .groupby("risk_class", dropna=False)
        .agg(
            policy_count=("risk_class", "count"),
            total_premium=("premium", "sum"),
            average_premium=("premium", "mean"),
            total_recommended_premium=(
                "recommended_premium",
                "sum",
            ),
            average_recommended_premium=(
                "recommended_premium",
                "mean",
            ),
        )
        .reset_index()
    )

    numeric_cols = [
        "total_premium",
        "average_premium",
        "total_recommended_premium",
        "average_recommended_premium",
    ]

    result[numeric_cols] = result[numeric_cols].round(2)

    return result.sort_values(
        "total_premium",
        ascending=False,
    )


def get_risk_claims_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Claims metrics by risk class.
    """

    result = (
        df
        .groupby("risk_class", dropna=False)
        .agg(
            policy_count=("risk_class", "count"),
            total_claims=("cost_claims_year", "sum"),
            average_claims=("cost_claims_year", "mean"),
        )
        .reset_index()
    )

    result[
        [
            "total_claims",
            "average_claims",
        ]
    ] = result[
        [
            "total_claims",
            "average_claims",
        ]
    ].round(2)

    return result.sort_values(
        "total_claims",
        ascending=False,
    )


def get_risk_profitability_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Profitability analysis by risk class.
    """

    result = (
        df
        .groupby("risk_class", dropna=False)
        .agg(
            policy_count=("risk_class", "count"),
            total_premium=("premium", "sum"),
            total_recommended_premium=(
                "recommended_premium",
                "sum",
            ),
            total_claims=("cost_claims_year", "sum"),
            avg_loss_ratio=("loss_ratio", "mean"),
        )
        .reset_index()
    )

    result["profit"] = result["total_premium"] - result["total_claims"]

    result["pricing_gap"] = (
        result["total_recommended_premium"] - result["total_premium"]
    )

    result["profit_margin_pct"] = (
        result["profit"] / result["total_premium"] * 100
    ).round(2)

    result["avg_loss_ratio_pct"] = (result["avg_loss_ratio"] * 100).round(2)

    result.drop(
        columns=["avg_loss_ratio"],
        inplace=True,
    )

    numeric_cols = [
        "total_premium",
        "total_recommended_premium",
        "total_claims",
        "profit",
        "pricing_gap",
    ]

    result[numeric_cols] = result[numeric_cols].round(2)

    return result.sort_values(
        "profit",
        ascending=False,
    )


def generate_risk_analytics(
    df: pd.DataFrame,
) -> RiskAnalyticsResult:
    """
    Generate complete portfolio risk analytics.

    Parameters
    ----------
    df : pd.DataFrame
        Master portfolio dataframe.

    Returns
    -------
    RiskAnalyticsResult
    """

    logger.info("Starting risk analytics generation...")

    validate_columns(
        df,
        REQUIRED_COLUMNS,
    )

    result = RiskAnalyticsResult(
        risk_distribution=get_risk_distribution(df),
        risk_by_age_band=get_risk_by_age_band(df),
        risk_by_policy_type=get_risk_by_policy_type(df),
        risk_by_channel=get_risk_by_channel(df),
        risk_premium_summary=get_risk_premium_summary(df),
        risk_claims_summary=get_risk_claims_summary(df),
        risk_profitability_summary=get_risk_profitability_summary(df),
    )

    logger.info("Risk analytics completed successfully.")

    return result
