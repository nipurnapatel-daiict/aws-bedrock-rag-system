"""
Purpose: Handle chat message endpoints with robust exception guards.
"""

from fastapi import APIRouter, Depends
from app.api.dependencies import get_chat_workflow
from app.orchestration.chat_workflow import ChatWorkflow
from app.exceptions.custom_exceptions import RetrievalException
from app.utils.response_formatter import ResponseFormatter

router = APIRouter()

@router.get("/messages/{thread_id}")
def get_thread_messages(
    thread_id: str,
    chat_workflow: ChatWorkflow = Depends(get_chat_workflow)
):
    """Retrieves chronological dialog exchanges for a specific thread workspace."""
    try:
        messages = chat_workflow.get_thread_messages( thread_id=thread_id)

        formatted_messages = [
            {
                "message_id": hit["_source"]["message_id"],
                "thread_id": hit["_source"]["thread_id"],
                "role": hit["_source"]["role"],
                "content": hit["_source"]["content"],
                "created_at": hit["_source"]["created_at"]
            }
            for hit in messages
            if "_source" in hit
        ]

        return ResponseFormatter.success_response(
            message="Messages fetched successfully.",
            data={"messages": formatted_messages}
        )

    except Exception as error:
        raise RetrievalException(
            message=f"Failed to retrieve chat messages for session room: '{thread_id}'.",
            details=str(error)
        )
