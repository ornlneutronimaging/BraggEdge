"""Logging configuration for neutronbraggedge.

This module provides Loguru-based logging configuration for the library.
By default, the logger is disabled to follow library best practices.
Users can enable logging by calling configure_logging().
"""

import sys

from loguru import logger

# Remove default handler - library best practice is to not emit logs by default
logger.remove()


# Default log format
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def configure_logging(
    level: str = "INFO",
    format: str = DEFAULT_FORMAT,
    colorize: bool = True,
) -> None:
    """Configure logging for neutronbraggedge.

    Parameters
    ----------
    level : str, optional
        Logging level. Default is "INFO".
        Valid levels: "TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL".
    format : str, optional
        Log message format string using Loguru format syntax.
    colorize : bool, optional
        Whether to colorize output. Default is True.

    Examples
    --------
    Enable logging with default settings:

    >>> from neutronbraggedge.logging_config import configure_logging
    >>> configure_logging()

    Enable debug logging:

    >>> configure_logging(level="DEBUG")

    Simple format without colors (for file output):

    >>> configure_logging(
    ...     format="{time} | {level} | {message}",
    ...     colorize=False
    ... )
    """
    # Remove any existing handlers before adding new one
    logger.remove()

    # Add stdout handler with specified configuration
    logger.add(
        sys.stdout,
        level=level,
        format=format,
        colorize=colorize,
    )


def enable_logging(level: str = "INFO") -> None:
    """Enable logging with sensible defaults.

    This is a convenience function that calls configure_logging with
    default parameters.

    Parameters
    ----------
    level : str, optional
        Logging level. Default is "INFO".

    Examples
    --------
    >>> from neutronbraggedge.logging_config import enable_logging
    >>> enable_logging()  # Enable INFO level logging
    >>> enable_logging("DEBUG")  # Enable DEBUG level logging
    """
    configure_logging(level=level)


def disable_logging() -> None:
    """Disable all logging output.

    Examples
    --------
    >>> from neutronbraggedge.logging_config import disable_logging
    >>> disable_logging()
    """
    logger.remove()
