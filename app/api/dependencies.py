"""
Purpose: Store reusable FastAPI dependencies.
"""

from app.orchestration.chat_workflow import ChatWorkflow
from app.orchestration.ingestion_workflow import IngestionWorkflow
from app.orchestration.rag_workflow import RAGWorkflow


def get_ingestion_workflow():
    return IngestionWorkflow()


def get_rag_workflow():
    return RAGWorkflow()


def get_chat_workflow():
    return ChatWorkflow()