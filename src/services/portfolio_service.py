from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd

from .base_Service import BaseService
from .underwriting_service import PROJECT_ROOT

from ..portfolio.metrics import (
    build_master_dataframe,
    generate_portfolio_analytics,
    save_portfolio_outputs,
)

from ..portfolio.executive_summary import (
    generate_executive_summary,
)

logger = logging.getLogger(__name__)


class PortfolioService(BaseService):
    """
    Executes the complete Portfolio Analytics pipeline.
    """

    def __init__(self) -> None:
        super().__init__("Portfolio Analytics")
        self.base_dir = Path(__file__).resolve().parents[2]

    # ======================================================
    # Data Loading
    # ======================================================

    def load_inputs(
        self,
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
    ]:

        logger.info("Loading processed dataset...")

        processed_df = pd.read_csv(
            PROJECT_ROOT
            / "data"
            / "processed"
            / "processed_data.csv"
        )

        logger.info("Loading underwriting predictions...")

        underwriting_df = pd.read_csv(
            self.base_dir
            / "outputs"
            / "underwriting"
            / "underwriting_predictions.csv"
        )

        logger.info("Loading pricing outputs...")

        pricing_df = pd.read_csv(
            self.base_dir
            / "outputs"
            / "pricing"
            / "premium_quotes.csv"
        )

        logger.info("Loading lapse outputs...")

        lapse_predictions = pd.read_csv(
            self.base_dir
            / "outputs"
            / "lapse"
            / "lapse_predictions.csv"
        )

        lapse_retention = pd.read_csv(
            self.base_dir
            / "outputs"
            / "lapse"
            / "lapse_retention_actions.csv"
        )

        # ==================================================
        # Standardize underwriting identifier
        # ==================================================

        if "applicant_id" in underwriting_df.columns:
            underwriting_df = underwriting_df.rename(
                columns={
                    "applicant_id": "row_id"
                }
            )

        # ==================================================
        # Merge lapse outputs
        # ==================================================

        lapse_df = lapse_predictions.merge(
            lapse_retention[
                [
                    "row_id",
                    "recommended_action",
                    "priority",
                    "estimated_revenue_loss",
                    "retention_cost",
                    "expected_roi",
                ]
            ],
            on="row_id",
            how="left",
        )

        # ==================================================
        # Rename columns expected by Portfolio Analytics
        # ==================================================

        lapse_df.rename(
            columns={
                "risk_segment": "retention_segment",
            },
            inplace=True,
        )

        return (
            processed_df,
            underwriting_df,
            pricing_df,
            lapse_df,
        )

    # ======================================================
    # Pipeline
    # ======================================================

    def run_pipeline(self) -> None:

        start = time.perf_counter()

        logger.info("=" * 70)
        logger.info("PORTFOLIO ANALYTICS PIPELINE")
        logger.info("=" * 70)

        (
            processed_df,
            underwriting_df,
            pricing_df,
            lapse_df,
        ) = self.load_inputs()

        logger.info("Building master dataframe...")

        master_df = build_master_dataframe(
            processed_df,
            underwriting_df,
            pricing_df,
            lapse_df,
        )

        logger.info("Generating portfolio analytics...")

        results = generate_portfolio_analytics(
            master_df
        )

        logger.info("Saving portfolio outputs...")

        save_portfolio_outputs(results)

        logger.info("Generating executive summary...")

        generate_executive_summary()

        elapsed = time.perf_counter() - start

        logger.info("=" * 70)
        logger.info(
            "Portfolio Analytics completed successfully in %.2f seconds.",
            elapsed,
        )
        logger.info("=" * 70)

    # ======================================================
    # Public API
    # ======================================================

    def execute(self) -> bool:

        try:
            self.run_pipeline()
            return True

        except Exception:

            logger.exception(
                "Portfolio Analytics pipeline failed."
            )

            return False

    # ======================================================
    # Alias
    # ======================================================

    def run(self):
        """
        Alias for the master pipeline.
        """
        return self.run_pipeline()