import json
import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd

# =============================================================================
# UNDERWRITING IMPORTS
# =============================================================================

from ..underwriting.train import (
    train_underwriting_model,
)

from ..underwriting.predict import (
    predict_underwriting,
    predict_applicant,
)

from ..underwriting.explain import (
    generate_global_shap_plots,
    generate_local_shap_plot,
    get_applicant_explanation,
)

from ..underwriting.run import (
    generate_underwriting_report,
)

# =============================================================================
# PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = PROJECT_ROOT / "models" / "underwriting"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "underwriting"

LOG_DIR = PROJECT_ROOT / "outputs" / "logs"

LOG_FILE = LOG_DIR / "underwriting_service.log"

MODEL_PATH = MODEL_DIR / "underwriting_model.pkl"

# =============================================================================
# OUTPUT FILES
# =============================================================================

METRICS_FILE = OUTPUT_DIR / "training_metrics.json"

SUMMARY_FILE = OUTPUT_DIR / "underwriting_summary.json"

FEATURE_IMPORTANCE_FILE = OUTPUT_DIR / "feature_importance.csv"

SHAP_IMPORTANCE_FILE = OUTPUT_DIR / "feature_importance_shap.csv"

PREDICTION_FILE = OUTPUT_DIR / "underwriting_predictions.csv"

EXPLANATION_FILE = OUTPUT_DIR / "applicant_explanation.json"

RULE_REPORT_FILE = OUTPUT_DIR / "rule_distribution.csv"

CONFUSION_MATRIX_FILE = OUTPUT_DIR / "confusion_matrix.csv"

CLASS_DISTRIBUTION_FILE = OUTPUT_DIR / "class_distribution.csv"

MODEL_METADATA_FILE = OUTPUT_DIR / "model_metadata.json"

SHAP_SUMMARY_FILE = OUTPUT_DIR / "shap_summary.png"

# =============================================================================
# LOGGER
# =============================================================================

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

logger = logging.getLogger(
    "underwriting_service",
)

logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    handler = logging.FileHandler(LOG_FILE)

    handler.setFormatter(formatter)

    logger.addHandler(handler)

# =============================================================================
# SERVICE
# =============================================================================


class UnderwritingService:
    """
    Production Service Layer for
    Underwriting Department.
    """

    # ------------------------------------------------------------------
    # TRAIN
    # ------------------------------------------------------------------

    def train(self):
        """
        Train underwriting model.
        """

        logger.info("=" * 70)
        logger.info("UNDERWRITING TRAINING STARTED")

        try:
            payload = train_underwriting_model()

            logger.info("Training completed successfully.")

            return payload

        except Exception:
            logger.exception("Training failed.")

            raise

    # ------------------------------------------------------------------
    # BATCH PREDICTION
    # ------------------------------------------------------------------

    def predict(self):
        """
        Batch underwriting prediction.
        """

        logger.info("=" * 70)
        logger.info("UNDERWRITING PREDICTION STARTED")

        try:
            df = predict_underwriting()

            logger.info("Prediction completed.")

            return df

        except Exception:
            logger.exception("Prediction failed.")

            raise

    # ------------------------------------------------------------------
    # SINGLE APPLICANT
    # ------------------------------------------------------------------

    def predict_applicant(
        self,
        applicant: dict,
    ):
        """
        Predict a single applicant.
        """

        logger.info("Predicting individual applicant.")

        try:
            result = predict_applicant(applicant)

            logger.info("Applicant prediction successful.")

            return result

        except Exception:
            logger.exception("Applicant prediction failed.")

            raise

    # ------------------------------------------------------------------
    # GLOBAL SHAP
    # ------------------------------------------------------------------

    def explain(
        self,
        sample_size: int = 1000,
    ):
        """
        Generate global SHAP analysis.
        """

        logger.info("=" * 70)
        logger.info("GLOBAL SHAP ANALYSIS")

        try:
            generate_global_shap_plots(
                sample_size=sample_size,
            )

            logger.info("Global SHAP completed.")

            return True

        except Exception:
            logger.exception("Global SHAP failed.")

            raise

    # ------------------------------------------------------------------
    # LOCAL SHAP
    # ------------------------------------------------------------------

    def explain_applicant(
        self,
        applicant_index: int,
    ):
        """
        Generate applicant explanation.
        """

        logger.info("Applicant explanation requested.")

        try:
            generate_local_shap_plot(applicant_index)

            explanation = get_applicant_explanation(applicant_index)

            logger.info("Applicant explanation generated.")

            return explanation

        except Exception:
            logger.exception("Applicant explanation failed.")

            raise

    # ------------------------------------------------------------------
    # GOVERNANCE REPORT
    # ------------------------------------------------------------------

    def generate_report(self):
        """
        Generate underwriting report.
        """

        logger.info("=" * 70)
        logger.info("UNDERWRITING REPORT")

        try:
            summary = generate_underwriting_report()

            logger.info("Summary generated.")

            return summary

        except Exception:
            logger.exception("Summary generation failed.")

            raise

    # ------------------------------------------------------------------
    # COMPLETE PIPELINE
    # ------------------------------------------------------------------

    def run_pipeline(self):
        """
        Complete underwriting workflow.

        Train

            ↓

        Predict

            ↓

        Global SHAP

            ↓

        Applicant SHAP

            ↓

        Summary
        """

        logger.info("=" * 70)
        logger.info("UNDERWRITING PIPELINE STARTED")

        self.train()

        self.predict()

        self.explain()

        self.explain_applicant(0)

        self.generate_report()

        logger.info("Pipeline completed successfully.")

        return True

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------

    @staticmethod
    def _load_json(path):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    @staticmethod
    def _load_csv(path):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        return pd.read_csv(path)

    # ------------------------------------------------------------------
    # TRAINING METRICS
    # ------------------------------------------------------------------

    def get_metrics(self):
        """
        Load underwriting training metrics.
        """

        logger.info("Loading training metrics.")

        return self._load_json(
            METRICS_FILE,
        )

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------

    def get_summary(self):
        """
        Load underwriting summary.
        """

        logger.info("Loading underwriting summary.")

        return self._load_json(
            SUMMARY_FILE,
        )

    # ------------------------------------------------------------------
    # FEATURE IMPORTANCE
    # ------------------------------------------------------------------

    def get_feature_importance(self):
        """
        Load XGBoost feature importance.
        """

        logger.info("Loading feature importance.")

        return self._load_csv(
            FEATURE_IMPORTANCE_FILE,
        )

    # ------------------------------------------------------------------
    # SHAP IMPORTANCE
    # ------------------------------------------------------------------

    def get_shap_importance(self):
        """
        Load SHAP feature importance.
        """

        logger.info("Loading SHAP importance.")

        return self._load_csv(
            SHAP_IMPORTANCE_FILE,
        )

    # ------------------------------------------------------------------
    # PREDICTIONS
    # ------------------------------------------------------------------

    def get_predictions(self):
        """
        Load underwriting predictions.
        """

        logger.info("Loading predictions.")

        return self._load_csv(
            PREDICTION_FILE,
        )

    # ------------------------------------------------------------------
    # MODEL METADATA
    # ------------------------------------------------------------------

    def get_model_metadata(self):
        """
        Load model metadata.
        """

        logger.info("Loading model metadata.")

        return self._load_json(
            MODEL_METADATA_FILE,
        )

    # ------------------------------------------------------------------
    # APPLICANT EXPLANATION
    # ------------------------------------------------------------------

    def get_explanation(
        self,
    ):
        """
        Load latest applicant explanation.
        """

        logger.info("Loading applicant explanation.")

        return self._load_json(
            EXPLANATION_FILE,
        )

    # ------------------------------------------------------------------
    # OUTPUT FILES
    # ------------------------------------------------------------------

    def list_outputs(self):
        """
        List all underwriting outputs.
        """

        logger.info("Listing output artifacts.")

        if not OUTPUT_DIR.exists():
            return []

        return sorted([file.name for file in OUTPUT_DIR.iterdir() if file.is_file()])

    # ------------------------------------------------------------------
    # HEALTH CHECK
    # ------------------------------------------------------------------

    def health_check(self):
        """
        Validate underwriting artifacts.
        """

        logger.info("Running health check.")

        status = {
            "model_exists": MODEL_PATH.exists(),
            "metrics_exists": METRICS_FILE.exists(),
            "summary_exists": SUMMARY_FILE.exists(),
            "feature_importance_exists": FEATURE_IMPORTANCE_FILE.exists(),
            "shap_importance_exists": SHAP_IMPORTANCE_FILE.exists(),
            "predictions_exists": PREDICTION_FILE.exists(),
            "rule_distribution_exists": RULE_REPORT_FILE.exists(),
            "confusion_matrix_exists": CONFUSION_MATRIX_FILE.exists(),
            "class_distribution_exists": CLASS_DISTRIBUTION_FILE.exists(),
            "metadata_exists": MODEL_METADATA_FILE.exists(),
            "shap_summary_exists": SHAP_SUMMARY_FILE.exists(),
            "explanation_exists": EXPLANATION_FILE.exists(),
        }

        status["healthy"] = all(status.values())

        logger.info(
            "Health Status: %s",
            status["healthy"],
        )

        return status

    # ------------------------------------------------------------------
    # DASHBOARD DATA
    # ------------------------------------------------------------------

    def dashboard_data(self):
        """
        Collect everything required by
        the dashboard.
        """

        logger.info("Preparing dashboard data.")

        return {
            "metrics": self.get_metrics(),
            "summary": self.get_summary(),
            "predictions": self.get_predictions(),
            "feature_importance": self.get_feature_importance(),
            "shap_importance": self.get_shap_importance(),
            "metadata": self.get_model_metadata(),
            "health": self.health_check(),
        }

# ------------------------------------------------------------------
# Alias
# ------------------------------------------------------------------

    def run(self):
        """
        Alias for the master pipeline.
        """
        return self.run_pipeline()
    # ------------------------------------------------------------------
    # REPRESENTATION
    # ------------------------------------------------------------------

    def __repr__(self):

        return "UnderwritingService(AI-AIP v2 Underwriting Engine)"


# =============================================================================
# MAIN
# =============================================================================


def main():
    """
    Standalone service test.
    """

    service = UnderwritingService()

    print("=" * 70)
    print("AI-AIP v2")
    print("Underwriting Service")
    print("=" * 70)

    health = service.health_check()

    print()

    print(
        "Engine Healthy :",
        health["healthy"],
    )

    print()

    print("Generated Outputs")

    for file in service.list_outputs():
        print(
            " -",
            file,
        )

    print()

    print("=" * 70)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    try:
        main()

    except Exception:
        logger.exception("Underwriting service failed.")

        raise
