"""
Purpose: Build prompts for RAG response generation.
"""

class PromptBuilder:

    @staticmethod
    def build_rag_prompt(user_query: str, context_chunks: list[str]) -> str:
        """Assembles context fragments and the user query into a clean, concise LLM prompt."""
        context = "\n\n".join(context_chunks)

        return (
f"You are a helpful, concise AI assistant.\n\n"
f"Instructions:\n"
f"- Answer the user query accurately using only the provided context.\n"
f"- Keep your response short, punchy, and direct (maximum 2-3 sentences).\n"
f"- Use brief bullet points only if absolutely necessary for list-based data.\n"
f"- Avoid long introductory phrases or repetitive conversational filler.\n\n"
f"Context:\n{context}\n\n"
f"User Query:\n{user_query}\n\n"
f"Answer:"
        )