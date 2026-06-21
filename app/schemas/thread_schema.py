"""
Purpose: Store chat thread models.
"""

from pydantic import BaseModel

class ThreadModel(BaseModel):

    thread_id: str
    title: str
    created_at: str