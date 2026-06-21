import os
import time
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier


def train_underwriting_model():
    t_start = time.time()
    print("Loading processed dataset...")
    # Read the data
    data_path = "data/processed/processed_data.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed dataset not found at {data_path}")

    df = pd.read_csv(data_path)

    # Define features and target
    categorical_features = [
        "gender",
        "type_policy",
        "type_product",
        "reimbursement",
        "distribution_channel",
    ]
    numeric_features = [
        "age",
        "exposure_time",
        "seniority_insured",
        "family_size",
        "claim_frequency",
        "claim_severity",
        "loss_ratio",
    ]

    X = df[categorical_features + numeric_features].copy()
    y = df["risk_class_encoded"].copy()

    print(f"Dataset shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")

    # Preprocess categorical features
    print("Preprocessing features...")
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            )
        ],
        remainder="passthrough",
    )

    # Fit and transform features
    X_transformed = preprocessor.fit_transform(X)

    # Get feature names after one-hot encoding
    cat_encoder = preprocessor.named_transformers_["cat"]
    one_hot_cols = cat_encoder.get_feature_names_out(categorical_features).tolist()
    feature_names = one_hot_cols + numeric_features

    X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names)

    # Train-test split (80/20, stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X_transformed_df, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Train set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")

    # ── Fast hyperparameter search ────────────────────────────────────
    # Use n_estimators=100 + 3-fold CV on a 30% subsample for speed.
    # Best params are then refit on the full train set at n_estimators=300.
    print("Sampling 30% of training data for fast GridSearchCV...")
    from sklearn.model_selection import StratifiedShuffleSplit
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.70, random_state=42)
    tune_idx, _ = next(sss.split(X_train, y_train))
    X_tune = X_train.iloc[tune_idx]
    y_tune = y_train.iloc[tune_idx]
    print(f"Tuning set shape: {X_tune.shape}")

    xgb_fast = XGBClassifier(
        n_estimators=100,   # fast for grid search
        max_depth=6,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
    )

    param_grid = {
        'learning_rate': [0.05, 0.1],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
    }

    print("Running GridSearchCV (3-fold, 8 combos, subsample)...")
    grid_search = GridSearchCV(
        estimator=xgb_fast,
        param_grid=param_grid,
        cv=3,
        scoring='f1_macro',
        n_jobs=-1,
        verbose=1,
    )
    grid_search.fit(X_tune, y_tune)

    best_params = grid_search.best_params_
    print(f"\nBest params from grid search: {best_params}")

    # ── Refit on full training set with n_estimators=300 ─────────────
    print("Refitting final model on full training set (n_estimators=300)...")
    best_model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
        **best_params,
    )
    best_model.fit(X_train, y_train)

    print("\nBest Hyperparameters:")
    print(grid_search.best_params_)

    # Evaluate model
    print("\nEvaluating model on test set...")
    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)

    # Print metrics
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(
        classification_report(
            y_test, y_pred, target_names=["Low", "Medium", "High", "VeryHigh"]
        )
    )

    # AUC-ROC calculation (One-vs-Rest, multi-class)
    auc_roc = roc_auc_score(y_test, y_pred_proba, multi_class="ovr", average="macro")
    print(f"\nMulti-class OvR AUC-ROC Score: {auc_roc:.4f}")

    if auc_roc < 0.80:
        print("WARNING: AUC-ROC is below the acceptance criteria threshold of 0.80!")
    else:
        print("SUCCESS: AUC-ROC meets the acceptance criteria threshold of 0.80.")

    # Save model and preprocessor payload
    payload = {
        "model": best_model,
        "preprocessor": preprocessor,
        "feature_names": feature_names,
        "categorical_features": categorical_features,
        "numeric_features": numeric_features,
    }

    # Ensure target directories exist (create parent before child)
    os.makedirs("models", exist_ok=True)
    os.makedirs("models/underwriting", exist_ok=True)

    # Save to both locations
    path1 = "models/underwriting_model.pkl"
    path2 = "models/underwriting/underwriting_model.pkl"

    joblib.dump(payload, path1)
    joblib.dump(payload, path2)

    elapsed = time.time() - t_start
    print(f"\n{'=' * 60}")
    print(f"  MODULE 2 — UNDERWRITING MODEL TRAINING COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Elapsed time  : {elapsed:.1f}s")
    print(f"  Model saved   : {path1}")
    print(f"  Model saved   : {path2}")
    print(f"  AUC-ROC (OvR) : {auc_roc:.4f}")
    print(f"{'=' * 60}\n")

    return best_model, preprocessor


if __name__ == "__main__":
    train_underwriting_model()
