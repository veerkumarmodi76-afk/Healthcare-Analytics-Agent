import time
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import shap


# ─────────────────────────────────────────────
# PROJECT ROOT (stable across runs)
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_data.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "underwriting" / "underwriting_model.pkl"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "underwriting"


# ─────────────────────────────────────────────
# SAFE SHAP DRIVER EXTRACTOR
# ─────────────────────────────────────────────
def extract_top_features(vals, feature_names):
    """
    Fully safe SHAP feature extractor:
    - prevents index errors
    - handles mismatch between SHAP and feature names
    """

    vals = np.asarray(vals).reshape(-1)

    n = min(len(vals), len(feature_names))  # 🛡️ key fix

    # trim safely
    vals = vals[:n]

    top_idx = np.argsort(np.abs(vals))[-3:][::-1]

    safe_features = []

    for i in top_idx:
        if i < len(feature_names):
            safe_features.append(feature_names[int(i)])
        else:
            safe_features.append(f"feature_{int(i)}")  # fallback label

    return ", ".join(safe_features)


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────
def predict_risk_scores():

    t_start = time.time()

    print("\n" + "=" * 60)
    print("  MODULE 2 — UNDERWRITING RISK SCORING")
    print("=" * 60)

    # ─────────────────────────────────────────────
    # LOAD MODEL
    # ─────────────────────────────────────────────
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    payload = joblib.load(MODEL_PATH)

    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    # ─────────────────────────────────────────────
    # LOAD DATA
    # ─────────────────────────────────────────────
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Input file not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    id_col = "applicant_id"
    if "ID_insured" in df.columns:
        id_col = "ID_insured"
    elif "ID" in df.columns:
        id_col = "ID"
    else:
        df["applicant_id"] = range(len(df))

    X = df[categorical_features + numeric_features].copy()

    # ─────────────────────────────────────────────
    # PREPROCESSING
    # ─────────────────────────────────────────────
    print("Preprocessing input data...")
    X_transformed = preprocessor.transform(X)
    X_df = pd.DataFrame(X_transformed, columns=feature_names)

    # ─────────────────────────────────────────────
    # PREDICTIONS
    # ─────────────────────────────────────────────
    print("Generating predictions...")
    y_pred = model.predict(X_df)
    y_proba = model.predict_proba(X_df)

    # Risk score
    predicted_class = np.argmax(y_proba, axis=1)

    risk_score = predicted_class * 25 + np.max(y_proba, axis=1) * 25

    class_map = {0: "Low", 1: "Medium", 2: "High", 3: "VeryHigh"}
    risk_labels = [class_map[int(i)] for i in y_pred]

    underwriting_flag = [
        "Standard" if i in [0, 1] else "Rated" if i == 2 else "Decline" for i in y_pred
    ]

    # ─────────────────────────────────────────────
    # SHAP (ROBUST VERSION)
    # ─────────────────────────────────────────────
    print("Computing SHAP drivers...")

    SAMPLE_SIZE = min(500, len(X_df))

    sample_idx = np.random.default_rng(42).choice(
        len(X_df), size=SAMPLE_SIZE, replace=False
    )

    X_sample = X_df.iloc[sample_idx]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)

    shap_driver_map = {}

    # ── CASE 1: LIST (old multiclass SHAP)
    if isinstance(shap_values, list):
        for i, idx in enumerate(sample_idx):
            cls = int(y_pred[idx])
            vals = shap_values[cls][i]

            shap_driver_map[idx] = extract_top_features(vals, feature_names)

    else:
        # ── CASE 2: ndarray (binary / new SHAP formats)
        for i, idx in enumerate(sample_idx):
            vals = shap_values[i]

            shap_driver_map[idx] = extract_top_features(vals, feature_names)

    top_drivers = [shap_driver_map.get(i, "see_explain_report") for i in range(len(df))]

    # ─────────────────────────────────────────────
    # OUTPUT
    # ─────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_df = pd.DataFrame({
        "row_id": df[id_col],
        "risk_score": risk_score,
        "risk_class": y_pred,
        "risk_class_label": risk_labels,
        "underwriting_flag": underwriting_flag,
        "shap_top3_drivers": top_drivers,
    })

    out1 = OUTPUT_DIR / "applicant_risk_scores.csv"
    out2 = OUTPUT_DIR / "applicant_risk_scores_backup.csv"

    output_df.to_csv(out1, index=False)
    output_df.to_csv(out2, index=False)

    # ─────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────
    elapsed = time.time() - t_start

    print("\n" + "=" * 60)
    print("  MODULE 2 COMPLETE")
    print("=" * 60)
    print(f"Time: {elapsed:.2f}s")
    print(f"Rows: {len(output_df):,}")
    print(f"Saved:")
    print(f"- {out1}")
    print(f"- {out2}")

    print("\nFlag distribution:")
    print(output_df["underwriting_flag"].value_counts())

    print("\nRisk class distribution:")
    print(output_df["risk_class_label"].value_counts())

    print("=" * 60 + "\n")

    return output_df


if __name__ == "__main__":
    predict_risk_scores()
