from .train import train_lapse_model
from .predict import predict_lapse
from .retention import (
    generate_retention_actions,
)


def run():

    train_lapse_model()

    predict_lapse()

    generate_retention_actions()

    print("Lapse Engine Complete")


if __name__ == "__main__":
    run()
