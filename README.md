# RAG Application

A Retrieval-Augmented Generation (RAG) complete conversational AI application built using:

- AWS S3
- FastAPI
- LangChain
- OpenSearch
- SentenceTransformers
- AWS Bedrock (Amazon Nova)
- Python

This project demonstrates how enterprise AI systems ingest documents, transform them into semantic vectors, store them alongside chat thread metadata, and leverage large language models (LLMs) to perform accurate question answering with persistent session memory.

---

## What This Project Does

* **Document Upload Pipeline**: Uploads PDF documents to AWS S3 for centralized cloud storage archiving.
* **Text Extraction**: Extracts layout string data from PDFs using PyMuPDF.
* **Semantic Chunking**: Splits large documents into meaningful sections using LangChain’s `RecursiveCharacterTextSplitter`.
* **Embedding Generation**: Converts text chunks into semantic vectors locally using SBERT (`all-MiniLM-L6-v2`).
* **Vector Indexing**: Stores embeddings inside an OpenSearch cluster using `knn_vector` alongside multi-turn chat metadata indices.
* **Session Orchestration**: Tracks individual conversation rooms and stores chronological chat dialog messages.
* **Retrieval-Augmented Inference**: Queries the vector index, formats isolated reference prompts, and invokes Amazon Nova Micro via the AWS Bedrock Converse API to deliver answers.

---

## Features

- PDF ingestion and upload pipeline
- AWS S3 integration
- Semantic text chunking using LangChain
- Local embedding generation using SentenceTransformers
- OpenSearch vector indexing and HNSW k-NN retrieval
- Context-grounded Retrieval-Augmented Generation
- Chat thread management and tracking
- Chronological message history storage
- Custom exception handling for database and model layers
- FastAPI prefix-mapped routing infrastructure
- Logging and validation support

---

## Technologies Used


| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | API development and endpoint routing |
| AWS S3 | PDF document cloud archiving |
| PyMuPDF | Local PDF text extraction |
| LangChain | Semantic text chunking |
| SentenceTransformers (`all-MiniLM-L6-v2`) | Embedding generation |
| OpenSearch | Vector and conversation metadata database |
| AWS Bedrock (`amazon.nova-micro-v1:0`) | LLM response generation |
| Boto3 | AWS S3 and Bedrock service integration |
| Pytest | Automated pipeline validation |

---

## Why PyMuPDF Instead of Textract?

AWS Textract is a paid OCR service and introduces recurring extraction costs.

PyMuPDF was selected because:

- free and lightweight
- excellent for text-based PDFs
- fast extraction speed
- simple integration
- ideal for local experimentation

The architecture remains fully compatible with future Textract integration.

---

## Why SentenceTransformers Instead of Titan Embeddings?

Amazon Titan Embeddings require Bedrock access and incur usage cost.

SentenceTransformers (`all-MiniLM-L6-v2`) was selected because:

- free local embedding generation
- strong semantic retrieval performance (outputs 384 dimensions)
- lightweight model size
- production-quality embeddings
- easy experimentation

This preserves the same vector ingestion architecture while reducing operational cost.

---

## Project Structure

```text
milestone-02-rag-application/
│
├── app/
│   │
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── ask_endpoint.py       # RAG pipeline routing
│   │   │   ├── health_endpoint.py    # Health status routing
│   │   │   ├── message_endpoint.py   # Message history routing
│   │   │   ├── thread_endpoint.py    # Chat thread workspace routing
│   │   │   └── upload_endpoint.py    # Document upload routing
│   │   ├── dependencies.py           # Dependency injection factory
│   │   └── routers.py                # Unified prefixed router setup
│   │
│   ├── core/
│   │   ├── config.py                 # Centralized Settings validation
│   │   ├── constants.py              # Application-wide constants
│   │   └── logger.py                 # Centralized logging configuration
│   │
│   ├── database/
│   │   ├── crud.py                   # OpenSearch core CRUD operations
│   │   ├── index_manager.py          # Automatic index compilation
│   │   └── opensearch_client.py      # Secure OpenSearch client setup
│   │
│   ├── exceptions/
│   │   └── custom_exceptions.py      # Structural exception wrappers
│   │
│   ├── llm/
│   │   └── bedrock_client.py         # AWS Bedrock Converse API interface
│   │
│   ├── orchestration/
│   │   ├── chat_workflow.py          # Chat log aggregator workflow
│   │   ├── ingestion_workflow.py     # Document preparation workflow
│   │   └── rag_workflow.py           # End-to-end RAG workflow
│   │
│   ├── schemas/
│   │   ├── document.py               # Vector chunk schemas
│   │   ├── message.py                # Conversation message schemas
│   │   ├── request.py                # Payload input validations
│   │   ├── response.py               # Payload output serializations
│   │   └── thread.py                 # Chat thread workspace schemas
│   │
│   └── main.py                       # Root entry point & lifespan manager
│
├── data/
│   └── sample_files/                 # Input evaluation documents
│
├── logs/                             # Application files rolling logs
│
├── tests/
│   ├── test_chat.py                  # RAG generation test script
│   ├── test_evaluation_15.py         # 15-Question quality test suite
│   ├── test_ingestion.py             # Document ingestion test script
│   └── test_retrieval.py             # Similarity search test script
│
├── .env                              # Environment variable keys
├── .gitignore                        # Git ignored folders list
├── requirements.txt                  # System dependency manifest
└── README.md                         # Project documentation manual
```

---

## Architecture Overview

```text
PDF Files
    ↓
AWS S3 Upload
    ↓
Text Extraction
    ↓
Semantic Chunking
    ↓
Embedding Generation
    ↓
OpenSearch Vector Indexing
    ↓
User Query → Semantic Retrieval → Prompt Building → AWS Bedrock LLM → Response
```

---

# Ingestion Pipeline Flow

The ingestion pipeline follows a clean orchestration strategy:

```text
File Upload & Validation
    ↓
S3 Bucket Storage Archival
    ↓
Local PyMuPDF Layout Parsing
    ↓
Recursive Chunk Partitioning
    ↓
Local Embedding Computation
    ↓
OpenSearch Vector DB Storage
```

---

## Steps Performed

### 1. Uploading PDFs to S3

The endpoint validates file formats and uploads the document to an AWS S3 bucket for tracking and reference.

---

### 2. Extracting Text from PDFs

PyMuPDF handles the layout parsing, reading page contents locally.

---

### 3. Semantic Chunking using LangChain

LangChain’s `RecursiveCharacterTextSplitter` processes the raw text.

Configuration:


| Parameter | Value |
|---|---|
| Chunk Size | 500 characters |
| Chunk Overlap | 100 characters |

---

### 4. Generating Embeddings

Each chunk is passed to the local Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

This converts text fragments into dense 384-dimension vectors.

---

### 5. OpenSearch Vector Indexing

The chunks and vectors are sent over the secure ngrok tunnel connection to be indexed under the environment target collection using:

- `knn_vector` field mappings
- HNSW (Hierarchical Navigable Small World) engine
- Cosine similarity tracking

---

### 6. Semantic Retrieval & Inference

The RAG workflow coordinates these tasks dynamically when an api request is received:

```text
User Query
    ↓
Generate Local Query Embedding
    ↓
OpenSearch HNSW k-NN Similarity Search
    ↓
Extract Top-K Context Snippets
    ↓
Assemble Left-Aligned Prompt Context
    ↓
Invoke AWS Bedrock Converse API (Amazon Nova Micro)
    ↓
Save Message Log Exchange & Return Response
```

---

# Retrieval Evaluation

The application contains a robust evaluation test script (`tests/test_evaluation_15.py`) processing **15 distinct evaluation questions** mapped to your document assets.

Testing can be triggered using your virtual environment Python module:

```bash
python -m pytest -v -s tests/test_evaluation_15.py
```

The evaluation confirms:

- **Context Grounding**: Accurate response synthesis using document data.
- **Session Continuity**: Message retention when follow-up queries pass an existing thread identifier.

---

## OpenSearch Vector Configuration

The system uses:

- HNSW indexing
- Cosine similarity matching (`cosinesimil`)
- k-NN vector parameters (`ef_construction: 128`, `m: 16`)

for efficient semantic retrieval.

---

## Conclusion
This end-to-end local RAG pipeline successfully integrates PyMuPDF extraction and Sentence Transformers (all-MiniLM-L6-v2) to eliminate cloud ingest costs [384 dimensions]. Chunks are indexed via OpenSearch HNSW k-NN vectors over a secure ngrok tunnel, supporting fully persistent multi-turn chat sessions. Finally, query answers are generated through Amazon Nova Micro via the modern AWS Bedrock Converse API, creating a robust architecture.
