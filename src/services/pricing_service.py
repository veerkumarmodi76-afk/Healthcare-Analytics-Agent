"""
pricing_service.py
==================

Service layer for the Pricing Department.

This service acts as the ONLY interface between:

Dashboard
↓

Pricing Department

↓

Outputs

Responsibilities
----------------
✓ Train pricing model
✓ Predict expected claim cost
✓ Generate premium quotes
✓ Generate pricing report
✓ Execute complete pricing pipeline

Author :
Version : 2.0.0
"""

import json
import logging
import os
from typing import Any

import pandas as pd

# =============================================================================
# IMPORT PRICING MODULES
# =============================================================================

from ..pricing.train import train_model
from ..pricing.predict import main as predict_claim_cost
from ..pricing.premium import main as generate_premium_quotes
from ..pricing.report import main as generate_pricing_report

# =============================================================================
# CONFIGURATION
# =============================================================================

MODEL_DIR = "models/pricing"

OUTPUT_DIR = "outputs/pricing"

LOG_DIR = "outputs/logs"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "pricing_model.pkl",
)

LOG_FILE = os.path.join(
    LOG_DIR,
    "pricing_service.log",
)

METRICS_PATH = os.path.join(
    OUTPUT_DIR,
    "metrics.json",
)

PREDICTION_SUMMARY_PATH = os.path.join(
    OUTPUT_DIR,
    "prediction_summary.json",
)

PREMIUM_SUMMARY_PATH = os.path.join(
    OUTPUT_DIR,
    "premium_summary.json",
)

FEATURE_IMPORTANCE_PATH = os.path.join(
    OUTPUT_DIR,
    "feature_importance.csv",
)

REPORT_PATH = os.path.join(
    OUTPUT_DIR,
    "pricing_report.md",
)

# =============================================================================
# LOGGER
# =============================================================================

os.makedirs(
    LOG_DIR,
    exist_ok=True,
)

logger = logging.getLogger(
    "pricing_service",
)

logger.setLevel(
    logging.INFO,
)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    handler = logging.FileHandler(LOG_FILE)

    handler.setFormatter(formatter)

    logger.addHandler(handler)

# =============================================================================
# SERVICE
# =============================================================================


class PricingService:
    """
    Service interface for Pricing Department.
    """

    # -------------------------------------------------------------------------
    # TRAIN
    # -------------------------------------------------------------------------

    def train(self) -> bool:
        """
        Train pricing model.
        """

        logger.info("=" * 70)
        logger.info("TRAINING PRICING MODEL")

        try:
            train_model()

            logger.info("Pricing model training completed.")

            return True

        except Exception:
            logger.exception("Pricing model training failed.")

            raise

    # -------------------------------------------------------------------------
    # PREDICT
    # -------------------------------------------------------------------------

    def predict(self):
        """
        Generate claim cost predictions.
        """

        logger.info("=" * 70)
        logger.info("GENERATING CLAIM PREDICTIONS")

        try:
            output = predict_claim_cost()

            logger.info("Prediction completed successfully.")

            return output

        except Exception:
            logger.exception("Prediction failed.")

            raise

    # -------------------------------------------------------------------------
    # PREMIUM
    # -------------------------------------------------------------------------

    def generate_quotes(self):
        """
        Generate premium quotes.
        """

        logger.info("=" * 70)
        logger.info("GENERATING PREMIUM QUOTES")

        try:
            output = generate_premium_quotes()

            logger.info("Premium generation completed.")

            return output

        except Exception:
            logger.exception("Premium generation failed.")

            raise

    # -------------------------------------------------------------------------
    # REPORT
    # -------------------------------------------------------------------------

    def generate_report(self):
        """
        Generate pricing report.
        """

        logger.info("=" * 70)
        logger.info("GENERATING PRICING REPORT")

        try:
            generate_pricing_report()

            logger.info("Pricing report generated.")

            return True

        except Exception:
            logger.exception("Pricing report failed.")

            raise

    # -------------------------------------------------------------------------
    # COMPLETE PIPELINE
    # -------------------------------------------------------------------------

    def run_pipeline(self):
        """
        Execute the complete pricing pipeline.

        Train
            ↓
        Predict
            ↓
        Premium
            ↓
        Report
        """

        logger.info("=" * 70)
        logger.info("STARTING COMPLETE PRICING PIPELINE")

        self.train()

        self.predict()

        self.generate_quotes()

        self.generate_report()

        logger.info("Pricing pipeline completed successfully.")

        return True

    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------

    @staticmethod
    def _load_json(path: str) -> dict[str, Any]:

        if not os.path.exists(path):
            raise FileNotFoundError(path)

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    @staticmethod
    def _load_csv(path: str) -> pd.DataFrame:

        if not os.path.exists(path):
            raise FileNotFoundError(path)

        return pd.read_csv(path)

    # -------------------------------------------------------------------------
    # METRICS
    # -------------------------------------------------------------------------

    def get_metrics(self) -> dict[str, Any]:
        """
        Load training metrics.
        """

        logger.info("Loading pricing metrics.")

        return self._load_json(
            METRICS_PATH,
        )

    # -------------------------------------------------------------------------
    # PREDICTION SUMMARY
    # -------------------------------------------------------------------------

    def get_prediction_summary(self) -> dict[str, Any]:
        """
        Load prediction summary.
        """

        logger.info("Loading prediction summary.")

        return self._load_json(
            PREDICTION_SUMMARY_PATH,
        )

    # -------------------------------------------------------------------------
    # PREMIUM SUMMARY
    # -------------------------------------------------------------------------

    def get_premium_summary(self) -> dict[str, Any]:
        """
        Load premium summary.
        """

        logger.info("Loading premium summary.")

        return self._load_json(
            PREMIUM_SUMMARY_PATH,
        )

    # -------------------------------------------------------------------------
    # FEATURE IMPORTANCE
    # -------------------------------------------------------------------------

    def get_feature_importance(
        self,
    ) -> pd.DataFrame:
        """
        Load feature importance.
        """

        logger.info("Loading feature importance.")

        return self._load_csv(
            FEATURE_IMPORTANCE_PATH,
        )

    # -------------------------------------------------------------------------
    # REPORT
    # -------------------------------------------------------------------------

    def get_report(self) -> str:
        """
        Load markdown report.
        """

        logger.info("Loading pricing report.")

        if not os.path.exists(
            REPORT_PATH,
        ):
            raise FileNotFoundError(REPORT_PATH)

        with open(
            REPORT_PATH,
            "r",
            encoding="utf-8",
        ) as f:
            return f.read()

    # -------------------------------------------------------------------------
    # OUTPUT FILES
    # -------------------------------------------------------------------------

    def list_outputs(self) -> list[str]:
        """
        Return every generated pricing output.
        """

        logger.info("Listing pricing outputs.")

        if not os.path.exists(
            OUTPUT_DIR,
        ):
            return []

        files = []

        for file in sorted(
            os.listdir(
                OUTPUT_DIR,
            )
        ):
            files.append(file)

        return files

    # -------------------------------------------------------------------------
    # HEALTH CHECK
    # -------------------------------------------------------------------------

    def health_check(self) -> dict[str, Any]:
        """
        Verify pricing engine health.
        """

        logger.info("Running pricing health check.")

        status = {
            "model_exists": os.path.exists(
                MODEL_PATH,
            ),
            "metrics_exists": os.path.exists(
                METRICS_PATH,
            ),
            "prediction_summary_exists": os.path.exists(
                PREDICTION_SUMMARY_PATH,
            ),
            "premium_summary_exists": os.path.exists(
                PREMIUM_SUMMARY_PATH,
            ),
            "feature_importance_exists": os.path.exists(
                FEATURE_IMPORTANCE_PATH,
            ),
            "report_exists": os.path.exists(
                REPORT_PATH,
            ),
        }

        status["healthy"] = all(status.values())

        logger.info(
            "Health Check: %s",
            status,
        )

        return status

    # -------------------------------------------------------------------------
    # DASHBOARD SUMMARY
    # -------------------------------------------------------------------------

    def dashboard_data(self) -> dict[str, Any]:
        """
        Returns all dashboard data in a
        single dictionary.
        """

        logger.info("Preparing dashboard data.")

        return {
            "metrics": self.get_metrics(),
            "prediction": self.get_prediction_summary(),
            "premium": self.get_premium_summary(),
            "feature_importance": self.get_feature_importance(),
            "health": self.health_check(),
        }

    # -------------------------------------------------------------------------
    # Alias
    # -------------------------------------------------------------------------

    def run(self):
        """
        Alias for the master pipeline.
        """
        return self.run_pipeline()
        
    # -------------------------------------------------------------------------
    # REPRESENTATION
    # -------------------------------------------------------------------------

    def __repr__(self):

        return "PricingService(AI-AIP v2 Pricing Engine)"


# =============================================================================
# MAIN
# =============================================================================


def main():
    """
    Standalone execution for testing.
    """

    service = PricingService()

    print("=" * 70)
    print("AI-AIP v2")
    print("Pricing Service")
    print("=" * 70)

    health = service.health_check()

    print()

    print("Pricing Engine Healthy :", health["healthy"])

    print()

    print("Available Outputs")

    for file in service.list_outputs():
        print(" -", file)

    print()

    print("=" * 70)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    try:
        main()

    except Exception:
        logger.exception("Pricing Service failed.")

        raise
