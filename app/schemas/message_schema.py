"""
Purpose: Store chat message models.
"""

from pydantic import BaseModel

class MessageModel(BaseModel):
    message_id: str
    thread_id: str
    role: str
    content: str
    created_at: str