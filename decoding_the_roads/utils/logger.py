# utils/logger.py
import logging

def setup_logger(name, level=logging.INFO):
    """Sets up and returns a logger that logs to the terminal."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:  # Check if handler exists
        handler = logging.StreamHandler()  # Log to the terminal
        formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s - %(name)s ')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


if __name__ == '__main__':
    logger = setup_logger(__name__, level=logging.DEBUG)
    logger.debug("This is a test debug message")
    logger.info("This is a test info message")
    logger.warning("This is a test warning message")
    logger.error("This is a test error message")
