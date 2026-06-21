import pandas as pd


def generate_retention_actions():

    df = pd.read_csv("outputs/lapse/lapse_predictions.csv")

    def segment(prob):

        if prob > 0.70:
            return "At-Risk"

        elif prob > 0.40:
            return "Watch"

        return "Stable"

    def action(segment):

        if segment == "At-Risk":
            return "Agent Call + Discount"

        elif segment == "Watch":
            return "Loyalty Email"

        return "No Action"

    df["retention_segment"] = df["lapse_probability"].apply(segment)

    df["recommended_action"] = df["retention_segment"].apply(action)

    df.to_csv(
        "outputs/lapse/lapse_risk_scores.csv",
        index=False,
    )

    print("Retention actions generated.")

    print(df["retention_segment"].value_counts())

    return df


if __name__ == "__main__":
    generate_retention_actions()
