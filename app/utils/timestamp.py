"""
Purpose: Generate timestamp values for application records.
"""

from datetime import datetime, timezone

class TimestampManager:

    @staticmethod
    def get_current_timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()
