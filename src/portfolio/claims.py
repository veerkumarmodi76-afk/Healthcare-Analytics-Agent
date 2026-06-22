from __future__ import annotations

import logging
from dataclasses import dataclass

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "age_band",
    "risk_class",
    "type_policy",
    "premium",
    "cost_claims_year",
    "claim_frequency",
    "claim_severity",
    "loss_ratio",
]


@dataclass(slots=True)
class ClaimsAnalyticsResult:
    """
    Container for claims analytics outputs.
    """

    portfolio_claims_summary: pd.DataFrame
    frequency_by_age: pd.DataFrame
    severity_by_age: pd.DataFrame
    loss_ratio_by_risk: pd.DataFrame
    loss_ratio_by_policy: pd.DataFrame
    top_loss_segments: pd.DataFrame


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
) -> None:
    """
    Validate dataframe columns.
    """

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def get_portfolio_claims_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Portfolio-level claims KPIs.
    """

    total_premium = df["premium"].sum()
    total_claims = df["cost_claims_year"].sum()

    portfolio_loss_ratio = total_claims / total_premium if total_premium > 0 else 0

    result = pd.DataFrame({
        "metric": [
            "total_premium",
            "total_claims",
            "avg_claim_frequency",
            "avg_claim_severity",
            "portfolio_loss_ratio",
        ],
        "value": [
            round(total_premium, 2),
            round(total_claims, 2),
            round(
                df["claim_frequency"].mean(),
                4,
            ),
            round(
                df["claim_severity"].mean(),
                2,
            ),
            round(
                portfolio_loss_ratio * 100,
                2,
            ),
        ],
    })

    return result


def get_frequency_by_age(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Claim frequency by age band.
    """

    result = (
        df
        .groupby("age_band", dropna=False)
        .agg(
            avg_frequency=(
                "claim_frequency",
                "mean",
            ),
            policy_count=(
                "age_band",
                "count",
            ),
        )
        .reset_index()
    )

    result["avg_frequency"] = result["avg_frequency"].round(4)

    return result.sort_values(
        "avg_frequency",
        ascending=False,
    )


def get_severity_by_age(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Claim severity by age band.
    """

    result = (
        df
        .groupby("age_band", dropna=False)
        .agg(
            avg_severity=(
                "claim_severity",
                "mean",
            ),
            total_claims=(
                "cost_claims_year",
                "sum",
            ),
        )
        .reset_index()
    )

    result["avg_severity"] = result["avg_severity"].round(2)

    result["total_claims"] = result["total_claims"].round(2)

    return result.sort_values(
        "avg_severity",
        ascending=False,
    )


def get_loss_ratio_by_risk(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Loss ratio by risk class.
    """

    result = (
        df
        .groupby("risk_class", dropna=False)
        .agg(
            total_premium=(
                "premium",
                "sum",
            ),
            total_claims=(
                "cost_claims_year",
                "sum",
            ),
            avg_loss_ratio=(
                "loss_ratio",
                "mean",
            ),
        )
        .reset_index()
    )

    result["avg_loss_ratio_pct"] = (result["avg_loss_ratio"] * 100).round(2)

    result.drop(
        columns=["avg_loss_ratio"],
        inplace=True,
    )

    result[
        [
            "total_premium",
            "total_claims",
        ]
    ] = result[
        [
            "total_premium",
            "total_claims",
        ]
    ].round(2)

    return result.sort_values(
        "avg_loss_ratio_pct",
        ascending=False,
    )


def get_loss_ratio_by_policy(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Loss ratio by policy type.
    """

    result = (
        df
        .groupby("type_policy", dropna=False)
        .agg(
            total_premium=(
                "premium",
                "sum",
            ),
            total_claims=(
                "cost_claims_year",
                "sum",
            ),
            avg_loss_ratio=(
                "loss_ratio",
                "mean",
            ),
        )
        .reset_index()
    )

    result["avg_loss_ratio_pct"] = (result["avg_loss_ratio"] * 100).round(2)

    result.drop(
        columns=["avg_loss_ratio"],
        inplace=True,
    )

    return result.sort_values(
        "avg_loss_ratio_pct",
        ascending=False,
    )


def get_top_loss_segments(
    df: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Highest loss-making portfolio segments.

    Segment Definition:
        age_band × risk_class
    """

    result = (
        df
        .groupby(
            ["age_band", "risk_class"],
            dropna=False,
        )
        .agg(
            policy_count=(
                "risk_class",
                "count",
            ),
            total_premium=(
                "premium",
                "sum",
            ),
            total_claims=(
                "cost_claims_year",
                "sum",
            ),
        )
        .reset_index()
    )

    result["loss_ratio_pct"] = (
        result["total_claims"] / result["total_premium"] * 100
    ).round(2)

    result["profit"] = (result["total_premium"] - result["total_claims"]).round(2)

    return (
        result
        .sort_values(
            "loss_ratio_pct",
            ascending=False,
        )
        .head(top_n)
        .reset_index(drop=True)
    )


def generate_claims_analytics(
    df: pd.DataFrame,
) -> ClaimsAnalyticsResult:
    """
    Generate complete claims analytics.

    Parameters
    ----------
    df : pd.DataFrame
        Master portfolio dataframe.

    Returns
    -------
    ClaimsAnalyticsResult
    """

    logger.info("Starting claims analytics generation...")

    validate_columns(
        df,
        REQUIRED_COLUMNS,
    )

    result = ClaimsAnalyticsResult(
        portfolio_claims_summary=get_portfolio_claims_summary(df),
        frequency_by_age=get_frequency_by_age(df),
        severity_by_age=get_severity_by_age(df),
        loss_ratio_by_risk=get_loss_ratio_by_risk(df),
        loss_ratio_by_policy=get_loss_ratio_by_policy(df),
        top_loss_segments=get_top_loss_segments(df),
    )

    logger.info("Claims analytics completed successfully.")

    return result
