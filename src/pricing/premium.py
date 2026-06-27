import os
import json
import logging
from datetime import datetime

import numpy as np
import pandas as pd


# =============================================================================
# CONFIGURATION
# =============================================================================

MODEL_VERSION = "2.0.0"

PREDICTION_PATH = "outputs/pricing/predicted_claim_cost.csv"
UNDERWRITING_PATH = "outputs/underwriting/underwriting_predictions.csv"

OUTPUT_DIR = "outputs/pricing"
LOG_DIR = "outputs/logs"

OUTPUT_CSV = os.path.join(OUTPUT_DIR, "premium_quotes.csv")
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "premium_summary.json")
METADATA_PATH = os.path.join(OUTPUT_DIR, "premium_metadata.json")

LOG_FILE = os.path.join(LOG_DIR, "pricing.log")


# =============================================================================
# BUSINESS PARAMETERS
# =============================================================================

LOADING_FACTORS = {
    "Low": 1.15,
    "Medium": 1.25,
    "High": 1.45,
    "VeryHigh": 1.65,
}

FIXED_EXPENSE = 100.0

VARIABLE_EXPENSE_RATE = 0.08

PROFIT_MARGIN_RATE = 0.10

MINIMUM_LOADING = 1.10

MINIMUM_PREMIUM = 500.0


# =============================================================================
# REQUIRED COLUMNS
# =============================================================================

PRICING_COLUMNS = [
    "predicted_claim_cost",
]

UNDERWRITING_COLUMNS = [
    "risk_class_label",
    "risk_score",
    "underwriting_flag",
]


# =============================================================================
# CREATE OUTPUT DIRECTORIES
# =============================================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger("premium_generation")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler(LOG_FILE)

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


# =============================================================================
# VALIDATION HELPERS
# =============================================================================


def validate_columns(df: pd.DataFrame, required_columns: list, name: str):
    """
    Ensure required columns exist.
    """

    missing = [c for c in required_columns if c not in df.columns]

    if missing:
        raise ValueError(f"{name} missing required columns: {missing}")


def validate_no_missing(df: pd.DataFrame, columns: list, name: str):
    """
    Ensure important columns have no null values.
    """

    for column in columns:
        if df[column].isna().any():
            count = df[column].isna().sum()

            raise ValueError(
                f"{name}: Column '{column}' contains {count} missing values."
            )


def validate_positive_claim_cost(df: pd.DataFrame):
    """
    Claim cost should never be negative.
    """

    if (df["predicted_claim_cost"] < 0).any():
        raise ValueError("Negative predicted claim costs detected.")


def validate_row_alignment(
    pricing_df: pd.DataFrame,
    underwriting_df: pd.DataFrame,
):
    """
    Verify both files represent exactly the same observations.
    """

    if len(pricing_df) != len(underwriting_df):
        raise ValueError(
            f"Row mismatch: "
            f"Pricing={len(pricing_df):,}, "
            f"Underwriting={len(underwriting_df):,}"
        )

    logger.info("Row count validation passed.")


def validate_row_identifier(
    pricing_df: pd.DataFrame,
    underwriting_df: pd.DataFrame,
):
    """
    If row_id exists in both files,
    verify ordering before merging.
    """

    if "row_id" in pricing_df.columns and "row_id" in underwriting_df.columns:
        if not pricing_df["row_id"].equals(underwriting_df["row_id"]):
            raise ValueError(
                "row_id mismatch between pricing and underwriting outputs."
            )

        logger.info("row_id validation passed.")


# =============================================================================
# DATA LOADING
# =============================================================================


def load_claim_predictions() -> pd.DataFrame:
    """
    Load pricing model predictions.
    """

    logger.info("Loading pricing prediction file.")

    if not os.path.exists(PREDICTION_PATH):
        raise FileNotFoundError(PREDICTION_PATH)

    df = pd.read_csv(PREDICTION_PATH)

    validate_columns(
        df,
        PRICING_COLUMNS,
        "Pricing predictions",
    )

    validate_no_missing(
        df,
        PRICING_COLUMNS,
        "Pricing predictions",
    )

    validate_positive_claim_cost(df)

    logger.info(
        "Pricing predictions loaded successfully (%d rows).",
        len(df),
    )

    return df


def load_underwriting_predictions() -> pd.DataFrame:
    """
    Load underwriting predictions.
    """

    logger.info("Loading underwriting predictions.")

    if not os.path.exists(UNDERWRITING_PATH):
        raise FileNotFoundError(UNDERWRITING_PATH)

    df = pd.read_csv(UNDERWRITING_PATH)

    validate_columns(
        df,
        UNDERWRITING_COLUMNS,
        "Underwriting predictions",
    )

    validate_no_missing(
        df,
        UNDERWRITING_COLUMNS,
        "Underwriting predictions",
    )

    logger.info(
        "Underwriting predictions loaded successfully (%d rows).",
        len(df),
    )

    return df


# =============================================================================
# MERGING
# =============================================================================


def merge_predictions(
    pricing_df: pd.DataFrame,
    underwriting_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine pricing and underwriting outputs.

    Uses row_id if available.
    Otherwise falls back to validated row order.
    """

    validate_row_alignment(
        pricing_df,
        underwriting_df,
    )

    validate_row_identifier(
        pricing_df,
        underwriting_df,
    )

    if "row_id" in pricing_df.columns and "row_id" in underwriting_df.columns:
        merged = pd.merge(
            pricing_df,
            underwriting_df[
                [
                    "row_id",
                    "risk_class_label",
                    "risk_score",
                    "underwriting_flag",
                ]
            ],
            on="row_id",
            how="inner",
            validate="one_to_one",
        )

        logger.info("Merged using row_id.")

    else:
        logger.warning("row_id not found. Using validated row order.")

        merged = pricing_df.copy()

        merged["risk_class_label"] = underwriting_df["risk_class_label"].values

        merged["risk_score"] = underwriting_df["risk_score"].values

        merged["underwriting_flag"] = underwriting_df["underwriting_flag"].values

    logger.info(
        "Merged dataframe created successfully (%d rows).",
        len(merged),
    )

    return merged


# =============================================================================
# PREMIUM HELPER FUNCTIONS
# =============================================================================


def calculate_loading_factor(risk_class: str) -> float:
    """
    Return loading factor based on underwriting risk class.
    """

    return LOADING_FACTORS.get(
        risk_class,
        MINIMUM_LOADING,
    )


def calculate_pure_premium(predicted_claim: float) -> float:
    """
    Pure premium equals expected claim cost.
    """

    return float(predicted_claim)


def calculate_expense_loading(
    predicted_claim: float,
) -> float:
    """
    Expense loading consists of
    fixed expense +
    variable percentage of claim cost.
    """

    return FIXED_EXPENSE + predicted_claim * VARIABLE_EXPENSE_RATE


def calculate_profit_margin(
    predicted_claim: float,
) -> float:
    """
    Target insurer profit.
    """

    return predicted_claim * PROFIT_MARGIN_RATE


# =============================================================================
# BUSINESS RULES
# =============================================================================


def apply_business_rules(premium_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply actuarial and business validation rules to the premium table.
    """

    logger.info("Applying business rules...")

    # -------------------------------------------------------------------------
    # Replace infinite values
    # -------------------------------------------------------------------------

    premium_df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True,
    )

    # -------------------------------------------------------------------------
    # Missing premium check
    # -------------------------------------------------------------------------

    if premium_df["recommended_premium"].isna().any():
        count = premium_df["recommended_premium"].isna().sum()

        logger.warning(
            "%d missing premium values found. Replacing with minimum premium.",
            count,
        )

        premium_df["recommended_premium"] = premium_df["recommended_premium"].fillna(
            MINIMUM_PREMIUM
        )

    # -------------------------------------------------------------------------
    # Premium should never be negative
    # -------------------------------------------------------------------------

    premium_df["recommended_premium"] = np.maximum(
        premium_df["recommended_premium"],
        0,
    )

    # -------------------------------------------------------------------------
    # Premium should be at least claim cost × minimum loading
    # -------------------------------------------------------------------------

    minimum_allowed = premium_df["predicted_claim_cost"] * MINIMUM_LOADING

    premium_df["recommended_premium"] = np.maximum(
        premium_df["recommended_premium"],
        minimum_allowed,
    )

    # -------------------------------------------------------------------------
    # Minimum premium floor
    # -------------------------------------------------------------------------

    premium_df["recommended_premium"] = np.maximum(
        premium_df["recommended_premium"],
        MINIMUM_PREMIUM,
    )

    logger.info("Business rules completed.")

    return premium_df


# =============================================================================
# PREMIUM ENGINE
# =============================================================================


def generate_premium_quotes(
    premium_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate all premium components.
    """

    logger.info("Generating premium quotes...")

    # -------------------------------------------------------------------------
    # Loading factor
    # -------------------------------------------------------------------------

    premium_df["loading_factor"] = premium_df["risk_class_label"].apply(
        calculate_loading_factor
    )

    # -------------------------------------------------------------------------
    # Pure premium
    # -------------------------------------------------------------------------

    premium_df["pure_premium"] = premium_df["predicted_claim_cost"].apply(
        calculate_pure_premium
    )

    # -------------------------------------------------------------------------
    # Risk premium
    # -------------------------------------------------------------------------

    premium_df["risk_premium"] = (
        premium_df["pure_premium"] * premium_df["loading_factor"]
    )

    # -------------------------------------------------------------------------
    # Expense loading
    # -------------------------------------------------------------------------

    premium_df["expense_loading"] = premium_df["pure_premium"].apply(
        calculate_expense_loading
    )

    # -------------------------------------------------------------------------
    # Profit margin
    # -------------------------------------------------------------------------

    premium_df["profit_margin"] = premium_df["pure_premium"].apply(
        calculate_profit_margin
    )

    # -------------------------------------------------------------------------
    # Final Premium
    # -------------------------------------------------------------------------

    premium_df["recommended_premium"] = (
        premium_df["risk_premium"]
        + premium_df["expense_loading"]
        + premium_df["profit_margin"]
    )

    # -------------------------------------------------------------------------
    # Round values
    # -------------------------------------------------------------------------

    numeric_columns = [
        "predicted_claim_cost",
        "pure_premium",
        "risk_premium",
        "expense_loading",
        "profit_margin",
        "recommended_premium",
    ]

    premium_df[numeric_columns] = premium_df[numeric_columns].round(2)

    premium_df = apply_business_rules(premium_df)

    logger.info("Premium calculation completed.")

    return premium_df


# =============================================================================
# SUMMARY
# =============================================================================


def generate_summary(
    premium_df: pd.DataFrame,
) -> dict:
    """
    Generate portfolio pricing summary.
    """

    logger.info("Generating premium summary...")

    summary = {
        "generated_at": datetime.now().isoformat(),
        "model_version": MODEL_VERSION,
        "rows": int(len(premium_df)),
        "average_claim_cost": round(
            premium_df["predicted_claim_cost"].mean(),
            2,
        ),
        "minimum_claim_cost": round(
            premium_df["predicted_claim_cost"].min(),
            2,
        ),
        "maximum_claim_cost": round(
            premium_df["predicted_claim_cost"].max(),
            2,
        ),
        "average_premium": round(
            premium_df["recommended_premium"].mean(),
            2,
        ),
        "minimum_premium": round(
            premium_df["recommended_premium"].min(),
            2,
        ),
        "maximum_premium": round(
            premium_df["recommended_premium"].max(),
            2,
        ),
        "average_loading_factor": round(
            premium_df["loading_factor"].mean(),
            3,
        ),
        "average_profit_margin": round(
            premium_df["profit_margin"].mean(),
            2,
        ),
        "average_expense_loading": round(
            premium_df["expense_loading"].mean(),
            2,
        ),
        "total_expected_claims": round(
            premium_df["predicted_claim_cost"].sum(),
            2,
        ),
        "total_portfolio_premium": round(
            premium_df["recommended_premium"].sum(),
            2,
        ),
        "total_profit_margin": round(
            premium_df["profit_margin"].sum(),
            2,
        ),
        "risk_distribution": premium_df["risk_class_label"].value_counts().to_dict(),
        "underwriting_distribution": premium_df["underwriting_flag"]
        .value_counts()
        .to_dict(),
    }

    logger.info("Premium summary generated.")

    return summary


# =============================================================================
# METADATA
# =============================================================================


def generate_metadata(
    premium_df: pd.DataFrame,
) -> dict:
    """
    Generate metadata describing the pricing run.
    """

    logger.info("Generating metadata...")

    metadata = {
        "model_name": "Healthcare Pricing Engine",
        "model_version": MODEL_VERSION,
        "generated_at": datetime.now().isoformat(),
        "algorithm": "Expected Claim Cost + Risk Loading + Expense Loading + Profit Margin",
        "pricing_formula": (
            "Recommended Premium = "
            "(Pure Premium × Loading Factor) "
            "+ Expense Loading "
            "+ Profit Margin"
        ),
        "rows_processed": int(len(premium_df)),
        "risk_classes": list(LOADING_FACTORS.keys()),
        "loading_factors": LOADING_FACTORS,
        "fixed_expense": FIXED_EXPENSE,
        "variable_expense_rate": VARIABLE_EXPENSE_RATE,
        "profit_margin_rate": PROFIT_MARGIN_RATE,
        "minimum_loading": MINIMUM_LOADING,
        "minimum_premium": MINIMUM_PREMIUM,
        "output_columns": premium_df.columns.tolist(),
    }

    logger.info("Metadata generated.")

    return metadata


# =============================================================================
# SAVE OUTPUTS
# =============================================================================


def save_outputs(
    premium_df: pd.DataFrame,
    summary: dict,
    metadata: dict,
) -> None:
    """
    Save all pricing outputs.
    """

    logger.info("Saving pricing outputs...")

    premium_df.to_csv(
        OUTPUT_CSV,
        index=False,
    )

    with open(
        SUMMARY_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            summary,
            f,
            indent=4,
        )

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            metadata,
            f,
            indent=4,
        )

    logger.info("Pricing outputs saved successfully.")


# =============================================================================
# MAIN PIPELINE
# =============================================================================


def main() -> pd.DataFrame:
    """
    Execute the complete premium generation pipeline.

    Returns
    -------
    pd.DataFrame
        Premium quotation dataframe.
    """

    logger.info("=" * 70)
    logger.info("PREMIUM GENERATION PIPELINE")
    logger.info("=" * 70)

    pricing_df = load_claim_predictions()

    underwriting_df = load_underwriting_predictions()

    premium_df = merge_predictions(
        pricing_df,
        underwriting_df,
    )

    premium_df = generate_premium_quotes(
        premium_df,
    )

    summary = generate_summary(
        premium_df,
    )

    metadata = generate_metadata(
        premium_df,
    )

    save_outputs(
        premium_df,
        summary,
        metadata,
    )

    logger.info("")
    logger.info("Portfolio Summary")
    logger.info("-----------------------------")
    logger.info(
        "Policies Processed : %d",
        len(premium_df),
    )
    logger.info(
        "Average Premium    : %.2f",
        premium_df["recommended_premium"].mean(),
    )
    logger.info(
        "Minimum Premium    : %.2f",
        premium_df["recommended_premium"].min(),
    )
    logger.info(
        "Maximum Premium    : %.2f",
        premium_df["recommended_premium"].max(),
    )
    logger.info(
        "Total Premium      : %.2f",
        premium_df["recommended_premium"].sum(),
    )

    logger.info("")
    logger.info("Outputs Generated")
    logger.info("-----------------------------")
    logger.info("[OK] %s", OUTPUT_CSV)
    logger.info("[OK] %s", SUMMARY_PATH)
    logger.info("[OK] %s", METADATA_PATH)

    logger.info("")
    logger.info("Premium generation completed successfully.")

    return premium_df


# =============================================================================
# ENTRY POINT
# =============================================================================


if __name__ == "__main__":
    try:
        main()

    except Exception:
        logger.exception("Premium generation failed.")

        raise
