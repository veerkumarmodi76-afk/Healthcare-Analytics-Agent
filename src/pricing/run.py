import logging
import os
import time

from .train import train_model
from .predict import main as prediction_pipeline
from .premium import main as premium_pipeline
from .report import main as report_pipeline


# =============================================================================
# LOGGER
# =============================================================================

LOG_DIR = "outputs/logs"
LOG_FILE = os.path.join(LOG_DIR, "pricing.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


# =============================================================================
# PIPELINE
# =============================================================================


def run():

    start = time.time()

    logger.info("=" * 80)
    logger.info("AI-AIP v2 PRICING DEPARTMENT")
    logger.info("=" * 80)

    try:
        # ---------------------------------------------------------------------
        # Stage 1
        # ---------------------------------------------------------------------

        logger.info("")
        logger.info("STAGE 1/4 : MODEL TRAINING")

        train_model()

        logger.info("✓ Model training completed.")

        # ---------------------------------------------------------------------
        # Stage 2
        # ---------------------------------------------------------------------

        logger.info("")
        logger.info("STAGE 2/4 : CLAIM COST PREDICTION")

        prediction_pipeline()

        logger.info("✓ Prediction completed.")

        # ---------------------------------------------------------------------
        # Stage 3
        # ---------------------------------------------------------------------

        logger.info("")
        logger.info("STAGE 3/4 : PREMIUM GENERATION")

        premium_pipeline()

        logger.info("✓ Premium generation completed.")

        # ---------------------------------------------------------------------
        # Stage 4
        # ---------------------------------------------------------------------

        logger.info("")
        logger.info("STAGE 4/4 : REPORT GENERATION")

        report_pipeline()

        logger.info("✓ Reports generated.")

        # ---------------------------------------------------------------------

        elapsed = time.time() - start

        logger.info("")
        logger.info("=" * 80)
        logger.info("PRICING PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)

        logger.info("Execution Time : %.2f seconds", elapsed)

        logger.info("")
        logger.info("Generated Outputs")
        logger.info("------------------------------")
        logger.info("Model")
        logger.info("  models/pricing/pricing_model.pkl")

        logger.info("")
        logger.info("Predictions")
        logger.info("  outputs/pricing/predicted_claim_cost.csv")
        logger.info("  outputs/pricing/prediction_summary.json")
        logger.info("  outputs/pricing/prediction_metadata.json")

        logger.info("")
        logger.info("Premium")
        logger.info("  outputs/pricing/premium_quotes.csv")
        logger.info("  outputs/pricing/premium_summary.json")
        logger.info("  outputs/pricing/premium_metadata.json")

        logger.info("")
        logger.info("Reports")
        logger.info("  outputs/pricing/pricing_report.md")
        logger.info("  outputs/pricing/pricing_report.json")

        logger.info("")
        logger.info("Metrics")
        logger.info("  outputs/pricing/metrics.json")
        logger.info("  outputs/pricing/feature_importance.csv")

        logger.info("=" * 80)

    except Exception:
        logger.exception("Pricing pipeline failed.")

        raise


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run()
