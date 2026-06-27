import logging

import numpy as np
import pandas as pd

# =============================================================================
# CONSTANTS
# =============================================================================

TARGET = "cost_claims_year"

REQUIRED_CATEGORICAL = [
    "gender",
    "type_policy",
    "type_product",
    "distribution_channel",
]

REQUIRED_NUMERIC = [
    "age",
    "family_size",
    "seniority_insured",
    "seniority_policy",
    "exposure_time",
    "IICIMUN",
    "IICIPROV",
    "C_GI",
    "C_II",
]

NON_NEGATIVE = [
    "age",
    "family_size",
    "seniority_insured",
    "seniority_policy",
    "exposure_time",
]

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================


def validate_training_dataset(df: pd.DataFrame) -> None:
    """
    Validate dataset before model training.

    Parameters
    ----------
    df : pd.DataFrame

    Raises
    ------
    ValueError
        If validation fails.
    """

    logging.info("Running pricing training validation.")

    required_columns = REQUIRED_CATEGORICAL + REQUIRED_NUMERIC + [TARGET]

    _check_empty_dataframe(df)
    _check_required_columns(df, required_columns)
    _check_missing_values(df, required_columns)
    _check_duplicates(df)
    _check_numeric_columns(df)
    _check_categorical_columns(df)
    _check_negative_values(df)
    _check_target(df)
    _check_constant_columns(df)

    logging.info("Training dataset validation completed successfully.")


def validate_prediction_dataset(df: pd.DataFrame) -> None:
    """
    Validate dataset before prediction.

    Parameters
    ----------
    df : pd.DataFrame

    Raises
    ------
    ValueError
        If validation fails.
    """

    logging.info("Running pricing prediction validation.")

    required_columns = REQUIRED_CATEGORICAL + REQUIRED_NUMERIC

    _check_empty_dataframe(df)
    _check_required_columns(df, required_columns)
    _check_missing_values(df, required_columns)
    _check_numeric_columns(df)
    _check_categorical_columns(df)
    _check_negative_values(df)

    logging.info("Prediction dataset validation completed successfully.")


def validate_model(payload: dict) -> None:
    """
    Validate model payload loaded from disk.

    Parameters
    ----------
    payload : dict

    Raises
    ------
    ValueError
        If payload is invalid.
    """

    logging.info("Validating pricing model payload.")

    required = [
        "model",
        "preprocessor",
        "feature_names",
        "categorical_features",
        "numeric_features",
    ]

    if payload is None:
        raise ValueError("Model payload is None.")

    for key in required:
        if key not in payload:
            raise ValueError(f"Missing model component: '{key}'.")

        if payload[key] is None:
            raise ValueError(f"Model component '{key}' is None.")

    logging.info("Model validation completed successfully.")


def validate_predictions(predictions) -> None:
    """
    Validate model predictions.

    Parameters
    ----------
    predictions : array-like

    Raises
    ------
    ValueError
        If predictions are invalid.
    """

    logging.info("Validating predictions.")

    predictions = np.asarray(predictions)

    if predictions.size == 0:
        raise ValueError("Prediction array is empty.")

    if np.isnan(predictions).any():
        raise ValueError("Predictions contain NaN values.")

    if np.isinf(predictions).any():
        raise ValueError("Predictions contain infinite values.")

    if (predictions < 0).any():
        raise ValueError("Predictions contain negative values.")

    _check_prediction_range(predictions)

    logging.info("Prediction validation completed successfully.")


# =============================================================================
# PRIVATE HELPERS
# =============================================================================


def _check_empty_dataframe(df: pd.DataFrame) -> None:
    """Check dataset is not empty."""

    if df.empty:
        raise ValueError("Dataset is empty.")


def _check_required_columns(
    df: pd.DataFrame,
    required_columns: list,
) -> None:
    """Check all required columns exist."""

    missing = [c for c in required_columns if c not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def _check_duplicates(df: pd.DataFrame) -> None:
    """Warn if duplicate rows exist."""

    duplicates = df.duplicated().sum()

    if duplicates > 0:
        logging.warning(
            "%d duplicate rows detected.",
            duplicates,
        )


def _check_missing_values(
    df: pd.DataFrame,
    required_columns: list,
) -> None:
    """Check missing values in required columns."""

    errors = []

    for col in required_columns:
        missing = df[col].isnull().sum()

        if missing > 0:
            errors.append(f"{col}: {missing} missing")

    if errors:
        raise ValueError("Missing values detected:\n" + "\n".join(errors))


def _check_numeric_columns(df: pd.DataFrame) -> None:
    """Validate numeric columns."""

    for col in REQUIRED_NUMERIC:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must be numeric.")


def _check_categorical_columns(df: pd.DataFrame) -> None:
    """Validate categorical columns."""

    for col in REQUIRED_CATEGORICAL:
        if df[col].isnull().all():
            raise ValueError(f"Categorical column '{col}' is completely missing.")

        if not (
            pd.api.types.is_object_dtype(df[col])
            or pd.api.types.is_categorical_dtype(df[col])
        ):
            logging.warning(
                "Column '%s' is not object/category dtype.",
                col,
            )


def _check_target(df: pd.DataFrame) -> None:
    """Validate target column."""

    if df[TARGET].isnull().any():
        raise ValueError("Target contains missing values.")

    if (df[TARGET] < 0).any():
        raise ValueError("Target contains negative values.")

    if df[TARGET].nunique() <= 1:
        raise ValueError("Target has no variance.")


def _check_negative_values(df: pd.DataFrame) -> None:
    """Validate non-negative features."""

    for col in NON_NEGATIVE:
        if (df[col] < 0).any():
            raise ValueError(f"Negative values detected in '{col}'.")


def _check_constant_columns(df: pd.DataFrame) -> None:
    """Warn about constant columns."""

    feature_columns = REQUIRED_CATEGORICAL + REQUIRED_NUMERIC

    for col in feature_columns:
        if df[col].nunique(dropna=False) == 1:
            logging.warning(
                "Constant feature detected: %s",
                col,
            )


def _check_prediction_range(
    predictions: np.ndarray,
) -> None:
    """
    Warn about suspicious prediction values.
    """

    if predictions.max() > 1_000_000:
        logging.warning("Very large prediction values detected.")

    if predictions.mean() == 0:
        logging.warning("Average prediction is zero.")

    if np.std(predictions) == 0:
        logging.warning("All predictions are identical.")
