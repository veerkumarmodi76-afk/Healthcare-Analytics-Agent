from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class DashboardDataService:
    """
    Dashboard data access layer.

    Responsible for loading all dashboard CSV outputs and exposing
    them through convenient methods for the Streamlit dashboard.
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
        """
        Load a CSV from the portfolio output directory.
        """

        file_path = self.output_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        return pd.read_csv(file_path)

    def get_csv(
        self,
        filename: str,
    ) -> pd.DataFrame:
        """
        Generic CSV loader.
        Useful for future download pages.
        """

        return self._load_csv(filename)

    # =====================================================
    # KPI DATA
    # =====================================================

    def get_executive_kpis(
        self,
    ) -> dict[str, float | str]:
        df = self._load_csv("executive_kpis.csv")

        return dict(
            zip(
                df["metric"],
                df["value"],
            )
        )

    def get_portfolio_metrics(
        self,
    ) -> dict[str, float | str]:
        df = self._load_csv("portfolio_metrics.csv")

        return dict(
            zip(
                df["metric"],
                df["value"],
            )
        )

    def get_portfolio_health(
        self,
    ) -> dict[str, float | str]:
        df = self._load_csv(
            "portfolio_health.csv"
        )

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
        return self._load_csv(
            "risk_distribution.csv"
        )

    def get_risk_profitability(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "risk_profitability.csv"
        )

    def get_risk_by_age_band(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "risk_by_age_band.csv"
        )

    def get_risk_by_policy_type(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "risk_by_policy_type.csv"
        )

    def get_risk_by_channel(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "risk_by_channel.csv"
        )

    def get_risk_premium_summary(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "risk_premium_summary.csv"
        )

    def get_risk_claims_summary(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "risk_claims_summary.csv"
        )

    # =====================================================
    # CLAIMS ANALYTICS
    # =====================================================

    def get_frequency_by_age(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "frequency_by_age.csv"
        )

    def get_severity_by_age(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "severity_by_age.csv"
        )

    def get_top_loss_segments(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "top_loss_segments.csv"
        )

    # =====================================================
    # TREND ANALYTICS
    # =====================================================

    def get_premium_trend(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "premium_trend.csv"
        )

    def get_claims_trend(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "claims_trend.csv"
        )

    def get_loss_ratio_trend(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "loss_ratio_trend.csv"
        )

    def get_lapse_trend(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "lapse_trend.csv"
        )

    def get_risk_mix_trend(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "risk_mix_trend.csv"
        )

    def get_portfolio_growth_summary(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "portfolio_growth_summary.csv"
        )

    # =====================================================
    # RETENTION ANALYTICS
    # =====================================================

    def get_retention_summary(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "retention_summary.csv"
        )

    # =====================================================
    # PRICING ANALYTICS
    # =====================================================

    def get_premium_leakage(
        self,
    ) -> pd.DataFrame:
        return self._load_csv(
            "premium_leakage.csv"
        )
    # =====================================================
    # DASHBOARD SUMMARY
    # =====================================================

    def get_dashboard_summary(
        self,
    ) -> dict[str, float | str]:
        """
        Returns a compact summary for dashboard header cards.
        """

        kpis = self.get_executive_kpis()
        portfolio = self.get_portfolio_metrics()
        health = self.get_portfolio_health()

        return {
            "total_policies": kpis.get(
                "total_policies",
                0,
            ),
            "total_insured": kpis.get(
                "total_insured",
                0,
            ),
            "total_premium": kpis.get(
                "total_premium",
                0,
            ),
            "total_claims": kpis.get(
                "total_claims",
                0,
            ),
            "loss_ratio": kpis.get(
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
            "portfolio_health_score": health.get(
                "portfolio_health_score",
                0,
            ),
            "portfolio_status": health.get(
                "portfolio_status",
                "Unknown",
            ),
        }

    # =====================================================
    # EXECUTIVE INSIGHTS
    # =====================================================

    def generate_executive_insights(
        self,
    ) -> list[str]:
        """
        Generate concise executive insights for the dashboard.
        """

        portfolio = self.get_portfolio_metrics()
        kpis = self.get_executive_kpis()
        health = self.get_portfolio_health()

        risk_profit = self.get_risk_profitability()
        retention = self.get_retention_summary()
        leakage = self.get_premium_leakage()

        insights: list[str] = []

        # Portfolio Health
        insights.append(
            f"Portfolio health score is "
            f"{health.get('portfolio_status', 'Unknown')}."
        )

        # Loss Ratio
        loss_ratio = float(
            kpis.get(
                "loss_ratio_pct",
                0,
            )
        )

        insights.append(
            f"Portfolio loss ratio is {loss_ratio:.2f}%."
        )

        # Average Risk
        avg_risk = float(
            portfolio.get(
                "avg_risk_score",
                0,
            )
        )

        insights.append(
            f"Average portfolio risk score is {avg_risk:.2f}."
        )

        # Lapse Probability
        lapse = float(
            portfolio.get(
                "avg_lapse_probability",
                0,
            )
        )

        insights.append(
            f"Average lapse probability is {lapse:.2f}%."
        )

        # Highest Claims
        if (
            not risk_profit.empty
            and "total_claims" in risk_profit.columns
        ):
            highest_claim = risk_profit.sort_values(
                "total_claims",
                ascending=False,
            ).iloc[0]

            insights.append(
                f"Highest claims originate from "
                f"{highest_claim['risk_class']} risk."
            )

        # Most Profitable Segment
        if (
            not risk_profit.empty
            and "profit" in risk_profit.columns
        ):
            best_segment = risk_profit.sort_values(
                "profit",
                ascending=False,
            ).iloc[0]

            insights.append(
                f"Highest portfolio profit comes from "
                f"{best_segment['risk_class']} risk."
            )

        # Largest Premium Exposure
        if (
            not retention.empty
            and "premium_at_risk" in retention.columns
        ):
            exposure = retention.sort_values(
                "premium_at_risk",
                ascending=False,
            ).iloc[0]

            insights.append(
                f"Highest premium exposure exists within "
                f"{exposure['retention_segment']} customers."
            )

        # Pricing Leakage
        if (
            not leakage.empty
            and "premium_leakage"in leakage.columns
        ):
            leak = leakage.sort_values(
                "premium_leakage",
                ascending=False,
            ).iloc[0]

            segment = (
                leak["risk_class"]
                if "risk_class" in leakage.columns
                else leak.iloc[0]
            )

            insights.append(
                f"Largest pricing leakage occurs in "
                f"{segment}."
            )

        return insights


# =====================================================
# FACTORY
# =====================================================

def get_dashboard_data_service(
    output_dir: str = "outputs/portfolio",
) -> DashboardDataService:
    """
    Factory function.
    """

    return DashboardDataService(
        output_dir=output_dir,
    )