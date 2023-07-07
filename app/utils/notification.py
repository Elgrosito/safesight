import os
from typing import Any
from twilio.rest import Client
from google.cloud import storage
import cv2
from PIL import Image
import io


def send_whatsapp_message(frame: Any):
    try:
        # Convierto la imagen
        _, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()

        image = Image.open(io.BytesIO(img_bytes))

        # Reducir el tamaño de la imagen
        output_io_stream = io.BytesIO()
        image.save(output_io_stream, format='JPEG', quality=20)
        output_io_stream.seek(0)
        img_bytes_reduced = output_io_stream.read()

        # Crea un cliente de Google Cloud Storage
        client = storage.Client()
        bucket = client.get_bucket('safesight')
        blob = bucket.blob('evidencia.jpeg')
        blob.upload_from_string(img_bytes_reduced, content_type='image/jpeg')

        # Obtiene la URL pública
        url_img = blob.public_url

        account_sid = os.environ['FB_ACCOUNTID']
        auth_token = os.environ['AUTH_TOKEN']

        client = Client(account_sid, auth_token)

        destination_phone = 'whatsapp:+573172885469'
        message = 'Hemos detectado un arma en una de sus cámaras'

        # Envía el mensaje de WhatsApp con la imagen adjunta
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=destination_phone,
            media_url=url_img
        )

        # Verifica el estado del mensaje
        if message.status == "queued" or message.status == "sent":
            return "Mensaje de WhatsApp enviado correctamente"
        else:
            return  message.error_message

    except Exception as e:
        print(f"Error al enviar el mensaje de WhatsApp: {e}")
        return str(e)
