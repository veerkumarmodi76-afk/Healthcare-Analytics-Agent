import pandas as pd
from pathlib import Path


# ─────────────────────────────────────────────
# PROJECT ROOT
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "underwriting"
RULE_DISTRIBUTION_PATH = OUTPUT_DIR / "rule_distribution.csv"


# ─────────────────────────────────────────────
# CREATE UNDERWRITING TARGET
# ─────────────────────────────────────────────
def create_underwriting_target(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # =====================================================
    # AGE SCORE
    # =====================================================
    age_score = pd.Series(0, index=df.index)

    age_score += (df["age"] >= 36).astype(int)
    age_score += (df["age"] >= 51).astype(int)
    age_score += (df["age"] >= 65).astype(int)

    # Result:
    # 18–35  -> 0
    # 36–50  -> 1
    # 51–64  -> 2
    # 65+    -> 3

    # =====================================================
    # FAMILY SIZE SCORE
    # =====================================================
    family_score = pd.Series(0, index=df.index)

    family_score += (df["family_size"] >= 3).astype(int)
    family_score += (df["family_size"] >= 5).astype(int)

    # Result:
    # 1–2 -> 0
    # 3–4 -> 1
    # 5+  -> 2

    # =====================================================
    # SENIORITY SCORE
    # =====================================================
    seniority_years = df["seniority_insured"].fillna(0)

    seniority_score = pd.Series(0, index=df.index)

    seniority_score += (seniority_years < 10).astype(int)
    seniority_score += (seniority_years < 5).astype(int)

    # Result:
    # 10+ years -> 0
    # 5–9 years -> 1
    # <5 years  -> 2

    # =====================================================
    # NEW BUSINESS SCORE
    # =====================================================
    if pd.api.types.is_numeric_dtype(df["new_business"]):
        new_business_score = df["new_business"].fillna(0).clip(0, 1).astype(int)
    else:
        new_business_score = (
            df["new_business"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
            .isin([
                "yes",
                "y",
                "true",
                "1",
                "new",
            ])
            .astype(int)
        )

    # =====================================================
    # REIMBURSEMENT SCORE
    # =====================================================
    reimbursement_score = pd.Series(0, index=df.index)

    if "reimbursement" in df.columns:
        if pd.api.types.is_numeric_dtype(df["reimbursement"]):
            reimbursement_score = df["reimbursement"].fillna(0).gt(0).astype(int)
        else:
            reimbursement_score = (
                df["reimbursement"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
                .isin([
                    "yes",
                    "y",
                    "true",
                    "1",
                ])
                .astype(int)
            )

    # Result:
    # No reimbursement -> 0
    # Reimbursement    -> 1

    # =====================================================
    # TOTAL UNDERWRITING SCORE
    # =====================================================
    df["uw_score"] = (
        age_score
        + family_score
        + seniority_score
        + new_business_score
        + reimbursement_score
    )

    # =====================================================
    # UNDERWRITING RISK CLASS
    # =====================================================
    conditions = [
        df["uw_score"] <= 2,
        df["uw_score"].between(3, 4),
        df["uw_score"].between(5, 6),
        df["uw_score"] >= 7,
    ]

    values = [
        "Low",
        "Medium",
        "High",
        "VeryHigh",
    ]

    df["uw_risk_class"] = pd.Series(index=df.index, dtype="object")

    for condition, value in zip(
        conditions,
        values,
        strict=False,
    ):
        df.loc[condition, "uw_risk_class"] = value

    # =====================================================
    # UNDERWRITING DECISION
    # =====================================================
    decision_map = {
        "Low": "Standard",
        "Medium": "Standard",
        "High": "Rated",
        "VeryHigh": "Decline",
    }

    df["underwriting_decision"] = df["uw_risk_class"].map(decision_map)

    # =====================================================
    # ENCODED TARGET
    # =====================================================
    encoding_map = {
        "Low": 0,
        "Medium": 1,
        "High": 2,
        "VeryHigh": 3,
    }

    df["uw_risk_class_encoded"] = df["uw_risk_class"].map(encoding_map)

    # =====================================================
    # RULE GOVERNANCE REPORT
    # =====================================================
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    distribution = df["uw_risk_class"].value_counts(dropna=False).reset_index()

    distribution.columns = [
        "uw_risk_class",
        "count",
    ]

    distribution["percentage"] = (
        distribution["count"] / distribution["count"].sum() * 100
    ).round(2)

    distribution.to_csv(
        RULE_DISTRIBUTION_PATH,
        index=False,
    )

    print(f"Rule distribution saved to: {RULE_DISTRIBUTION_PATH}")

    return df


# ─────────────────────────────────────────────
# TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    sample = pd.DataFrame({
        "age": [25, 45, 60, 75],
        "family_size": [1, 3, 5, 6],
        "seniority_insured": [12, 8, 3, 1],
        "new_business": [
            "No",
            "Yes",
            "Yes",
            "Yes",
        ],
        "reimbursement": [
            "No",
            "No",
            "Yes",
            "Yes",
        ],
    })

    result = create_underwriting_target(sample)

    print(
        result[
            [
                "uw_score",
                "uw_risk_class",
                "underwriting_decision",
                "uw_risk_class_encoded",
            ]
        ]
    )
