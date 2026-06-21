"""
Purpose: Coordinate end-to-end PDF processing, embedding, and vector database indexing.
"""

from app.schemas.document_schema import DocumentChunk  
from app.core.config import Settings
from app.database.crud import OpenSearchCRUD
from app.utils.pdf_extractor import PDFExtractor
from app.utils.chunking import TextChunker
from app.utils.embeddings import EmbeddingGenerator
from app.utils.id_generator import IDGenerator


class IngestionService:
    def __init__(self):
        self.db = OpenSearchCRUD()

    def process_and_index_pdf(self, file_path: str, file_name: str) -> int:
        """Runs the entire ingestion pipeline and pushes document vectors to OpenSearch."""
        
        full_text = PDFExtractor.extract_text(file_path)
        
        text_chunks = TextChunker.create_chunks(full_text)
        
        prepared_chunks = self.prepare_document_chunks(file_name, text_chunks)
        
        target_index = Settings.OPENSEARCH_INDEX 
        for chunk in prepared_chunks:
            self.db.insert_document(
                index_name=target_index,
                document_id=chunk.chunk_id,
                document_body=chunk.model_dump()  
            )
            
        return len(prepared_chunks)

    @staticmethod
    def prepare_document_chunks(document_name: str, text_chunks: list[str]) -> list[DocumentChunk]:
        """Prepares structural schema instances with unique IDs and local vector embeddings."""
        embeddings = EmbeddingGenerator.generate_embeddings(text_chunks)

        prepared_chunks = []

        for chunk_text, embedding in zip(text_chunks, embeddings):
            prepared_chunks.append(
                DocumentChunk(
                    chunk_id=IDGenerator.generate_id(),
                    document_name=document_name,
                    chunk_text=chunk_text,
                    embedding_vector=embedding
                )
            )

        return prepared_chunks
