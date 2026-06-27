import pandas as pd
from pathlib import Path


INPUT_PATH = Path("outputs/lapse/lapse_predictions.csv")
OUTPUT_PATH = Path("outputs/lapse/lapse_retention_actions.csv")


def calculate_priority(segment):

    priority = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4,
        "Very Low": 5,
    }

    return priority.get(segment, 5)


def estimate_retention_cost(segment):

    costs = {
        "Critical": 5000,
        "High": 2500,
        "Medium": 1000,
        "Low": 300,
        "Very Low": 0,
    }

    return costs.get(segment, 0)


def recommend_action(segment):

    actions = {
        "Critical": "Immediate Relationship Manager Call + Premium Review",
        "High": "Agent Call + Loyalty Discount",
        "Medium": "Personalized Renewal Offer",
        "Low": "Automated Reminder Email",
        "Very Low": "No Action Required",
    }

    return actions.get(segment, "No Action")


def expected_revenue_loss(probability):

    # Placeholder business assumption.
    # Replace with premium-based calculation later.
    return round(probability * 50000, 2)


def estimate_roi(revenue_loss, retention_cost):

    if retention_cost == 0:
        return 0

    return round(revenue_loss / retention_cost, 2)


def generate_retention_actions():

    print("=" * 60)
    print("RETENTION ANALYTICS")
    print("=" * 60)

    df = pd.read_csv(INPUT_PATH)

    df["priority"] = df["risk_segment"].apply(calculate_priority)

    df["estimated_revenue_loss"] = df["lapse_probability"].apply(expected_revenue_loss)

    df["retention_cost"] = df["risk_segment"].apply(estimate_retention_cost)

    df["expected_roi"] = [
        estimate_roi(loss, cost)
        for loss, cost in zip(
            df["estimated_revenue_loss"],
            df["retention_cost"],
        )
    ]

    df["recommended_action"] = df["risk_segment"].apply(recommend_action)

    df = df.sort_values(
        [
            "priority",
            "lapse_probability",
        ],
        ascending=[True, False],
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"Retention report saved to {OUTPUT_PATH}")
    print()

    print("Retention Segments")
    print(df["risk_segment"].value_counts())

    print()
    print(
        "Estimated Revenue at Risk : ₹{:,.2f}".format(
            df["estimated_revenue_loss"].sum()
        )
    )

    print("Estimated Campaign Cost : ₹{:,.2f}".format(df["retention_cost"].sum()))

    return df


if __name__ == "__main__":
    generate_retention_actions()
