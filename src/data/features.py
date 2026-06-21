import pandas as pd
import numpy as np


def create_features(df):

    df["insured_duration"] = df["period"] - df["year_effect_insured"]

    df["policy_duration"] = df["period"] - df["year_effect_policy"]

    df["family_size"] = df.groupby(["ID_policy", "period"])["ID_insured"].transform(
        "count"
    )

    df["claim_frequency"] = df["n_medical_services"] / (df["exposure_time"] + 0.01)

    df["claim_severity"] = np.where(
        df["n_medical_services"] > 0,
        df["cost_claims_year"] / df["n_medical_services"],
        0,
    )

    df["loss_ratio"] = np.where(
        df["premium"] > 0, df["cost_claims_year"] / df["premium"], 0
    )

    df["premium_per_exposure"] = df["premium"] / (df["exposure_time"] + 0.01)

    df["claims_per_exposure"] = df["cost_claims_year"] / (df["exposure_time"] + 0.01)

    df["age_band"] = pd.cut(
        df["age"],
        bins=[-1, 25, 35, 50, 65, 150],
        labels=["18-25", "26-35", "36-50", "51-65", "65+"],
    )

    df["seniority_band"] = pd.cut(
        df["seniority_insured"],
        bins=[-1, 2, 5, 10, 100],
        labels=["0-2", "3-5", "6-10", "10+"],
    )

    df["lapse_binary"] = df["lapse"].replace({1: 1, 2: 0, 3: 1})

    return df
