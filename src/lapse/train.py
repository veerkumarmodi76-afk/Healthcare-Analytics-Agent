"""
Lapse Analytics Engine - Production Training Pipeline
-----------------------------------------------------
Part 1/2

Responsibilities
----------------
1. Load processed dataset
2. Validate required columns
3. Build preprocessing pipeline
4. Create train/test split
5. Define candidate ML models
6. Utility functions used by Part 2

Outputs (generated in Part 2)
-----------------------------
models/lapse/
    lapse_model.pkl
    feature_importance.csv
    shap_summary.csv
    model_metrics.json

outputs/lapse/
    classification_report.txt
    confusion_matrix.csv
    roc_curve.csv
"""

import json
import logging
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

from .evaluation import evaluate_predictions

import shap


###############################################################################
# Configuration
###############################################################################

RANDOM_STATE = 42

DATA_PATH = Path("data/processed/processed_data.csv")

MODEL_DIR = Path("models/lapse")

OUTPUT_DIR = Path("outputs/lapse")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


###############################################################################
# Logging
###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


###############################################################################
# Feature Configuration
###############################################################################

CATEGORICAL_FEATURES = [
    "gender",
    "type_policy",
    "type_product",
    "distribution_channel",
    "age_band",
    "seniority_band",
    "portfolio_segment",
]

NUMERIC_FEATURES = [
    "age",
    "premium",
    "family_size",
    "seniority_insured",
    "seniority_policy",
    "premium_per_exposure",
    "claims_per_exposure",
    "age_band_score",
    "segment_score",
    "portfolio_segment_encoded",
]

TARGET_COLUMN = "lapse_binary"


###############################################################################
# Data Validation
###############################################################################


def validate_dataset(df: pd.DataFrame) -> None:
    """
    Ensures dataset contains every required column.
    """

    required = CATEGORICAL_FEATURES + NUMERIC_FEATURES + [TARGET_COLUMN]

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(f"Dataset missing columns: {missing}")

    if df.empty:
        raise ValueError("Dataset is empty.")

    logger.info("Dataset validation passed.")


###############################################################################
# Load Dataset
###############################################################################


def load_dataset():

    logger.info("Loading processed dataset...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    validate_dataset(df)

    logger.info(
        "Dataset Shape: %s rows × %s columns",
        df.shape[0],
        df.shape[1],
    )

    return df


###############################################################################
# Preprocessing
###############################################################################


def build_preprocessor():

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="passthrough",
    )


###############################################################################
# Train/Test Split
###############################################################################


def prepare_data(df):

    X = df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]

    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    logger.info(
        "Training samples: %d",
        len(X_train),
    )

    logger.info(
        "Testing samples: %d",
        len(X_test),
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


###############################################################################
# Candidate Models
###############################################################################


def build_candidate_models():

    return {
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "XGBoost": XGBClassifier(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=4.5,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }


###############################################################################
# Pipeline Builder
###############################################################################


def build_pipeline(model):

    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "model",
                model,
            ),
        ]
    )


###############################################################################
# Cross Validation
###############################################################################


def evaluate_cv(model_pipeline, X, y):

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    scores = cross_val_score(
        model_pipeline,
        X,
        y,
        scoring="roc_auc",
        cv=cv,
        n_jobs=-1,
    )

    return {
        "mean_auc": float(scores.mean()),
        "std_auc": float(scores.std()),
    }


###############################################################################
# Feature Names
###############################################################################


def get_feature_names(preprocessor):

    categorical = (
        preprocessor
        .named_transformers_["categorical"]
        .get_feature_names_out(CATEGORICAL_FEATURES)
        .tolist()
    )

    return categorical + NUMERIC_FEATURES


###############################################################################
# Artifact Saving Utilities
###############################################################################


def save_json(data, filepath):

    with open(filepath, "w") as file:
        json.dump(
            data,
            file,
            indent=4,
        )


def save_dataframe(df, filepath):

    df.to_csv(
        filepath,
        index=False,
    )


def save_text(text, filepath):

    with open(filepath, "w") as file:
        file.write(text)


###############################################################################
# Model Training
###############################################################################


def train_candidate_models(
    X_train,
    y_train,
):

    logger.info("=" * 70)
    logger.info("Training Candidate Models")
    logger.info("=" * 70)

    models = build_candidate_models()

    trained_models = {}
    cv_results = {}

    best_auc = -1.0
    best_name = None
    best_pipeline = None

    for model_name, model in models.items():
        logger.info("Training %s...", model_name)

        pipeline = build_pipeline(model)

        pipeline.fit(
            X_train,
            y_train,
        )

        cv_metrics = evaluate_cv(
            pipeline,
            X_train,
            y_train,
        )

        trained_models[model_name] = pipeline
        cv_results[model_name] = cv_metrics

        logger.info(
            "%s | Mean CV AUC = %.4f ± %.4f",
            model_name,
            cv_metrics["mean_auc"],
            cv_metrics["std_auc"],
        )

        if cv_metrics["mean_auc"] > best_auc:
            best_auc = cv_metrics["mean_auc"]
            best_name = model_name
            best_pipeline = pipeline

    logger.info("=" * 70)
    logger.info("Best Model : %s", best_name)
    logger.info("Cross Validation AUC : %.4f", best_auc)
    logger.info("=" * 70)

    return (
        best_name,
        best_pipeline,
        trained_models,
        cv_results,
    )


###############################################################################
# Test Evaluation
###############################################################################


def evaluate_model(
    pipeline,
    X_test,
    y_test,
):

    logger.info("Evaluating best model...")

    y_pred = pipeline.predict(X_test)

    y_probability = pipeline.predict_proba(X_test)[:, 1]

    metrics, report, matrix_df, roc_df = evaluate_predictions(
        y_test,
        y_pred,
        y_probability,
    )

    logger.info("")
    logger.info("Model Performance")
    logger.info("---------------------------")

    for metric, value in metrics.items():
        logger.info(
            "%s : %.4f",
            metric.upper(),
            value,
        )

    logger.info("")
    logger.info("Classification Report")
    logger.info("\n%s", report)

    return (
        metrics,
        report,
        matrix_df,
        roc_df,
        y_pred,
        y_probability,
    )


###############################################################################
# Feature Importance
###############################################################################


def generate_feature_importance(pipeline):

    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feature_names = get_feature_names(preprocessor)

    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_

    elif hasattr(model, "coef_"):
        importance = np.abs(model.coef_[0])

    else:
        logger.warning("Feature importance unavailable.")
        return None

    feature_df = (
        pd
        .DataFrame({
            "feature": feature_names,
            "importance": importance,
        })
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    feature_df.to_csv(
        MODEL_DIR / "feature_importance.csv",
        index=False,
    )

    logger.info("Feature importance saved.")

    return feature_df


###############################################################################
# SHAP
###############################################################################


def generate_shap_summary(
    pipeline,
    X_train,
):

    try:
        preprocessor = pipeline.named_steps["preprocessor"]
        model = pipeline.named_steps["model"]

        # Use a sample instead of the entire dataset
        sample_size = min(1000, len(X_train))

        X_sample = X_train.sample(
            n=sample_size,
            random_state=42,
        )

        X_processed = preprocessor.transform(X_sample)

        explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(X_processed)

        feature_names = get_feature_names(preprocessor)

        shap_df = pd.DataFrame({
            "feature": feature_names,
            "mean_abs_shap": np.abs(shap_values).mean(axis=0),
        })

        shap_df = shap_df.sort_values(
            "mean_abs_shap",
            ascending=False,
        ).reset_index(drop=True)

        shap_df.to_csv(
            MODEL_DIR / "shap_summary.csv",
            index=False,
        )

        logger.info("SHAP summary saved.")

    except Exception as e:
        logger.warning(
            "SHAP generation skipped: %s",
            e,
        )


###############################################################################
# Save Model
###############################################################################


def save_model(pipeline):

    payload = {
        "model": pipeline.named_steps["model"],
        "preprocessor": pipeline.named_steps["preprocessor"],
        "categorical_features": CATEGORICAL_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "feature_names": get_feature_names(pipeline.named_steps["preprocessor"]),
    }

    joblib.dump(
        payload,
        MODEL_DIR / "lapse_model.pkl",
    )

    logger.info("Model saved.")


###############################################################################
# Main Training Pipeline
###############################################################################


def train_lapse_model():

    logger.info("=" * 70)
    logger.info("LAPSE ANALYTICS PIPELINE")
    logger.info("=" * 70)

    df = load_dataset()

    X_train, X_test, y_train, y_test = prepare_data(df)

    (
        best_name,
        best_pipeline,
        trained_models,
        cv_results,
    ) = train_candidate_models(
        X_train,
        y_train,
    )

    (
        metrics,
        report,
        matrix_df,
        roc_df,
        y_pred,
        y_probability,
    ) = evaluate_model(
        best_pipeline,
        X_test,
        y_test,
    )


    generate_feature_importance(
        best_pipeline,
    )

    save_model(
        best_pipeline,
    )

    try:

        generate_shap_summary(
            best_pipeline,
            X_train,
        )

    except Exception as e:

        logger.warning(
            "SHAP generation skipped: %s",
            e,
        )

    logger.info("")
    logger.info("Best Model : %s", best_name)
    logger.info("ROC-AUC    : %.4f", metrics["roc_auc"])
    logger.info("Training Complete.")


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":
    train_lapse_model()