"""
Purpose: Validate uploaded files and request data.
"""

from pathlib import Path
from app.core.constants import ApplicationConstants


class FileValidator:
    @staticmethod
    def validate_pdf_file(file_name: str) -> bool:
        file_extension = Path(file_name).suffix.lower()
        return file_extension in ApplicationConstants.SUPPORTED_FILE_TYPES