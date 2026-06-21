import os
import joblib
import numpy as np
import pandas as pd


def predict_claim_cost():

    payload = joblib.load("models/pricing/pricing_model.pkl")

    model = payload["model"]

    preprocessor = payload["preprocessor"]

    categorical_features = payload["categorical_features"]

    numeric_features = payload["numeric_features"]

    df = pd.read_csv("data/processed/processed_data.csv")

    X = df[categorical_features + numeric_features]

    X_processed = preprocessor.transform(X)

    predictions = np.maximum(np.expm1(model.predict(X_processed)), 0)

    output_df = pd.DataFrame({
        "row_id": range(len(df)),
        "predicted_claim_cost": predictions,
    })

    os.makedirs(
        "outputs/pricing",
        exist_ok=True,
    )

    output_df.to_csv(
        "outputs/pricing/predicted_claim_cost.csv",
        index=False,
    )

    print("Claim cost predictions saved.")

    print(output_df["predicted_claim_cost"].describe())

    return output_df


if __name__ == "__main__":
    predict_claim_cost()
