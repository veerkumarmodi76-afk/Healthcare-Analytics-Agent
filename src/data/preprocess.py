from pathlib import Path
import logging
import traceback

from .ingest import load_dataset
from .quality import run_data_quality_checks
from .clean import clean_data
from .features import create_features
from .risk import create_segments

from ..config.paths import Paths
from ..config.logging_config import get_logger

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / "pipeline_log.txt"

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# =====================================================
# Preprocessing Pipeline
# =====================================================


def run():
    """
    Complete AI-AIP preprocessing pipeline.

    Steps
    -----
    1. Load dataset
    2. Run data quality checks
    3. Clean dataset
    4. Create engineered features
    5. Create portfolio segments
    6. Save processed dataset

    Outputs
    -------
    data/processed/processed_data.csv

    outputs/
    ├── pipeline_log.txt
    └── preprocessing/
        ├── data_quality_report.csv
        ├── feature_dictionary.csv
        └── segmentation_summary.csv
    """

    try:
        logging.info("=" * 70)
        logging.info("AI-AIP PREPROCESSING PIPELINE STARTED")
        logging.info("=" * 70)

        # -------------------------------------------------
        # Load Dataset
        # -------------------------------------------------

        df, summary = load_dataset(
            input_path=Paths.RAW_DATA_FILE,
            return_summary=True,
        )

        logging.info(
            f"Dataset loaded successfully "
            f"({summary['rows']} rows, "
            f"{summary['columns']} columns)"
        )

        # -------------------------------------------------
        # Data Quality Checks
        # -------------------------------------------------

        quality_results = run_data_quality_checks(df)

        # -------------------------------------------------
        # Data Cleaning
        # -------------------------------------------------

        df = clean_data(df)

        logging.info(f"Dataset shape after cleaning: {df.shape}")

        # -------------------------------------------------
        # Feature Engineering
        # -------------------------------------------------

        df = create_features(df)

        logging.info(f"Dataset shape after feature engineering: {df.shape}")

        # -------------------------------------------------
        # Portfolio Segmentation
        # -------------------------------------------------

        logging.info("Creating portfolio segments...")

        df = create_segments(df)

        logging.info(f"Dataset shape after segmentation: {df.shape}")

        # -------------------------------------------------
        # Save Processed Dataset
        # -------------------------------------------------

        output_path = BASE_DIR / "data" / "processed" / "processed_data.csv"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)

        # -------------------------------------------------
        # Completion Log
        # -------------------------------------------------

        logging.info("=" * 70)
        logging.info("PIPELINE COMPLETED SUCCESSFULLY")
        logging.info(f"Final Dataset Shape: {df.shape}")
        logging.info(f"Processed Dataset Saved: {output_path}")
        logging.info(f"Pipeline Log Saved: {LOG_FILE}")
        logging.info("=" * 70)

        return df

    except Exception as e:
        logging.error("=" * 70)
        logging.error("PIPELINE FAILED")
        logging.error(str(e))
        logging.error(traceback.format_exc())
        logging.error("=" * 70)

        raise


def run_pipeline(
    input_path: Path | str,
    output_dir: Path | str | None = None,
):
    """
    Production preprocessing pipeline.
    """

    try:
        input_path = Path(input_path)

        if output_dir is None:
            output_dir = OUTPUT_DIR / "preprocessing"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        logging.info("=" * 70)
        logging.info("AI-AIP PREPROCESSING PIPELINE STARTED")
        logging.info("=" * 70)

        logging.info(f"Input Dataset : {input_path}")

        # -------------------------------
        # Load Dataset
        # -------------------------------

        df, summary = load_dataset(
            input_path=input_path,
            return_summary=True,
        )

        logging.info(
            f"Dataset loaded successfully "
            f"({summary['rows']} rows, "
            f"{summary['columns']} columns)"
        )

        # -------------------------------
        # Data Quality Checks
        # -------------------------------

        run_data_quality_checks(df)

        # -------------------------------
        # Cleaning
        # -------------------------------

        df = clean_data(df)

        # -------------------------------
        # Feature Engineering
        # -------------------------------

        df = create_features(df)

        # -------------------------------
        # Segmentation
        # -------------------------------

        df = create_segments(df)

        # -------------------------------
        # Save Processed Dataset
        # -------------------------------

        processed_dataset = BASE_DIR / "data" / "processed" / "processed_data.csv"

        processed_dataset.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(processed_dataset, index=False)

        logging.info(f"Processed dataset saved to {processed_dataset}")

        return df

    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())
        raise


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    run()
