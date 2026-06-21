from .train import train_pricing_model
from .predict import predict_claim_cost
from .premium import generate_premium_quotes


def run():

    train_pricing_model()

    predict_claim_cost()

    generate_premium_quotes()

    print("Pricing Engine Complete")


if __name__ == "__main__":
    run()
