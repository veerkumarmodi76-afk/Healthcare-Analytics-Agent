import os
import joblib
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")  # Headless backend to prevent GUI issues
import matplotlib.pyplot as plt
import shap


def load_payload():
    model_path = "models/underwriting_model.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Trained model not found at {model_path}. Please run train.py first."
        )
    return joblib.load(model_path)


def generate_global_shap_plots(
    input_path="data/processed/processed_data.csv",
    output_dir="outputs",
    sample_size=1000,
):
    print("Loading model payload and input data...")
    payload = load_payload()
    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    df = pd.read_csv(input_path)

    # Take a representative subsample of size 1000 for SHAP speed
    print(f"Sampling {sample_size} rows for SHAP explanation...")
    df_sample = df.sample(n=sample_size, random_state=42).copy()

    X = df_sample[categorical_features + numeric_features].copy()
    X_transformed = preprocessor.transform(X)
    X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names)

    print("Computing SHAP values (raw arrays for multiclass)...")
    explainer = shap.TreeExplainer(model)
    # shap_values is a list of 4 arrays: one per class, each (n_samples, n_features)
    shap_values = explainer.shap_values(X_transformed_df)

    # Ensure output directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "underwriting"), exist_ok=True)

    class_names = ["Low", "Medium", "High", "VeryHigh"]

    # ── Plot 1: Combined mean |SHAP| across all classes ──────────────
    print("Generating global SHAP summary bar plot (all classes)...")
    # Average absolute SHAP values across all classes → shape (n_features,)
    mean_abs_shap = np.mean([np.abs(sv) for sv in shap_values], axis=0)

    plt.figure(figsize=(10, 8))
    shap.summary_plot(
        shap_values,
        X_transformed_df,
        feature_names=feature_names,
        class_names=class_names,
        plot_type="bar",
        max_display=15,
        show=False,
    )
    plt.title("Global Feature Importance (mean |SHAP|, all classes)", fontsize=13, pad=12)
    plt.tight_layout()

    path1 = os.path.join(output_dir, "shap_summary.png")
    path2 = os.path.join(output_dir, "underwriting", "shap_summary.png")

    plt.savefig(path1, dpi=300)
    plt.savefig(path2, dpi=300)
    plt.close()

    print(f"Saved global SHAP plots to:\n- {path1}\n- {path2}")
    return shap_values, feature_names


def generate_local_shap_plot(
    applicant_idx, input_path="data/processed/processed_data.csv", output_dir="outputs"
):
    payload = load_payload()
    model = payload["model"]
    preprocessor = payload["preprocessor"]
    feature_names = payload["feature_names"]
    categorical_features = payload["categorical_features"]
    numeric_features = payload["numeric_features"]

    df = pd.read_csv(input_path)

    if applicant_idx < 0 or applicant_idx >= len(df):
        raise ValueError(
            f"applicant_idx {applicant_idx} is out of bounds for dataset of size {len(df)}"
        )

    row = df.iloc[[applicant_idx]].copy()
    X = row[categorical_features + numeric_features].copy()
    X_transformed = preprocessor.transform(X)
    X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names)

    # Get prediction class and proba
    pred_class = model.predict(X_transformed_df)[0]
    pred_proba = model.predict_proba(X_transformed_df)[0]
    class_name = {0: "Low", 1: "Medium", 2: "High", 3: "VeryHigh"}[pred_class]

    print(f"Generating local SHAP explanation for applicant index {applicant_idx}...")
    print(f"Predicted class: {class_name} (Prob: {pred_proba[pred_class]:.4f})")

    explainer = shap.TreeExplainer(model)
    # TreeExplainer output varies by input size:
    #   multi-row  → list of arrays, one per class, each (n_samples, n_features)
    #   single-row → 3-D ndarray (n_samples, n_features, n_classes)
    shap_values = explainer.shap_values(X_transformed_df)

    if isinstance(shap_values, list):
        # list[class] → (n_samples, n_features)
        sv_for_class = shap_values[pred_class][0]
    else:
        # ndarray shape (n_samples, n_features, n_classes)
        sv_for_class = shap_values[0, :, pred_class]

    expected_val = explainer.expected_value
    if isinstance(expected_val, (list, np.ndarray)):
        expected_val = expected_val[pred_class]

    # Generate waterfall plot using low-level API (stable for multiclass)
    plt.figure(figsize=(10, 6))
    shap.waterfall_plot(
        shap.Explanation(
            values=sv_for_class,
            base_values=expected_val,
            data=X_transformed_df.iloc[0].values,
            feature_names=feature_names,
        ),
        max_display=10,
        show=False,
    )
    plt.title(
        f"SHAP Waterfall Plot for Applicant {applicant_idx} (Predicted: {class_name})",
        fontsize=12,
        pad=20,
    )
    plt.tight_layout()

    path1 = os.path.join(output_dir, f"applicant_{applicant_idx}_waterfall.png")
    path2 = os.path.join(
        output_dir, "underwriting", f"applicant_{applicant_idx}_waterfall.png"
    )

    plt.savefig(path1, dpi=300)
    plt.savefig(path2, dpi=300)
    plt.close()

    print(f"Saved local SHAP waterfall plot to:\n- {path1}\n- {path2}")


if __name__ == "__main__":
    generate_global_shap_plots()
    # Generate explanation for the first applicant
    generate_local_shap_plot(0)
