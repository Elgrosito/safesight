from uuid import uuid4
from google.cloud import storage
from fastapi import UploadFile
from app.utils.logger import logger
from PIL import Image
from io import BytesIO

CREDENTIALS = ""
BUCKET_NAME = ""

class GCStorage:
    def __init__(self, bucket_name: str, storage_client):
        self.bucket_name = bucket_name
        self.storage_client = storage_client

    def upload_file(self, file):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        file_path = str(uuid4())
        blob = bucket.blob(file_path)
        blob.upload_from_file(file.file.read(), content_type="image/jpeg")
        file_url = f"https://storage.googleapis.com/{self.bucket_name}/{file_path}/{file.filename}"
        return file_url

    def delete_file(self, file_url: str):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        file_path = file_url.split('/')[-2]
        try:
            blob = bucket.blob(file_path)
            blob.delete()
        except google.cloud.exceptions.NotFound:
            logger.info(f"File not found: {file_url}")
        except Exception as e:
            logger.error(f"Error deleting file: {file_url}. {str(e)}")

    def retrieve_file_url(self, file_name: str):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        image_url = blob.public_url
        image_bytes = blob.download_as_bytes()
        return image_bytes
