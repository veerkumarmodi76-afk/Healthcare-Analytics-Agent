"""
====================================================
Healthcare Analytics Agent — Full Pipeline Runner
====================================================
Runs all analytic modules in sequence:
  Module 2 : Underwriting Risk Scoring
  (Modules 3-5 placeholders — extend as built)

Usage:
    python run_all.py
    python run_all.py --module underwriting   # run only underwriting
====================================================
"""

import os
import sys
import time
import argparse


def run_module_underwriting():
    """Module 2: Train, score, and explain underwriting risk."""
    print("\n" + "=" * 60)
    print("  MODULE 2 — UNDERWRITING RISK SCORING")
    print("=" * 60)

    from underwriting.train import train_underwriting_model
    from underwriting.predict import predict_risk_scores
    from underwriting.explain import (
        generate_global_shap_plots,
        generate_local_shap_plot,
    )

    # Step 1 — Train (skip if model already exists)
    model_path = "models/underwriting_model.pkl"
    if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
        print(f"\n[Step 1/3] Model already exists at {model_path} — skipping training.")
    else:
        print("\n[Step 1/3] Training XGBoost underwriting model...")
        train_underwriting_model()

    # Step 2 — Predict
    print("\n[Step 2/3] Generating applicant risk scores...")
    results_df = predict_risk_scores(
        input_path="data/processed/processed_data.csv", output_dir="outputs"
    )

    # Step 3 — Explain (SHAP)
    print("\n[Step 3/3] Generating SHAP global & local explanations...")
    generate_global_shap_plots(
        input_path="data/processed/processed_data.csv",
        output_dir="outputs",
        sample_size=1000,
    )
    generate_local_shap_plot(0, output_dir="outputs")

    return results_df


def write_executive_summary(results):
    """Write a consolidated executive summary to outputs/executive_summary.txt."""
    lines = [
        "=" * 60,
        "  HEALTHCARE ANALYTICS AGENT — EXECUTIVE SUMMARY",
        "=" * 60,
        "",
    ]

    if "underwriting" in results:
        df = results["underwriting"]
        lines += [
            "MODULE 2 — UNDERWRITING RISK SCORING",
            "-" * 40,
            f"  Total applicants scored : {len(df):,}",
            f"  Risk score (mean)       : {df['risk_score'].mean():.2f}",
            f"  Risk score (std)        : {df['risk_score'].std():.2f}",
            "",
            "  Underwriting Flag Distribution:",
        ]
        for flag, cnt in df["underwriting_flag"].value_counts().items():
            pct = cnt / len(df) * 100
            lines.append(f"    {flag:<14}: {cnt:>8,}  ({pct:.1f}%)")
        lines += [
            "",
            "  Risk Class Distribution:",
        ]
        for lbl, cnt in df["risk_class_label"].value_counts().items():
            pct = cnt / len(df) * 100
            lines.append(f"    {lbl:<14}: {cnt:>8,}  ({pct:.1f}%)")
        lines.append("")

    lines += ["=" * 60, "  END OF REPORT", "=" * 60]

    summary_path = "outputs/executive_summary.txt"
    with open(summary_path, "w") as f:
        f.write("\n".join(lines))

    print(f"\nExecutive summary saved to: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Healthcare Analytics Agent — Pipeline Runner"
    )
    parser.add_argument(
        "--module",
        choices=["underwriting", "all"],
        default="all",
        help="Which module to run (default: all)",
    )
    args = parser.parse_args()

    # Ensure we run from project root and src/ is on the path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    sys.path.insert(0, script_dir)
    sys.path.insert(0, os.path.join(script_dir, "src"))

    t0 = time.time()
    results = {}

    if args.module in ("underwriting", "all"):
        results["underwriting"] = run_module_underwriting()

    write_executive_summary(results)

    total = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"  ALL MODULES COMPLETE  —  Total elapsed: {total:.1f}s")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
