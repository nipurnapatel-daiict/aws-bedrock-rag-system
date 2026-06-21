"""
Purpose: Create and manage OpenSearch client connection.
"""

from opensearchpy import OpenSearch, RequestsHttpConnection
from app.core.config import Settings
from app.exceptions.custom_exceptions import OpenSearchConnectionException


class OpenSearchClient:
    @staticmethod
    def get_client() -> OpenSearch:
        try:
            # clean_host = Settings.OPENSEARCH_HOST.replace("https://", "").replace("http://", "")
            # port = int(Settings.OPENSEARCH_PORT)
            clean_host = "localhost"
            port = 9200
            
            return OpenSearch(
                hosts=[{"host": clean_host, "port": port}],
                use_ssl=False,         
                verify_certs=False,    
                http_compress=True,
                connection_class=RequestsHttpConnection
            )
        except Exception as e:
            raise OpenSearchConnectionException(
                message="Could not initialize connection to OpenSearch.",
                details=str(e)
            )
