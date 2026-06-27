from pathlib import Path
import pandas as pd
import logging
from typing import Dict, Tuple
from ..config.logging_config import get_logger

# =====================================================
# Configuration
# =====================================================

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

BASE_DIR = Path.cwd()
DATA_PATH = BASE_DIR / "data" / "raw" / "raw_data.csv"

# Minimum columns required for AI-AIP pipeline
REQUIRED_COLUMNS = [
    "ID_policy",
    "ID_insured",
    "age",
    "premium",
    "exposure_time",
    "period",
    "cost_claims_year",
]

# =====================================================
# File Loaders
# =====================================================


def load_csv(path: Path) -> pd.DataFrame:
    """Load CSV file."""
    logging.info(f"Loading CSV: {path}")
    return pd.read_csv(path)


def load_excel(path: Path) -> pd.DataFrame:
    """Load Excel file."""
    logging.info(f"Loading Excel: {path}")
    return pd.read_excel(path)


# =====================================================
# Validation
# =====================================================


def validate_schema(df: pd.DataFrame) -> None:
    """
    Validate dataset schema.

    Raises
    ------
    ValueError
        If required columns are missing.
    """
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_cols:
        raise ValueError(
            f"Dataset validation failed.\n"
            f"Missing required columns: {sorted(missing_cols)}"
        )

    logging.info("Schema validation passed.")


# =====================================================
# Metadata
# =====================================================


def get_dataset_summary(df: pd.DataFrame) -> Dict:
    """
    Generate dataset metadata for upload center/dashboard.

    Returns
    -------
    dict
    """
    memory_mb = round(df.memory_usage(deep=True).sum() / (1024**2), 2)

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "memory_usage_mb": memory_mb,
        "column_names": list(df.columns),
    }


# =====================================================
# Main Loader
# =====================================================


def load_dataset(
    input_path: Path | str,
    validate: bool = True,
    return_summary: bool = False,
) -> pd.DataFrame | Tuple[pd.DataFrame, Dict]:
    """
    Load dataset from CSV or Excel.

    Parameters
    ----------
    input_path : str | Path
        Dataset path.
    validate : bool
        Run schema validation.
    return_summary : bool
        Return metadata dictionary.

    Returns
    -------
    DataFrame
        Loaded dataset

    OR

    (DataFrame, Dict)
        Dataset and summary metadata
    """

    input_path = Path(input_path)

    logging.info("Loading dataset...")
    logging.info(f"Resolved path: {input_path}")

    if not input_path.exists():
        raise FileNotFoundError(f"Data file not found at {input_path}")

    suffix = input_path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(input_path)

    elif suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(input_path)

    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    logging.info(f"Dataset shape: {df.shape}")

    if validate:
        validate_schema(df)

    summary = get_dataset_summary(df)

    logging.info(
        f"Rows={summary['rows']} | "
        f"Columns={summary['columns']} | "
        f"Memory={summary['memory_usage_mb']} MB"
    )

    if return_summary:
        return df, summary

    return df


# =====================================================
# Test Run
# =====================================================

if __name__ == "__main__":
    try:
        df, summary = load_dataset(input_path=DATA_PATH, return_summary=True)

        print("\nDATASET SUMMARY")
        print("-" * 40)

        for key, value in summary.items():
            print(f"{key}: {value}")

    except Exception as e:
        logging.error(str(e))
