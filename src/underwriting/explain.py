import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap


# ─────────────────────────────────────────────
# PROJECT ROOT (stable, no cwd dependency)
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_data.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "underwriting" / "underwriting_model.pkl"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
UNDERWRITING_DIR = OUTPUT_DIR / "underwriting"


# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
def load_payload():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run train.py first.")
    return joblib.load(MODEL_PATH)


# ─────────────────────────────────────────────
# GLOBAL SHAP (SUMMARY PLOT)
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

    sample_size = min(sample_size, len(df))
    df_sample = df.sample(sample_size, random_state=42)

    X = df_sample[categorical_features + numeric_features]
    X_transformed = preprocessor.transform(X)
    X_df = pd.DataFrame(X_transformed, columns=feature_names)

    print("Computing SHAP values...")

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_df)

    # ─────────────────────────────────────────────
    # OUTPUT DIRS (NO NESTING EVER)
    # ─────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    UNDERWRITING_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating SHAP summary plot...")

    plt.figure(figsize=(10, 8))

    # multiclass-safe handling
    shap.summary_plot(
        shap_values, X_df, feature_names=feature_names, show=False, max_display=15
    )

    plt.title("Global SHAP Feature Importance", fontsize=13)
    plt.tight_layout()

    out1 = OUTPUT_DIR / "shap_summary.png"
    out2 = UNDERWRITING_DIR / "shap_summary.png"

    plt.savefig(out1, dpi=300)
    plt.savefig(out2, dpi=300)
    plt.close()

    print(f"Saved global SHAP plots:")
    print(f"- {out1}")
    print(f"- {out2}")

    return shap_values, feature_names


# ─────────────────────────────────────────────
# LOCAL SHAP (WATERFALL)
# ─────────────────────────────────────────────
def generate_local_shap_plot(applicant_idx):
    print(f"Generating local SHAP for index {applicant_idx}...")

    payload = load_payload()
    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    df = pd.read_csv(DATA_PATH)

    if applicant_idx < 0 or applicant_idx >= len(df):
        raise ValueError("Invalid applicant index")

    row = df.iloc[[applicant_idx]]
    X = row[categorical_features + numeric_features]

    X_transformed = preprocessor.transform(X)
    X_df = pd.DataFrame(X_transformed, columns=feature_names)

    pred_class = model.predict(X_df)[0]
    proba = model.predict_proba(X_df)[0]

    class_names = {0: "Low", 1: "Medium", 2: "High", 3: "VeryHigh"}
    class_name = class_names[pred_class]

    print(f"Predicted class: {class_name} ({proba[pred_class]:.4f})")

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_df)

    # ─────────────────────────────────────────────
    # SAFE MULTICLASS EXTRACTION
    # ─────────────────────────────────────────────
    if isinstance(shap_values, list):
        sv = shap_values[pred_class][0]
    else:
        sv = shap_values[0, :, pred_class]

    base_value = explainer.expected_value
    if isinstance(base_value, (list, np.ndarray)):
        base_value = base_value[pred_class]

    # ─────────────────────────────────────────────
    # OUTPUT DIRS
    # ─────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    UNDERWRITING_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating waterfall plot...")

    plt.figure(figsize=(10, 6))

    shap.waterfall_plot(
        shap.Explanation(
            values=sv,
            base_values=base_value,
            data=X_df.iloc[0].values,
            feature_names=feature_names,
        ),
        show=False,
    )

    plt.title(
        f"SHAP Explanation - Applicant {applicant_idx} ({class_name})", fontsize=12
    )

    plt.tight_layout()

    out1 = OUTPUT_DIR / f"applicant_{applicant_idx}_waterfall.png"
    out2 = UNDERWRITING_DIR / f"applicant_{applicant_idx}_waterfall.png"

    plt.savefig(out1, dpi=300)
    plt.savefig(out2, dpi=300)
    plt.close()

    print(f"Saved local SHAP plots:")
    print(f"- {out1}")
    print(f"- {out2}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    generate_global_shap_plots()
    generate_local_shap_plot(0)
