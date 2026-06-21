"""
Purpose: Orchestrate chat history and thread workflows.
"""

from app.core.constants import ApplicationConstants
from app.database.crud import OpenSearchCRUD

class ChatWorkflow:

    def __init__(self):
        self.crud = OpenSearchCRUD()

    def get_thread_messages(self,thread_id: str) -> list[dict]:
        """Fetches chronological messages tied to a specific session workspace ID."""
        search_query = {
            "query": {
                "term": {
                    "thread_id": thread_id
                }
            },
            "sort": [
                {
                    "created_at": {
                        "order": "asc"
                    }
                }
            ]
        }

        response = self.crud.search_documents(
            index_name=ApplicationConstants.MESSAGE_INDEX,
            query=search_query
        )

        if response and "hits" in response and "hits" in response["hits"]:
            return response["hits"]["hits"]
            
        return []

    def get_recent_threads(self) -> list[dict]:
        """Lists active and recent user chat sessions sorted by newest creation times."""
        search_query = {
            "sort": [
                {
                    "created_at": {
                        "order": "desc"
                    }
                }
            ]
        }

        response = self.crud.search_documents(
            index_name=ApplicationConstants.THREAD_INDEX,
            query=search_query
        )

        if response and "hits" in response and "hits" in response["hits"]:
            return response["hits"]["hits"]
            
        return []
