"""
pipeline_logger.py

Central logging utility for the Healthcare Analytics Agent
Master Pipeline.

This logger records the execution of every pipeline stage
to both the console and:

outputs/pipeline_log.txt
"""

from __future__ import annotations

import logging
from pathlib import Path
from datetime import datetime

from ..config.paths import Paths


class PipelineLogger:
    """
    Central logger for the master pipeline.

    Features
    --------
    • Console logging
    • File logging
    • Stage banners
    • Success / Failure messages
    • Execution summary
    """

    LOGGER_NAME = "HealthcarePipeline"

    def __init__(self):

        self.log_file = Paths.OUTPUT_DIR / "pipeline_log.txt"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(self.LOGGER_NAME)
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File handler
        file_handler = logging.FileHandler(
            self.log_file,
            mode="w",
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    # --------------------------------------------------
    # General Messages
    # --------------------------------------------------

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    # --------------------------------------------------
    # Pipeline Events
    # --------------------------------------------------

    def pipeline_started(self):

        self.logger.info("=" * 70)
        self.logger.info("Healthcare Analytics Agent")
        self.logger.info("Master Pipeline Started")
        self.logger.info(
            f"Execution Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.logger.info("=" * 70)

    def pipeline_completed(self, execution_time: float):

        self.logger.info("=" * 70)
        self.logger.info("Pipeline Completed Successfully")
        self.logger.info(
            f"Total Execution Time : {execution_time:.2f} seconds"
        )
        self.logger.info("=" * 70)

    def pipeline_failed(self, stage: str, reason: str):

        self.logger.error("=" * 70)
        self.logger.error("PIPELINE FAILED")
        self.logger.error(f"Failed Stage : {stage}")
        self.logger.error(f"Reason       : {reason}")
        self.logger.error("=" * 70)

    # --------------------------------------------------
    # Stage Events
    # --------------------------------------------------

    def stage_started(self, stage: str):

        self.logger.info("")
        self.logger.info("-" * 50)
        self.logger.info(f"Starting Stage : {stage}")
        self.logger.info("-" * 50)

    def stage_completed(self, stage: str, duration: float):

        self.logger.info(
            f"✓ {stage} completed successfully "
            f"({duration:.2f} seconds)"
        )

    def stage_failed(self, stage: str, error: Exception):

        self.logger.error(
            f"✗ {stage} failed"
        )
        self.logger.error(str(error))

    def stage_skipped(self, stage: str):

        self.logger.warning(
            f"⏭ {stage} skipped"
        )

    # --------------------------------------------------
    # Progress
    # --------------------------------------------------

    def progress(self, current: int, total: int, stage: str):

        self.logger.info(
            f"[{current}/{total}] {stage}"
        )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def execution_summary(self, state):

        self.logger.info("")
        self.logger.info("=" * 70)
        self.logger.info("Execution Summary")
        self.logger.info("=" * 70)

        for stage in state.stages.values():

            duration = (
                f"{stage.duration_seconds:.2f}s"
                if stage.duration_seconds
                else "-"
            )

            self.logger.info(
                f"{stage.name:<20}"
                f"{stage.status:<12}"
                f"{duration}"
            )

        self.logger.info("-" * 70)
        self.logger.info(
            f"Overall Status : {state.overall_status}"
        )
        self.logger.info(
            f"Execution Time : {state.execution_time:.2f} seconds"
        )
        self.logger.info("=" * 70)