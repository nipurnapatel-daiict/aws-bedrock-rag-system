"""
Purpose: Manage chat thread operations.
"""

from app.core.constants import ApplicationConstants
from app.database.crud import OpenSearchCRUD
from app.schemas.thread_schema import ThreadModel
from app.utils.id_generator import IDGenerator
from app.utils.timestamp import TimestampManager


class ThreadService:

    def __init__(self):
        self.crud = OpenSearchCRUD()

    def create_thread(self,title: str) -> ThreadModel:
        thread = ThreadModel(
            thread_id=IDGenerator.generate_id(),
            title=title,
            created_at=TimestampManager.get_current_timestamp()
        )

        self.crud.insert_document(
            index_name=ApplicationConstants.THREAD_INDEX,
            document_id=thread.thread_id,
            document_body=thread.model_dump()
        )

        return thread
