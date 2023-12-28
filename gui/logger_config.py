import logging
from rich.logging import RichHandler


def configure_logger(logger_name: str = __name__, log_level: int = logging.DEBUG, fmt: str = "%(message)s") -> (
        logging.Logger):
    """
    Configure a logger with the RichHandler.

    Args:
        logger_name (str): The name of the logger.
        log_level (int, optional): The logging level. Defaults to logging.DEBUG.
        fmt (str, optional): The log message format. Defaults to "%(message)s".

    Returns:
        logging.Logger: The configured logger.
    """
    logging.basicConfig(
        level=log_level,
        format=fmt,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    logger = logging.getLogger(logger_name)
    return logger


