"""
Purpose: Split extracted text into manageable chunks.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.constants import ApplicationConstants


class TextChunker:

    @staticmethod
    def create_chunks(text: str) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=ApplicationConstants.CHUNK_SIZE,
            chunk_overlap=ApplicationConstants.CHUNK_OVERLAP
        )

        return text_splitter.split_text(text)