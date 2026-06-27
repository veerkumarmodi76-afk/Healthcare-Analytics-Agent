from pathlib import Path
import pandas as pd
import numpy as np
import logging
from ..config.logging_config import get_logger

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

# =====================================================
# Output Configuration
# =====================================================

FEATURE_OUTPUT_DIR = Path("outputs/preprocessing")

FEATURE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_DICT_FILE = FEATURE_OUTPUT_DIR / "feature_dictionary.csv"

# =====================================================
# Feature Dictionary Export
# =====================================================


def export_feature_dictionary(df: pd.DataFrame, original_columns: set) -> None:
    """
    Export feature metadata for transparency.
    """

    feature_sources = []

    for col in df.columns:
        if col == "lapse_binary":
            source = "Target"

        elif col in original_columns:
            source = "Original"

        else:
            source = "Engineered"

        feature_sources.append(source)

    feature_dict = pd.DataFrame({
        "feature_name": df.columns,
        "feature_source": feature_sources,
        "dtype": [str(dtype) for dtype in df.dtypes],
        "missing_values": [df[col].isna().sum() for col in df.columns],
        "unique_values": [df[col].nunique(dropna=True) for col in df.columns],
    })

    feature_dict.to_csv(FEATURE_DICT_FILE, index=False)

    logging.info(f"Feature dictionary saved to: {FEATURE_DICT_FILE}")


# =====================================================
# Feature Engineering
# =====================================================


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature Engineering Pipeline

    Creates:
    - family_size
    - age_band
    - seniority_band
    - premium_per_exposure
    - claims_per_exposure
    - lapse_binary

    Exports:
    - feature_dictionary.csv
    """

    logging.info("Creating engineered features...")

    # -----------------------------------------
    # Track original columns
    # -----------------------------------------

    original_columns = set(df.columns)

    # -----------------------------------------
    # Exposure (temporary)
    # -----------------------------------------

    if "exposure_time" in df.columns:
        df["exposure"] = df["exposure_time"].replace(0, np.nan)

        logging.info(f"{df['exposure'].isna().sum()} zero exposures converted to NaN")

    # -----------------------------------------
    # Family Size
    # -----------------------------------------

    family_cols = ["ID_policy", "period", "ID_insured"]

    if all(col in df.columns for col in family_cols):
        df["family_size"] = df.groupby(["ID_policy", "period"])["ID_insured"].transform(
            "count"
        )

        df["family_size"] = df["family_size"].clip(lower=1)

    # -----------------------------------------
    # Age Bands
    # -----------------------------------------

    if "age" in df.columns:
        df["age_band"] = pd.cut(
            df["age"],
            bins=[-1, 25, 35, 50, 65, 150],
            labels=["18-25", "26-35", "36-50", "51-65", "65+"],
        )

    # -----------------------------------------
    # Seniority Bands
    # -----------------------------------------

    if "seniority_insured" in df.columns:
        df["seniority_band"] = pd.cut(
            df["seniority_insured"],
            bins=[-1, 2, 5, 10, 100],
            labels=["0-2", "3-5", "6-10", "10+"],
        )

    # -----------------------------------------
    # Premium Per Exposure
    # -----------------------------------------

    if "premium" in df.columns and "exposure" in df.columns:
        df["premium_per_exposure"] = df["premium"] / df["exposure"]

    # -----------------------------------------
    # Claims Per Exposure
    # -----------------------------------------

    if "cost_claims_year" in df.columns and "exposure" in df.columns:
        df["claims_per_exposure"] = df["cost_claims_year"] / df["exposure"]

    # -----------------------------------------
    # Claim Frequency
    # -----------------------------------------

    if (
        "n_medical_services" in df.columns
        and "exposure" in df.columns
    ):
        df["claim_frequency"] = (
            df["n_medical_services"]
            / df["exposure"]
        )

    # -----------------------------------------
    # Claim Severity
    # -----------------------------------------

    if (
        "cost_claims_year" in df.columns
        and "n_medical_services" in df.columns
    ):
        df["claim_severity"] = (
            df["cost_claims_year"]
            / df["n_medical_services"].replace(0, np.nan)
        )

    # -----------------------------------------
    # Loss Ratio
    # -----------------------------------------

    if (
        "cost_claims_year" in df.columns
        and "premium" in df.columns
    ):
        df["loss_ratio"] = (
            df["cost_claims_year"]
            / df["premium"].replace(0, np.nan)
        )

    # -----------------------------------------
    # Infinite Value Cleanup
    # -----------------------------------------

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # -----------------------------------------
    # Exposure Feature Cleanup
    # -----------------------------------------

    # -----------------------------------------
    # Feature Cleanup
    # -----------------------------------------

    exposure_features = [
        "premium_per_exposure",
        "claims_per_exposure",
        "claim_frequency",
        "claim_severity",
        "loss_ratio",
    ]

    for col in exposure_features:
        if col in df.columns:
            missing_before = df[col].isna().sum()

            df[col] = df[col].fillna(0)

            if missing_before > 0:
                logging.info(f"{col}: filled {missing_before} missing values with 0")

    # -----------------------------------------
    # Target Engineering
    # -----------------------------------------

    if "lapse" in df.columns:
        df["lapse_binary"] = df["lapse"].replace({1: 1, 2: 0, 3: 1})

    # -----------------------------------------
    # Remove Temporary Columns
    # -----------------------------------------

    if "exposure" in df.columns:
        df.drop(columns=["exposure"], inplace=True)

    # -----------------------------------------
    # Export Feature Dictionary
    # -----------------------------------------

    export_feature_dictionary(df, original_columns)

    logging.info(f"Feature engineering completed. Final shape: {df.shape}")

    return df


# =====================================================
# Test Run
# =====================================================

if __name__ == "__main__":
    sample_df = pd.DataFrame({
        "ID_policy": [1, 1, 2],
        "period": [1, 1, 1],
        "ID_insured": [101, 102, 103],
        "age": [24, 45, 70],
        "seniority_insured": [1, 6, 12],
        "premium": [1000, 1500, 2000],
        "cost_claims_year": [300, 400, 700],
        "exposure_time": [1.0, 2.0, 0],
        "lapse": [1, 2, 3],
    })

    engineered_df = create_features(sample_df)

    print(engineered_df.head())
