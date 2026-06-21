import joblib
import pandas as pd


def predict_lapse():

    payload = joblib.load("models/lapse/lapse_model.pkl")

    model = payload["model"]

    preprocessor = payload["preprocessor"]

    categorical_features = payload["categorical_features"]

    numeric_features = payload["numeric_features"]

    df = pd.read_csv("data/processed/processed_data.csv")

    X = df[categorical_features + numeric_features]

    X_processed = preprocessor.transform(X)

    lapse_probability = model.predict_proba(X_processed)[:, 1]

    output_df = pd.DataFrame({
        "row_id": range(len(df)),
        "lapse_probability": lapse_probability,
    })

    output_df.to_csv(
        "outputs/lapse/lapse_predictions.csv",
        index=False,
    )

    print("Lapse predictions saved.")

    return output_df


if __name__ == "__main__":
    predict_lapse()
