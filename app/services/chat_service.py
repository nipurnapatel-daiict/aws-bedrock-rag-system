"""
Purpose: Manage chat message operations.
"""

from app.core.constants import ApplicationConstants
from app.database.crud import OpenSearchCRUD
from app.schemas.message_schema import MessageModel
from app.utils.id_generator import IDGenerator
from app.utils.timestamp import TimestampManager


class ChatService:

    def __init__(self):
        self.crud = OpenSearchCRUD()

    def save_message(self, thread_id: str,role: str,content: str) -> MessageModel:
        message = MessageModel(
            message_id=IDGenerator.generate_id(),
            thread_id=thread_id,
            role=role,
            content=content,
            created_at=TimestampManager.get_current_timestamp()
        )

        self.crud.insert_document(
            index_name=ApplicationConstants.MESSAGE_INDEX,
            document_id=message.message_id,
            document_body=message.model_dump()
        )

        return message
