from __future__ import annotations

import json
import logging
import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from xgboost import XGBRegressor


# =============================================================================
# PATHS
# =============================================================================

DATA_PATH = "data/processed/processed_data.csv"

MODEL_PATH = "models/pricing/pricing_model.pkl"

OUTPUT_DIR = "outputs/pricing"

LOG_DIR = "outputs/logs"


# =============================================================================
# CONFIGURATION
# =============================================================================

TARGET = "cost_claims_year"

RANDOM_STATE = 42

TEST_SIZE = 0.20


# =============================================================================
# FEATURES
# =============================================================================

DROP_COLUMNS = [
    # identifiers
    "ID",
    "ID_policy",
    "ID_insured",
    # dates
    "date_effect_insured",
    "date_lapse_insured",
    "date_effect_policy",
    "date_lapse_policy",
    # derived years
    "year_effect_insured",
    "year_lapse_insured",
    "year_effect_policy",
    "year_lapse_policy",
    # target
    TARGET,
    # other departments
    "lapse",
    "lapse_binary",
    "risk_score",
    # leakage
    "claims_per_exposure",
    "n_medical_services",
]


CATEGORICAL_FEATURES = [
    "gender",
    "type_policy",
    "type_policy_dg",
    "type_product",
    "distribution_channel",
    "reimbursement",
    "new_business",
    "age_band",
    "seniority_band",
    "portfolio_segment",
    # insurance category codes
    "C_H",
    "C_GI",
    "C_II",
    "C_IE_P",
    "C_IE_S",
    "C_IE_T",
    "C_GE_P",
    "C_GE_S",
    "C_GE_T",
    "C_C",
]


NUMERIC_FEATURES = [
    "period",
    "exposure_time",
    "seniority_insured",
    "seniority_policy",
    "age",
    "premium",
    "premium_per_exposure",
    "family_size",
    "n_insured_pc",
    "n_insured_mun",
    "n_insured_prov",
    "IICIMUN",
    "IICIPROV",
    "age_band_score",
    "segment_score",
    "portfolio_segment_encoded",
]


# =============================================================================
# LOGGER
# =============================================================================


def configure_logger() -> None:

    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(LOG_DIR, "pricing.log"),
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        force=True,
    )


# =============================================================================
# DATA VALIDATION
# =============================================================================


def validate_dataset(df: pd.DataFrame) -> None:

    logging.info("Running dataset validation.")

    if df.empty:
        raise ValueError("Dataset is empty.")

    if TARGET not in df.columns:
        raise ValueError(f"Missing target column '{TARGET}'.")

    if df[TARGET].isna().any():
        raise ValueError("Target contains missing values.")

    duplicates = df.duplicated().sum()

    if duplicates > 0:
        logging.warning(
            "Duplicate rows detected: %s",
            duplicates,
        )

    logging.info("Dataset validation completed.")


# =============================================================================
# FEATURE VALIDATION
# =============================================================================


def validate_features(df: pd.DataFrame):

    required = CATEGORICAL_FEATURES + NUMERIC_FEATURES + [TARGET]

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(f"Missing feature columns: {missing}")


# =============================================================================
# FEATURE PREPARATION
# =============================================================================


def prepare_training_data(df: pd.DataFrame):

    validate_features(df)

    feature_columns = CATEGORICAL_FEATURES + NUMERIC_FEATURES

    X = df[feature_columns].copy()

    y = np.log1p(df[TARGET])

    return (
        X,
        y,
        feature_columns,
        CATEGORICAL_FEATURES,
        NUMERIC_FEATURES,
    )


# =============================================================================
# PREPROCESSOR
# =============================================================================


def build_preprocessor():

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
        ]
    )

    return preprocessor


# =============================================================================
# MODEL
# =============================================================================


def build_model():

    return XGBRegressor(
        objective="reg:squarederror",
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=6,
        min_child_weight=3,
        subsample=0.80,
        colsample_bytree=0.80,
        reg_alpha=0.50,
        reg_lambda=2.00,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


# =============================================================================
# TRAINING
# =============================================================================


def train_model():

    configure_logger()

    logging.info("=" * 80)
    logging.info("Pricing model training started.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    print("=" * 70)
    print("PRICING MODEL TRAINING")
    print("=" * 70)

    print("Loading processed dataset...")

    df = pd.read_csv(DATA_PATH)

    logging.info(
        "Dataset loaded successfully (%s rows).",
        len(df),
    )

    validate_dataset(df)

    X, y, feature_columns, categorical_features, numeric_features = (
        prepare_training_data(df)
    )

    logging.info("Building preprocessing pipeline.")

    preprocessor = build_preprocessor()

    X_processed = preprocessor.fit_transform(X)

    feature_names = preprocessor.get_feature_names_out().tolist()

    logging.info("Splitting dataset.")

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X_processed,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    logging.info("Initializing XGBoost model.")

    model = build_model()

    print("Training pricing model...")

    model.fit(
        X_train,
        y_train,
    )

    logging.info("Training completed.")

    print("Evaluating model...")

    y_pred_log = model.predict(X_test)

    y_pred = np.expm1(y_pred_log)

    y_true = np.expm1(y_test)

    mae = mean_absolute_error(
        y_true,
        y_pred,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred,
        )
    )

    r2 = r2_score(
        y_true,
        y_pred,
    )

    logging.info(
        "Evaluation completed (MAE %.2f RMSE %.2f R² %.4f)",
        mae,
        rmse,
        r2,
    )

    if r2 < 0.45:
        raise ValueError(
            f"""
Pricing model failed quality validation.

R² = {r2:.4f}

Expected R² >= 0.50

Model will not be saved.
"""
        )

    metrics = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "training_rows": int(len(X_train)),
        "testing_rows": int(len(X_test)),
    }

    # =========================================================================
    # FEATURE IMPORTANCE
    # =========================================================================

    logging.info("Calculating feature importance.")

    importance_df = (
        pd
        .DataFrame({
            "feature": feature_names,
            "importance": model.feature_importances_,
        })
        .sort_values(
            by="importance",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    feature_importance_path = os.path.join(
        OUTPUT_DIR,
        "feature_importance.csv",
    )

    importance_df.to_csv(
        feature_importance_path,
        index=False,
    )

    logging.info(
        "Feature importance saved to %s",
        feature_importance_path,
    )

    # =========================================================================
    # SAVE METRICS
    # =========================================================================

    metrics_path = os.path.join(
        OUTPUT_DIR,
        "metrics.json",
    )

    with open(
        metrics_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metrics,
            file,
            indent=4,
        )

    logging.info(
        "Training metrics saved to %s",
        metrics_path,
    )

    # =========================================================================
    # SAVE MODEL
    # =========================================================================

    payload = {
        "model": model,
        "preprocessor": preprocessor,
        "feature_names": feature_names,
        "categorical_features": categorical_features,
        "numeric_features": numeric_features,
        "metrics": metrics,
        "created_at": datetime.now().isoformat(),
        "model_name": "Healthcare Pricing Model",
        "model_version": "2.0.0",
        "algorithm": "XGBoost Regressor",
        "target": TARGET,
    }

    joblib.dump(
        payload,
        MODEL_PATH,
    )

    logging.info(
        "Model saved to %s",
        MODEL_PATH,
    )

    # =========================================================================
    # SAVE METADATA
    # =========================================================================

    metadata = {
        "generated_at": datetime.now().isoformat(),
        "model_name": "Healthcare Pricing Model",
        "model_version": "2.0.0",
        "algorithm": "XGBoost Regressor",
        "target": TARGET,
        "rows_processed": int(len(df)),
        "training_rows": int(len(X_train)),
        "testing_rows": int(len(X_test)),
        "feature_count": len(feature_names),
        "categorical_features": categorical_features,
        "numeric_features": numeric_features,
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
    }

    metadata_path = os.path.join(
        OUTPUT_DIR,
        "training_metadata.json",
    )

    with open(
        metadata_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            indent=4,
        )

    logging.info(
        "Training metadata saved to %s",
        metadata_path,
    )

    print()
    print("=" * 70)
    print("MODEL PERFORMANCE")
    print("=" * 70)
    print(f"MAE             : {mae:.2f}")
    print(f"RMSE            : {rmse:.2f}")
    print(f"R² Score        : {r2:.4f}")
    print(f"Training Rows   : {len(X_train):,}")
    print(f"Testing Rows    : {len(X_test):,}")
    print("=" * 70)

    print()
    print("Generated Files")
    print("------------------------------")
    print(MODEL_PATH)
    print(metrics_path)
    print(feature_importance_path)
    print(metadata_path)
    print("=" * 70)

    logging.info("Pricing model training completed successfully.")

    return payload


# =============================================================================
# MAIN
# =============================================================================


def main() -> dict:
    """
    Execute the complete pricing model
    training pipeline.

    Returns
    -------
    dict
        Trained model payload.
    """

    logging.info("=" * 70)
    logging.info("PRICING MODEL TRAINING PIPELINE")
    logging.info("=" * 70)

    payload = train_model()

    logging.info("")
    logging.info("=" * 70)
    logging.info("TRAINING COMPLETED SUCCESSFULLY")
    logging.info("=" * 70)

    logging.info("Generated Outputs")
    logging.info("------------------------------")
    logging.info("Model")
    logging.info("  %s", MODEL_PATH)

    logging.info("")
    logging.info("Metrics")
    logging.info("  %s", os.path.join(OUTPUT_DIR, "metrics.json"))

    logging.info("")
    logging.info("Feature Importance")
    logging.info(
        "  %s",
        os.path.join(
            OUTPUT_DIR,
            "feature_importance.csv",
        ),
    )

    logging.info("")
    logging.info("Training Metadata")
    logging.info(
        "  %s",
        os.path.join(
            OUTPUT_DIR,
            "training_metadata.json",
        ),
    )

    logging.info("=" * 70)

    print()
    print("=" * 70)
    print("PRICING MODEL TRAINING COMPLETE")
    print("=" * 70)
    print(f"Model                : {MODEL_PATH}")
    print(f"Metrics              : {os.path.join(OUTPUT_DIR, 'metrics.json')}")
    print(
        f"Feature Importance   : {os.path.join(OUTPUT_DIR, 'feature_importance.csv')}"
    )
    print(
        f"Training Metadata    : {os.path.join(OUTPUT_DIR, 'training_metadata.json')}"
    )
    print("=" * 70)

    return payload


# =============================================================================
# ENTRY POINT
# =============================================================================


if __name__ == "__main__":
    try:
        main()

    except Exception:
        logging.exception("Pricing model training failed.")
        raise
