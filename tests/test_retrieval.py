"""
Purpose: Test document retrieval workflow.
"""

from app.services.retrieval_service import RetrievalService
from app.utils.embeddings import EmbeddingGenerator


def test_similarity_retrieval():
    """Verifies that vector search functions smoothly against the OpenSearch cluster."""
    retrieval_service = RetrievalService()

    query_embedding = EmbeddingGenerator.generate_embedding(
        text="What is transformer?"
    )

    results = retrieval_service.retrieve_similar_chunks(
        query_embedding=query_embedding
    )

    assert results is not None
    assert isinstance(results, list)
