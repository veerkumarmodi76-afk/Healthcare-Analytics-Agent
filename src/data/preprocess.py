from .clean import clean_data
from .features import create_features
from .risk import create_risk_classes
from .ingest import load_data
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parents[2]


def run():

    df = load_data()

    df = clean_data(df)
    df = create_features(df)
    df = create_risk_classes(df)

    output_path = BASE_DIR / "data" / "processed" / "processed_data.csv"

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        index=False,
    )

    logging.info("Processing complete")
    logging.info(f"Final shape: {df.shape}")


if __name__ == "__main__":
    run()
