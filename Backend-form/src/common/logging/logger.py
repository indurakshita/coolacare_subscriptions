import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import os


def initiate_logs(level=logging.DEBUG):
    """
    Initializes a logger and sets up log file rotation.

    Parameters:
        level (int, optional): The log level to set for the logger. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: A configured logger with log file rotation.
    """
    filename = "hourly.log"
    log_directory = Path(__file__).parent / "logs"
    filepath = os.path.join(log_directory, filename)

    # Create the log directory if it doesn't exist
    log_directory.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    handler = TimedRotatingFileHandler(filepath, when="H", interval=1)
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


logger = initiate_logs(level=logging.DEBUG)
