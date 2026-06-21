"""
Purpose: Provide application health check endpoints with structural exception guards.
"""

from fastapi import APIRouter
from app.core.config import Settings
from app.exceptions.custom_exceptions import RetrievalException

router = APIRouter()

@router.get("/health")
def health_check():
    """Simple endpoint to verify server and database targeting status."""
    try:
        host = Settings.OPENSEARCH_HOST 
        port = Settings.OPENSEARCH_PORT 
        protocol = "https" if port == "443" else "http"
        opensearch_url = f"{protocol}://{host}:{port}"

        return {
            "status": "healthy",
            "opensearch_target": opensearch_url,
            "index_target": Settings.OPENSEARCH_INDEX,
            "embedding_model": Settings.EMBEDDING_MODEL
        }
        
    except Exception as error:
        raise RetrievalException(
            message="Health check assessment failed due to internal configuration issues.",
            details=str(error)
        )
