import time
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import shap


# ─────────────────────────────────────────────
# PROJECT ROOT
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_data.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "underwriting" / "underwriting_model.pkl"

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "underwriting"
PREDICTION_FILE = OUTPUT_DIR / "underwriting_predictions.csv"


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
RISK_CLASS_MAP = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "VeryHigh",
}

DECISION_MAP = {
    "Low": "Standard",
    "Medium": "Standard",
    "High": "Rated",
    "VeryHigh": "Decline",
}

RISK_WEIGHTS = np.array([25, 50, 75, 100])


# ─────────────────────────────────────────────
# LOAD MODEL PAYLOAD
# ─────────────────────────────────────────────
def load_payload():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    return joblib.load(MODEL_PATH)


# ─────────────────────────────────────────────
# SAFE SHAP DRIVER EXTRACTION
# ─────────────────────────────────────────────
def extract_top_features(vals, feature_names):

    vals = np.asarray(vals).reshape(-1)

    n = min(
        len(vals),
        len(feature_names),
    )

    vals = vals[:n]

    top_idx = np.argsort(np.abs(vals))[-3:][::-1]

    features = []

    for idx in top_idx:
        if idx < len(feature_names):
            features.append(feature_names[int(idx)])
        else:
            features.append(f"feature_{int(idx)}")

    return ", ".join(features)


# ─────────────────────────────────────────────
# SINGLE APPLICANT PREDICTION
# ─────────────────────────────────────────────
def predict_applicant(applicant_dict):

    payload = load_payload()

    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    applicant_df = pd.DataFrame([applicant_dict])

    X = applicant_df[categorical_features + numeric_features]

    X_transformed = preprocessor.transform(X)

    X_df = pd.DataFrame(
        X_transformed,
        columns=feature_names,
    )

    y_pred = model.predict(X_df)[0]

    y_proba = model.predict_proba(X_df)[0]

    risk_class = RISK_CLASS_MAP[int(y_pred)]

    risk_score = float(
        np.dot(
            y_proba,
            RISK_WEIGHTS,
        )
    )

    confidence = float(np.max(y_proba))

    decision = DECISION_MAP[risk_class]

    # SHAP
    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_df)

    if isinstance(shap_values, list):
        vals = shap_values[int(y_pred)][0]

    else:
        vals = shap_values[0]

        if vals.ndim == 2:
            vals = vals[:, int(y_pred)]

    top_drivers = extract_top_features(
        vals,
        feature_names,
    )

    return {
        "risk_class": risk_class,
        "risk_score": round(risk_score, 2),
        "decision": decision,
        "confidence": round(confidence, 4),
        "top_drivers": top_drivers,
    }


# ─────────────────────────────────────────────
# BATCH PREDICTION
# ─────────────────────────────────────────────
def predict_underwriting():

    t_start = time.time()

    print("\n" + "=" * 60)
    print("UNDERWRITING PREDICTION ENGINE")
    print("=" * 60)

    payload = load_payload()

    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Input file not found at {DATA_PATH}")

    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH)

    # ─────────────────────────────────────────────
    # ROW IDENTIFIER
    # ─────────────────────────────────────────────
    row_id = pd.Series(
        range(len(df)),
        name="row_id",
    )
    # ─────────────────────────────────────────────
    # PREPROCESS
    # ─────────────────────────────────────────────
    X = df[categorical_features + numeric_features].copy()

    print("Transforming features...")

    X_transformed = preprocessor.transform(X)

    X_df = pd.DataFrame(
        X_transformed,
        columns=feature_names,
    )

    # ─────────────────────────────────────────────
    # PREDICTIONS
    # ─────────────────────────────────────────────
    print("Generating predictions...")

    y_pred = model.predict(X_df)

    y_proba = model.predict_proba(X_df)

    risk_class = [RISK_CLASS_MAP[int(x)] for x in y_pred]

    confidence = np.max(
        y_proba,
        axis=1,
    )

    risk_score = np.dot(
        y_proba,
        RISK_WEIGHTS,
    )

    decisions = [DECISION_MAP[x] for x in risk_class]

    # ─────────────────────────────────────────────
    # SHAP DRIVERS
    # ─────────────────────────────────────────────
    print("Computing SHAP drivers...")

    sample_size = min(
        500,
        len(X_df),
    )

    rng = np.random.default_rng(42)

    sample_idx = rng.choice(
        len(X_df),
        size=sample_size,
        replace=False,
    )

    X_sample = X_df.iloc[sample_idx]

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_sample)

    shap_driver_map = {}

    if isinstance(shap_values, list):
        for pos, idx in enumerate(sample_idx):
            pred_class = int(y_pred[idx])

            vals = shap_values[pred_class][pos]

            shap_driver_map[idx] = extract_top_features(
                vals,
                feature_names,
            )

    else:
        for pos, idx in enumerate(sample_idx):
            vals = shap_values[pos]

            shap_driver_map[idx] = extract_top_features(
                vals,
                feature_names,
            )

    top_drivers = [
        shap_driver_map.get(
            i,
            "see_explain_report",
        )
        for i in range(len(df))
    ]

    # ─────────────────────────────────────────────
    # OUTPUT DATASET
    # ─────────────────────────────────────────────
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_df = pd.DataFrame({
        "row_id": row_id,
        "risk_score": np.round(
            risk_score,
            2,
        ),
        "risk_class_label": risk_class,
        "underwriting_flag": decisions,
        "confidence": np.round(
            confidence,
            4,
        ),
        "top_drivers": top_drivers,
    })

    output_df.to_csv(
        PREDICTION_FILE,
        index=False,
    )

    elapsed = time.time() - t_start

    # ─────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PREDICTION COMPLETE")
    print("=" * 60)

    print(f"Rows Processed : {len(output_df):,}")

    print(f"Time Taken     : {elapsed:.2f}s")

    print(f"Output File    : {PREDICTION_FILE}")

    print("\nDecision Distribution:")

    print(output_df["underwriting_flag"].value_counts())

    print("\nRisk Distribution:")

    print(output_df["risk_class_label"].value_counts())

    print("=" * 60)

    return output_df


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    predict_underwriting()
