"""
Purpose: Handle AWS S3 document operations.
"""

import boto3
from app.core.config import Settings  
from app.exceptions.custom_exceptions import S3UploadException  


class S3Service:

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION
        )

    def upload_file(self, file_path: str, file_name: str) -> str:
        try:
            self.client.upload_file(
                file_path,
                Settings.S3_BUCKET_NAME,
                file_name
            )
            return file_name
        except Exception as error:
            raise S3UploadException(
                message=f"Failed to upload file '{file_name}' to S3 bucket.",
                details=str(error)
            )
