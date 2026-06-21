"""
Purpose: Generate unique identifiers for application entities.
"""

import uuid

class IDGenerator:
    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())