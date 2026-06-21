import os
import time
import joblib
import pandas as pd
import numpy as np
import shap
from xgboost import XGBClassifier

# Resolve project root relative to this file for robust path handling
PROJECT_ROOT = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if "__file__" in dir()
    else os.getcwd()
)


def predict_risk_scores(
    input_path="data/processed/processed_data.csv", output_dir="outputs"
):
    t_start = time.time()
    print(f"\n{'=' * 60}")
    print(f"  MODULE 2 — UNDERWRITING RISK SCORING")
    print(f"{'=' * 60}")
    print(f"Loading model payload...")
    model_path = "models/underwriting_model.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Trained model not found at {model_path}. Please run train.py first."
        )

    payload = joblib.load(model_path)
    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    print(f"Loading input dataset from {input_path}...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at {input_path}")

    df = pd.read_csv(input_path)

    # Check if applicant ID exists
    if "ID_insured" in df.columns:
        applicant_id_col = "ID_insured"
    elif "ID" in df.columns:
        applicant_id_col = "ID"
    else:
        # Create a sequential ID if not found
        df["applicant_id"] = range(len(df))
        applicant_id_col = "applicant_id"

    X = df[categorical_features + numeric_features].copy()

    print("Preprocessing input data...")
    X_transformed = preprocessor.transform(X)
    X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names)

    print("Generating predictions...")
    y_pred = model.predict(X_transformed_df)
    y_pred_proba = model.predict_proba(X_transformed_df)

    # Calculate composite risk score: (p_0 * 0 + p_1 * 1/3 + p_2 * 2/3 + p_3 * 1.0) * 100
    print("Computing probability-weighted risk scores...")
    risk_score = (
        y_pred_proba[:, 0] * 0.0
        + y_pred_proba[:, 1] * (1.0 / 3.0)
        + y_pred_proba[:, 2] * (2.0 / 3.0)
        + y_pred_proba[:, 3] * 1.0
    ) * 100.0

    # Map class index to risk class label
    class_map = {0: "Low", 1: "Medium", 2: "High", 3: "VeryHigh"}
    risk_class_labels = [class_map[val] for val in y_pred]

    # Underwriting flags: Low/Medium -> Standard, High -> Rated, VeryHigh -> Decline
    print("Segmenting applicants into Standard / Rated / Decline flags...")
    underwriting_flag = []
    for val in y_pred:
        if val in [0, 1]:
            underwriting_flag.append("Standard")
        elif val == 2:
            underwriting_flag.append("Rated")
        else:
            underwriting_flag.append("Decline")

    # Calculate SHAP top-3 drivers on a representative sample (fast).
    # Full-population SHAP is generated separately in explain.py (1K sample).
    SHAP_SAMPLE_SIZE = 500
    print(
        f"Calculating SHAP top-3 drivers on {SHAP_SAMPLE_SIZE}-row sample "
        f"(full explainability in explain.py)..."
    )
    sample_idx = np.random.default_rng(42).choice(
        len(X_transformed_df), size=min(SHAP_SAMPLE_SIZE, len(X_transformed_df)), replace=False
    )
    X_shap_sample = X_transformed_df.iloc[sample_idx]
    y_shap_sample = y_pred[sample_idx]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_shap_sample)

    # Get SHAP values for the predicted class on the sample
    shap_for_sample = np.zeros((len(sample_idx), len(feature_names)))
    if isinstance(shap_values, list):
        for c in range(4):
            mask = y_shap_sample == c
            if mask.any():
                shap_for_sample[mask] = shap_values[c][mask]
    else:
        if len(shap_values.shape) == 3:
            shap_for_sample = shap_values[np.arange(len(sample_idx)), :, y_shap_sample]
        else:
            shap_for_sample = shap_values

    # Build lookup: original row index -> top-3 driver string
    shap_driver_map = {}
    for k, orig_i in enumerate(sample_idx):
        abs_shap = np.abs(shap_for_sample[k])
        top_indices = np.argsort(abs_shap)[::-1][:3]
        top_feats = [feature_names[idx] for idx in top_indices]
        shap_driver_map[orig_i] = ", ".join(top_feats)

    print("Filling SHAP top-3 drivers for all applicants...")
    top_drivers = [
        shap_driver_map.get(i, "see_explain_report")
        for i in range(len(y_pred))
    ]

    # Build final output DataFrame
    output_df = pd.DataFrame({
        "applicant_id": df[applicant_id_col],
        "risk_score": risk_score,
        "risk_class": y_pred,  # numeric class (0, 1, 2, 3) as per Page 12 acceptance criteria
        "risk_class_label": risk_class_labels,
        "underwriting_flag": underwriting_flag,
        "shap_top3_drivers": top_drivers,
    })

    # Ensure target directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "underwriting"), exist_ok=True)

    # Define file paths
    path1 = os.path.join(output_dir, "applicant_risk_scores.csv")
    path2 = os.path.join(output_dir, "underwriting", "applicant_risk_scores.csv")

    output_df.to_csv(path1, index=False)
    output_df.to_csv(path2, index=False)

    elapsed = time.time() - t_start
    print(f"\n{'=' * 60}")
    print(f"  MODULE 2 — RISK SCORING COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Elapsed time   : {elapsed:.1f}s")
    print(f"  Output rows    : {len(output_df):,}")
    print(
        f"  Risk score     : mean={output_df['risk_score'].mean():.2f}, "
        f"std={output_df['risk_score'].std():.2f}"
    )
    print(f"  Saved to       : {path1}")
    print(f"  Saved to       : {path2}")
    print(f"\n  Underwriting Flag Distribution:")
    for flag, cnt in output_df["underwriting_flag"].value_counts().items():
        pct = cnt / len(output_df) * 100
        print(f"    {flag:<12}: {cnt:>8,}  ({pct:.1f}%)")
    print(f"\n  Risk Class Distribution:")
    for lbl, cnt in output_df["risk_class_label"].value_counts().items():
        pct = cnt / len(output_df) * 100
        print(f"    {lbl:<12}: {cnt:>8,}  ({pct:.1f}%)")
    print(f"{'=' * 60}\n")

    return output_df


if __name__ == "__main__":
    predict_risk_scores()
