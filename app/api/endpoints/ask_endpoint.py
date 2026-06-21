"""
Purpose: Handle RAG question-answer endpoints with robust exception isolation.
"""

from fastapi import APIRouter, Depends
from app.api.dependencies import get_rag_workflow
from app.orchestration.rag_workflow import RAGWorkflow
from app.schemas.request_schema import AskRequest
from app.exceptions.custom_exceptions import RetrievalException
from app.utils.response_formatter import ResponseFormatter
from app.core.logger import LoggerManager

logger = LoggerManager.get_logger()
router = APIRouter()


@router.post("/ask")
def ask_question(
    request: AskRequest,
    rag_workflow: RAGWorkflow = Depends(get_rag_workflow)
):
    """
    Executes the full local embedding, ngrok vector search, and Bedrock Nova pipeline.

    ### Session Management Instructions:
    * **New Chat Session:** If you want to initiate a new chat, keep the `thread_id` field `null` (or omit it entirely).
    * **Existing Chat Session:** To continue an ongoing conversation, execute the `/threads` endpoint first, find the specific `thread_id` using its associated `title`, and pass that identifier in the request payload.
    """
    try:
        logger.info(f"Processing ask request: {request.query[:50]}...")
        pipeline_output = rag_workflow.generate_response(
            user_query=request.query,
            thread_id=request.thread_id
        )

        return ResponseFormatter.success_response(
            message="Response generated successfully.",
            data={
                "response": pipeline_output["response"],
                "thread_id": pipeline_output["thread_id"]
            }
        )

    except Exception as error:
        logger.error(f"RAG pipeline failed: {str(error)}")
        raise RetrievalException(
            message="The RAG pipeline failed to synthesize an answer for your query.",
            details=str(error)
        )

