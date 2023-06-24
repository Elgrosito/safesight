import tensorflow as tf
from google.cloud import storage
import os

class GetData():
    @staticmethod
    def read_image_from_gcs(bucket_name, blob_name):
        """Read an image from a blob in the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Descarga el blob a un objeto BytesIO
        blob_string = blob.download_as_bytes()
        image_tensor = tf.image.decode_image(blob_string)
        return image_tensor

    @classmethod
    def get_images(cls):
        bucket_name = os.getenv('BUCKET_NAME')
        images = []

        # Cliente de storage
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(bucket_name, prefix='images/')

        # Lee cada imagen en memoria
        for blob in blobs:
            images.append(cls.read_image_from_gcs(bucket_name, blob.name))

        return images
