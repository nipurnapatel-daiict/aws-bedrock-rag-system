"""
Purpose: Generate vector embeddings from text chunks.
"""

from sentence_transformers import SentenceTransformer
from app.core.config import Settings
from app.exceptions.custom_exceptions import EmbeddingGenerationException

class EmbeddingGenerator:
    model = SentenceTransformer(Settings.EMBEDDING_MODEL)

    @classmethod
    def generate_embedding(cls, text: str) -> list[float]:
        try:
            embedding = cls.model.encode(text)
            return embedding.tolist()
        except Exception as error:
            raise EmbeddingGenerationException(
                f"Embedding generation failed: {error}"
            )

    @classmethod
    def generate_embeddings(cls, text_chunks: list[str]) -> list[list[float]]:
        try:
            embeddings = cls.model.encode(text_chunks)
            return [embedding.tolist() for embedding in embeddings]
        except Exception as error:
            raise EmbeddingGenerationException(
                f"Batch embedding generation failed: {error}"
            )