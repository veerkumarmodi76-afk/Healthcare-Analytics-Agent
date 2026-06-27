import os
import json
import logging
from datetime import datetime

import pandas as pd

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = "outputs/pricing"

LOG_DIR = "outputs/logs"

REPORT_MD = os.path.join(
    OUTPUT_DIR,
    "pricing_report.md",
)

REPORT_JSON = os.path.join(
    OUTPUT_DIR,
    "pricing_report.json",
)

METRICS_PATH = os.path.join(
    OUTPUT_DIR,
    "metrics.json",
)

PREDICTION_SUMMARY_PATH = os.path.join(
    OUTPUT_DIR,
    "prediction_summary.json",
)

PREMIUM_SUMMARY_PATH = os.path.join(
    OUTPUT_DIR,
    "premium_summary.json",
)

PREMIUM_METADATA_PATH = os.path.join(
    OUTPUT_DIR,
    "premium_metadata.json",
)

FEATURE_IMPORTANCE_PATH = os.path.join(
    OUTPUT_DIR,
    "feature_importance.csv",
)

MODEL_VERSION = "2.0.0"

# =============================================================================
# LOGGER
# =============================================================================

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("pricing_report")

logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    handler = logging.FileHandler(
        os.path.join(
            LOG_DIR,
            "pricing.log",
        )
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

# =============================================================================
# VALIDATION
# =============================================================================


def validate_required_files():
    """
    Ensure all required pricing outputs exist.
    """

    required = [
        METRICS_PATH,
        PREDICTION_SUMMARY_PATH,
        PREMIUM_SUMMARY_PATH,
        PREMIUM_METADATA_PATH,
        FEATURE_IMPORTANCE_PATH,
    ]

    missing = [file for file in required if not os.path.exists(file)]

    if missing:
        raise FileNotFoundError(f"Missing required files:\n{missing}")

    logger.info("All required report files found.")


# =============================================================================
# LOADERS
# =============================================================================


def load_json(path):
    """
    Load JSON file.
    """

    logger.info(f"Loading {path}")

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def load_feature_importance():
    """
    Load feature importance CSV.
    """

    logger.info("Loading feature importance.")

    return pd.read_csv(FEATURE_IMPORTANCE_PATH)


# =============================================================================
# FEATURE IMPORTANCE
# =============================================================================


def get_top_features(
    importance_df,
    top_n=10,
):
    """
    Return top N important features.
    """

    importance_df = importance_df.sort_values(
        "importance",
        ascending=False,
    )

    return importance_df.head(top_n)


# =============================================================================
# LOAD ALL REPORT DATA
# =============================================================================


def load_all_data():
    """
    Load every pricing artifact.
    """

    validate_required_files()

    metrics = load_json(METRICS_PATH)

    prediction = load_json(PREDICTION_SUMMARY_PATH)

    premium = load_json(PREMIUM_SUMMARY_PATH)

    metadata = load_json(PREMIUM_METADATA_PATH)

    importance = load_feature_importance()

    logger.info("Pricing outputs loaded successfully.")

    return {
        "metrics": metrics,
        "prediction": prediction,
        "premium": premium,
        "metadata": metadata,
        "importance": importance,
    }


# =============================================================================
# MARKDOWN HELPERS
# =============================================================================


def write_header(lines):
    """
    Report title.
    """

    lines.append("# Pricing Department Report")

    lines.append("")

    lines.append(f"Generated : {datetime.now()}")

    lines.append(f"Version : {MODEL_VERSION}")

    lines.append("")

    lines.append("---")

    lines.append("")


def write_training_section(
    lines,
    metrics,
):
    """
    Training metrics.
    """

    lines.append("## Model Performance")

    lines.append("")

    lines.append(f"- MAE : {metrics['mae']:.2f}")

    lines.append(f"- RMSE : {metrics['rmse']:.2f}")

    lines.append(f"- R² : {metrics['r2']:.4f}")

    lines.append(f"- Training Rows : {metrics['training_rows']}")

    lines.append(f"- Testing Rows : {metrics['testing_rows']}")

    lines.append("")


def write_prediction_section(
    lines,
    prediction,
):
    """
    Prediction summary.
    """

    lines.append("## Prediction Summary")

    lines.append("")

    lines.append(f"- Rows Predicted : {prediction['rows_predicted']}")

    lines.append(f"- Average Claim Cost : {prediction['average_prediction']:.2f}")

    lines.append(f"- Minimum Claim Cost : {prediction['minimum_prediction']:.2f}")

    lines.append(f"- Maximum Claim Cost : {prediction['maximum_prediction']:.2f}")

    lines.append("")


# =============================================================================
# PREMIUM SUMMARY
# =============================================================================


def write_premium_section(
    lines,
    premium,
):
    """
    Premium portfolio summary.
    """

    lines.append("## Premium Summary")
    lines.append("")

    lines.append(f"- Average Premium : {premium['average_premium']:.2f}")

    lines.append(f"- Minimum Premium : {premium['minimum_premium']:.2f}")

    lines.append(f"- Maximum Premium : {premium['maximum_premium']:.2f}")

    lines.append(f"- Average Loading Factor : {premium['average_loading_factor']:.3f}")

    lines.append(
        f"- Average Expense Loading : {premium['average_expense_loading']:.2f}"
    )

    lines.append(f"- Average Profit Margin : {premium['average_profit_margin']:.2f}")

    lines.append(f"- Total Expected Claims : {premium['total_expected_claims']:.2f}")

    lines.append(
        f"- Total Portfolio Premium : {premium['total_portfolio_premium']:.2f}"
    )

    lines.append(f"- Total Profit Margin : {premium['total_profit_margin']:.2f}")

    lines.append("")


# =============================================================================
# FEATURE IMPORTANCE
# =============================================================================


def write_feature_importance_section(
    lines,
    importance_df,
):
    """
    Top pricing features.
    """

    lines.append("## Top Important Features")
    lines.append("")

    top_features = get_top_features(
        importance_df,
        top_n=10,
    )

    for _, row in top_features.iterrows():
        lines.append(f"- {row['feature']} : {row['importance']:.5f}")

    lines.append("")


# =============================================================================
# METADATA
# =============================================================================


def write_metadata_section(
    lines,
    metadata,
):
    """
    Model metadata.
    """

    lines.append("## Model Metadata")
    lines.append("")

    lines.append(f"- Model : {metadata['model_name']}")

    lines.append(f"- Version : {metadata['model_version']}")

    lines.append(f"- Generated : {metadata['generated_at']}")

    lines.append(f"- Rows Processed : {metadata['rows_processed']}")

    lines.append(f"- Algorithm : {metadata['algorithm']}")

    lines.append(f"- Pricing Formula : {metadata['pricing_formula']}")

    lines.append("")


# =============================================================================
# MARKDOWN REPORT
# =============================================================================


def generate_markdown_report(
    report_data,
):
    """
    Generate markdown report.
    """

    logger.info("Generating markdown report.")

    lines = []

    write_header(lines)

    write_training_section(
        lines,
        report_data["metrics"],
    )

    write_prediction_section(
        lines,
        report_data["prediction"],
    )

    write_premium_section(
        lines,
        report_data["premium"],
    )

    write_feature_importance_section(
        lines,
        report_data["importance"],
    )

    write_metadata_section(
        lines,
        report_data["metadata"],
    )

    with open(
        REPORT_MD,
        "w",
        encoding="utf-8",
    ) as f:
        f.write("\n".join(lines))

    logger.info("Markdown report saved.")


# =============================================================================
# JSON REPORT
# =============================================================================


def generate_json_report(
    report_data,
):
    """
    Generate dashboard-ready report.
    """

    logger.info("Generating JSON report.")

    report = {
        "generated_at": datetime.now().isoformat(),
        "version": MODEL_VERSION,
        "training": report_data["metrics"],
        "prediction": report_data["prediction"],
        "premium": report_data["premium"],
        "metadata": report_data["metadata"],
        "top_features": get_top_features(
            report_data["importance"],
            top_n=10,
        ).to_dict(orient="records"),
    }

    with open(
        REPORT_JSON,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            report,
            f,
            indent=4,
        )

    logger.info("JSON report saved.")


# =============================================================================
# MAIN
# =============================================================================


def main():
    """
    Execute pricing report generation.
    """

    logger.info("=" * 70)
    logger.info("PRICING REPORT GENERATION")
    logger.info("=" * 70)

    report_data = load_all_data()

    generate_markdown_report(
        report_data,
    )

    generate_json_report(
        report_data,
    )

    logger.info("")
    logger.info("Reports Generated")

    logger.info(
        "Markdown : %s",
        REPORT_MD,
    )

    logger.info(
        "JSON : %s",
        REPORT_JSON,
    )

    logger.info("")
    logger.info("Pricing report generation completed successfully.")

    print()

    print("=" * 70)
    print("PRICING REPORT COMPLETE")
    print("=" * 70)
    print(f"Markdown Report : {REPORT_MD}")
    print(f"JSON Report     : {REPORT_JSON}")
    print("=" * 70)


# =============================================================================
# ENTRY POINT
# =============================================================================


if __name__ == "__main__":
    try:
        main()

    except Exception:
        logger.exception("Pricing report generation failed.")

        raise
