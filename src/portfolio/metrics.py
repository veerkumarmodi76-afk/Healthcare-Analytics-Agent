from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .risk import RiskAnalyticsResult, generate_risk_analytics
from .claims import ClaimsAnalyticsResult, generate_claims_analytics
from .trends import TrendsAnalyticsResult, generate_trend_analytics

logger = logging.getLogger(__name__)


MASTER_REQUIRED_COLUMNS = [
    "ID_policy",
    "ID_insured",
    "period",
    "premium",
    "cost_claims_year",
    "claim_frequency",
    "claim_severity",
    "loss_ratio",
    "lapse_binary",
]


@dataclass(slots=True)
class PortfolioAnalyticsResult:
    risk: RiskAnalyticsResult
    claims: ClaimsAnalyticsResult
    trends: TrendsAnalyticsResult
    executive_kpis: pd.DataFrame
    portfolio_metrics: pd.DataFrame
    premium_leakage: pd.DataFrame
    retention_summary: pd.DataFrame


def validate_master_dataframe(df: pd.DataFrame) -> None:
    missing = [c for c in MASTER_REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing master columns: {missing}")


def build_master_dataframe(
    processed_df: pd.DataFrame,
    underwriting_df: pd.DataFrame,
    pricing_df: pd.DataFrame,
    lapse_df: pd.DataFrame,
) -> pd.DataFrame:

    processed_df = processed_df.copy()
    processed_df["row_id"] = processed_df.index
    processed_df = processed_df.drop(
        columns=[
            "risk_class",
            "risk_score",
        ],
        errors="ignore",
    )

    master_df = (
        processed_df
        .merge(
            underwriting_df[
                ["row_id", "risk_score", "risk_class_label", "underwriting_flag"]
            ],
            on="row_id",
            how="left",
        )
        .merge(
            pricing_df[["row_id", "predicted_claim_cost", "recommended_premium"]],
            on="row_id",
            how="left",
        )
        .merge(
            lapse_df[
                [
                    "row_id",
                    "lapse_probability",
                    "retention_segment",
                    "recommended_action",
                ]
            ],
            on="row_id",
            how="left",
        )
    )

    master_df.rename(
        columns={"risk_class_label": "risk_class"},
        inplace=True,
    )

    return master_df


def generate_executive_kpis(df: pd.DataFrame) -> pd.DataFrame:

    total_premium = df["premium"].sum()
    total_claims = df["cost_claims_year"].sum()

    return pd.DataFrame({
        "metric": [
            "total_policies",
            "total_insured",
            "total_premium",
            "total_claims",
            "avg_claim_frequency",
            "avg_claim_severity",
            "portfolio_loss_ratio_pct",
            "lapse_rate_pct",
        ],
        "value": [
            df["ID_policy"].nunique(),
            df["ID_insured"].nunique(),
            round(total_premium, 2),
            round(total_claims, 2),
            round(df["claim_frequency"].mean(), 4),
            round(df["claim_severity"].mean(), 2),
            round((total_claims / total_premium) * 100, 2),
            round(df["lapse_binary"].mean() * 100, 2),
        ],
    })


def generate_portfolio_metrics(df: pd.DataFrame) -> pd.DataFrame:

    total_premium = df["premium"].sum()
    total_claims = df["cost_claims_year"].sum()

    return pd.DataFrame({
        "metric": [
            "total_premium",
            "total_claims",
            "total_profit",
            "loss_ratio_pct",
            "avg_risk_score",
            "avg_lapse_probability",
        ],
        "value": [
            round(total_premium, 2),
            round(total_claims, 2),
            round(total_premium - total_claims, 2),
            round((total_claims / total_premium) * 100, 2),
            round(df["risk_score"].mean(), 2),
            round(df["lapse_probability"].mean() * 100, 2),
        ],
    })


def generate_premium_leakage(df: pd.DataFrame) -> pd.DataFrame:

    result = (
        df
        .groupby("risk_class", dropna=False)
        .agg(
            actual_premium=("premium", "sum"),
            recommended_premium=("recommended_premium", "sum"),
        )
        .reset_index()
    )

    result["premium_leakage"] = result["recommended_premium"] - result["actual_premium"]

    return result.sort_values(
        "premium_leakage",
        ascending=False,
    )


def generate_retention_summary(df: pd.DataFrame) -> pd.DataFrame:

    return (
        df
        .groupby("retention_segment", dropna=False)
        .agg(
            customers=("retention_segment", "count"),
            premium_at_risk=("premium", "sum"),
        )
        .reset_index()
    )


def generate_portfolio_analytics(
    master_df: pd.DataFrame,
) -> PortfolioAnalyticsResult:

    validate_master_dataframe(master_df)

    risk_results = generate_risk_analytics(master_df)
    claims_results = generate_claims_analytics(master_df)
    trends_results = generate_trend_analytics(master_df)

    return PortfolioAnalyticsResult(
        risk=risk_results,
        claims=claims_results,
        trends=trends_results,
        executive_kpis=generate_executive_kpis(master_df),
        portfolio_metrics=generate_portfolio_metrics(master_df),
        premium_leakage=generate_premium_leakage(master_df),
        retention_summary=generate_retention_summary(master_df),
    )


def save_portfolio_outputs(
    results: PortfolioAnalyticsResult,
    output_dir: str = "outputs/portfolio",
) -> None:

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # KPI Outputs
    results.executive_kpis.to_csv(output_path / "executive_kpis.csv", index=False)

    results.portfolio_metrics.to_csv(output_path / "portfolio_metrics.csv", index=False)

    results.premium_leakage.to_csv(output_path / "premium_leakage.csv", index=False)

    results.retention_summary.to_csv(output_path / "retention_summary.csv", index=False)

    # Risk Analytics
    results.risk.risk_distribution.to_csv(
        output_path / "risk_distribution.csv", index=False
    )

    results.risk.risk_by_age_band.to_csv(
        output_path / "risk_by_age_band.csv", index=False
    )

    results.risk.risk_by_policy_type.to_csv(
        output_path / "risk_by_policy_type.csv", index=False
    )

    results.risk.risk_by_channel.to_csv(
        output_path / "risk_by_channel.csv", index=False
    )

    results.risk.risk_premium_summary.to_csv(
        output_path / "risk_premium_summary.csv", index=False
    )

    results.risk.risk_claims_summary.to_csv(
        output_path / "risk_claims_summary.csv", index=False
    )

    results.risk.risk_profitability_summary.to_csv(
        output_path / "risk_profitability.csv", index=False
    )

    # Claims Analytics
    results.claims.frequency_by_age.to_csv(
        output_path / "frequency_by_age.csv", index=False
    )

    results.claims.severity_by_age.to_csv(
        output_path / "severity_by_age.csv", index=False
    )

    results.claims.top_loss_segments.to_csv(
        output_path / "top_loss_segments.csv", index=False
    )

    # Trend Analytics
    results.trends.premium_trend.to_csv(output_path / "premium_trend.csv", index=False)

    results.trends.claims_trend.to_csv(output_path / "claims_trend.csv", index=False)

    results.trends.loss_ratio_trend.to_csv(
        output_path / "loss_ratio_trend.csv", index=False
    )

    results.trends.lapse_trend.to_csv(output_path / "lapse_trend.csv", index=False)

    results.trends.risk_mix_trend.to_csv(
        output_path / "risk_mix_trend.csv", index=False
    )

    results.trends.portfolio_growth_summary.to_csv(
        output_path / "portfolio_growth_summary.csv", index=False
    )
