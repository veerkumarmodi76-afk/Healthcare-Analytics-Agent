from ..services.portfolio_service import PortfolioService


def run() -> None:
    """
    Portfolio Analytics entry point.
    """
    service = PortfolioService()
    success = service.execute()

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    run()