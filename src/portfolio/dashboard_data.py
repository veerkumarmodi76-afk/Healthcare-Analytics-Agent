from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

import pandas as pd

logger = logging.getLogger(__name__)


class DashboardDataService:
    """
    Dashboard data access layer.
    """

    def __init__(
        self,
        output_dir: str = "outputs/portfolio",
    ) -> None:

        self.output_dir = Path(output_dir)

    # =====================================================
    # Generic Loader
    # =====================================================

    def _load_csv(
        self,
        filename: str,
    ) -> pd.DataFrame:

        file_path = self.output_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return pd.read_csv(file_path)

    # =====================================================
    # KPI DATA
    # =====================================================

    def get_executive_kpis(
        self,
    ) -> Dict[str, float]:

        df = self._load_csv("executive_kpis.csv")

        return dict(
            zip(
                df["metric"],
                df["value"],
            )
        )

    def get_portfolio_metrics(
        self,
    ) -> Dict[str, float]:

        df = self._load_csv("portfolio_metrics.csv")

        return dict(
            zip(
                df["metric"],
                df["value"],
            )
        )

    # =====================================================
    # RISK ANALYTICS
    # =====================================================

    def get_risk_distribution(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("risk_distribution.csv")

    def get_risk_profitability(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("risk_profitability.csv")

    # =====================================================
    # CLAIMS ANALYTICS
    # =====================================================

    def get_frequency_by_age(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("frequency_by_age.csv")

    def get_severity_by_age(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("severity_by_age.csv")

    def get_top_loss_segments(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("top_loss_segments.csv")

    # =====================================================
    # TREND ANALYTICS
    # =====================================================

    def get_premium_trend(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("premium_trend.csv")

    def get_claims_trend(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("claims_trend.csv")

    def get_loss_ratio_trend(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("loss_ratio_trend.csv")

    def get_lapse_trend(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("lapse_trend.csv")

    # =====================================================
    # RETENTION ANALYTICS
    # =====================================================

    def get_retention_summary(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("retention_summary.csv")

    # =====================================================
    # PRICING ANALYTICS
    # =====================================================

    def get_premium_leakage(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("premium_leakage.csv")

    # =====================================================
    # DASHBOARD SUMMARY
    # =====================================================

    def get_dashboard_summary(
        self,
    ) -> dict:

        kpis = self.get_executive_kpis()

        portfolio = self.get_portfolio_metrics()

        return {
            "total_policies": kpis.get(
                "total_policies",
                0,
            ),
            "total_insured": kpis.get(
                "total_insured",
                0,
            ),
            "total_premium": portfolio.get(
                "total_premium",
                0,
            ),
            "total_claims": portfolio.get(
                "total_claims",
                0,
            ),
            "loss_ratio": portfolio.get(
                "loss_ratio_pct",
                0,
            ),
            "avg_risk_score": portfolio.get(
                "avg_risk_score",
                0,
            ),
            "avg_lapse_probability": portfolio.get(
                "avg_lapse_probability",
                0,
            ),
        }

    # =====================================================
    # EXECUTIVE INSIGHTS
    # =====================================================

    def generate_executive_insights(
        self,
    ) -> list[str]:

        portfolio = self.get_portfolio_metrics()

        risk_df = self.get_risk_profitability()

        retention_df = self.get_retention_summary()

        insights = []

        loss_ratio = portfolio.get(
            "loss_ratio_pct",
            0,
        )

        insights.append(f"Portfolio loss ratio is {loss_ratio:.2f}%.")

        if not risk_df.empty:
            top_risk = risk_df.sort_values(
                "total_claims",
                ascending=False,
            ).iloc[0]

            insights.append(
                f"Highest claims originate from {top_risk['risk_class']} risk business."
            )

        if not retention_df.empty:
            highest_segment = retention_df.sort_values(
                "premium_at_risk",
                ascending=False,
            ).iloc[0]

            insights.append(
                f"Highest premium exposure "
                f"is within "
                f"{highest_segment['retention_segment']} "
                f"customers."
            )

        return insights


# ==========================================================
# FACTORY
# ==========================================================


def get_dashboard_data_service(
    output_dir: str = "outputs/portfolio",
) -> DashboardDataService:

    return DashboardDataService(output_dir=output_dir)

    # =====================================================
    # RISK PORTFOLIO ANALYTICS
    # =====================================================

    def get_risk_by_age_band(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("risk_by_age_band.csv")

    def get_risk_by_policy_type(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("risk_by_policy_type.csv")

    def get_risk_by_channel(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("risk_by_channel.csv")

    def get_risk_premium_summary(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("risk_premium_summary.csv")

    def get_risk_claims_summary(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("risk_claims_summary.csv")

    def get_risk_mix_trend(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("risk_mix_trend.csv")

    def get_portfolio_growth_summary(
        self,
    ) -> pd.DataFrame:

        return self._load_csv("portfolio_growth_summary.csv")


def get_risk_mix_trend(
    self,
) -> pd.DataFrame:

    return self._load_csv("risk_mix_trend.csv")


def get_portfolio_growth_summary(
    self,
) -> pd.DataFrame:

    return self._load_csv("portfolio_growth_summary.csv")
