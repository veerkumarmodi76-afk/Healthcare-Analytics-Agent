import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

from xgboost import XGBClassifier


def train_lapse_model():

    print("Loading processed dataset...")

    df = pd.read_csv("data/processed/processed_data.csv")

    categorical_features = [
        "gender",
        "type_policy",
        "type_product",
        "distribution_channel",
        "age_band",
    ]

    numeric_features = [
        "age",
        "premium",
        "family_size",
        "seniority_insured",
        "seniority_policy",
        "risk_score",
        "claim_frequency",
        "loss_ratio",
    ]

    X = df[categorical_features + numeric_features]

    y = df["lapse_binary"]

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

    X_train, X_test, y_train, y_test = train_test_split(
        X_processed,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=4.52,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
    )

    print("Training lapse model...")

    model.fit(
        X_train,
        y_train,
    )

    y_pred = model.predict(X_test)

    y_proba = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(
        y_test,
        y_proba,
    )

    print("\nClassification Report")
    print(
        classification_report(
            y_test,
            y_pred,
        )
    )

    print("\nConfusion Matrix")
    print(
        confusion_matrix(
            y_test,
            y_pred,
        )
    )

    print(f"\nAUC: {auc:.4f}")

    payload = {
        "model": model,
        "preprocessor": preprocessor,
        "feature_names": feature_names,
        "categorical_features": categorical_features,
        "numeric_features": numeric_features,
    }

    os.makedirs(
        "models/lapse",
        exist_ok=True,
    )

    os.makedirs(
        "outputs/lapse",
        exist_ok=True,
    )

    joblib.dump(
        payload,
        "models/lapse/lapse_model.pkl",
    )

    print("Lapse model saved.")


if __name__ == "__main__":
    train_lapse_model()
