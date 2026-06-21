"""
Purpose: Stores custom application exceptions with detailed error tracking.
"""

class RAGAppException(Exception):
    def __init__(self, message: str, details: str = None):
        super().__init__(message)
        self.message = message
        self.details = details


class OpenSearchConnectionException(RAGAppException):
    """Raised when OpenSearch connection fails."""


class OpenSearchIndexException(RAGAppException):
    """Raised when OpenSearch index operation fails."""


class S3UploadException(RAGAppException):
    """Raised when S3 upload fails."""


class DocumentExtractionException(RAGAppException):
    """Raised when PDF extraction fails (e.g., PyMuPDF errors)."""


class EmbeddingGenerationException(RAGAppException):
    """Raised when local sentence embedding generation fails."""


class RetrievalException(RAGAppException):
    """Raised during vector or keyword search retrieval failure."""


class ChatHistoryException(RAGAppException):
    """Raised during chat history storage/retrieval operations."""
