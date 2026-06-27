import json
import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
)

from xgboost import XGBClassifier

from .rules import create_underwriting_target


# ─────────────────────────────────────────────
# PROJECT ROOT
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_data.csv"

MODEL_DIR = PROJECT_ROOT / "models" / "underwriting"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "underwriting"

MODEL_PATH = MODEL_DIR / "underwriting_model.pkl"

FEATURE_IMPORTANCE_PATH = OUTPUT_DIR / "feature_importance.csv"

METRICS_PATH = OUTPUT_DIR / "training_metrics.json"

CONFUSION_MATRIX_PATH = OUTPUT_DIR / "confusion_matrix.csv"

CLASS_DISTRIBUTION_PATH = OUTPUT_DIR / "class_distribution.csv"

MODEL_METADATA_PATH = OUTPUT_DIR / "model_metadata.json"

MODEL_VERSION = "1.0"


# ─────────────────────────────────────────────
# TRAIN MODEL
# ─────────────────────────────────────────────
def train_underwriting_model():

    print("Loading processed dataset...")

    df = pd.read_csv(DATA_PATH)

    # ─────────────────────────────────────────────
    # BUSINESS RULE TARGET
    # ─────────────────────────────────────────────
    print("Creating underwriting target...")

    df = create_underwriting_target(df)

    target = "uw_risk_class_encoded"

    # ─────────────────────────────────────────────
    # FINAL FEATURE SET
    # ─────────────────────────────────────────────
    categorical_features = [
        "gender",
        "type_policy",
        "type_policy_dg",
        "type_product",
        "distribution_channel",
        "new_business",
        "age_band",
        "seniority_band",
    ]

    numeric_features = [
        "age",
        "family_size",
        "seniority_insured",
        "seniority_policy",
    ]

    required_columns = categorical_features + numeric_features + [target]

    missing_cols = [c for c in required_columns if c not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    X = df[categorical_features + numeric_features].copy()

    y = df[target].copy()

    print(f"Rows: {len(df):,}")

    # ─────────────────────────────────────────────
    # PREPROCESSOR
    # ─────────────────────────────────────────────
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                categorical_features,
            )
        ],
        remainder="passthrough",
    )

    X_processed = preprocessor.fit_transform(X)

    feature_names = (
        preprocessor
        .named_transformers_["cat"]
        .get_feature_names_out(categorical_features)
        .tolist()
        + numeric_features
    )

    X_processed = pd.DataFrame(
        X_processed,
        columns=feature_names,
    )

    # ─────────────────────────────────────────────
    # TRAIN TEST SPLIT
    # ─────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # ─────────────────────────────────────────────
    # MODEL
    # ─────────────────────────────────────────────
    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.80,
        colsample_bytree=0.80,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1,
    )

    print("Training underwriting model...")

    model.fit(
        X_train,
        y_train,
    )

    # ─────────────────────────────────────────────
    # EVALUATION
    # ─────────────────────────────────────────────
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        y_pred,
    )

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True,
    )

    cm = confusion_matrix(
        y_test,
        y_pred,
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
        )
    )

    print("\nConfusion Matrix:")
    print(cm)

    print(f"\nAccuracy: {accuracy:.4f}")

    # ─────────────────────────────────────────────
    # CREATE FOLDERS
    # ─────────────────────────────────────────────
    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ─────────────────────────────────────────────
    # SAVE MODEL
    # ─────────────────────────────────────────────
    payload = {
        "model": model,
        "preprocessor": preprocessor,
        "feature_names": feature_names,
        "categorical_features": categorical_features,
        "numeric_features": numeric_features,
        "model_version": MODEL_VERSION,
    }

    joblib.dump(
        payload,
        MODEL_PATH,
    )

    # ─────────────────────────────────────────────
    # FEATURE IMPORTANCE
    # ─────────────────────────────────────────────
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_,
    })

    importance_df = importance_df.sort_values(
        "importance",
        ascending=False,
    )

    importance_df.to_csv(
        FEATURE_IMPORTANCE_PATH,
        index=False,
    )

    # ─────────────────────────────────────────────
    # METRICS
    # ─────────────────────────────────────────────
    metrics = {
        "accuracy": float(accuracy),
        "rows": int(len(df)),
        "features": int(len(feature_names)),
        "classes": int(len(y.unique())),
        "classification_report": report,
    }

    with open(
        METRICS_PATH,
        "w",
    ) as f:
        json.dump(
            metrics,
            f,
            indent=4,
        )

    # ─────────────────────────────────────────────
    # CONFUSION MATRIX
    # ─────────────────────────────────────────────
    pd.DataFrame(cm).to_csv(
        CONFUSION_MATRIX_PATH,
        index=False,
    )

    # ─────────────────────────────────────────────
    # CLASS DISTRIBUTION
    # ─────────────────────────────────────────────
    class_dist = pd.Series(y).value_counts().sort_index().reset_index()

    class_dist.columns = [
        "class",
        "count",
    ]

    class_dist.to_csv(
        CLASS_DISTRIBUTION_PATH,
        index=False,
    )

    # ─────────────────────────────────────────────
    # MODEL GOVERNANCE METADATA
    # ─────────────────────────────────────────────
    metadata = {
        "model_name": "underwriting",
        "version": MODEL_VERSION,
        "trained_on": datetime.now().strftime("%Y-%m-%d"),
        "features": len(categorical_features + numeric_features),
        "classes": len(y.unique()),
    }

    with open(
        MODEL_METADATA_PATH,
        "w",
    ) as f:
        json.dump(
            metadata,
            f,
            indent=4,
        )

    # ─────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("UNDERWRITING TRAINING COMPLETE")
    print("=" * 60)

    print(f"Model Version : {MODEL_VERSION}")
    print(f"Accuracy      : {accuracy:.4f}")

    print("\nArtifacts:")

    print(MODEL_PATH)
    print(FEATURE_IMPORTANCE_PATH)
    print(METRICS_PATH)
    print(CONFUSION_MATRIX_PATH)
    print(CLASS_DISTRIBUTION_PATH)
    print(MODEL_METADATA_PATH)

    print("=" * 60)

    return payload


# ─────────────────────────────────────────────
# LOAD TRAINING METRICS
# ─────────────────────────────────────────────
def get_training_metrics():

    if not METRICS_PATH.exists():
        raise FileNotFoundError(f"Metrics file not found: {METRICS_PATH}")

    with open(
        METRICS_PATH,
        "r",
    ) as f:
        return json.load(f)


if __name__ == "__main__":
    train_underwriting_model()
