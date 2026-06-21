import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def create_risk_classes(df):

    risk_features = ["loss_ratio", "claim_frequency", "age"]

    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(df[risk_features])

    scaled_df = pd.DataFrame(scaled, columns=risk_features)

    df["risk_score"] = (
        0.50 * scaled_df["loss_ratio"]
        + 0.30 * scaled_df["claim_frequency"]
        + 0.20 * scaled_df["age"]
    )

    df["risk_class"] = pd.qcut(
        df["risk_score"], q=4, labels=["Low", "Medium", "High", "VeryHigh"]
    )

    df["risk_class_encoded"] = (
        df["risk_class"]
        .astype(str)
        .map({
            "Low": 0,
            "Medium": 1,
            "High": 2,
            "VeryHigh": 3,
        })
    )

    return df
