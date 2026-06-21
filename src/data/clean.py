import pandas as pd


def clean_data(df):

    date_cols = [
        "date_effect_insured",
        "date_lapse_insured",
        "date_effect_policy",
        "date_lapse_policy",
    ]

    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df["insured_lapsed_flag"] = df["date_lapse_insured"].notna().astype(int)

    df["policy_lapsed_flag"] = df["date_lapse_policy"].notna().astype(int)

    num_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    cat_cols = df.select_dtypes(include=["object"]).columns

    for col in cat_cols:
        df[col] = df[col].fillna("Unknown")

    return df
