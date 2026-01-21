"""
Logging configuration for MVC application.
"""

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2026-01-21"
__version__ = "1.0.0.0"

import logging
import sys


def setup_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        name: The name for the logger (typically __name__).
        level: The logging level (default: DEBUG).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
