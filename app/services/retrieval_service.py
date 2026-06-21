"""
Purpose: Retrieve relevant document chunks from OpenSearch.
"""

from app.core.config import Settings
from app.core.constants import ApplicationConstants
from app.database.crud import OpenSearchCRUD


class RetrievalService:

    def __init__(self):
        self.crud = OpenSearchCRUD()

    def retrieve_similar_chunks(self, query_embedding: list[float]) -> list[dict]:
        """Queries the ngrok OpenSearch index for top-K matching vector chunks."""
        
        target_index = Settings.OPENSEARCH_INDEX 

        search_query = {
            "size": ApplicationConstants.TOP_K_RESULTS,
            "query": {
                "knn": {
                    "embedding_vector": {
                        "vector": query_embedding,
                        "k": ApplicationConstants.TOP_K_RESULTS
                    }
                }
            }
        }

        response = self.crud.search_documents(
            index_name=target_index,
            query=search_query
        )

        if response and "hits" in response and "hits" in response["hits"]:
            return response["hits"]["hits"]
            
        return []
