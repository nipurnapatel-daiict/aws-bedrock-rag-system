"""
Purpose: Store document-related data models.
"""

from pydantic import BaseModel

class DocumentChunk(BaseModel):

    chunk_id: str
    document_name: str
    chunk_text: str
    embedding_vector: list[float]


class DocumentEmbedding(BaseModel):

    chunk_id: str
    embedding_vector: list[float]
