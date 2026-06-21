"""
Purpose: Handle document upload endpoints with robust cleanup and exception guards.
"""

import os
from fastapi import APIRouter, Depends, File, UploadFile
from app.api.dependencies import get_ingestion_workflow
from app.orchestration.ingestion_workflow import IngestionWorkflow
from app.utils.response_formatter import ResponseFormatter
from app.exceptions.custom_exceptions import DocumentExtractionException

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    ingestion_workflow: IngestionWorkflow = Depends(get_ingestion_workflow)
):
    temp_file_path = f"temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        ingestion_workflow.process_document(
            file_path=temp_file_path,
            file_name=file.filename
        )

        return ResponseFormatter.success_response(
            message="Document processed and indexed successfully.",
            data={"document_name": file.filename}
        )

    except Exception as error:
        raise DocumentExtractionException(
            message=f"Failed to complete processing for document '{file.filename}'.",
            details=str(error)
        )

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
