"""
run_pipeline.py

Healthcare Analytics Agent

Master entry point for executing the complete
Healthcare Insurance Decision Intelligence Pipeline.

Usage
-----
python run_pipeline.py
"""

from __future__ import annotations

import sys
import traceback

from src.pipeline import PipelineRunner


def print_header() -> None:
    print("\n" + "=" * 80)
    print("Healthcare Analytics Agent")
    print("Healthcare Insurance Decision Intelligence Platform")
    print("=" * 80)
    print("Starting Master Pipeline...\n")


def print_footer(success: bool) -> None:
    print("\n" + "=" * 80)

    if success:
        print("Pipeline completed successfully.")
    else:
        print("Pipeline terminated with errors.")

    print("=" * 80)


def main() -> int:
    print_header()

    runner = PipelineRunner()

    try:
        runner.run()

        print_footer(True)

        return 0

    except Exception as exc:

        print("\n" + "=" * 80)
        print("PIPELINE FAILED")
        print("=" * 80)

        stage = getattr(exc, "stage", "Unknown")

        print(f"Stage : {stage}")
        print(f"Reason: {exc}")

        print("\nDetailed Traceback\n")
        traceback.print_exc()

        print_footer(False)

        return 1


if __name__ == "__main__":
    sys.exit(main())