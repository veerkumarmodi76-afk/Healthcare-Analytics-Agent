from src.data.preprocess import run as run_preprocessing

from src.underwriting.run import run as run_underwriting

from src.pricing.run import run as run_pricing

from src.lapse.run import run as run_lapse

from src.portfolio.run import run as run_portfolio

import logging

logging.basicConfig(level=logging.INFO)


def main():

    print("\n" + "=" * 60)
    print("PHASE 1 : DATA PREPROCESSING")
    print("=" * 60)

    run_preprocessing()

    print("\n" + "=" * 60)
    print("PHASE 2 : UNDERWRITING ENGINE")
    print("=" * 60)

    run_underwriting()

    print("\n" + "=" * 60)
    print("PHASE 3 : PRICING ENGINE")
    print("=" * 60)

    run_pricing()

    print("\n" + "=" * 60)
    print("PHASE 4 : LAPSE ENGINE")
    print("=" * 60)

    run_lapse()

    print("\n" + "=" * 60)
    print("PHASE 5 : PORTFOLIO ANALYTICS")
    print("=" * 60)

    run_portfolio()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
