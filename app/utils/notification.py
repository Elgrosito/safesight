import os
from typing import Any
import cv2
from twilio.rest import Client
from google.cloud import storage
import cv2
import numpy as np

def send_whatsapp_message(frame: Any):
    try:
        # Convierto la imagen
        _, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()

        # Crea un cliente de Google Cloud Storage
        client = storage.Client()
        bucket = client.get_bucket('safesight')
        blob = bucket.blob('evidencia.jpg')
        blob.upload_from_string(img_bytes, content_type='image/jpeg')

        # Obtiene la URL pública
        url_img = blob.public_url
        print(url_img)

        fb_account_id = os.environ['FB_ACCOUNTID']
        auth_token = os.environ['AUTH_TOKEN']

        client = Client(fb_account_id, auth_token)

        destination_phone = 'whatsapp:+573172885469'
        message = 'Hemos detectado un arma en una de sus cámaras'

        # Envía el mensaje de WhatsApp con la imagen adjunta
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=destination_phone,
            media_url='https://i.pinimg.com/564x/a8/17/4f/a8174f08ecba552fcabc5295862d92bf.jpg'
        )

        # Verifica el estado del mensaje
        if message.status == "queued" or message.status == "sent":
            return "Mensaje de WhatsApp enviado correctamente"
        else:
            return  message.error_message

    except Exception as e:
        print(f"Error al enviar el mensaje de WhatsApp: {e}")
        return str(e)
