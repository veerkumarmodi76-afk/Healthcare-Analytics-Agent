"""
generate_sample_data.py
------------------------
WHAT THIS FILE DOES:
Your teammates (Members 2-5) will eventually give you CSV files with their
model predictions. Since they haven't delivered yet, this script creates
FAKE versions of those files so you can build and test your validation
process right now. Later, you just replace these fake files with the real
ones - your validation script doesn't need to change.

HOW TO RUN:
    python generate_sample_data.py

This will create a folder called "sample_data" with these files:
    - applicant_risk_scores.csv     (from Member 2: Underwriting)
    - predicted_claim_cost.csv      (from Member 3: Pricing)
    - lapse_risk_scores.csv         (from Member 5: Lapse Analytics)
"""

import pandas as pd
import numpy as np

# Setting a "seed" makes the random numbers reproducible - you'll get the
# same fake data every time you run this, which makes testing easier.
np.random.seed(42)

N = 500  # number of fake customers/applicants

# ---------------------------------------------------------------
# 1. UNDERWRITING RISK SCORES (Member 2's expected output)
# ---------------------------------------------------------------
# Real models predict a "risk_score" (probability of high risk, 0 to 1)
# and an "actual_risk_flag" (1 = turned out to be high risk, 0 = not),
# which is what you compare against to check accuracy.

applicant_id = np.arange(1, N + 1)
age = np.random.randint(18, 70, N)
bmi = np.round(np.random.normal(25, 4, N), 1)

# Fake "true" risk depends loosely on age and bmi (so it's not random noise)
true_risk_prob = 1 / (1 + np.exp(-(0.04 * (age - 40) + 0.08 * (bmi - 25))))
actual_risk_flag = np.random.binomial(1, true_risk_prob)

# Fake "predicted" risk score = true probability + some random model error
predicted_risk_score = np.clip(
    true_risk_prob + np.random.normal(0, 0.12, N), 0, 1
)

risk_df = pd.DataFrame({
    "applicant_id": applicant_id,
    "age": age,
    "bmi": bmi,
    "predicted_risk_score": predicted_risk_score.round(3),
    "actual_risk_flag": actual_risk_flag
})

# ---------------------------------------------------------------
# 2. PREDICTED CLAIM COST (Member 3's expected output)
# ---------------------------------------------------------------
true_claim_cost = (
    2000 + 50 * age + 30 * (bmi - 25) ** 2 + np.random.normal(0, 500, N)
)
true_claim_cost = np.clip(true_claim_cost, 500, None)

predicted_claim_cost = true_claim_cost * np.random.normal(1, 0.15, N)
predicted_claim_cost = np.clip(predicted_claim_cost, 500, None)

claim_df = pd.DataFrame({
    "applicant_id": applicant_id,
    "actual_claim_cost": true_claim_cost.round(2),
    "predicted_claim_cost": predicted_claim_cost.round(2)
})

# ---------------------------------------------------------------
# 3. LAPSE RISK SCORES (Member 5's expected output)
# ---------------------------------------------------------------
tenure_years = np.round(np.random.uniform(0.5, 15, N), 1)
true_lapse_prob = 1 / (1 + np.exp(-(1.5 - 0.2 * tenure_years)))
actual_lapse_flag = np.random.binomial(1, true_lapse_prob)
predicted_lapse_score = np.clip(
    true_lapse_prob + np.random.normal(0, 0.12, N), 0, 1
)

lapse_df = pd.DataFrame({
    "applicant_id": applicant_id,
    "tenure_years": tenure_years,
    "predicted_lapse_score": predicted_lapse_score.round(3),
    "actual_lapse_flag": actual_lapse_flag
})

# ---------------------------------------------------------------
# SAVE ALL FILES
# ---------------------------------------------------------------
import os
os.makedirs("sample_data", exist_ok=True)

risk_df.to_csv("sample_data/applicant_risk_scores.csv", index=False)
claim_df.to_csv("sample_data/predicted_claim_cost.csv", index=False)
lapse_df.to_csv("sample_data/lapse_risk_scores.csv", index=False)

print("Done! Created 3 sample files inside the 'sample_data' folder:")
print(" - sample_data/applicant_risk_scores.csv")
print(" - sample_data/predicted_claim_cost.csv")
print(" - sample_data/lapse_risk_scores.csv")
print("\nThese mimic what Members 2, 3, and 5 will eventually give you.")
