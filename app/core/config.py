"""
Purpose: Centralized application configuration management.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME")
    APP_VERSION = os.getenv("APP_VERSION")
    
    API_HOST = os.getenv("API_HOST")
    API_PORT = os.getenv("APP_PORT")
    
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")

    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    
    OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "opensearch-node")
    OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", 9200))
    OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "analytics-copilot-index")
    
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    MODEL_ID = os.getenv("MODEL_ID")

    @classmethod
    def validate_settings(cls):
        required_settings = {
            "AWS_ACCESS_KEY_ID": cls.AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": cls.AWS_SECRET_ACCESS_KEY,
            "AWS_REGION": cls.AWS_REGION,
            "S3_BUCKET_NAME": cls.S3_BUCKET_NAME,
        }

        missing_settings = [
            key for key, value in required_settings.items() if not value
        ]

        if missing_settings:
            raise EnvironmentError(
                f"Missing required environment variables: {missing_settings}"
            )
            
            
# if __name__ == "__main__":
#     print(Settings.OPENSEARCH_URL)