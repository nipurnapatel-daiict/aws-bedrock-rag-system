"""
Purpose: Handle OpenSearch CRUD operations with structural error handling.
"""

from opensearchpy.exceptions import NotFoundError
from app.database.opensearch_client import OpenSearchClient
from app.exceptions.custom_exceptions import OpenSearchIndexException, RetrievalException


class OpenSearchCRUD:

    def __init__(self):
        self.client = OpenSearchClient.get_client()

    def insert_document(self, index_name: str, document_id: str, document_body: dict) -> dict:
        """Inserts or updates a document in a specified index."""
        try:
            return self.client.index(
                index=index_name,
                id=document_id,
                body=document_body,
                refresh=True
            )
        except Exception as e:
            raise OpenSearchIndexException(
                message=f"Failed to insert document ID {document_id} into index '{index_name}'",
                details=str(e)
            )

    def search_documents(self, index_name: str, query: dict) -> dict:
        """Executes vector or keyword queries against a target index."""
        try:
            return self.client.search(
                index=index_name,
                body=query
            )
        except Exception as e:
            raise RetrievalException(
                message=f"Search execution failed on index '{index_name}'",
                details=str(e)
            )

    def delete_document(self, index_name: str, document_id: str) -> dict:
        """Removes a document from the collection by ID."""
        try:
            return self.client.delete(
                index=index_name,
                id=document_id,
                refresh=True
            )
        except NotFoundError:
            ## Return a controlled structure if the document to delete wasn't there
            return {"result": "not_found", "id": document_id}
        except Exception as e:
            raise OpenSearchIndexException(
                message=f"Failed to delete document ID {document_id} from index '{index_name}'",
                details=str(e)
            )

    def get_document(self, index_name: str, document_id: str) -> dict | None:
        """Retrieves an explicit document by ID. Returns None if missing."""
        try:
            return self.client.get(
                index=index_name,
                id=document_id
            )
        except NotFoundError:
            ## Prevents a crash by returning None gracefully if the document is absent
            return None
        except Exception as e:
            raise RetrievalException(
                message=f"Failed fetching document ID {document_id} from index '{index_name}'",
                details=str(e)
            )
