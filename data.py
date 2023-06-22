import tensorflow as tf
from google.cloud import storage
import os

bucket_name = os.getenv('BUCKET_NAME')

def read_image_from_gcs(bucket_name, blob_name):
    """Read an image from a blob in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Descarga el blob a un objeto BytesIO
    blob_string = blob.download_as_bytes()
    image_tensor = tf.image.decode_image(blob_string)
    return image_tensor

# La ubicación de tus imágenes en tu bucket
blob_prefix = "images"

# Cliente de storage
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blobs = bucket.list_blobs(prefix=blob_prefix)

# Lee cada imagen en memoria
for blob in blobs:
    image = read_image_from_gcs(bucket_name, blob.name)
