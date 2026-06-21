"""
Purpose: Store API response models.
"""

from pydantic import BaseModel

class UploadResponse(BaseModel):
    status: str
    message: str
    document_name: str


class AskResponse(BaseModel):
    status: str
    response: str
    thread_id: str