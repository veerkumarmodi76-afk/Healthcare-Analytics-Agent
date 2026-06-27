import pandas as pd
import logging
from ..config.logging_config import get_logger

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

# =====================================================
# Configuration
# =====================================================

# Categorical columns to standardize
CATEGORICAL_COLUMNS = [
    "gender",
    "type_policy",
    "type_policy_dg",
    "type_product",
    "distribution_channel",
]

# Columns that should never be negative
NON_NEGATIVE_COLUMNS = [
    "age",
    "premium",
    "cost_claims_year",
    "exposure_time",
]

# =====================================================
# Validation Helpers
# =====================================================


def validate_negative_values(df: pd.DataFrame) -> None:
    """
    Generate warnings for negative values
    in columns that should always be >= 0.
    """

    for col in NON_NEGATIVE_COLUMNS:
        if col not in df.columns:
            continue

        negative_count = (df[col] < 0).sum()

        if negative_count > 0:
            logging.warning(f"{negative_count} negative values detected in '{col}'")


def standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize categorical text values.

    Example:
    male -> Male
    MALE -> Male
    """

    for col in CATEGORICAL_COLUMNS:
        if col not in df.columns:
            continue

        df[col] = df[col].astype(str).str.strip().str.title()

    return df


# =====================================================
# Main Cleaning Function
# =====================================================


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning pipeline.

    Steps:
    1. Remove duplicates
    2. Parse date columns
    3. Impute missing numerical values
    4. Impute missing categorical values
    5. Standardize text fields
    6. Validate negative values

    Returns
    -------
    pd.DataFrame
    """

    logging.info("Starting data cleaning...")

    # -------------------------------------------------
    # Remove duplicate records
    # -------------------------------------------------

    before_rows = len(df)

    df = df.drop_duplicates()

    removed_rows = before_rows - len(df)

    logging.info(f"Removed {removed_rows} duplicate rows")

    # -------------------------------------------------
    # Date Parsing
    # -------------------------------------------------

    date_cols = [
        "date_effect_insured",
        "date_lapse_insured",
        "date_effect_policy",
        "date_lapse_policy",
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # -------------------------------------------------
    # Numerical Imputation
    # -------------------------------------------------

    num_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in num_cols:
        missing_count = df[col].isna().sum()

        if missing_count > 0:
            df[col] = df[col].fillna(df[col].median())

            logging.info(
                f"Imputed {missing_count} missing values in numerical column '{col}'"
            )

    # -------------------------------------------------
    # Categorical Imputation
    # -------------------------------------------------

    cat_cols = df.select_dtypes(include=["object"]).columns

    for col in cat_cols:
        missing_count = df[col].isna().sum()

        if missing_count > 0:
            df[col] = df[col].fillna("Unknown")

            logging.info(
                f"Imputed {missing_count} missing values in categorical column '{col}'"
            )

    # -------------------------------------------------
    # Text Standardization
    # -------------------------------------------------

    df = standardize_text(df)

    # -------------------------------------------------
    # Validation Checks
    # -------------------------------------------------

    validate_negative_values(df)

    logging.info(f"Cleaning completed. Final shape: {df.shape}")

    return df


# =====================================================
# Test Run
# =====================================================

if __name__ == "__main__":
    sample_data = pd.DataFrame({
        "gender": ["male", " MALE ", "Female"],
        "premium": [1000, -500, 1200],
        "age": [30, 40, -10],
    })

    cleaned_df = clean_data(sample_data)

    print(cleaned_df.head())
