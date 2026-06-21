"""
Purpose: FastAPI application entry point.
"""

from fastapi import FastAPI
from app.api.routers import api_router
from app.core.config import Settings
from app.core.logger import LoggerManager
from app.database.index_manager import IndexManager

logger = LoggerManager.get_logger()

app = FastAPI(
    title=Settings.APP_NAME or "RAG Application Backend",
    version=Settings.APP_VERSION or "1.0.0"
)


@app.on_event("startup")
def startup_event():
    try:
        Settings.validate_settings()
        
        index_manager = IndexManager()
        index_manager.create_all_indices()

        logger.info(f"{Settings.APP_NAME} initialized successfully. Indices verified.")
    except Exception as e:
        logger.critical(f"Application failed to initialize: {str(e)}")
        raise e


# --- ROOT ROUTE WITH A SIMPLE WELCOME MESSAGE ---
@app.get("/")
def read_root():
    """Simple welcome message at the absolute root endpoint."""
    return {
        "status": "online",
        "message": f"Welcome to {Settings.APP_NAME or 'RAG Application Backend'}",
        "version": Settings.APP_VERSION or "1.0.0"
    }


# Include your prefixed routes safely
app.include_router(api_router)
