# app/core/logger.py
import logging
import os
import sys

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "logs")
LOG_DIR = os.path.abspath(LOG_DIR)
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    # File handler with UTF-8 encoding
    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, f"{name}.log"),
        encoding='utf-8'
    )
    
    # Stream handler with UTF-8 encoding for Windows compatibility
    stream_handler = logging.StreamHandler(sys.stdout)
    
    # For Windows, reconfigure stdout to handle UTF-8
    if sys.platform == 'win32':
        try:
            # Try to reconfigure stdout to UTF-8
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # type: ignore
        except Exception:
            # If reconfiguration fails, stream handler will use 'replace' error handling
            pass
    
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(fmt)
    stream_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
