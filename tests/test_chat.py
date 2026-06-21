"""
Purpose: Test RAG chat workflow.
"""

from app.orchestration.rag_workflow import RAGWorkflow


def test_rag_response_generation():
    """Validates end-to-end RAG response generation and session tracking."""
    workflow = RAGWorkflow()

    response = workflow.generate_response(
        user_query="Explain artificial intelligence."
    )

    assert response is not None
    assert "response" in response
    assert "thread_id" in response
    assert isinstance(response["response"], str)
