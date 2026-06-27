"""
AI-AIP v2
Preprocessing Service

Acts as the interface between the dashboard and the preprocessing
department. The dashboard should interact ONLY with this service and
never call preprocessing scripts directly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from ..config.paths import Paths
from .base_Service import BaseService

# Department pipeline
from ..data.preprocess import run_pipeline


class PreprocessingService(BaseService):
    """
    Service wrapper around the preprocessing department.

    Responsibilities
    ----------------
    • Load datasets
    • Validate input files
    • Execute preprocessing pipeline
    • Expose processed data
    • Provide dashboard-friendly APIs
    """

    def __init__(self) -> None:
        super().__init__("preprocessing")

        self.raw_dataset: Optional[pd.DataFrame] = None
        self.processed_dataset: Optional[pd.DataFrame] = None

        self.processed_dataset_path = Paths.PROCESSED_DATA_DIR / "processed_data.csv"

        self.logger.info("PreprocessingService initialized.")

    # ==========================================================
    # Dataset Loading
    # ==========================================================

    def load_dataset(self, dataset_path: Path | str) -> pd.DataFrame:
        """
        Load CSV or Excel dataset.

        Parameters
        ----------
        dataset_path : Path | str

        Returns
        -------
        pd.DataFrame
        """

        dataset_path = Path(dataset_path)

        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        suffix = dataset_path.suffix.lower()

        self.logger.info(f"Loading dataset: {dataset_path}")

        if suffix == ".csv":
            df = pd.read_csv(dataset_path)

        elif suffix in [".xlsx", ".xls"]:
            df = pd.read_excel(dataset_path)

        else:
            raise ValueError(f"Unsupported file type: {suffix}")

        self.raw_dataset = df

        self.logger.info(
            f"Dataset loaded successfully ({len(df):,} rows, {len(df.columns)} columns)"
        )

        return df

    # ==========================================================
    # Validation
    # ==========================================================

    def validate_dataset(
        self,
        df: Optional[pd.DataFrame] = None,
    ) -> Dict[str, Any]:
        """
        Perform lightweight validation before preprocessing.
        """

        if df is None:
            df = self.raw_dataset

        if df is None:
            raise ValueError("No dataset loaded.")

        validation = {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "is_empty": df.empty,
            "valid": True,
        }

        if df.empty:
            validation["valid"] = False

        return validation

    # ==========================================================
    # Pipeline Execution
    # ==========================================================

    def run_pipeline(
        self,
        dataset_path: Optional[Path | str] = None,
    ) -> pd.DataFrame:
            """
            Execute the preprocessing department.

            Parameters
            ----------
            dataset_path : optional
                Path to the raw dataset. If omitted, the project's
                default raw dataset is used.

            Returns
            -------
            pd.DataFrame
                Processed dataset.
            """

            self.logger.info("Starting preprocessing pipeline...")

            # Use default dataset if none is supplied
            if dataset_path is None:
                dataset_path = Paths.RAW_DATA_FILE

            dataset_path = Path(dataset_path)

            self.load_dataset(dataset_path)

            run_pipeline(
                input_path=dataset_path,
                output_dir=Paths.PROCESSED_DATA_DIR,
            )

            if not self.processed_dataset_path.exists():
                raise FileNotFoundError(
                    "Processed dataset was not generated."
                )

            self.processed_dataset = pd.read_csv(
                self.processed_dataset_path
            )

            self.logger.info(
                "Preprocessing pipeline completed successfully."
            )

            return self.processed_dataset

    # ==========================================================
    # Dataset Access
    # ==========================================================

    def get_raw_dataset(self) -> Optional[pd.DataFrame]:
        """
        Return raw dataset.
        """
        return self.raw_dataset

    def get_processed_dataset(self) -> Optional[pd.DataFrame]:
        """
        Return processed dataset.
        """

        if self.processed_dataset is not None:
            return self.processed_dataset

        if self.processed_dataset_path.exists():
            self.processed_dataset = pd.read_csv(self.processed_dataset_path)

            return self.processed_dataset

        return None

    # ==========================================================
    # Dataset Information
    # ==========================================================

    def dataset_summary(
        self,
        processed: bool = True,
    ) -> Dict[str, Any]:
        """
        Basic dataset summary.
        """

        df = self.get_processed_dataset() if processed else self.raw_dataset

        if df is None:
            return {}

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_mb": round(
                df.memory_usage(deep=True).sum() / 1024**2,
                2,
            ),
            "missing_values": int(df.isna().sum().sum()),
            "duplicates": int(df.duplicated().sum()),
        }

    # ==========================================================
    # Status
    # ==========================================================

    def is_processed(self) -> bool:
        """
        Returns True if processed data exists.
        """

        return self.processed_dataset_path.exists()

    # ==========================================================
    # Reports
    # ==========================================================

    def get_quality_report(self) -> Optional[str]:
        """
        Return the data quality report as text.
        """

        report_path = Paths.OUTPUT_DIR / "preprocessing" / "quality_report.md"

        if not report_path.exists():
            self.logger.warning("Quality report not found.")
            return None

        return report_path.read_text(encoding="utf-8")

    def get_feature_dictionary(self) -> Optional[str]:
        """
        Return the feature dictionary.
        """

        dictionary_path = Paths.OUTPUT_DIR / "preprocessing" / "feature_dictionary.md"

        if not dictionary_path.exists():
            self.logger.warning("Feature dictionary not found.")
            return None

        return dictionary_path.read_text(encoding="utf-8")

    # ==========================================================
    # Pipeline Outputs
    # ==========================================================

    def get_pipeline_outputs(self) -> Dict[str, Any]:
        """
        Returns available preprocessing outputs.
        """

        output_dir = self.get_output_directory()

        outputs = {
            "processed_dataset": self.processed_dataset_path.exists(),
            "quality_report": False,
            "feature_dictionary": False,
            "files": self.list_outputs(),
        }

        quality = output_dir / "quality_report.md"
        feature = output_dir / "feature_dictionary.md"

        outputs["quality_report"] = quality.exists()
        outputs["feature_dictionary"] = feature.exists()

        return outputs

    # ==========================================================
    # Dashboard Data
    # ==========================================================

    def dashboard_data(self) -> Dict[str, Any]:
        """
        Data consumed directly by the Streamlit dashboard.
        """

        df = self.get_processed_dataset()

        if df is None:
            return {}

        dashboard = {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicates": int(df.duplicated().sum()),
            "memory_mb": round(
                df.memory_usage(deep=True).sum() / 1024**2,
                2,
            ),
            "column_names": list(df.columns),
            "numeric_columns": list(df.select_dtypes(include="number").columns),
            "categorical_columns": list(df.select_dtypes(exclude="number").columns),
        }

        return dashboard

    # ==========================================================
    # Processing Statistics
    # ==========================================================

    def processing_statistics(self) -> Dict[str, Any]:
        """
        High-level preprocessing statistics.
        """

        raw = self.raw_dataset
        processed = self.get_processed_dataset()

        if raw is None or processed is None:
            return {}

        return {
            "raw_rows": len(raw),
            "processed_rows": len(processed),
            "raw_columns": len(raw.columns),
            "processed_columns": len(processed.columns),
            "rows_removed": len(raw) - len(processed),
            "new_features": (len(processed.columns) - len(raw.columns)),
        }

    # ==========================================================
    # Before vs After Summary
    # ==========================================================

    def before_vs_after_summary(self) -> Dict[str, Any]:
        """
        Comparison between raw and processed datasets.
        """

        raw = self.raw_dataset
        processed = self.get_processed_dataset()

        if raw is None or processed is None:
            return {}

        return {
            "raw_missing": int(raw.isna().sum().sum()),
            "processed_missing": int(processed.isna().sum().sum()),
            "raw_duplicates": int(raw.duplicated().sum()),
            "processed_duplicates": int(processed.duplicated().sum()),
            "raw_columns": len(raw.columns),
            "processed_columns": len(processed.columns),
        }

    # ==========================================================
    # Export
    # ==========================================================

    def export_processed_dataset(
        self,
        destination: Path | str,
    ) -> Path:
        """
        Export processed dataset.
        """

        df = self.get_processed_dataset()

        if df is None:
            raise ValueError("Processed dataset unavailable.")

        destination = Path(destination)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(destination, index=False)

        self.logger.info(f"Processed dataset exported to {destination}")

        return destination

    # ==========================================================
    # Metrics
    # ==========================================================

    def get_metrics(self) -> Dict[str, Any]:
        """
        Metrics exposed to the dashboard.
        """

        df = self.get_processed_dataset()

        if df is None:
            return {}

        return {
            "records": len(df),
            "features": len(df.columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicates": int(df.duplicated().sum()),
        }

    # ==========================================================
    # Health Check
    # ==========================================================

    def health_check(self) -> Dict[str, Any]:
        """
        Extended service health check.
        """

        health = super().health_check()

        health.update({
            "raw_loaded": self.raw_dataset is not None,
            "processed_exists": (self.processed_dataset_path.exists()),
            "quality_report": (
                (self.get_output_directory() / "quality_report.md").exists()
            ),
            "feature_dictionary": (
                (self.get_output_directory() / "feature_dictionary.md").exists()
            ),
        })

        return health

    # ==========================================================
    # Alias
    # ==========================================================

    def run(self):
        """
        Alias for PipelineRunner.
        """
        return self.run_pipeline()

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self) -> Dict[str, Any]:
        """
        Complete preprocessing summary.
        """

        return {
            "service": self.service_name,
            "health": self.health_check(),
            "dataset": self.dataset_summary(),
            "statistics": self.processing_statistics(),
            "outputs": self.get_pipeline_outputs(),
        }
