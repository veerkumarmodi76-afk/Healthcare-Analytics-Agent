"""
validation_toolkit.py

Production Validation Toolkit
-----------------------------

Performs pre-flight validation before the master pipeline starts.

Validation Checks
-----------------
✓ Project directory structure
✓ Required datasets
✓ Model directories
✓ Output directories
✓ Reports directory
✓ Configuration package

This toolkit does NOT validate model performance.
It validates whether the project is ready to execute.
"""

from __future__ import annotations

from pathlib import Path


class ValidationToolkit:
    """
    Performs project validation before pipeline execution.
    """

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.errors = []

    # ==========================================================
    # Helpers
    # ==========================================================

    def _exists(self, path: Path, description: str):

        if not path.exists():
            self.errors.append(f"{description}: {path}")

    # ==========================================================
    # Directory Validation
    # ==========================================================

    def validate_directories(self):

        required = {
            "Source Directory": self.project_root / "src",
            "Data Directory": self.project_root / "data",
            "Models Directory": self.project_root / "models",
            "Outputs Directory": self.project_root / "outputs",
            "Reports Directory": self.project_root / "reports",
            "Configuration Directory": self.project_root / "src" / "config",
        }

        for description, path in required.items():
            self._exists(path, description)

    # ==========================================================
    # Dataset Validation
    # ==========================================================

    def validate_datasets(self):

        required = {
            "Raw Dataset": (
                self.project_root
                / "data"
                / "raw"
                / "raw_data.csv"
            ),
        }

        for description, path in required.items():
            self._exists(path, description)

    # ==========================================================
    # Model Validation
    # ==========================================================

    def validate_models(self):

        required = {
            "Underwriting Model Folder": (
                self.project_root
                / "models"
                / "underwriting"
            ),
            "Pricing Model Folder": (
                self.project_root
                / "models"
                / "pricing"
            ),
            "Lapse Model Folder": (
                self.project_root
                / "models"
                / "lapse"
            ),
        }

        for description, path in required.items():
            self._exists(path, description)

    # ==========================================================
    # Output Validation
    # ==========================================================

    def validate_outputs(self):

        required = {
            "Preprocessing Output": (
                self.project_root
                / "outputs"
                / "preprocessing"
            ),
            "Underwriting Output": (
                self.project_root
                / "outputs"
                / "underwriting"
            ),
            "Pricing Output": (
                self.project_root
                / "outputs"
                / "pricing"
            ),
            "Lapse Output": (
                self.project_root
                / "outputs"
                / "lapse"
            ),
            "Portfolio Output": (
                self.project_root
                / "outputs"
                / "portfolio"
            ),
        }

        for description, path in required.items():
            self._exists(path, description)

    # ==========================================================
    # Complete Validation
    # ==========================================================

    def validate_project(self):

        print("\n" + "=" * 70)
        print("PROJECT VALIDATION")
        print("=" * 70)

        self.errors.clear()

        self.validate_directories()

        self.validate_datasets()

        self.validate_models()

        self.validate_outputs()

        if self.errors:

            print("\nValidation Failed\n")

            for error in self.errors:
                print(f"✗ {error}")

            raise RuntimeError(
                "Project validation failed."
            )

        print("✓ Project structure validated.")
        print("✓ Required datasets found.")
        print("✓ Model directories found.")
        print("✓ Output directories found.")
        print("✓ Validation completed successfully.")

        return True


if __name__ == "__main__":

    ValidationToolkit().validate_project()