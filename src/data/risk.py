from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import logging
from ..config.logging_config import get_logger

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

# =====================================================
# Output Configuration
# =====================================================

OUTPUT_DIR = Path("outputs/preprocessing")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEGMENT_SUMMARY_FILE = OUTPUT_DIR / "segmentation_summary.csv"

# =====================================================
# Segment Summary Export
# =====================================================


def export_segment_summary(df: pd.DataFrame) -> None:
    """
    Export portfolio segmentation summary.
    """

    summary = (
        df
        .groupby("portfolio_segment")
        .agg(
            policy_count=("portfolio_segment", "count"),
            avg_segment_score=("segment_score", "mean"),
        )
        .reset_index()
    )

    summary["portfolio_pct"] = (
        summary["policy_count"] / summary["policy_count"].sum() * 100
    ).round(2)

    summary.to_csv(SEGMENT_SUMMARY_FILE, index=False)

    logging.info(f"Segmentation summary saved to: {SEGMENT_SUMMARY_FILE}")


# =====================================================
# Portfolio Segmentation
# =====================================================


def create_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Business-Oriented Portfolio Segmentation

    Drivers:
    - claims_per_exposure
    - premium_per_exposure
    - age_band
    - family_size

    Outputs:
    - portfolio_segment
    - portfolio_segment_encoded
    - segment_score
    """

    logging.info("Creating portfolio segments...")

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    required_cols = [
        "claims_per_exposure",
        "premium_per_exposure",
        "age_band",
        "family_size",
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required segmentation columns: {missing}")

    # -------------------------------------------------
    # Age Band Risk Mapping
    # -------------------------------------------------

    age_risk_map = {
        "18-25": 1,
        "26-35": 2,
        "36-50": 3,
        "51-65": 4,
        "65+": 5,
    }

    df["age_band_score"] = df["age_band"].astype(str).map(age_risk_map).fillna(3)

    # -------------------------------------------------
    # Segmentation Features
    # -------------------------------------------------

    segmentation_features = [
        "claims_per_exposure",
        "premium_per_exposure",
        "age_band_score",
        "family_size",
    ]

    segmentation_df = (
        df[segmentation_features].replace([np.inf, -np.inf], np.nan).fillna(0)
    )

    # -------------------------------------------------
    # Scaling
    # -------------------------------------------------

    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(segmentation_df)

    scaled_df = pd.DataFrame(scaled, columns=segmentation_features, index=df.index)

    # -------------------------------------------------
    # Portfolio Risk Score
    # -------------------------------------------------

    df["segment_score"] = (
        0.45 * scaled_df["claims_per_exposure"]
        + 0.25 * scaled_df["premium_per_exposure"]
        + 0.20 * scaled_df["age_band_score"]
        + 0.10 * scaled_df["family_size"]
    )

    # -------------------------------------------------
    # Segment Labels
    # -------------------------------------------------

    segment_labels = [
        "Low Exposure",
        "Moderate Exposure",
        "High Exposure",
        "Critical Exposure",
    ]

    # -------------------------------------------------
    # Robust Segmentation Logic
    # -------------------------------------------------

    unique_scores = df["segment_score"].nunique()

    if unique_scores >= 4:
        try:
            df["portfolio_segment"] = pd.qcut(
                df["segment_score"], q=4, labels=segment_labels
            )

        except ValueError:
            logging.warning("qcut failed. Using percentile fallback.")

            percentiles = df["segment_score"].rank(pct=True)

            df["portfolio_segment"] = pd.cut(
                percentiles,
                bins=[0, 0.25, 0.50, 0.75, 1.0],
                labels=segment_labels,
                include_lowest=True,
            )

    else:
        logging.warning(
            f"Only {unique_scores} unique "
            f"segment scores detected. "
            f"Using percentile fallback."
        )

        percentiles = df["segment_score"].rank(pct=True)

        df["portfolio_segment"] = pd.cut(
            percentiles,
            bins=[0, 0.25, 0.50, 0.75, 1.0],
            labels=segment_labels,
            include_lowest=True,
        )

    # -------------------------------------------------
    # Segment Encoding
    # -------------------------------------------------

    segment_map = {
        "Low Exposure": 0,
        "Moderate Exposure": 1,
        "High Exposure": 2,
        "Critical Exposure": 3,
    }

    df["portfolio_segment_encoded"] = (
        df["portfolio_segment"].astype(str).map(segment_map)
    )

    # -------------------------------------------------
    # Export Segment Summary
    # -------------------------------------------------

    export_segment_summary(df)

    # -------------------------------------------------
    # logger
    # -------------------------------------------------

    segment_summary = df["portfolio_segment"].value_counts().sort_index()

    logging.info(f"\nPortfolio Segment Distribution:\n{segment_summary}")

    logging.info("Portfolio segmentation completed.")

    return df


# =====================================================
# Test Run
# =====================================================

if __name__ == "__main__":
    sample_df = pd.DataFrame({
        "claims_per_exposure": [100, 200, 400, 900, 1200],
        "premium_per_exposure": [1000, 1500, 2000, 3000, 4500],
        "age_band": ["18-25", "36-50", "51-65", "65+", "65+"],
        "family_size": [1, 2, 3, 5, 6],
    })

    segmented_df = create_segments(sample_df)

    print(
        segmented_df[
            ["segment_score", "portfolio_segment", "portfolio_segment_encoded"]
        ]
    )
