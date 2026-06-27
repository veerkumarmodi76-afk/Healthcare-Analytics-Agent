from pathlib import Path


class Paths:
    """
    Centralized filesystem paths for AI-AIP.

    Every module in the project should use this class instead of creating
    its own filesystem paths.
    """

    # ==========================================================
    # Project Root
    # ==========================================================

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    # ==========================================================
    # Source Code
    # ==========================================================

    SRC_DIR = PROJECT_ROOT / "src"

    CONFIG_DIR = SRC_DIR / "config"

    DASHBOARD_DIR = SRC_DIR / "dashboard"

    COPILOT_DIR = SRC_DIR / "copilot"

    # ==========================================================
    # Data
    # ==========================================================

    DATA_DIR = PROJECT_ROOT / "data"

    RAW_DATA_DIR = DATA_DIR / "raw"

    PROCESSED_DATA_DIR = DATA_DIR / "processed"

    RAW_DATA_FILE = RAW_DATA_DIR / "raw_data.csv"

    PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "processed_data.csv"

    UPLOADS_DIR = DATA_DIR / "uploads"

    # ==========================================================
    # Models
    # ==========================================================

    MODELS_DIR = PROJECT_ROOT / "models"

    UNDERWRITING_MODEL_DIR = MODELS_DIR / "underwriting"

    PRICING_MODEL_DIR = MODELS_DIR / "pricing"

    LAPSE_MODEL_DIR = MODELS_DIR / "lapse"

    COST_PREDICTION_MODEL_DIR = MODELS_DIR / "cost_prediction"

    # ==========================================================
    # Outputs
    # ==========================================================

    OUTPUT_DIR = PROJECT_ROOT / "outputs"

    PREPROCESSING_OUTPUT = OUTPUT_DIR / "preprocessing"

    UNDERWRITING_OUTPUT = OUTPUT_DIR / "underwriting"

    PRICING_OUTPUT = OUTPUT_DIR / "pricing"

    LAPSE_OUTPUT = OUTPUT_DIR / "lapse"

    PORTFOLIO_OUTPUT = OUTPUT_DIR / "portfolio"

    LOG_DIR = OUTPUT_DIR / "logs"

    # ==========================================================
    # Reports
    # ==========================================================

    REPORT_DIR = PROJECT_ROOT / "reports"

    DOCS_DIR = PROJECT_ROOT / "docs"

    # ==========================================================
    # Miscellaneous
    # ==========================================================

    NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

    TEMP_DIR = SRC_DIR / "temp"

    TEST_DIR = PROJECT_ROOT / "tests"

    # ==========================================================
    # Directory Creation
    # ==========================================================

    @classmethod
    def create_directories(cls):
        """
        Create all required project directories.
        Safe to call multiple times.
        """

        directories = [
            cls.DATA_DIR,
            cls.RAW_DATA_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.MODELS_DIR,
            cls.UNDERWRITING_MODEL_DIR,
            cls.PRICING_MODEL_DIR,
            cls.LAPSE_MODEL_DIR,
            cls.COST_PREDICTION_MODEL_DIR,
            cls.OUTPUT_DIR,
            cls.PREPROCESSING_OUTPUT,
            cls.UNDERWRITING_OUTPUT,
            cls.PRICING_OUTPUT,
            cls.LAPSE_OUTPUT,
            cls.PORTFOLIO_OUTPUT,
            cls.LOG_DIR,
            cls.REPORT_DIR,
            cls.DOCS_DIR,
            cls.TEMP_DIR,
            cls.UPLOADS_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)