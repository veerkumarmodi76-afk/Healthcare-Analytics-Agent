"""
reports.py

Generates business reports for the Lapse Analytics Engine.
"""

import json
from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("outputs/lapse")
MODEL_DIR = Path("models/lapse")

PREDICTIONS = OUTPUT_DIR / "lapse_predictions.csv"
RETENTION = OUTPUT_DIR / "lapse_retention_actions.csv"
FEATURES = MODEL_DIR / "feature_importance.csv"
METRICS = MODEL_DIR / "model_metrics.json"


def load_metrics():

    if METRICS.exists():
        with open(METRICS, "r") as f:
            return json.load(f)

    return {}


def load_feature_importance():

    if FEATURES.exists():
        return pd.read_csv(FEATURES)

    return pd.DataFrame()


def generate_report():

    print("=" * 60)
    print("LAPSE REPORT GENERATOR")
    print("=" * 60)

    predictions = pd.read_csv(PREDICTIONS)
    retention = pd.read_csv(RETENTION)

    metrics = load_metrics()

    features = load_feature_importance()

    total_customers = len(predictions)

    avg_probability = predictions["lapse_probability"].mean()

    segment_counts = {
        str(segment): int(count)
        for segment, count in predictions["risk_segment"].value_counts().items()
    }

    revenue_at_risk = (
        retention["estimated_revenue_loss"].sum()
        if "estimated_revenue_loss" in retention.columns
        else 0
    )

    retention_cost = (
        retention["retention_cost"].sum()
        if "retention_cost" in retention.columns
        else 0
    )

    report = {
    "model_metrics": metrics,
    "customers_processed": int(total_customers),
    "average_lapse_probability": float(round(avg_probability, 4)),
    "risk_distribution": segment_counts,
    "estimated_revenue_at_risk": float(round(revenue_at_risk, 2)),
    "estimated_retention_cost": float(round(retention_cost, 2)),
    "top_features": (
        features.head(10)["feature"].astype(str).tolist()
        if not features.empty
        else []
    ),
    }

    with open(
        OUTPUT_DIR / "lapse_summary.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False,
        )

    markdown = f"""# Lapse Analytics Report

## Model Performance

- Accuracy: {metrics.get("accuracy", "N/A")}
- Precision: {metrics.get("precision", "N/A")}
- Recall: {metrics.get("recall", "N/A")}
- F1 Score: {metrics.get("f1", "N/A")}
- ROC AUC: {metrics.get("roc_auc", "N/A")}

---

## Portfolio Summary

Customers Processed: {total_customers}

Average Lapse Probability: {avg_probability:.4f}

Estimated Revenue at Risk: ₹{revenue_at_risk:,.2f}

Estimated Retention Cost: ₹{retention_cost:,.2f}

---

## Risk Distribution

"""

    for segment, count in segment_counts.items():
        markdown += f"- {segment}: {count}\n"

    markdown += "\n---\n\n## Top Important Features\n\n"

    if not features.empty:
        for _, row in features.head(10).iterrows():
            markdown += f"- {row['feature']} ({row['importance']:.4f})\n"

    else:
        markdown += "- Feature importance unavailable\n"

    markdown += """

---

## Recommended Business Actions

- Prioritize customers in the Critical and High risk segments.
- Focus retention campaigns on customers with the highest expected revenue loss.
- Monitor Medium-risk customers through automated renewal reminders.
- Review feature importance regularly to understand changing lapse drivers.
"""

    with open(
            OUTPUT_DIR / "lapse_summary.md",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(markdown)

    print("Reports generated successfully.")

    return report


if __name__ == "__main__":
    generate_report()
