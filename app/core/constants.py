"""
Purpose: Stores reusable application constants.
"""

class ApplicationConstants:

    API_PREFIX = "/rag-app/v1"

    THREAD_INDEX = "chat_threads_index"
    MESSAGE_INDEX = "chat_messages_index"

    VECTOR_DIMENSION = 384

    KNN_VECTOR_TYPE = "knn_vector"
    KNN_ENGINE = "nmslib"
    SPACE_TYPE = "cosinesimil"

    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100

    TOP_K_RESULTS = 5

    USER_ROLE = "user"
    CHATBOT_ROLE = "chatbot"

    SUPPORTED_FILE_TYPES = [".pdf"]

    LOGGER_NAME = "rag_application"
    LOG_DIRECTORY = "logs"
    LOG_FILE_NAME = "application.log"

    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"