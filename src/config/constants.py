"""
Global constants used across AI-AIP.
"""

APPROVED_FILE_TYPES = [".csv", ".xlsx", ".xls"]

MODEL_NAMES = {
    "underwriting": "underwriting_model.pkl",
    "pricing": "pricing_model.pkl",
    "lapse": "lapse_model.pkl",
}

REPORT_NAMES = {
    "quality": "quality_report.md",
    "feature_dictionary": "feature_dictionary.md",
    "pricing": "pricing_report.md",
    "executive": "executive_report.md",
}

DEFAULT_PLOT_SIZE = (12, 6)

DEFAULT_CMAP = "Blues"

RISK_CLASSES = [
    "Low",
    "Medium",
    "High",
]

UNDERWRITING_DECISIONS = [
    "Preferred",
    "Standard",
    "Rated",
    "Decline",
]

LOG_LEVEL = "INFO"

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
