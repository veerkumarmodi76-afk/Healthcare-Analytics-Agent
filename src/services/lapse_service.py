"""
lapse_service.py

Production Lapse Analytics Service
"""

from pathlib import Path

from  .base_Service import BaseService

from ..lapse.train import train_lapse_model
from ..lapse.predict import predict_lapse
from ..lapse.retention import generate_retention_actions
from ..lapse.reports import generate_report


class LapseService(BaseService):
    """
    End-to-end Lapse Analytics Service.
    """

    def __init__(
        self,
        processed_data_path="data/processed/processed_data.csv",
    ):

        super().__init__("Lapse Analytics")

        self.processed_data_path = Path(processed_data_path)

        self.outputs = {}

    ####################################################################
    # Validation
    ####################################################################

    def validate_inputs(self):

        if not self.processed_data_path.exists():
            raise FileNotFoundError(
                f"Processed dataset not found:\n{self.processed_data_path}"
            )

        self.logger.info("Input validation successful.")

    ####################################################################
    # Training
    ####################################################################

    def train(self):

        self.logger.info("Training lapse model...")

        train_lapse_model()

    ####################################################################
    # Prediction
    ####################################################################

    def predict(self):

        self.logger.info("Generating predictions...")

        predictions = predict_lapse()

        self.outputs["predictions"] = predictions

        return predictions

    ####################################################################
    # Retention
    ####################################################################

    def retention(self):

        self.logger.info("Generating retention actions...")

        report = generate_retention_actions()

        self.outputs["retention"] = report

        return report

    ####################################################################
    # Reporting
    ####################################################################

    def report(self):

        self.logger.info("Generating business report...")

        summary = generate_report()

        self.outputs["summary"] = summary

        return summary

    ####################################################################
    # Pipeline
    ####################################################################

    def run_pipeline(self):

        self.logger.info("=" * 70)
        self.logger.info("LAPSE ANALYTICS PIPELINE")
        self.logger.info("=" * 70)

        self.validate_inputs()

        self.train()

        self.predict()

        self.retention()

        self.report()

        self.logger.info("Pipeline completed successfully.")

        return self.outputs

    ####################################################################
    # Alias
    ####################################################################

    def run(self):

        return self.run_pipeline()


if __name__ == "__main__":
    service = LapseService()

    service.run_pipeline()
