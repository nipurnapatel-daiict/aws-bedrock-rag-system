"""
Purpose: Orchestrate complete RAG question-answer workflow.
"""

from app.core.constants import ApplicationConstants
from app.llm.bedrock_client import BedrockClient
from app.llm.prompt_builder import PromptBuilder
from app.services.chat_service import ChatService
from app.services.retrieval_service import RetrievalService
from app.services.thread_service import ThreadService
from app.utils.embeddings import EmbeddingGenerator


class RAGWorkflow:

    def __init__(self):
        self.thread_service = ThreadService()
        self.chat_service = ChatService()
        self.retrieval_service = RetrievalService()
        self.bedrock_client = BedrockClient()

    def generate_response(self, user_query: str, thread_id: str | None = None) -> dict:
        """Coordinates history persistence, local embedding lookup, k-NN search, and Bedrock inference."""

        if not thread_id:
            created_thread = self.thread_service.create_thread(title=user_query[:50])
            thread_id = created_thread.thread_id

        self.chat_service.save_message(
            thread_id=thread_id,
            role=ApplicationConstants.USER_ROLE,
            content=user_query
        )

        query_embedding = EmbeddingGenerator.generate_embedding(text=user_query)

        retrieved_chunks = self.retrieval_service.retrieve_similar_chunks(query_embedding=query_embedding)

        context_chunks = [
            chunk["_source"]["chunk_text"]
            for chunk in retrieved_chunks
            if "_source" in chunk and "chunk_text" in chunk["_source"]
        ]

        prompt = PromptBuilder.build_rag_prompt(
            user_query=user_query,
            context_chunks=context_chunks
        )

        llm_response = self.bedrock_client.generate_response(prompt=prompt)

        self.chat_service.save_message(
            thread_id=thread_id,
            role=ApplicationConstants.CHATBOT_ROLE,
            content=llm_response
        )

        return {
            "thread_id": thread_id,
            "response": llm_response
        }
