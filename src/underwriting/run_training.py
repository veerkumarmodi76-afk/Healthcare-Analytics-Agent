import json
import pandas as pd
from pathlib import Path

from .train import train_underwriting_model
from .predict import predict_underwriting
from .explain import (
    generate_global_shap_plots,
    generate_local_shap_plot,
)


# ─────────────────────────────────────────────
# PROJECT ROOT
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "underwriting"

PREDICTIONS_FILE = OUTPUT_DIR / "underwriting_predictions.csv"

SUMMARY_FILE = OUTPUT_DIR / "underwriting_summary.json"


# ─────────────────────────────────────────────
# UNDERWRITING SUMMARY
# ─────────────────────────────────────────────
def generate_underwriting_report():

    print("\nGenerating underwriting summary...")

    if not PREDICTIONS_FILE.exists():
        raise FileNotFoundError(f"Prediction file not found: {PREDICTIONS_FILE}")

    df = pd.read_csv(PREDICTIONS_FILE)

    total_applicants = len(df)

    risk_distribution = df["risk_class_label"].value_counts(normalize=True) * 100

    decision_distribution = df["underwriting_flag"].value_counts(normalize=True) * 100

    summary = {
        "total_applicants": int(total_applicants),
        "low_risk_pct": round(
            float(risk_distribution.get("Low", 0)),
            2,
        ),
        "medium_risk_pct": round(
            float(risk_distribution.get("Medium", 0)),
            2,
        ),
        "high_risk_pct": round(
            float(risk_distribution.get("High", 0)),
            2,
        ),
        "veryhigh_risk_pct": round(
            float(risk_distribution.get("VeryHigh", 0)),
            2,
        ),
        "standard_pct": round(
            float(
                decision_distribution.get(
                    "Standard",
                    0,
                )
            ),
            2,
        ),
        "rated_pct": round(
            float(
                decision_distribution.get(
                    "Rated",
                    0,
                )
            ),
            2,
        ),
        "decline_pct": round(
            float(
                decision_distribution.get(
                    "Decline",
                    0,
                )
            ),
            2,
        ),
        "average_risk_score": round(
            float(df["risk_score"].mean()),
            2,
        ),
        "average_confidence": round(
            float(df["confidence"].mean()),
            4,
        ),
    }

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        SUMMARY_FILE,
        "w",
    ) as f:
        json.dump(
            summary,
            f,
            indent=4,
        )

    print(f"Summary saved: {SUMMARY_FILE}")

    return summary


# ─────────────────────────────────────────────
# MASTER UNDERWRITING PIPELINE
# ─────────────────────────────────────────────
def run():

    print("\n" + "=" * 70)
    print("UNDERWRITING ANALYTICS PIPELINE")
    print("=" * 70)

    # Step 1
    train_underwriting_model()

    # Step 2
    predict_underwriting()

    # Step 3
    generate_global_shap_plots()

    # Step 4
    generate_local_shap_plot(0)

    # Step 5
    generate_underwriting_report()

    print("\n" + "=" * 70)
    print("UNDERWRITING PIPELINE COMPLETE")
    print("=" * 70)

    print("\nArtifacts Generated:")

    print(
        "\nTraining:"
        "\n- underwriting_model.pkl"
        "\n- feature_importance.csv"
        "\n- training_metrics.json"
        "\n- confusion_matrix.csv"
        "\n- class_distribution.csv"
    )

    print("\nPredictions:\n- underwriting_predictions.csv")

    print(
        "\nExplainability:"
        "\n- shap_summary.png"
        "\n- feature_importance_shap.csv"
        "\n- applicant_explanation.csv"
        "\n- applicant_explanation.json"
        "\n- applicant_0_waterfall.png"
    )

    print("\nGovernance:\n- rule_distribution.csv\n- underwriting_summary.json")

    print("=" * 70)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    run()
  
