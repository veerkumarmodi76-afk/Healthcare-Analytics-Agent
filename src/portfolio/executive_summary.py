from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class ExecutiveSummaryGenerator:
    def __init__(
        self,
        output_dir: str = "outputs/portfolio",
    ) -> None:

        self.output_dir = Path(output_dir)

    # =====================================================
    # Utilities
    # =====================================================

    def _load_csv(
        self,
        filename: str,
    ) -> pd.DataFrame:

        path = self.output_dir / filename

        if not path.exists():
            raise FileNotFoundError(f"{path} not found")

        return pd.read_csv(path)

    # =====================================================
    # Summary Builder
    # =====================================================

    def generate_summary(
        self,
    ) -> str:

        portfolio_metrics = self._load_csv("portfolio_metrics.csv")

        risk_profitability = self._load_csv("risk_profitability.csv")

        retention_summary = self._load_csv("retention_summary.csv")

        premium_leakage = self._load_csv("premium_leakage.csv")

        metrics = dict(
            zip(
                portfolio_metrics["metric"],
                portfolio_metrics["value"],
            )
        )

        total_premium = metrics.get(
            "total_premium",
            0,
        )

        total_claims = metrics.get(
            "total_claims",
            0,
        )

        total_profit = metrics.get(
            "total_profit",
            0,
        )

        loss_ratio = metrics.get(
            "loss_ratio_pct",
            0,
        )

        avg_risk_score = metrics.get(
            "avg_risk_score",
            0,
        )

        avg_lapse_probability = metrics.get(
            "avg_lapse_probability",
            0,
        )

        summary = []

        summary.append("PORTFOLIO EXECUTIVE SUMMARY")

        summary.append("=" * 40)

        summary.append("")

        summary.append(f"Total Premium: {total_premium:,.2f}")

        summary.append(f"Total Claims: {total_claims:,.2f}")

        summary.append(f"Total Profit: {total_profit:,.2f}")

        summary.append(f"Portfolio Loss Ratio: {loss_ratio:.2f}%")

        summary.append(f"Average Risk Score: {avg_risk_score:.2f}")

        summary.append(f"Average Lapse Probability: {avg_lapse_probability:.2f}%")

        summary.append("")
        summary.append("RISK PORTFOLIO ANALYSIS")
        summary.append("-" * 30)

        if not risk_profitability.empty:
            highest_claim_segment = risk_profitability.sort_values(
                "total_claims",
                ascending=False,
            ).iloc[0]

            summary.append(
                f"Highest claim burden "
                f"originates from "
                f"{highest_claim_segment['risk_class']} "
                f"risk business."
            )

            summary.append(
                f"Associated claims cost: {highest_claim_segment['total_claims']:,.2f}"
            )

        summary.append("")
        summary.append("PRICING ANALYSIS")
        summary.append("-" * 30)

        if not premium_leakage.empty:
            highest_leakage = premium_leakage.sort_values(
                "premium_leakage",
                ascending=False,
            ).iloc[0]

            summary.append(
                f"Largest pricing gap "
                f"observed in "
                f"{highest_leakage['risk_class']} "
                f"risk segment."
            )

            summary.append(
                f"Premium leakage: {highest_leakage['premium_leakage']:,.2f}"
            )

        summary.append("")
        summary.append("RETENTION ANALYSIS")
        summary.append("-" * 30)

        if not retention_summary.empty:
            highest_risk = retention_summary.sort_values(
                "premium_at_risk",
                ascending=False,
            ).iloc[0]

            summary.append(
                f"Highest premium exposure "
                f"exists within "
                f"{highest_risk['retention_segment']} "
                f"customers."
            )

            summary.append(f"Premium exposure: {highest_risk['premium_at_risk']:,.2f}")

        summary.append("")
        summary.append("RECOMMENDATIONS")
        summary.append("-" * 30)

        if loss_ratio > 80:
            summary.append("- Review underwriting guidelines for high-risk segments.")

        if avg_lapse_probability > 20:
            summary.append("- Expand retention campaigns for at-risk policyholders.")

        summary.append("- Monitor premium leakage across risk classes.")

        summary.append("- Review pricing adequacy quarterly.")

        return "\n".join(summary)

    # =====================================================
    # Save
    # =====================================================

    def save_summary(
        self,
        filename: str = "executive_summary.txt",
    ) -> str:

        summary = self.generate_summary()

        path = self.output_dir / filename

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(summary)

        logger.info(f"Executive summary saved: {path}")

        return str(path)


def generate_executive_summary(
    output_dir: str = "outputs/portfolio",
) -> str:

    generator = ExecutiveSummaryGenerator(output_dir=output_dir)

    return generator.save_summary()
