"""
pipeline_status.py

Pipeline Execution Component

Responsibilities
----------------
- Execute the master pipeline
- Display real-time progress
- Show current pipeline stage
- Show execution summary
- Display errors gracefully

No pipeline logic lives here.
"""

from __future__ import annotations

import streamlit as st

from ...pipeline.pipeline_runner import PipelineRunner
from ...pipeline.pipeline_state import PipelineState
from pathlib import Path
from ...config.paths import Paths



# ==========================================================
# Session State
# ==========================================================

def initialize_pipeline_session() -> None:
    """Initialize Streamlit session state."""

    defaults = {
        "pipeline_state": None,
        "pipeline_running": False,
        "pipeline_finished": False,
        "pipeline_success": False,
        "pipeline_log": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ==========================================================
# Dashboard Callback
# ==========================================================

def _dashboard_callback(state: PipelineState) -> None:
    """
    Called automatically whenever the pipeline state changes.
    """

    st.session_state.pipeline_state = state


# ==========================================================
# Pipeline Execution
# ==========================================================

def run_pipeline() -> bool:
    """
    Execute the complete Healthcare Analytics pipeline.
    """

    initialize_pipeline_session()

    st.session_state.pipeline_running = True
    st.session_state.pipeline_finished = False
    st.session_state.pipeline_success = False

    runner = PipelineRunner(
        progress_callback=_dashboard_callback
    )

    try:

        success = runner.run()
        log_file = Paths.OUTPUT_DIR / "pipeline_log.txt"

        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                st.session_state.pipeline_log = f.read()

        st.session_state.pipeline_running = False
        st.session_state.pipeline_finished = True
        st.session_state.pipeline_success = success

        return success

    except Exception as e:

        st.session_state.pipeline_running = False
        st.session_state.pipeline_finished = True
        st.session_state.pipeline_success = False

        st.exception(e)

    return False


# ==========================================================
# Progress Display
# ==========================================================

def show_pipeline_progress() -> None:
    """
    Display current pipeline progress.
    """

    initialize_pipeline_session()

    state: PipelineState | None = st.session_state.pipeline_state

    if state is None:

        st.info("Pipeline has not started.")

        return

    st.subheader("Pipeline Progress")

    st.progress(state.progress)
    st.subheader("Execution Log")

    log_container = st.container(height=400)

    with log_container:
        st.code(
            st.session_state.pipeline_log,
            language="text",
        )

    current_stage = (
        state.current_stage
        if state.current_stage
        else "Waiting..."
    )

    st.info(f"Current Stage: **{current_stage}**")

    st.write("")

    for stage in state.stages.values():

        icon = {
            "Pending": "⚪",
            "Running": "🟡",
            "Success": "🟢",
            "Failed": "🔴",
            "Skipped": "⚫",
        }.get(stage.status, "⚪")

        st.write(
            f"{icon} **{stage.name}** — {stage.status}"
        )


# ==========================================================
# Execution Summary
# ==========================================================

def show_execution_summary() -> None:
    """
    Display final pipeline execution summary.
    """

    initialize_pipeline_session()

    state: PipelineState | None = st.session_state.pipeline_state

    if state is None:
        return

    st.subheader("Execution Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Status",
            state.overall_status,
        )

    with col2:
        st.metric(
            "Execution Time",
            f"{state.execution_time:.2f} s",
        )

    with col3:
        completed = sum(
            stage.status == "Success"
            for stage in state.stages.values()
        )

        st.metric(
            "Completed Stages",
            f"{completed}/{len(state.stages)}",
        )

    if state.overall_status == "Success":

        st.success(
            "Healthcare Analytics Pipeline completed successfully."
        )

    elif state.overall_status == "Failed":

        failed_stage = next(
            (
                stage
                for stage in state.stages.values()
                if stage.status == "Failed"
            ),
            None,
        )

        if failed_stage:

            st.error(
                f"Pipeline failed during **{failed_stage.name}**"
            )

            if failed_stage.error_message:

                st.exception(
                    failed_stage.error_message
                )


# ==========================================================
# Combined Component
# ==========================================================

def render_pipeline_status() -> None:
    """
    Render the complete pipeline status widget.
    """

    show_pipeline_progress()

    st.divider()

    show_execution_summary()