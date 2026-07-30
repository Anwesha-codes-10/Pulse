"""
Centralized logging configuration for the Pulse project.
"""

import logging

LOGGER_NAME = "pulse"


logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.INFO)

if not logger.handlers:
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    )

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

logger.propagate = False