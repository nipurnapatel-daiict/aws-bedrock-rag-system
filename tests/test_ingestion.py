"""
Purpose: Test document ingestion workflow.
"""

from app.orchestration.ingestion_workflow import IngestionWorkflow

def test_document_ingestion():
    workflow = IngestionWorkflow()

    response = workflow.process_document(
        file_path="data/sample_files/langchain_file2.pdf",
        file_name="data/sample_files/langchain_file3.pdf"
    )

    assert response is not None
    assert len(response) > 0
