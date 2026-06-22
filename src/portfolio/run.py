from pathlib import Path
import pandas as pd

from .metrics import (
    build_master_dataframe,
    generate_portfolio_analytics,
    save_portfolio_outputs,
)

from .executive_summary import (
    generate_executive_summary,
)


BASE_DIR = Path(__file__).resolve().parents[2]


def run():

    print("Loading portfolio inputs...")

    processed_df = pd.read_csv(BASE_DIR / "data" / "processed" / "processed_data.csv")

    underwriting_df = pd.read_csv(
        BASE_DIR / "outputs" / "underwriting" / "applicant_risk_scores.csv"
    )

    pricing_df = pd.read_csv(BASE_DIR / "outputs" / "pricing" / "premium_quotes.csv")

    lapse_df = pd.read_csv(BASE_DIR / "outputs" / "lapse" / "lapse_risk_scores.csv")

    print("Building master dataframe...")

    master_df = build_master_dataframe(
        processed_df,
        underwriting_df,
        pricing_df,
        lapse_df,
    )

    print("Generating portfolio analytics...")

    results = generate_portfolio_analytics(master_df)

    print("Saving outputs...")

    save_portfolio_outputs(results)

    print("Generating executive summary...")

    generate_executive_summary()

    print("Portfolio Analytics Complete")


if __name__ == "__main__":
    run()
