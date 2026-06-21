from pathlib import Path
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path.cwd()
DATA_PATH = BASE_DIR / "data" / "raw" / "raw_data.csv"


def load_data(path=DATA_PATH):
    logging.info("Loading dataset...")
    logging.info(f"Resolved path: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Data file not found at {path}")

    df = pd.read_csv(path)

    logging.info(f"Dataset shape: {df.shape}")
    return df
