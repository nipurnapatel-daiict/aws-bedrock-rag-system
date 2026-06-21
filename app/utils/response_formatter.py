"""
Purpose: Format standardized API responses.
"""

from app.core.constants import ApplicationConstants

class ResponseFormatter:

    @staticmethod
    def success_response(message: str, data: dict = None) -> dict:
        response = {
            "status": ApplicationConstants.STATUS_SUCCESS,
            "message": message
        }
        if data:
            response.update(data)
        return response

    @staticmethod
    def error_response(message: str) -> dict:
        return {
            "status": ApplicationConstants.STATUS_FAILED,
            "message": message
        }
