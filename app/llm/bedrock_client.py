"""
Purpose: Handle AWS Bedrock model interactions using the modern Converse API for Amazon Nova.
"""

import boto3
from app.core.config import Settings
from app.exceptions.custom_exceptions    import RetrievalException


class BedrockClient:

    def __init__(self):
        self.client = boto3.client(
            service_name="bedrock-runtime",
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION
        )

    def generate_response(self, prompt: str) -> str:
        """Invokes AWS Bedrock text generation using the official Converse API structure."""
        
        model_id = Settings.MODEL_ID

        messages = [
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ]

        inference_config = {
            "maxTokens": 512,
            "temperature": 0.5,
            "topP": 0.9
        }

        try:
            response = self.client.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig=inference_config
            )

            output_text = response["output"]["message"]["content"][0]["text"]
            return output_text

        except Exception as error:
            print(f"\n[CRITICAL LLM ERROR] Converse API failed for model: {model_id}. Reason: {str(error)}\n")
            raise RetrievalException(
                message=f"AWS Bedrock inference failed using model instance '{model_id}'.",
                details=str(error)
            )
