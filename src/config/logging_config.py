from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from .constants import LOG_FORMAT, LOG_LEVEL
from .paths import Paths


# Ensure required directories exist
Paths.create_directories()


def get_logger(name: str) -> logging.Logger:
    """
    Create or return a configured logger.

    Parameters
    ----------
    name : str
        Logger name (typically the service name).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(LOG_FORMAT)

    # ---------------------------------------------------------
    # Console Handler
    # ---------------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    # ---------------------------------------------------------
    # Rotating File Handler
    # ---------------------------------------------------------

    log_file = Paths.LOG_DIR / f"{name}.log"

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    # ---------------------------------------------------------
    # Register Handlers
    # ---------------------------------------------------------

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent messages propagating to the root logger
    logger.propagate = False

    return logger
