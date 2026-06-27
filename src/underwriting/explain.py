import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import shap


# ─────────────────────────────────────────────
# PROJECT ROOT
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_data.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "underwriting" / "underwriting_model.pkl"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "underwriting"

GLOBAL_SHAP_PNG = OUTPUT_DIR / "shap_summary.png"
GLOBAL_SHAP_CSV = OUTPUT_DIR / "feature_importance_shap.csv"

LOCAL_EXPLANATION_CSV = OUTPUT_DIR / "applicant_explanation.csv"
LOCAL_EXPLANATION_JSON = OUTPUT_DIR / "applicant_explanation.json"


# ─────────────────────────────────────────────
# LOAD MODEL PAYLOAD
# ─────────────────────────────────────────────
def load_payload():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    return joblib.load(MODEL_PATH)


# ─────────────────────────────────────────────
# GLOBAL SHAP ANALYSIS
# ─────────────────────────────────────────────
def generate_global_shap_plots(sample_size=1000):

    print("Loading model and data...")

    payload = load_payload()

    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    df = pd.read_csv(DATA_PATH)

    sample_size = min(
        sample_size,
        len(df),
    )

    df_sample = df.sample(
        sample_size,
        random_state=42,
    )

    X = df_sample[categorical_features + numeric_features]

    X_transformed = preprocessor.transform(X)

    X_df = pd.DataFrame(
        X_transformed,
        columns=feature_names,
    )

    print("Computing SHAP values...")

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ─────────────────────────────────────────────
    # SHAP SUMMARY PLOT
    # ─────────────────────────────────────────────
    print("Generating SHAP summary plot...")

    plt.figure(figsize=(10, 8))

    shap.summary_plot(
        shap_values,
        X_df,
        feature_names=feature_names,
        show=False,
        max_display=15,
    )

    plt.title(
        "Global SHAP Feature Importance",
        fontsize=13,
    )

    plt.tight_layout()

    plt.savefig(
        GLOBAL_SHAP_PNG,
        dpi=300,
    )

    plt.close()

    # ─────────────────────────────────────────────
    # SHAP FEATURE IMPORTANCE CSV
    # ─────────────────────────────────────────────
    print("Generating SHAP importance table...")

    if isinstance(shap_values, list):
        mean_abs_shap = np.mean(
            [np.abs(class_values) for class_values in shap_values],
            axis=(0, 1),
        )

    elif shap_values.ndim == 3:
        mean_abs_shap = np.mean(
            np.abs(shap_values),
            axis=(0, 2),
        )

    else:
        mean_abs_shap = np.mean(
            np.abs(shap_values),
            axis=0,
        )

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "mean_abs_shap": mean_abs_shap,
    })

    importance_df = importance_df.sort_values(
        "mean_abs_shap",
        ascending=False,
    ).reset_index(drop=True)

    importance_df["rank"] = importance_df.index + 1

    importance_df.to_csv(
        GLOBAL_SHAP_CSV,
        index=False,
    )

    print(f"Saved: {GLOBAL_SHAP_PNG}")
    print(f"Saved: {GLOBAL_SHAP_CSV}")

    return shap_values, feature_names


# ─────────────────────────────────────────────
# LOCAL APPLICANT EXPLANATION
# ─────────────────────────────────────────────
def generate_local_shap_plot(applicant_idx=0):

    print(f"Generating explanation for applicant {applicant_idx}")

    payload = load_payload()

    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    df = pd.read_csv(DATA_PATH)

    if applicant_idx >= len(df):
        raise ValueError(f"Applicant index out of range: {applicant_idx}")

    row = df.iloc[[applicant_idx]]

    X = row[categorical_features + numeric_features]

    X_transformed = preprocessor.transform(X)

    X_df = pd.DataFrame(
        X_transformed,
        columns=feature_names,
    )

    pred_class = model.predict(X_df)[0]

    proba = model.predict_proba(X_df)[0]

    class_map = {
        0: "Low",
        1: "Medium",
        2: "High",
        3: "VeryHigh",
    }

    risk_class = class_map[int(pred_class)]

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_df)

    # ─────────────────────────────────────────────
    # MULTICLASS SAFE EXTRACTION
    # ─────────────────────────────────────────────
    if isinstance(shap_values, list):
        local_shap = shap_values[int(pred_class)][0]

    elif shap_values.ndim == 3:
        local_shap = shap_values[0, :, int(pred_class)]

    else:
        local_shap = shap_values[0]

    base_value = explainer.expected_value

    if isinstance(
        base_value,
        (list, np.ndarray),
    ):
        base_value = base_value[int(pred_class)]

    # ─────────────────────────────────────────────
    # WATERFALL PLOT
    # ─────────────────────────────────────────────
    waterfall_file = OUTPUT_DIR / f"applicant_{applicant_idx}_waterfall.png"

    plt.figure(figsize=(10, 6))

    shap.waterfall_plot(
        shap.Explanation(
            values=local_shap,
            base_values=base_value,
            data=X_df.iloc[0].values,
            feature_names=feature_names,
        ),
        show=False,
    )

    plt.title(
        f"Applicant {applicant_idx} - {risk_class}",
        fontsize=12,
    )

    plt.tight_layout()

    plt.savefig(
        waterfall_file,
        dpi=300,
    )

    plt.close()

    # ─────────────────────────────────────────────
    # LOCAL EXPLANATION CSV
    # ─────────────────────────────────────────────
    explanation_df = pd.DataFrame({
        "feature": feature_names,
        "impact": local_shap,
    })

    explanation_df["direction"] = np.where(
        explanation_df["impact"] >= 0,
        "Increase Risk",
        "Decrease Risk",
    )

    explanation_df["abs_impact"] = explanation_df["impact"].abs()

    explanation_df = explanation_df.sort_values(
        "abs_impact",
        ascending=False,
    ).drop(columns=["abs_impact"])

    explanation_df.to_csv(
        LOCAL_EXPLANATION_CSV,
        index=False,
    )

    # ─────────────────────────────────────────────
    # COPILOT JSON
    # ─────────────────────────────────────────────
    top_features = explanation_df.head(10).to_dict(orient="records")

    explanation_json = {
        "applicant_index": int(applicant_idx),
        "predicted_risk_class": risk_class,
        "confidence": float(np.max(proba)),
        "top_explanations": top_features,
    }

    with open(
        LOCAL_EXPLANATION_JSON,
        "w",
    ) as f:
        json.dump(
            explanation_json,
            f,
            indent=4,
        )

    print(f"Saved: {waterfall_file}")
    print(f"Saved: {LOCAL_EXPLANATION_CSV}")
    print(f"Saved: {LOCAL_EXPLANATION_JSON}")

    return explanation_df


# ─────────────────────────────────────────────
# COPILOT HELPER
# ─────────────────────────────────────────────
def get_applicant_explanation(applicant_idx=0):

    generate_local_shap_plot(applicant_idx)

    with open(
        LOCAL_EXPLANATION_JSON,
        "r",
    ) as f:
        return json.load(f)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    generate_global_shap_plots()

    generate_local_shap_plot(0)
