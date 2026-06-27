import joblib
import numpy as np
import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/processed/processed_data.csv")
MODEL_PATH = Path("models/lapse/lapse_model.pkl")
FEATURE_IMPORTANCE_PATH = Path("models/lapse/feature_importance.csv")
OUTPUT_PATH = Path("outputs/lapse/lapse_predictions.csv")


def load_feature_importance():

    if FEATURE_IMPORTANCE_PATH.exists():
        return pd.read_csv(FEATURE_IMPORTANCE_PATH)["feature"].head(5).tolist()

    return []


def assign_risk_segment(probability):

    if probability >= 0.80:
        return "Critical"

    elif probability >= 0.60:
        return "High"

    elif probability >= 0.40:
        return "Medium"

    elif probability >= 0.20:
        return "Low"

    return "Very Low"


def prediction_confidence(probability):

    return max(probability, 1 - probability)


def predict_lapse():

    print("=" * 60)
    print("LAPSE PREDICTION")
    print("=" * 60)

    payload = joblib.load(MODEL_PATH)

    model = payload["model"]
    preprocessor = payload["preprocessor"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    df = pd.read_csv(DATA_PATH)

    X = df[categorical_features + numeric_features]

    X_processed = preprocessor.transform(X)

    probabilities = model.predict_proba(X_processed)[:, 1]

    predictions = model.predict(X_processed)

    important_features = load_feature_importance()

    primary_reason = (
        important_features[0]
        if len(important_features) > 0
        else "Highest Model Feature"
    )

    secondary_reason = (
        important_features[1]
        if len(important_features) > 1
        else "Secondary Model Feature"
    )

    output = pd.DataFrame({
        "row_id": range(len(df)),
        "predicted_lapse": predictions,
        "lapse_probability": probabilities.round(4),
        "confidence": [round(prediction_confidence(x), 4) for x in probabilities],
        "risk_segment": [assign_risk_segment(x) for x in probabilities],
        "primary_reason": primary_reason,
        "secondary_reason": secondary_reason,
    })

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"Predictions saved to {OUTPUT_PATH}")
    print()
    print("Risk Distribution")
    print(output["risk_segment"].value_counts())
    print()
    print(f"Average Lapse Probability : {output['lapse_probability'].mean():.4f}")

    return output


if __name__ == "__main__":
    predict_lapse()
