"""
====================================================
AI-AIP : Data Preprocessing & Feature Engineering
Owner: Veer Kumar Modi

Purpose:
1. Load raw insurance dataset
2. Handle missing values
3. Create engineered actuarial features
4. Create lapse target
5. Create underwriting risk classes
6. Save processed dataset

Output:
data/processed/processed_data.csv
====================================================
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# ====================================================
# LOAD DATA
# ====================================================

print("Loading dataset...")

df = pd.read_csv("../../data/raw/raw_data.csv")

print(f"Dataset Shape: {df.shape}")


# ====================================================
# DATE CONVERSION
# ====================================================
# Convert string dates to datetime format
# This helps if we need date-based analysis later

date_cols = [
    "date_effect_insured",
    "date_lapse_insured",
    "date_effect_policy",
    "date_lapse_policy",
]

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")


# ====================================================
# CREATE LAPSE FLAGS
# ====================================================
# Missing lapse date means policy is still active

df["insured_lapsed_flag"] = df["date_lapse_insured"].notna().astype(int)

df["policy_lapsed_flag"] = df["date_lapse_policy"].notna().astype(int)


# ====================================================
# MISSING VALUE HANDLING
# ====================================================

print("Handling missing values...")

# Numerical columns
num_cols = df.select_dtypes(include=["int64", "float64"]).columns

for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Categorical columns
cat_cols = df.select_dtypes(include=["object"]).columns

for col in cat_cols:
    df[col] = df[col].fillna("Unknown")


# ====================================================
# FEATURE ENGINEERING
# ====================================================

print("Creating engineered features...")


# ----------------------------------------------------
# 1. Duration Features
# ----------------------------------------------------
# How long insured/policy has existed

df["insured_duration"] = df["period"] - df["year_effect_insured"]

df["policy_duration"] = df["period"] - df["year_effect_policy"]


# ----------------------------------------------------
# 2. Family Size
# ----------------------------------------------------
# Number of insured persons under same policy

df["family_size"] = df.groupby("ID_policy")["ID_insured"].transform("count")


# ----------------------------------------------------
# 3. Claim Frequency
# ----------------------------------------------------
# Medical services per exposure unit

df["claim_frequency"] = df["n_medical_services"] / (df["exposure_time"] + 0.01)


# ----------------------------------------------------
# 4. Claim Severity
# ----------------------------------------------------
# Average cost per medical service

df["claim_severity"] = df["cost_claims_year"] / (df["n_medical_services"] + 1)


# ----------------------------------------------------
# 5. Loss Ratio
# ----------------------------------------------------
# Most important actuarial KPI
# Claims divided by premium

df["loss_ratio"] = df["cost_claims_year"] / (df["premium"] + 1)


# ----------------------------------------------------
# 6. Premium per Exposure
# ----------------------------------------------------

df["premium_per_exposure"] = df["premium"] / (df["exposure_time"] + 0.01)


# ----------------------------------------------------
# 7. Claims per Exposure
# ----------------------------------------------------

df["claims_per_exposure"] = df["cost_claims_year"] / (df["exposure_time"] + 0.01)


# ====================================================
# AGE BANDS
# ====================================================

df["age_band"] = pd.cut(
    df["age"],
    bins=[0, 25, 35, 50, 65, 120],
    labels=["18-25", "26-35", "36-50", "51-65", "65+"],
)


# ====================================================
# SENIORITY BANDS
# ====================================================

df["seniority_band"] = pd.cut(
    df["seniority_insured"],
    bins=[-1, 2, 5, 10, 100],
    labels=["0-2", "3-5", "6-10", "10+"],
)


# ====================================================
# CREATE LAPSE TARGET
# ====================================================
# Binary target for Member 5

df["lapse_binary"] = df["lapse"].replace({1: 1, 2: 0, 3: 1})


# ====================================================
# CREATE RISK SCORE
# ====================================================
# Used for underwriting target creation

print("Creating risk score...")


risk_features = ["loss_ratio", "claim_frequency", "age"]

scaler = MinMaxScaler()

scaled = scaler.fit_transform(df[risk_features])

scaled_df = pd.DataFrame(scaled, columns=risk_features)

df["risk_score"] = (
    0.50 * scaled_df["loss_ratio"]
    + 0.30 * scaled_df["claim_frequency"]
    + 0.20 * scaled_df["age"]
)


# ====================================================
# CREATE RISK CLASS
# ====================================================
# Target for Underwriting Team

df["risk_class"] = pd.qcut(
    df["risk_score"], q=4, labels=["Low", "Medium", "High", "VeryHigh"]
)


# ====================================================
# OPTIONAL:
# ENCODE RISK CLASS NUMERIC
# ====================================================

df["risk_class_encoded"] = df["risk_class"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "VeryHigh": 3,
})


# ====================================================
# FINAL COLUMN SELECTION
# ====================================================

print("Preparing final dataset...")


final_columns = [
    "ID_policy",
    "ID_insured",
    "period",
    "age",
    "gender",
    "type_policy",
    "type_policy_dg",
    "type_product",
    "reimbursement",
    "new_business",
    "distribution_channel",
    "premium",
    "cost_claims_year",
    "n_medical_services",
    "exposure_time",
    "seniority_insured",
    "seniority_policy",
    "family_size",
    "insured_duration",
    "policy_duration",
    "claim_frequency",
    "claim_severity",
    "loss_ratio",
    "premium_per_exposure",
    "claims_per_exposure",
    "age_band",
    "seniority_band",
    "lapse_binary",
    "insured_lapsed_flag",
    "policy_lapsed_flag",
    "risk_score",
    "risk_class",
    "risk_class_encoded",
]

processed_df = df[final_columns]


# ====================================================
# SAVE OUTPUT
# ====================================================

output_path = "../../data/processed/processed_data.csv"

processed_df.to_csv(output_path, index=False)

print("\nProcessing Complete")
print(f"Saved to: {output_path}")
print(f"Final Shape: {processed_df.shape}")

print("\nRisk Class Distribution")
print(processed_df["risk_class"].value_counts())
