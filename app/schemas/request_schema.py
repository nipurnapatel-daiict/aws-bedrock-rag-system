"""
Purpose: Store API request models.
"""

from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str
    thread_id: str | None = None


class UploadRequest(BaseModel):
    file_name: str