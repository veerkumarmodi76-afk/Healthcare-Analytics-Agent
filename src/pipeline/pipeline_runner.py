"""
pipeline_runner.py

Master Pipeline Runner

Responsibilities
----------------
- Execute every pipeline stage in order
- Track pipeline state
- Log progress
- Handle failures gracefully
- Produce execution summary

No analytics logic lives here.
"""

from __future__ import annotations

import time

from .pipeline_logger import PipelineLogger
from .pipeline_state import PipelineState

from .pipeline_exceptions import (
    ValidationException,
    PreprocessingException,
    UnderwritingException,
    PricingException,
    LapseException,
    PortfolioException,
)

from ..validation.validation_toolkit import ValidationToolkit

from ..services.preprocessing_service import PreprocessingService
from ..services.underwriting_service import UnderwritingService
from ..services.pricing_service import PricingService
from ..services.lapse_service import LapseService
from ..services.portfolio_service import PortfolioService


class PipelineRunner:
    """
    Executes the complete Healthcare Analytics workflow.
    """

    STAGES = [
        ("Validation", ValidationException),
        ("Preprocessing", PreprocessingException),
        ("Underwriting", UnderwritingException),
        ("Pricing", PricingException),
        ("Lapse", LapseException),
        ("Portfolio", PortfolioException),
    ]

    def __init__(self, progress_callback=None):

        self.logger = PipelineLogger()
        self.state = PipelineState()

        self.progress_callback = progress_callback

        self.validation = ValidationToolkit()

        self.preprocessing = PreprocessingService()
        self.underwriting = UnderwritingService()
        self.pricing = PricingService()
        self.lapse = LapseService()
        self.portfolio = PortfolioService()

    # ==========================================================
    # Public Entry Point
    # ==========================================================

    def run(self) -> bool:

        self.logger.pipeline_started()
        self.state.start_pipeline()
        self._notify_progress()

        pipeline_start = time.perf_counter()

        try:

            self._execute_stage(
                stage_name="Validation",
                func=self.validation.validate_project,
                exception_cls=ValidationException,
            )

            self._execute_stage(
                stage_name="Preprocessing",
                func=self.preprocessing.run,
                exception_cls=PreprocessingException,
            )

            self._execute_stage(
                stage_name="Underwriting",
                func=self.underwriting.run,
                exception_cls=UnderwritingException,
            )

            self._execute_stage(
                stage_name="Pricing",
                func=self.pricing.run,
                exception_cls=PricingException,
            )

            self._execute_stage(
                stage_name="Lapse",
                func=self.lapse.run,
                exception_cls=LapseException,
            )

            self._execute_stage(
                stage_name="Portfolio",
                func=self.portfolio.run,
                exception_cls=PortfolioException,
            )

            total_time = time.perf_counter() - pipeline_start

            self.state.complete_pipeline()
            self._notify_progress()

            self.logger.pipeline_completed(total_time)

            self.logger.execution_summary(self.state)

            return True

        except Exception as e:

            self.state.fail_pipeline()
            self._notify_progress()

            self.logger.pipeline_failed(
                getattr(e, "stage", "Unknown"),
                str(e),
            )

            self.logger.execution_summary(self.state)

            raise

    # ==========================================================
    # Generic Stage Executor
    # ==========================================================

    def _execute_stage(
        self,
        stage_name: str,
        func,
        exception_cls,
    ) -> None:

        current_stage = (
            [s[0] for s in self.STAGES].index(stage_name)
            + 1
        )

        total_stages = len(self.STAGES)

        self.logger.progress(
            current_stage,
            total_stages,
            stage_name,
        )

        self.state.start_stage(stage_name)
        self._notify_progress()

        self.logger.stage_started(stage_name)

        stage_start = time.perf_counter()

        try:

            func()

            duration = time.perf_counter() - stage_start

            self.state.complete_stage(stage_name)
            self._notify_progress()

            self.logger.stage_completed(
                stage_name,
                duration,
            )

            self.state.print_progress()

        except Exception as e:

            self.state.fail_stage(
                stage_name,
                str(e),
            )
            self._notify_progress()

            self.logger.stage_failed(
                stage_name,
                e,
            )

            raise exception_cls(str(e)) from e
    
    def _notify_progress(self):
        """
        Notify any UI (Streamlit) that the pipeline state has changed.
        """
        if self.progress_callback:
            self.progress_callback(self.state)