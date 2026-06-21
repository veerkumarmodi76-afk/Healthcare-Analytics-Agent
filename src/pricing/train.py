import os
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from xgboost import XGBRegressor


def train_pricing_model():

    print("Loading processed dataset...")

    df = pd.read_csv("data/processed/processed_data.csv")

    categorical_features = [
        "gender",
        "type_policy",
        "type_product",
        "distribution_channel",
    ]

    numeric_features = [
        "age",
        "family_size",
        "seniority_insured",
        "seniority_policy",
        "exposure_time",
        "n_medical_services",
        "claim_frequency",
        "claim_severity",
        "risk_score",
        "IICIMUN",
        "IICIPROV",
        "C_GI",
        "C_II",
    ]

    target = "cost_claims_year"

    X = df[categorical_features + numeric_features]

    y = np.log1p(df[target])

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
    )

    model = XGBRegressor(
        n_estimators=500,
        max_depth=8,
        learning_rate=0.03,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=5,
        random_state=42,
        n_jobs=-1,
    )

    print("Training pricing model...")

    model.fit(X_train, y_train)

    y_pred_log = model.predict(X_test)

    y_pred = np.expm1(y_pred_log)

    y_actual = np.expm1(y_test)

    mae = mean_absolute_error(y_actual, y_pred)

    r2 = r2_score(y_actual, y_pred)

    print(f"MAE : {mae:.2f}")
    print(f"R²  : {r2:.4f}")

    payload = {
        "model": model,
        "preprocessor": preprocessor,
        "feature_names": feature_names,
        "categorical_features": categorical_features,
        "numeric_features": numeric_features,
    }

    os.makedirs(
        "models/pricing",
        exist_ok=True,
    )

    os.makedirs(
        "outputs/pricing",
        exist_ok=True,
    )

    joblib.dump(
        payload,
        "models/pricing/pricing_model.pkl",
    )

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_,
    })

    importance_df.sort_values(
        "importance",
        ascending=False,
    ).to_csv(
        "outputs/pricing/feature_importance.csv",
        index=False,
    )

    print("Pricing model saved successfully.")


if __name__ == "__main__":
    train_pricing_model()
