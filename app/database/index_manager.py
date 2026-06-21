"""
Purpose: Manage OpenSearch index creation and validation.
"""

from app.core.config import Settings
from app.core.constants import ApplicationConstants
from app.exceptions.custom_exceptions import OpenSearchIndexException
from app.database.opensearch_client import OpenSearchClient


class IndexManager:

    def __init__(self):
        self.client = OpenSearchClient.get_client()

    def create_document_index(self):
        target_index = Settings.OPENSEARCH_INDEX 

        try:
            index_exists = False
            try:
                self.client.indices.get(index=target_index)
                index_exists = True
            except Exception:
                index_exists = False

            if index_exists:
                print(f"Index {target_index} already exists.")
                return

            index_mapping = {
                "settings": {
                    "index": {
                        "knn": "true", 
                        "number_of_shards": 1,
                        "number_of_replicas": 1
                    }
                },
                "mappings": {
                    "properties": {
                        "chunk_id": {"type": "keyword"},
                        "document_name": {"type": "keyword"},
                        "chunk_text": {"type": "text"},
                        "embedding_vector": {
                            "type": "knn_vector", 
                            "dimension": ApplicationConstants.VECTOR_DIMENSION,
                            "method": {
                                "name": "hnsw",
                                "engine": "nmslib", 
                                "space_type": "l2",
                                "parameters": {
                                    "ef_construction": 128,
                                    "m": 16
                                }
                            }
                        }
                    }
                }
            }

            print(f"Creating index: {target_index}...")
            self.client.indices.create(index=target_index, body=index_mapping)
            print("Index created successfully!")

        except Exception as e:
            print(f"--- OPENSEARCH ERROR DETAILS --- \n{str(e)}\n-------------------")
            raise OpenSearchIndexException(
                message=f"Failed to compile or check document vector index: {target_index}",
                details=str(e)
            )


    def create_thread_index(self):
        try:
            if self.client.indices.exists(index=ApplicationConstants.THREAD_INDEX):
                return

            mapping = {
                "mappings": {
                    "properties": {
                        "thread_id": {
                            "type": "keyword"
                        },
                        "title": {
                            "type": "text"
                        },
                        "created_at": {
                            "type": "date"
                        }
                    }
                }
            }

            self.client.indices.create(index=ApplicationConstants.THREAD_INDEX, body=mapping)
        except Exception as e:
            raise OpenSearchIndexException(
                message=f"Failed to create chat thread index: {ApplicationConstants.THREAD_INDEX}",
                details=str(e)
            )

    def create_message_index(self):
        try:
            if self.client.indices.exists(index=ApplicationConstants.MESSAGE_INDEX):
                return

            mapping = {
                "mappings": {
                    "properties": {
                        "message_id": {
                            "type": "keyword"
                        },
                        "thread_id": {
                            "type": "keyword"
                        },
                        "role": {
                            "type": "keyword"
                        },
                        "content": {
                            "type": "text"
                        },
                        "created_at": {
                            "type": "date"
                        }
                    }
                }
            }

            self.client.indices.create(index=ApplicationConstants.MESSAGE_INDEX, body=mapping)
        except Exception as e:
            raise OpenSearchIndexException(
                message=f"Failed to build message history index: {ApplicationConstants.MESSAGE_INDEX}",
                details=str(e)
            )

    def create_all_indices(self):
        self.create_document_index()
        self.create_thread_index()
        self.create_message_index()
