"""
evaluation.py
-------------

Utilities for evaluating lapse prediction models.

Outputs
-------
outputs/lapse/
    confusion_matrix.csv
    classification_report.txt
    roc_curve.csv

models/lapse/
    model_metrics.json
"""

import json
from pathlib import Path

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
)


OUTPUT_DIR = Path("outputs/lapse")
MODEL_DIR = Path("models/lapse")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)


###############################################################################
# Metric Calculation
###############################################################################


def calculate_metrics(
    y_true,
    y_pred,
    y_probability,
):
    """
    Compute evaluation metrics.
    """

    return {
        "accuracy": round(
            accuracy_score(y_true, y_pred),
            4,
        ),
        "precision": round(
            precision_score(y_true, y_pred),
            4,
        ),
        "recall": round(
            recall_score(y_true, y_pred),
            4,
        ),
        "f1": round(
            f1_score(y_true, y_pred),
            4,
        ),
        "roc_auc": round(
            roc_auc_score(
                y_true,
                y_probability,
            ),
            4,
        ),
    }


###############################################################################
# Evaluation Pipeline
###############################################################################


def evaluate_predictions(
    y_true,
    y_pred,
    y_probability,
):
    """
    Complete evaluation pipeline.

    Returns
    -------
    metrics : dict
    report : str
    matrix_df : pd.DataFrame
    roc_df : pd.DataFrame
    """

    ###########################################################################
    # Metrics
    ###########################################################################

    metrics = calculate_metrics(
        y_true,
        y_pred,
        y_probability,
    )

    with open(
        MODEL_DIR / "model_metrics.json",
        "w",
    ) as f:
        json.dump(
            metrics,
            f,
            indent=4,
        )

    ###########################################################################
    # Classification Report
    ###########################################################################

    report = classification_report(
        y_true,
        y_pred,
    )

    with open(
        OUTPUT_DIR / "classification_report.txt",
        "w",
    ) as f:
        f.write(report)

    ###########################################################################
    # Confusion Matrix
    ###########################################################################

    matrix = confusion_matrix(
        y_true,
        y_pred,
    )

    matrix_df = pd.DataFrame(
        matrix,
        index=[
            "Actual_0",
            "Actual_1",
        ],
        columns=[
            "Predicted_0",
            "Predicted_1",
        ],
    )

    matrix_df.to_csv(
        OUTPUT_DIR / "confusion_matrix.csv",
        index=True,
    )

    ###########################################################################
    # ROC Curve
    ###########################################################################

    fpr, tpr, thresholds = roc_curve(
        y_true,
        y_probability,
    )

    roc_df = pd.DataFrame({
        "threshold": thresholds,
        "false_positive_rate": fpr,
        "true_positive_rate": tpr,
    })

    roc_df.to_csv(
        OUTPUT_DIR / "roc_curve.csv",
        index=False,
    )

    ###########################################################################
    # Console Output
    ###########################################################################

    print("\nModel Performance")
    print("-" * 30)

    for key, value in metrics.items():
        print(f"{key:12}: {value:.4f}")

    print("\nClassification Report")
    print(report)

    ###########################################################################
    # Return Everything Needed by train.py
    ###########################################################################

    return (
        metrics,
        report,
        matrix_df,
        roc_df,
    )
