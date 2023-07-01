import os
from typing import Any
from twilio.rest import Client

def send_whatsapp_message(object: Any):
    print(object)

    fb_account_id = os.environ['FB_ACCOUNTID']
    auth_token = os.environ['AUTH_TOKEN']

    client = Client(fb_account_id, auth_token)

    destination_phone = 'whatsapp:+573172885469'
    message = 'Hemos detectado un arma en una de sus cámaras'
    url_img = 'https://i.pinimg.com/564x/77/b2/f4/77b2f43d5805eb85f022bbb47b74cc46.jpg'

    # Envía el mensaje de WhatsApp con la imagen adjunta
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=destination_phone,
        media_url=[url_img]
    )

    # Verifica el estado del mensaje
    if message.status == "queued" or message.status == "sent":
        return "Mensaje de WhatsApp enviado correctamente"
    else:
        return  message.error_message
