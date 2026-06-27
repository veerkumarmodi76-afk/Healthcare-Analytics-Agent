import json
import logging
import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd

from .validation import (
    validate_model,
    validate_prediction_dataset,
    validate_predictions,
)

# =============================================================================
# CONSTANTS
# =============================================================================

MODEL_PATH = "models/pricing/pricing_model.pkl"

DATA_PATH = "data/processed/processed_data.csv"

OUTPUT_DIR = "outputs/pricing"

CSV_PATH = os.path.join(
    OUTPUT_DIR,
    "predicted_claim_cost.csv",
)

SUMMARY_PATH = os.path.join(
    OUTPUT_DIR,
    "prediction_summary.json",
)

METADATA_PATH = os.path.join(
    OUTPUT_DIR,
    "prediction_metadata.json",
)

MODEL_VERSION = "2.0.0"

TARGET_NAME = "expected_claim_cost"

DATASET_NAME = "processed_data.csv"

# =============================================================================
# LOGGER
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# =============================================================================
# MODEL LOADING
# =============================================================================


def load_model() -> dict:
    """
    Load and validate the trained pricing model.

    Returns
    -------
    dict
        Model payload containing model, preprocessor,
        feature names, and metadata.

    Raises
    ------
    FileNotFoundError
        If model file does not exist.

    ValueError
        If model validation fails.
    """

    logger.info("Loading pricing model...")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    payload = joblib.load(MODEL_PATH)

    validate_model(payload)

    logger.info("Pricing model loaded successfully.")

    return payload


# =============================================================================
# DATA LOADING
# =============================================================================


def load_dataset() -> pd.DataFrame:
    """
    Load processed dataset for prediction.

    Returns
    -------
    pd.DataFrame
        Processed dataframe.

    Raises
    ------
    FileNotFoundError
        If processed dataset does not exist.

    ValueError
        If dataset validation fails.
    """

    logger.info("Loading processed dataset...")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    validate_prediction_dataset(df)

    logger.info(
        "Dataset loaded successfully (%d rows).",
        len(df),
    )

    return df


# =============================================================================
# PREDICTION
# =============================================================================


def predict_claim_cost(
    payload: dict,
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Generate claim cost predictions.

    Parameters
    ----------
    payload : dict
        Loaded model payload.

    df : pd.DataFrame
        Prediction dataset.

    Returns
    -------
    tuple
        Output dataframe and prediction array.
    """

    logger.info("Preparing feature matrix...")

    categorical_features = payload["categorical_features"]

    numeric_features = payload["numeric_features"]

    expected_features = categorical_features + numeric_features

    # -------------------------------------------------------------------------
    # Validate required input columns
    # -------------------------------------------------------------------------

    missing_columns = [
        column for column in expected_features if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Prediction dataset is missing required feature columns: {missing_columns}"
        )

    extra_columns = sorted(set(df.columns) - set(expected_features))

    if extra_columns:
        logger.info(
            "Ignoring %d additional columns not used by the pricing model.",
            len(extra_columns),
        )

    X = df[expected_features].copy()
    logger.info(
        "Transforming %d feature columns...",
        X.shape[1],
    )

    X_processed = payload["preprocessor"].transform(X)

    logger.info("Generating predictions...")

    predictions = payload["model"].predict(X_processed)

    # Reverse log1p transformation
    predictions = np.expm1(predictions)

    # Business rule:
    # Claim cost cannot be negative
    predictions = np.maximum(
        predictions,
        0.0,
    )

    validate_predictions(predictions)

    output_df = pd.DataFrame({
        "row_id": np.arange(len(df)),
        "predicted_claim_cost": predictions,
    })

    logger.info("Prediction completed successfully.")

    return output_df, predictions


def save_predictions(output_df: pd.DataFrame) -> None:
    """
    Save prediction CSV.

    Parameters
    ----------
    output_df : pd.DataFrame
        Prediction dataframe.
    """

    logger.info("Saving prediction CSV...")

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    output_df.to_csv(
        CSV_PATH,
        index=False,
    )

    logger.info(
        "Prediction CSV saved to %s",
        CSV_PATH,
    )


# =============================================================================
# SUMMARY
# =============================================================================


def save_summary(predictions: np.ndarray) -> None:
    """
    Save prediction summary statistics.
    """

    logger.info("Saving prediction summary...")

    summary = {
        "prediction_date": datetime.now().isoformat(),
        "rows_predicted": int(len(predictions)),
        "minimum_prediction": float(np.min(predictions)),
        "maximum_prediction": float(np.max(predictions)),
        "average_prediction": float(np.mean(predictions)),
        "median_prediction": float(np.median(predictions)),
        "standard_deviation": float(np.std(predictions)),
        "total_expected_claim_cost": float(np.sum(predictions)),
    }

    with open(
        SUMMARY_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            summary,
            f,
            indent=4,
        )

    logger.info("Prediction summary saved.")


# =============================================================================
# METADATA
# =============================================================================


def save_metadata(
    payload: dict,
    df: pd.DataFrame,
) -> None:
    """
    Save prediction metadata.
    """

    logger.info("Saving prediction metadata...")

    metadata = {
        "model_version": MODEL_VERSION,
        "target": TARGET_NAME,
        "prediction_dataset": DATASET_NAME,
        "generated_at": datetime.now().isoformat(),
        "generated_by": "AI-AIP v2",
        "rows_processed": int(len(df)),
        "feature_count": int(len(payload["feature_names"])),
        "categorical_features": payload["categorical_features"],
        "numeric_features": payload["numeric_features"],
    }

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            metadata,
            f,
            indent=4,
        )

    logger.info("Prediction metadata saved.")


# =============================================================================
# MAIN
# =============================================================================


def main() -> pd.DataFrame:
    """
    Execute the complete pricing
    prediction pipeline.

    Returns
    -------
    pd.DataFrame
        Prediction dataframe.
    """

    logger.info("=" * 70)
    logger.info("PRICING PREDICTION PIPELINE")
    logger.info("=" * 70)

    payload = load_model()

    df = load_dataset()

    output_df, predictions = predict_claim_cost(
        payload,
        df,
    )

    save_predictions(output_df)

    save_summary(predictions)

    save_metadata(
        payload,
        df,
    )

    logger.info("")
    logger.info("Prediction Statistics")
    logger.info("---------------------")
    logger.info(
        "Rows      : %d",
        len(predictions),
    )
    logger.info(
        "Minimum   : %.2f",
        predictions.min(),
    )
    logger.info(
        "Maximum   : %.2f",
        predictions.max(),
    )
    logger.info(
        "Average   : %.2f",
        predictions.mean(),
    )
    logger.info(
        "Median    : %.2f",
        np.median(predictions),
    )
    logger.info(
        "Std Dev   : %.2f",
        predictions.std(),
    )

    logger.info("")
    logger.info("Outputs Generated:")
    logger.info(
        "[OK] %s",
        CSV_PATH,
    )
    logger.info(
        "[OK] %s",
        SUMMARY_PATH,
    )
    logger.info(
        "[OK] %s",
        METADATA_PATH,
    )

    logger.info("")
    logger.info("Pricing prediction pipeline completed successfully.")

    return output_df


# =============================================================================
# ENTRY POINT
# =============================================================================


if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        logger.exception("Prediction pipeline failed.")

        raise
