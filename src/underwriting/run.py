from .explain import (
    generate_global_shap_plots,
    generate_local_shap_plot,
)
from .predict import predict_risk_scores
from .train import train_underwriting_model


def run():

    train_underwriting_model()

    predict_risk_scores()

    generate_global_shap_plots()

    generate_local_shap_plot(0)

    print("Phase 3 Complete")


if __name__ == "__main__":
    run()
