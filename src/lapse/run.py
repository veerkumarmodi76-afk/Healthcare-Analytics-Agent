"""
Lapse Analytics Engine
----------------------
Pipeline Runner

Workflow
--------
1. Train Model
2. Predict Lapse Probability
3. Generate Retention Actions
4. Generate Business Reports

Outputs
-------
models/lapse/
outputs/lapse/
"""

import time

from .train import train_lapse_model
from .predict import predict_lapse
from .retention import generate_retention_actions
from .reports import generate_report


def run():

    print("=" * 70)
    print("LAPSE ANALYTICS ENGINE")
    print("=" * 70)

    start_time = time.time()

    # ------------------------------------------------------------------
    # Step 1 : Model Training
    # ------------------------------------------------------------------

    print("\n[1/4] Training Lapse Model...\n")
    train_lapse_model()

    # ------------------------------------------------------------------
    # Step 2 : Portfolio Prediction
    # ------------------------------------------------------------------

    print("\n[2/4] Generating Predictions...\n")
    predictions = predict_lapse()

    # ------------------------------------------------------------------
    # Step 3 : Retention Analytics
    # ------------------------------------------------------------------

    print("\n[3/4] Generating Retention Actions...\n")
    retention_report = generate_retention_actions()

    # ------------------------------------------------------------------
    # Step 4 : Business Report Generation
    # ------------------------------------------------------------------

    print("\n[4/4] Generating Reports...\n")
    report = generate_report()

    elapsed = time.time() - start_time

    print("\n" + "=" * 70)
    print("LAPSE ANALYTICS PIPELINE COMPLETED")
    print("=" * 70)

    print(f"Execution Time           : {elapsed:.2f} seconds")
    print(f"Customers Processed      : {len(predictions):,}")
    print(f"Average Lapse Probability: {report['average_lapse_probability']:.4f}")
    print(f"Estimated Revenue at Risk: ₹{report['estimated_revenue_at_risk']:,.2f}")
    print(f"Estimated Retention Cost : ₹{report['estimated_retention_cost']:,.2f}")

    print("\nRisk Segment Distribution")
    print(retention_report["risk_segment"].value_counts().to_string())

    print("\nTop Recommended Actions")
    print(retention_report["recommended_action"].value_counts().to_string())

    print("\nReports Generated Successfully")
    print("  lapse_summary.md")
    print("  lapse_summary.json")

    print("\nGenerated Artifacts")

    print("\nmodels/lapse/")
    print("  lapse_model.pkl")
    print("  feature_importance.csv")
    print("  model_metrics.json")
    print("  shap_summary.csv")

    print("\noutputs/lapse/")
    print("  lapse_predictions.csv")
    print("  lapse_retention_actions.csv")
    print("  classification_report.txt")
    print("  confusion_matrix.csv")
    print("  roc_curve.csv")
    print("  lapse_summary.md")
    print("  lapse_summary.json")

    print("\nPipeline Status : SUCCESS")
    print("=" * 70)

    return {
        "predictions": predictions,
        "retention_report": retention_report,
        "report": report,
        "execution_time": elapsed,
    }


if __name__ == "__main__":
    run()