"""
Purpose: Handle chat thread endpoints with exception isolation.
"""

from fastapi import APIRouter, Depends
from app.api.dependencies import get_chat_workflow
from app.orchestration.chat_workflow import ChatWorkflow
from app.exceptions.custom_exceptions import RetrievalException
from app.utils.response_formatter import ResponseFormatter

router = APIRouter()

@router.get("/threads")
def get_recent_threads(chat_workflow: ChatWorkflow = Depends(get_chat_workflow)):
    """Retrieves active chat threads from the OpenSearch history index."""
    try:
        threads = chat_workflow.get_recent_threads()
        
        formatted_threads = [
            {
                "thread_id": hit["_source"]["thread_id"],
                "title": hit["_source"]["title"],
                "created_at": hit["_source"]["created_at"]
            }
            for hit in threads
            if "_source" in hit
        ]

        return ResponseFormatter.success_response(
            message="Threads fetched successfully.",
            data={"threads": formatted_threads}
        )

    except Exception as error:
        raise RetrievalException(
            message="Failed to retrieve recent conversational workspaces.",
            details=str(error)
        )

