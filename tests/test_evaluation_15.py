"""
Purpose: Bulk evaluate RAG pipeline retrieval and generation quality using 15 precise context questions.
"""

import pytest
from app.orchestration.rag_workflow import RAGWorkflow


def test_rag_fifteen_questions_evaluation():
    """Executes a 15-question benchmark to document retrieval quality and Amazon Nova responses."""
    workflow = RAGWorkflow()

    eval_questions = [
        # Section 1: Transformer Architecture Questions 
        "What was the main problem with sequential processing before transformers?",
        "Explain the 'Satellite View' analogy used to describe how a transformer works.",
        "How does self-attention handle the relationship between words like 'it' and 'phone'?",
        "What are the specific roles of Expert 1, Expert 2, and Expert 3 in Multi-Head Attention?",
        "Why do transformers need Positional Encoding, and what analogy is used for it?",
        "What is the difference between the Encoder (The Chef) and the Decoder (The Waiter)?",
        "How does a transformer model learn during the training phase?",
        
        # Section 2: LangChain Framework Questions 
        "What is LangChain and what is the 'LEGO connectors' analogy describing?",
        "List the four sequential steps a typical LangChain 'chain' might perform.",
        "What are the three major weaknesses of LLMs that LangChain fixes?",
        "Identify two common locations or enterprise use cases where LangChain is used.",
        "When should a developer move past a prototype and start using LangChain?",
        "Explain the 'Open Book exam' analogy regarding LangChain's Retrieval (RAG) process.",
        "What is an Agent in LangChain and how does the 'smart intern' analogy apply to it?",
        "How does LangChain serve as a 'universal remote' for different AI models?"
    ]

    ## Initialize a unified thread ID to evaluate conversation history tracking
    thread_id = None  

    
    for index, question in enumerate(eval_questions, 1):
        ## Run through full pipeline: Embedding -> ngrok OpenSearch k-NN -> Prompt Builder -> Bedrock Converse
        output = workflow.generate_response(user_query=question, thread_id=thread_id)
        
        thread_id = output["thread_id"]
        response_text = output["response"]

        assert response_text is not None
        assert isinstance(response_text, str)
        assert len(response_text.strip()) > 0

        print(f"\n [EVALUATION TEST {index}/15]")
        print(f"QUESTION  : {question}")
        print(f"NOVA AMZN : {response_text.strip()}")
        print(f"THREAD ID : {thread_id}")
        print("-" * 80)
        
