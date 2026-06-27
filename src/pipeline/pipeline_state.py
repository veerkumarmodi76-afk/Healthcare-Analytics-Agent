"""
pipeline_state.py

Maintains the runtime state of the master pipeline.
This class is responsible for tracking execution progress,
timings, stage status, and overall pipeline health.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class StageState:
    """
    Represents the execution state of a single pipeline stage.
    """

    name: str
    status: str = "Pending"          # Pending | Running | Success | Failed | Skipped
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None
    current_stage: str = ""
    current_stage_number: int = 0
    total_stages: int = 6


@dataclass
class PipelineState:
    """
    Tracks the execution state of the complete pipeline.
    """

    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    overall_status: str = "Not Started"

    stages: Dict[str, StageState] = field(default_factory=dict)

    def add_stage(self, stage_name: str) -> None:
        """
        Register a new pipeline stage.
        """
        if stage_name not in self.stages:
            self.stages[stage_name] = StageState(name=stage_name)

    def start_pipeline(self) -> None:
        """
        Mark pipeline execution as started.
        """
        self.started_at = datetime.now()
        self.overall_status = "Running"

    def complete_pipeline(self) -> None:
        """
        Mark pipeline execution as completed successfully.
        """
        self.completed_at = datetime.now()
        self.overall_status = "Success"

    def fail_pipeline(self) -> None:
        """
        Mark pipeline execution as failed.
        """
        self.completed_at = datetime.now()
        self.overall_status = "Failed"

    def start_stage(self, stage_name: str) -> None:
        """
        Mark a stage as currently executing.
        """
        self.add_stage(stage_name)

        stage = self.stages[stage_name]
        stage.status = "Running"
        self.current_stage = stage_name

        self.current_stage_number = (
            list(self.stages.keys()).index(stage_name) + 1
        )

        stage.started_at = datetime.now()

    def complete_stage(self, stage_name: str) -> None:
        """
        Mark a stage as completed successfully.
        """
        stage = self.stages[stage_name]

        stage.completed_at = datetime.now()
        stage.status = "Success"

        if stage.started_at:
            stage.duration_seconds = (
                stage.completed_at - stage.started_at
            ).total_seconds()

    def fail_stage(self, stage_name: str, error_message: str) -> None:
        """
        Mark a stage as failed.
        """
        stage = self.stages[stage_name]

        stage.completed_at = datetime.now()
        stage.status = "Failed"
        stage.error_message = str(error_message)

        if stage.started_at:
            stage.duration_seconds = (
                stage.completed_at - stage.started_at
            ).total_seconds()

    def skip_stage(self, stage_name: str) -> None:
        """
        Mark a stage as skipped.
        """
        self.add_stage(stage_name)
        self.stages[stage_name].status = "Skipped"

    @property
    def execution_time(self) -> float:
        """
        Returns the total pipeline execution time in seconds.
        """
        if self.completed_at is None:
            return 0.0

        return (
            self.completed_at - self.started_at
        ).total_seconds()

    def summary(self) -> dict:
        """
        Return a serializable summary of the pipeline execution.
        """
        return {
            "overall_status": self.overall_status,
            "started_at": self.started_at.strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": (
                self.completed_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.completed_at
                else None
            ),
            "execution_time_seconds": round(self.execution_time, 2),
            "stages": {
                name: {
                    "status": stage.status,
                    "duration_seconds": stage.duration_seconds,
                    "error": stage.error_message,
                }
                for name, stage in self.stages.items()
            },
        }

    def print_progress(self) -> None:
        """
        Print the current pipeline progress to the console.
        """
        print("\nPipeline Progress")
        print("-" * 40)

        for stage in self.stages.values():
            icon = {
                "Pending": "○",
                "Running": "▶",
                "Success": "✓",
                "Failed": "✗",
                "Skipped": "⏭",
            }.get(stage.status, "?")

            print(f"{icon} {stage.name:<20} {stage.status}")

        print("-" * 40)
        print(f"Overall Status : {self.overall_status}")

        if self.completed_at:
            print(f"Execution Time : {self.execution_time:.2f} seconds")

    @property
    def progress(self) -> float:
        """
        Returns pipeline completion percentage (0–1).
        """

        total = len(self.stages)

        if total == 0:
            return 0.0

        completed = sum(
            1
            for stage in self.stages.values()
            if stage.status == "Success"
        )

        return completed / total