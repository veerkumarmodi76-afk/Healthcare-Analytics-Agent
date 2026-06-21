import os
import numpy as np
import pandas as pd


LOADINGS = {
    "Low": 1.15,
    "Medium": 1.25,
    "High": 1.45,
    "VeryHigh": 1.65,
}


def generate_premium_quotes():

    print("Loading pricing predictions...")

    claims_df = pd.read_csv("outputs/pricing/predicted_claim_cost.csv")

    print("Loading underwriting predictions...")

    risk_df = pd.read_csv("outputs/underwriting/applicant_risk_scores.csv")

    # Safety check
    if len(claims_df) != len(risk_df):
        raise ValueError(
            f"Row mismatch: pricing={len(claims_df):,}, underwriting={len(risk_df):,}"
        )

    print(f"Rows verified: {len(claims_df):,}")

    # Since both outputs were generated from the same
    # processed dataset and preserve row order,
    # we can directly align rows without merging.

    premium_df = claims_df.copy()

    premium_df["risk_class_label"] = risk_df["risk_class_label"].values

    premium_df["risk_score"] = risk_df["risk_score"].values

    premium_df["underwriting_flag"] = risk_df["underwriting_flag"].values

    premium_df["loading_factor"] = premium_df["risk_class_label"].map(LOADINGS)

    premium_df["recommended_premium"] = (
        premium_df["predicted_claim_cost"] * premium_df["loading_factor"]
    )

    # Safety floor
    premium_df["recommended_premium"] = np.maximum(
        premium_df["recommended_premium"],
        premium_df["predicted_claim_cost"] * 1.10,
    )

    premium_df["recommended_premium"] = np.maximum(premium_df["recommended_premium"], 0)

    os.makedirs(
        "outputs/pricing",
        exist_ok=True,
    )

    output_file = "outputs/pricing/premium_quotes.csv"

    premium_df.to_csv(
        output_file,
        index=False,
    )

    print("\nPremium quotes generated successfully")
    print(f"Saved: {output_file}")

    print("\nRisk Class Distribution:")
    print(premium_df["risk_class_label"].value_counts())

    print("\nPremium Summary:")
    print(
        premium_df[
            [
                "predicted_claim_cost",
                "recommended_premium",
            ]
        ].describe()
    )

    return premium_df


if __name__ == "__main__":
    generate_premium_quotes()
