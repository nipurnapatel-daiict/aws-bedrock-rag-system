"""
Purpose: Extract text content from PDF documents.
"""

import fitz
from app.exceptions.custom_exceptions import DocumentExtractionException


class PDFExtractor:

    @staticmethod
    def extract_text(file_path: str) -> str:

        try:
            document = fitz.open(file_path)
            extracted_text = []
            for page in document:
                extracted_text.append(page.get_text())

            return "\n".join(extracted_text)

        except Exception as error:
            raise DocumentExtractionException(
                f"Failed to extract PDF content: {error}"
            )