"""
Purpose: Orchestrate complete document ingestion workflow.
"""

from app.core.config import Settings
from app.core.constants import ApplicationConstants
from app.exceptions.custom_exceptions import OpenSearchIndexException
from app.database.crud import OpenSearchCRUD
from app.services.s3_service import S3Service
from app.services.ingestion_service import IngestionService
from app.utils.chunking import TextChunker
from app.utils.pdf_extractor import PDFExtractor
from app.utils.validators import FileValidator


class IngestionWorkflow:

    def __init__(self):
        self.s3_service = S3Service()
        self.ingestion_service = IngestionService()
        self.crud = OpenSearchCRUD()

    def process_document(self,file_path: str,file_name: str):
        is_valid_file = FileValidator.validate_pdf_file(file_name)

        if not is_valid_file:
            raise ValueError("Only PDF files are supported.")

        self.s3_service.upload_file(
            file_path=file_path,
            file_name=file_name
        )

        extracted_text = PDFExtractor.extract_text(file_path=file_path)

        text_chunks = TextChunker.create_chunks(text=extracted_text)

        prepared_chunks = (
            self.ingestion_service.prepare_document_chunks(
                document_name=file_name,
                text_chunks=text_chunks
            )
        )

        target_index = Settings.OPENSEARCH_INDEX 

        try:
            for chunk in prepared_chunks:
                self.crud.insert_document(
                    index_name=target_index,
                    document_id=chunk.chunk_id,
                    document_body=chunk.model_dump()
                )
        except Exception as error:
            raise OpenSearchIndexException(
                message=f"Ingestion pipeline failed while indexing chunks to cluster target: {target_index}",
                details=str(error)
            )

        return prepared_chunks
