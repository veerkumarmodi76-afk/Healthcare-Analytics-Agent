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

OUTPUT_DIR = Path("outputs/preprocessing")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = OUTPUT_DIR / "data_quality_report.csv"

# =====================================================
# Configuration
# =====================================================

NEGATIVE_CHECK_COLUMNS = [
    "age",
    "premium",
    "cost_claims_year",
    "exposure_time",
]

HIGH_MISSING_THRESHOLD = 50.0

# =====================================================
# Dataset Overview
# =====================================================


def get_dataset_overview(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate dataset-level summary metrics.
    """

    memory_mb = round(df.memory_usage(deep=True).sum() / (1024**2), 2)

    return pd.DataFrame({
        "metric": ["rows", "columns", "memory_usage_mb"],
        "value": [len(df), len(df.columns), memory_mb],
    })


# =====================================================
# Missing Values Report
# =====================================================


def get_missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Missing values by column.
    """

    return pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_pct": (df.isna().mean() * 100).round(2).values,
    })


# =====================================================
# High Missing Columns Report
# =====================================================


def get_high_missing_report(
    df: pd.DataFrame, threshold: float = HIGH_MISSING_THRESHOLD
) -> pd.DataFrame:
    """
    Flag columns exceeding missing threshold.
    """

    missing_pct = (df.isna().mean() * 100).round(2)

    report = pd.DataFrame({
        "column": missing_pct.index,
        "missing_pct": missing_pct.values,
    })

    report["high_missing_flag"] = report["missing_pct"] > threshold

    return report


# =====================================================
# Duplicate Report
# =====================================================


def get_duplicate_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Duplicate row summary.
    """

    duplicate_count = int(df.duplicated().sum())

    duplicate_pct = round(duplicate_count / len(df) * 100, 2)

    return pd.DataFrame({
        "metric": ["duplicate_rows", "duplicate_pct"],
        "value": [duplicate_count, duplicate_pct],
    })


# =====================================================
# Datatype Report
# =====================================================


def get_dtype_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Column datatype summary.
    """

    return pd.DataFrame({
        "column": df.columns,
        "dtype": [str(dtype) for dtype in df.dtypes],
    })


# =====================================================
# Outlier Report (IQR)
# =====================================================


def get_outlier_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect outliers using IQR method.
    """

    numeric_cols = df.select_dtypes(include=np.number).columns

    results = []

    for col in numeric_cols:
        series = df[col].dropna()

        if len(series) == 0:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        outlier_count = ((series < lower) | (series > upper)).sum()

        outlier_pct = round(outlier_count / len(series) * 100, 2)

        results.append({
            "column": col,
            "outlier_count": int(outlier_count),
            "outlier_pct": outlier_pct,
        })

    return pd.DataFrame(results)


# =====================================================
# Negative Value Report
# =====================================================


def get_negative_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect invalid negative values.
    """

    results = []

    for col in NEGATIVE_CHECK_COLUMNS:
        if col not in df.columns:
            continue

        negative_count = int((df[col] < 0).sum())

        negative_pct = round(negative_count / len(df) * 100, 2)

        results.append({
            "column": col,
            "negative_count": negative_count,
            "negative_pct": negative_pct,
        })

    return pd.DataFrame(results)


# =====================================================
# Constant Column Report
# =====================================================


def get_constant_column_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect columns with only one unique value.
    """

    results = []

    for col in df.columns:
        unique_values = df[col].nunique(dropna=False)

        results.append({
            "column": col,
            "unique_values": unique_values,
            "is_constant": unique_values == 1,
        })

    return pd.DataFrame(results)


# =====================================================
# Main Quality Runner
# =====================================================


def run_data_quality_checks(df: pd.DataFrame) -> dict:
    """
    Run all quality checks and export report.

    Output:
    outputs/preprocessing/data_quality_report.csv
    """

    logging.info("Running data quality checks...")

    # ------------------------------------------
    # Generate Reports
    # ------------------------------------------

    overview = get_dataset_overview(df)

    missing = get_missing_report(df)

    high_missing = get_high_missing_report(df)

    duplicates = get_duplicate_report(df)

    dtypes = get_dtype_report(df)

    outliers = get_outlier_report(df)

    negative_values = get_negative_value_report(df)

    constant_columns = get_constant_column_report(df)

    # ------------------------------------------
    # Export Consolidated Report
    # ------------------------------------------

    sections = []

    sections.append(pd.DataFrame({"section": ["DATASET_OVERVIEW"]}))
    sections.append(overview)

    sections.append(pd.DataFrame({"section": ["MISSING_VALUES"]}))
    sections.append(missing)

    sections.append(pd.DataFrame({"section": ["HIGH_MISSING_COLUMNS"]}))
    sections.append(high_missing)

    sections.append(pd.DataFrame({"section": ["DUPLICATES"]}))
    sections.append(duplicates)

    sections.append(pd.DataFrame({"section": ["DATATYPES"]}))
    sections.append(dtypes)

    sections.append(pd.DataFrame({"section": ["OUTLIERS"]}))
    sections.append(outliers)

    sections.append(pd.DataFrame({"section": ["NEGATIVE_VALUES"]}))
    sections.append(negative_values)

    sections.append(pd.DataFrame({"section": ["CONSTANT_COLUMNS"]}))
    sections.append(constant_columns)

    report = pd.concat(sections, ignore_index=True)

    report.to_csv(REPORT_FILE, index=False)

    logging.info(f"Quality report saved to: {REPORT_FILE}")

    # ------------------------------------------
    # Dashboard Warnings
    # ------------------------------------------

    high_missing_cols = high_missing[high_missing["high_missing_flag"]]

    if len(high_missing_cols) > 0:
        logging.warning(
            f"{len(high_missing_cols)} columns "
            f"have > {HIGH_MISSING_THRESHOLD}% missing values"
        )

    constant_cols = constant_columns[constant_columns["is_constant"]]

    if len(constant_cols) > 0:
        logging.warning(f"{len(constant_cols)} constant columns detected")

    # ------------------------------------------
    # Return Results
    # ------------------------------------------

    return {
        "overview": overview,
        "missing": missing,
        "high_missing": high_missing,
        "duplicates": duplicates,
        "dtypes": dtypes,
        "outliers": outliers,
        "negative_values": negative_values,
        "constant_columns": constant_columns,
    }


# =====================================================
# Test Run
# =====================================================

if __name__ == "__main__":
    sample_df = pd.DataFrame({
        "age": [20, 25, -5, 999],
        "premium": [1000, None, -500, 50000],
        "cost_claims_year": [100, 200, -50, 100000],
        "gender": ["M", None, "F", "M"],
        "constant_col": [1, 1, 1, 1],
    })

    results = run_data_quality_checks(sample_df)

    print("\nDataset Overview")
    print(results["overview"])

    print("\nMissing Values")
    print(results["missing"])

    print("\nOutliers")
    print(results["outliers"])
