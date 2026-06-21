"""
Purpose: Provides centralized logging configuration.
"""

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.constants import ApplicationConstants


class LoggerManager:

    @classmethod
    def get_logger(cls) -> logging.Logger:
        log_dir_name = getattr(ApplicationConstants, "LOG_DIRECTORY", "logs")
        log_file_name = getattr(ApplicationConstants, "LOG_FILE_NAME", "application.log")
        logger_name = getattr(ApplicationConstants, "LOGGER_NAME", "rag_application")

        log_directory = Path(log_dir_name)
        log_directory.mkdir(exist_ok=True)

        logger = logging.getLogger(logger_name)

        ## CRITICAL: Prevents adding duplicate handlers on multiple imports in FastAPI
        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        ## Rotating File Handler (1MB limit per file, 5 backups)
        file_handler = RotatingFileHandler(
            filename=log_directory / log_file_name,
            maxBytes=1024 * 1024,
            backupCount=5,
            encoding="utf-8"  
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger
    
