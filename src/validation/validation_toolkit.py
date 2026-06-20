"""
validation_toolkit.py
-----------------------
YOUR MAIN VALIDATION SCRIPT (Member 6 Role: Model Testing, Benchmarking,
Business Insights)

WHAT THIS DOES:
1. Loads each teammate's prediction file.
2. Tests how accurate each model is (Model Testing).
3. Compares each model against a "dumb baseline" - i.e. what if we just
   guessed the average instead of using AI? This proves whether the AI
   model is actually worth using (Benchmarking).
4. Prints out plain-English business insights you can paste into the
   executive_summary.txt deliverable (Business Insights).

HOW TO RUN:
    python validation_toolkit.py

WHEN REAL FILES ARRIVE FROM TEAMMATES:
    Just change the file paths in the CONFIG section below to point to
    their real CSV files. Nothing else needs to change, AS LONG AS their
    columns are named similarly (predicted_X, actual_X). If their column
    names differ, just rename them in the CONFIG section.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    roc_auc_score, accuracy_score, mean_absolute_error,
    mean_squared_error, r2_score
)

# =====================================================================
# CONFIG - change these paths when real files arrive from teammates
# =====================================================================
RISK_FILE = "sample_data/applicant_risk_scores.csv"
CLAIM_FILE = "sample_data/predicted_claim_cost.csv"
LAPSE_FILE = "sample_data/lapse_risk_scores.csv"

# Decision threshold: above this predicted score, we classify as "high risk"
RISK_THRESHOLD = 0.5
LAPSE_THRESHOLD = 0.5


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# =====================================================================
# 1. VALIDATE UNDERWRITING RISK MODEL (classification problem)
# =====================================================================
def validate_risk_model():
    section("1. UNDERWRITING RISK MODEL VALIDATION")
    df = pd.read_csv(RISK_FILE)

    y_true = df["actual_risk_flag"]
    y_pred_prob = df["predicted_risk_score"]
    y_pred_class = (y_pred_prob >= RISK_THRESHOLD).astype(int)

    # AUC: measures how well the model RANKS risky vs non-risky applicants.
    # 0.5 = no better than coin flip. 1.0 = perfect. Above 0.7 is decent.
    auc = roc_auc_score(y_true, y_pred_prob)

    # Accuracy: % of applicants correctly classified as risky/not risky
    acc = accuracy_score(y_true, y_pred_class)

    # BASELINE: what if we just predicted "everyone is average risk"
    # (i.e. always guess the most common outcome)?
    baseline_pred = np.full_like(y_true, y_true.mode()[0])
    baseline_acc = accuracy_score(y_true, baseline_pred)

    print(f"Model AUC Score:          {auc:.3f}  (closer to 1.0 = better)")
    print(f"Model Accuracy:           {acc:.1%}")
    print(f"Baseline Accuracy:        {baseline_acc:.1%}  (always guessing the majority class)")
    print(f"Improvement over baseline: {(acc - baseline_acc)*100:+.1f} percentage points")

    return {
        "auc": auc, "accuracy": acc, "baseline_accuracy": baseline_acc
    }


# =====================================================================
# 2. VALIDATE CLAIM COST MODEL (regression problem)
# =====================================================================
def validate_claim_cost_model():
    section("2. CLAIM COST PREDICTION MODEL VALIDATION")
    df = pd.read_csv(CLAIM_FILE)

    y_true = df["actual_claim_cost"]
    y_pred = df["predicted_claim_cost"]

    # MAE: average rupee error per prediction (lower = better)
    mae = mean_absolute_error(y_true, y_pred)
    # RMSE: similar to MAE but penalizes big mistakes more heavily
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    # R2: % of variation in claim cost the model successfully explains
    # (1.0 = perfect, 0 = no better than guessing the average for everyone)
    r2 = r2_score(y_true, y_pred)

    # BASELINE: what if we just predicted the average claim cost for everyone?
    baseline_pred = np.full_like(y_true, y_true.mean())
    baseline_mae = mean_absolute_error(y_true, baseline_pred)

    print(f"Model MAE (avg ₹ error):   ₹{mae:,.2f}")
    print(f"Model RMSE:                ₹{rmse:,.2f}")
    print(f"Model R² Score:            {r2:.3f}  (1.0 = perfect fit)")
    print(f"Baseline MAE (guess avg):  ₹{baseline_mae:,.2f}")
    improvement = (1 - mae / baseline_mae) * 100
    print(f"Improvement over baseline: {improvement:+.1f}% lower error")

    return {
        "mae": mae, "rmse": rmse, "r2": r2,
        "baseline_mae": baseline_mae, "improvement_pct": improvement
    }


# =====================================================================
# 3. VALIDATE LAPSE PREDICTION MODEL (classification problem)
# =====================================================================
def validate_lapse_model():
    section("3. LAPSE PREDICTION MODEL VALIDATION")
    df = pd.read_csv(LAPSE_FILE)

    y_true = df["actual_lapse_flag"]
    y_pred_prob = df["predicted_lapse_score"]
    y_pred_class = (y_pred_prob >= LAPSE_THRESHOLD).astype(int)

    auc = roc_auc_score(y_true, y_pred_prob)
    acc = accuracy_score(y_true, y_pred_class)

    baseline_pred = np.full_like(y_true, y_true.mode()[0])
    baseline_acc = accuracy_score(y_true, baseline_pred)

    print(f"Model AUC Score:          {auc:.3f}  (closer to 1.0 = better)")
    print(f"Model Accuracy:           {acc:.1%}")
    print(f"Baseline Accuracy:        {baseline_acc:.1%}  (always guessing the majority class)")
    print(f"Improvement over baseline: {(acc - baseline_acc)*100:+.1f} percentage points")

    return {
        "auc": auc, "accuracy": acc, "baseline_accuracy": baseline_acc
    }


# =====================================================================
# 4. GENERATE BUSINESS INSIGHTS (plain English summary)
# =====================================================================
def generate_business_insights(risk_results, claim_results, lapse_results):
    section("4. BUSINESS INSIGHTS SUMMARY (paste into executive_summary.txt)")

    insights = []

    insights.append(
        f"- The underwriting risk model achieved an AUC of "
        f"{risk_results['auc']:.2f} and accuracy of {risk_results['accuracy']:.1%}, "
        f"outperforming a naive baseline by "
        f"{(risk_results['accuracy']-risk_results['baseline_accuracy'])*100:.1f} "
        f"percentage points, indicating it meaningfully improves applicant "
        f"risk classification over guessing."
    )

    insights.append(
        f"- The claim cost prediction model reduced average prediction "
        f"error by {claim_results['improvement_pct']:.1f}% compared to simply "
        f"using the portfolio average claim cost, with an R² of "
        f"{claim_results['r2']:.2f}, showing strong explanatory power for "
        f"pricing decisions."
    )

    insights.append(
        f"- The lapse prediction model reached an AUC of "
        f"{lapse_results['auc']:.2f}, allowing the business to proactively "
        f"identify at-risk policyholders for retention campaigns rather "
        f"than reacting after lapse occurs."
    )

    for line in insights:
        print(line)

    return insights


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    risk_results = validate_risk_model()
    claim_results = validate_claim_cost_model()
    lapse_results = validate_lapse_model()
    insights = generate_business_insights(risk_results, claim_results, lapse_results)

    section("DONE")
    print("Copy the Business Insights section above into your executive_summary.txt")
