import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(logger_name="app"):
    """
    Configures logging: output to console and file with log rotation.
    Returns a logger instance.
    """
    log_file = os.getenv('LOG_FILE', 'app.log')

    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(module)s:%(funcName)s:%(lineno)d] - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # Add handlers if not already added
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    logger.info("Logging setup complete")
    return logger

# Get logger instance
logger = setup_logging()

# Functions for logging messages
def log_query(query):
    logger.info(f"Executing query: {query}")

def log_error(error):
    logger.error(f"SQL error: {error}")

def log_warning(warning):
    logger.warning(f"Warning: {warning}")

def log_debug(debug_message):
    logger.debug(f"Debugging: {debug_message}")
