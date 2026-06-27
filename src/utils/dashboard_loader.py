"""
dashboard_loader.py (Part 1)

Production DashboardLoader

Contains:
- Imports
- Initialization
- Safe Cached Readers
- Validation Helpers
- Generic Metric Helper
- Executive APIs
- Risk APIs
"""

from __future__ import annotations

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

import pandas as pd

from src.config.paths import Paths

logger = logging.getLogger(__name__)


class DashboardLoader:
    """
    Centralized data access layer for the Healthcare Analytics Dashboard.

    Responsibilities
    ----------------
    • Safe loading of dashboard outputs
    • Cached file access
    • Graceful handling of missing files
    • Business metric extraction
    """

    def __init__(self) -> None:
        self.outputs = Paths.OUTPUT_DIR

        self.portfolio = Paths.PORTFOLIO_OUTPUT
        self.pricing = Paths.PRICING_OUTPUT
        self.underwriting = Paths.UNDERWRITING_OUTPUT
        self.lapse = Paths.LAPSE_OUTPUT
        self.preprocessing = Paths.PREPROCESSING_OUTPUT

    # ==========================================================
    # Cached Readers
    # ==========================================================

    @staticmethod
    @lru_cache(maxsize=64)
    def _read_csv(path: str) -> pd.DataFrame:
        """Read CSV with caching."""
        try:
            return pd.read_csv(path)
        except Exception as e:
            logger.warning(f"Unable to load CSV: {path} ({e})")
            return pd.DataFrame()

    @staticmethod
    @lru_cache(maxsize=64)
    def _read_json(path: str) -> dict:
        """Read JSON with caching."""
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Unable to load JSON: {path} ({e})")
            return {}

    @staticmethod
    @lru_cache(maxsize=64)
    def _read_text(path: str) -> str:
        """Read text with caching."""
        try:
            return Path(path).read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Unable to load text: {path} ({e})")
            return ""

    # ==========================================================
    # Reader Wrappers
    # ==========================================================

    def _csv(self, path: Path) -> pd.DataFrame:
        return self._read_csv(str(path))

    def _json(self, path: Path) -> dict:
        return self._read_json(str(path))

    def _text(self, path: Path) -> str:
        return self._read_text(str(path))

    # ==========================================================
    # Validation Helpers
    # ==========================================================

    def _validate_columns(
        self,
        df: pd.DataFrame,
        required: list[str],
    ) -> pd.DataFrame:
        """
        Validate required columns.

        Returns an empty dataframe if validation fails.
        """
        if df.empty:
            return df

        missing = [c for c in required if c not in df.columns]

        if missing:
            logger.warning(
                "Missing columns %s",
                missing,
            )
            return pd.DataFrame()

        return df

    def _metric(
        self,
        dataframe: pd.DataFrame,
        metric: str,
        default: float = 0.0,
    ) -> float:
        """
        Extract a value from metric/value tables.
        """
        if dataframe.empty:
            return default

        try:
            value = dataframe.loc[
                dataframe["metric"] == metric,
                "value",
            ].iloc[0]

            return float(value)

        except Exception:
            logger.warning("Metric '%s' not found.", metric)
            return default

    # ==========================================================
    # Portfolio Validation
    # ==========================================================

    def portfolio_exists(self) -> bool:
        """Returns True if essential dashboard outputs exist."""
        required = [
            self.portfolio / "executive_kpis.csv",
            self.portfolio / "portfolio_metrics.csv",
            self.portfolio / "portfolio_health.csv",
        ]

        return all(file.exists() for file in required)

    def pipeline_status(self) -> str:
        return "READY" if self.portfolio_exists() else "NOT_READY"

    def last_pipeline_run(self):
        log = self.outputs / "pipeline_log.txt"

        if log.exists():
            return log.stat().st_mtime

        return None

    # ==========================================================
    # Executive APIs
    # ==========================================================

    def executive_kpis(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "executive_kpis.csv"),
            ["metric", "value"],
        )

    def portfolio_metrics(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "portfolio_metrics.csv"),
            ["metric", "value"],
        )

    def portfolio_health(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "portfolio_health.csv"),
            ["metric", "value"],
        )

    def executive_summary(self) -> str:
        return self._text(
            self.portfolio / "executive_summary.txt"
        )

    # ==========================================================
    # Business Executive Metrics
    # ==========================================================

    def get_total_policies(self) -> int:
        return int(
            self._metric(
                self.executive_kpis(),
                "total_policies",
            )
        )

    def get_total_premium(self) -> float:
        return self._metric(
            self.executive_kpis(),
            "total_premium",
        )

    def get_total_claims(self) -> float:
        return self._metric(
            self.executive_kpis(),
            "total_claims",
        )

    def get_total_profit(self) -> float:
        return self._metric(
            self.executive_kpis(),
            "total_profit",
        )

    def get_loss_ratio(self) -> float:
        return self._metric(
            self.executive_kpis(),
            "loss_ratio_pct",
        )

    def get_health_score(self) -> float:
        return self._metric(
            self.portfolio_health(),
            "portfolio_health_score",
        )

    # ==========================================================
    # Risk APIs
    # ==========================================================

    def risk_distribution(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "risk_distribution.csv"),
            ["risk_class", "policy_count", "percentage"],
        )

    def risk_by_age(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "risk_by_age_band.csv"),
            ["age_band", "risk_class", "policy_count"],
        )

    def risk_by_channel(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "risk_by_channel.csv"),
            ["distribution_channel", "risk_class", "policy_count"],
        )

    def risk_by_policy(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "risk_by_policy_type.csv"),
            ["type_policy", "risk_class", "policy_count"],
        )

    def risk_profitability(self) -> pd.DataFrame:
        return self._csv(
            self.portfolio / "risk_profitability.csv"
        )

    def risk_claims_summary(self) -> pd.DataFrame:
        return self._csv(
            self.portfolio / "risk_claims_summary.csv"
        )

    def risk_premium_summary(self) -> pd.DataFrame:
        return self._csv(
            self.portfolio / "risk_premium_summary.csv"
        )
    # ==========================================================
    # Claims APIs
    # ==========================================================

    def claim_frequency(self) -> pd.DataFrame:
        """Load claim frequency by age band."""
        return self._validate_columns(
            self._csv(self.portfolio / "frequency_by_age.csv"),
            ["age_band", "avg_frequency", "policy_count"],
        )

    def claim_severity(self) -> pd.DataFrame:
        """Load claim severity by age band."""
        return self._validate_columns(
            self._csv(self.portfolio / "severity_by_age.csv"),
            ["age_band", "avg_severity", "total_claims"],
        )

    def top_loss_segments(self) -> pd.DataFrame:
        """Load top loss-making portfolio segments."""
        return self._validate_columns(
            self._csv(self.portfolio / "top_loss_segments.csv"),
            [
                "age_band",
                "risk_class",
                "policy_count",
                "total_premium",
                "total_claims",
                "loss_ratio_pct",
                "profit",
            ],
        )
    
    def claim_summary(self) -> pd.DataFrame:
        """Claims summary."""
        return self.risk_claims_summary()


    def load_claim_summary(self) -> pd.DataFrame:
        """Backward compatibility alias."""
        return self.claim_summary()

    # ==========================================================
    # Pricing APIs
    # ==========================================================

    def premium_quotes(self) -> pd.DataFrame:
        """Load premium quotations."""
        return self._csv(
            self.pricing / "premium_quotes.csv"
        )

    def premium_summary(self) -> dict[str, Any]:
        """Load premium summary JSON."""
        return self._json(
            self.pricing / "premium_summary.json"
        )

    def pricing_report(self) -> dict[str, Any]:
        """Load pricing report JSON."""
        return self._json(
            self.pricing / "pricing_report.json"
        )

    def prediction_summary(self) -> dict[str, Any]:
        """Load prediction summary."""
        return self._json(
            self.pricing / "prediction_summary.json"
        )

    def pricing_metrics(self) -> dict[str, Any]:
        """Load pricing metrics."""
        return self._json(
            self.pricing / "metrics.json"
        )

    def premium_metadata(self) -> dict[str, Any]:
        """Load premium metadata."""
        return self._json(
            self.pricing / "premium_metadata.json"
        )

    def premium_leakage(self) -> pd.DataFrame:
        """Load premium leakage analysis."""
        return self._csv(
            self.portfolio / "premium_leakage.csv"
        )

    # ==========================================================
    # Retention APIs
    # ==========================================================

    def lapse_predictions(self) -> pd.DataFrame:
        """Load lapse predictions."""
        return self._csv(
            self.lapse / "lapse_predictions.csv"
        )

    def lapse_summary(self) -> dict[str, Any]:
        """Load lapse summary."""
        return self._json(
            self.lapse / "lapse_summary.json"
        )

    def retention_summary(self) -> pd.DataFrame:
        """Load retention summary."""
        return self._validate_columns(
            self._csv(
                self.portfolio / "retention_summary.csv"
            ),
            [
                "retention_segment",
                "customers",
                "premium_at_risk",
            ],
        )

    def get_average_lapse_probability(self) -> float:
        """
        Calculate average lapse probability from prediction output.
        """

        df = self.lapse_predictions()

        if df.empty:
            return 0.0

        probability_columns = [
            "lapse_probability",
            "probability",
            "prediction_probability",
            "avg_lapse_probability",
        ]

        for column in probability_columns:
            if column in df.columns:
                return float(df[column].mean())

        return self._metric(
            self.portfolio_metrics(),
            "avg_lapse_probability",
        )

    # ==========================================================
    # Trend APIs
    # ==========================================================

    def premium_trend(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "premium_trend.csv"),
            [
                "period",
                "total_premium",
                "policy_count",
                "premium_growth_pct",
            ],
        )

    def claims_trend(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "claims_trend.csv"),
            [
                "period",
                "total_claims",
                "claims_growth_pct",
            ],
        )

    def loss_ratio_trend(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(
                self.portfolio / "loss_ratio_trend.csv"
            ),
            [
                "period",
                "avg_loss_ratio_pct",
            ],
        )

    def lapse_trend(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(self.portfolio / "lapse_trend.csv"),
            [
                "period",
                "total_policies",
                "lapse_rate_pct",
            ],
        )

    def growth_trend(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(
                self.portfolio /
                "portfolio_growth_summary.csv"
            ),
            [
                "metric",
                "value",
            ],
        )

    def risk_mix_trend(self) -> pd.DataFrame:
        return self._validate_columns(
            self._csv(
                self.portfolio / "risk_mix_trend.csv"
            ),
            [
                "period",
                "risk_class",
                "policy_count",
                "percentage",
            ],
        )

    # ==========================================================
    # Underwriting APIs
    # ==========================================================

    def underwriting_predictions(self) -> pd.DataFrame:
        return self._csv(
            self.underwriting /
            "underwriting_predictions.csv"
        )

    def underwriting_summary(self) -> dict[str, Any]:
        return self._json(
            self.underwriting /
            "underwriting_summary.json"
        )

    def underwriting_metadata(self) -> dict[str, Any]:
        return self._json(
            self.underwriting /
            "model_metadata.json"
        )

    # ==========================================================
    # Download Centre
    # ==========================================================

    def available_reports(self) -> dict[str, Path]:
        """
        Return every downloadable output file.
        """

        reports: dict[str, Path] = {}

        folders = [
            self.preprocessing,
            self.portfolio,
            self.pricing,
            self.underwriting,
            self.lapse,
        ]

        for folder in folders:

            if not folder.exists():
                continue

            for file in folder.iterdir():

                if file.is_file():
                    reports[file.name] = file

        return reports

    # ==========================================================
    # Generic Loader
    # ==========================================================

    def load(self, relative_path: str) -> Any:
        """
        Generic loader for any file inside outputs/.
        """

        path = self.outputs / relative_path

        if path.suffix == ".csv":
            return self._csv(path)

        if path.suffix == ".json":
            return self._json(path)

        if path.suffix in (".txt", ".md"):
            return self._text(path)

        raise ValueError(
            f"Unsupported file type: {path.suffix}"
        )
    # ==========================================================
    # Backward Compatibility (load_* API)
    # ==========================================================

    # ---------- Executive ----------

    def load_executive_kpis(self) -> pd.DataFrame:
        return self.executive_kpis()

    def load_portfolio_metrics(self) -> pd.DataFrame:
        return self.portfolio_metrics()

    def load_portfolio_health(self) -> pd.DataFrame:
        return self.portfolio_health()

    def load_executive_summary(self) -> str:
        return self.executive_summary()

    # ---------- Risk ----------

    def load_risk_distribution(self) -> pd.DataFrame:
        return self.risk_distribution()

    def load_risk_by_age(self) -> pd.DataFrame:
        return self.risk_by_age()

    def load_risk_by_channel(self) -> pd.DataFrame:
        return self.risk_by_channel()

    def load_risk_by_policy(self) -> pd.DataFrame:
        return self.risk_by_policy()

    def load_risk_profitability(self) -> pd.DataFrame:
        return self.risk_profitability()

    def load_risk_claims_summary(self) -> pd.DataFrame:
        return self.risk_claims_summary()

    def load_risk_premium_summary(self) -> pd.DataFrame:
        return self.risk_premium_summary()

    # ---------- Claims ----------

    def load_claim_frequency(self) -> pd.DataFrame:
        return self.claim_frequency()

    def load_claim_severity(self) -> pd.DataFrame:
        return self.claim_severity()

    def load_top_loss_segments(self) -> pd.DataFrame:
        return self.top_loss_segments()

    # ---------- Pricing ----------

    def load_premium_quotes(self) -> pd.DataFrame:
        return self.premium_quotes()

    def load_premium_summary(self) -> dict[str, Any]:
        return self.premium_summary()

    def load_pricing_report(self) -> dict[str, Any]:
        return self.pricing_report()

    def load_prediction_summary(self) -> dict[str, Any]:
        return self.prediction_summary()

    def load_pricing_metrics(self) -> dict[str, Any]:
        return self.pricing_metrics()

    def load_premium_metadata(self) -> dict[str, Any]:
        return self.premium_metadata()

    def load_premium_leakage(self) -> pd.DataFrame:
        return self.premium_leakage()

    # ---------- Retention ----------

    def load_lapse_predictions(self) -> pd.DataFrame:
        return self.lapse_predictions()

    def load_lapse_summary(self) -> dict[str, Any]:
        return self.lapse_summary()

    def load_retention_summary(self) -> pd.DataFrame:
        return self.retention_summary()

    # ---------- Trends ----------

    def load_premium_trend(self) -> pd.DataFrame:
        return self.premium_trend()

    def load_claims_trend(self) -> pd.DataFrame:
        return self.claims_trend()

    def load_loss_ratio_trend(self) -> pd.DataFrame:
        return self.loss_ratio_trend()

    def load_lapse_trend(self) -> pd.DataFrame:
        return self.lapse_trend()

    def load_growth_trend(self) -> pd.DataFrame:
        return self.growth_trend()

    def load_risk_mix_trend(self) -> pd.DataFrame:
        return self.risk_mix_trend()

    # ---------- Underwriting ----------

    def load_underwriting_predictions(self) -> pd.DataFrame:
        return self.underwriting_predictions()

    def load_underwriting_summary(self) -> dict[str, Any]:
        return self.underwriting_summary()

    def load_underwriting_metadata(self) -> dict[str, Any]:
        return self.underwriting_metadata()

    # ==========================================================
    # Dashboard Helpers
    # ==========================================================

    def get_portfolio_health(self) -> pd.DataFrame:
        return self.portfolio_health()

    def dashboard_ready(self) -> bool:
        """
        Returns True when the minimum dashboard datasets exist.
        """
        return (
            not self.executive_kpis().empty
            and not self.portfolio_metrics().empty
            and not self.portfolio_health().empty
        )

    def refresh_cache(self) -> None:
        """
        Clear all cached file readers.
        """
        self._read_csv.cache_clear()
        self._read_json.cache_clear()
        self._read_text.cache_clear()

        logger.info("Dashboard cache cleared.")

    def health_check(self) -> dict[str, Any]:
        """
        Dashboard diagnostic summary.
        """
        return {
            "dashboard_ready": self.dashboard_ready(),
            "pipeline_status": self.pipeline_status(),
            "portfolio_exists": self.portfolio_exists(),
            "last_pipeline_run": self.last_pipeline_run(),
            "available_reports": len(self.available_reports()),
            "portfolio_files": {
                "executive_kpis": (
                    self.portfolio / "executive_kpis.csv"
                ).exists(),
                "portfolio_metrics": (
                    self.portfolio / "portfolio_metrics.csv"
                ).exists(),
                "portfolio_health": (
                    self.portfolio / "portfolio_health.csv"
                ).exists(),
                "risk_distribution": (
                    self.portfolio / "risk_distribution.csv"
                ).exists(),
                "premium_trend": (
                    self.portfolio / "premium_trend.csv"
                ).exists(),
                "claims_trend": (
                    self.portfolio / "claims_trend.csv"
                ).exists(),
                "retention_summary": (
                    self.portfolio / "retention_summary.csv"
                ).exists(),
            },
        }

    # ==========================================================
    # Utility Methods
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"DashboardLoader("
            f"status='{self.pipeline_status()}', "
            f"reports={len(self.available_reports())})"
        )