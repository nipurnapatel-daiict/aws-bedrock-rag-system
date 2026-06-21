"""
Purpose: Register and prefix all application API routes.
"""

from fastapi import APIRouter
from app.core.constants import ApplicationConstants
from app.api.endpoints.ask_endpoint import router as ask_router
from app.api.endpoints.health_endpoint import router as health_router
from app.api.endpoints.message_endpoint import router as message_router
from app.api.endpoints.thread_endpoint import router as thread_router
from app.api.endpoints.upload_endpoint import router as upload_router

api_router = APIRouter(prefix=ApplicationConstants.API_PREFIX)

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(upload_router, tags=["Upload"])
api_router.include_router(ask_router, tags=["RAG"])
api_router.include_router(thread_router, tags=["Threads"])
api_router.include_router(message_router, tags=["Messages"])
