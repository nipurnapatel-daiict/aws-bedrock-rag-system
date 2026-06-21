"""
Purpose: Intercepts custom application exceptions and converts them to clean JSON responses.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import RAGAppException
from app.core.logger import LoggerManager

logger = LoggerManager.get_logger()


def register_exception_handlers(app: FastAPI) -> None:
    """Registers global exception interceptors to the FastAPI application instance."""

    @app.exception_handler(RAGAppException)
    async def rag_application_exception_handler(request: Request, exc: RAGAppException):
        error_class_name = exc.__class__.__name__

        logger.error(
            f"Caught Application Error: [{error_class_name}] -> "
            f"Message: {exc.message} | Details: {exc.details or 'None provided'}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "status": "failed",
                "error": error_class_name,
                "message": exc.message,
            },
        )
