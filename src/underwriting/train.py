import joblib
import pandas as pd
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from xgboost import XGBClassifier


# ─────────────────────────────────────────────
# PROJECT ROOT (stable no matter where you run)
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_data.csv"
MODEL_DIR = PROJECT_ROOT / "models" / "underwriting"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "underwriting"

MODEL_PATH = MODEL_DIR / "underwriting_model.pkl"
FEATURE_IMPORTANCE_PATH = OUTPUT_DIR / "feature_importance.csv"


def train_underwriting_model():
    print("Loading processed dataset...")

    df = pd.read_csv(DATA_PATH)

    categorical_features = [
        "gender",
        "type_policy",
        "type_policy_dg",
        "type_product",
        "reimbursement",
        "new_business",
        "distribution_channel",
        "age_band",
        "seniority_band",
    ]

    numeric_features = [
        "age",
        "family_size",
        "seniority_insured",
        "seniority_policy",
        "exposure_time",
    ]

    target = "risk_class_encoded"

    X = df[categorical_features + numeric_features]
    y = df[target]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
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

    X_processed = pd.DataFrame(X_processed, columns=feature_names)

    X_train, X_test, y_train, y_test = train_test_split(
        X_processed,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1,
    )

    print("Training model...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}")

    # ─────────────────────────────────────────────
    # SAVE MODEL PAYLOAD
    # ─────────────────────────────────────────────
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "model": model,
        "preprocessor": preprocessor,
        "feature_names": feature_names,
        "categorical_features": categorical_features,
        "numeric_features": numeric_features,
    }

    joblib.dump(payload, MODEL_PATH)

    # ─────────────────────────────────────────────
    # FEATURE IMPORTANCE
    # ─────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    importance_df.to_csv(FEATURE_IMPORTANCE_PATH, index=False)

    print("\nModel saved successfully:")
    print(f"- {MODEL_PATH}")
    print(f"- {FEATURE_IMPORTANCE_PATH}")


if __name__ == "__main__":
    train_underwriting_model()
