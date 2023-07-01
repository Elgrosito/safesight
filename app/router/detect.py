import base64
from fastapi import APIRouter, Request

from app.utils.notification import send_whatsapp_message

router = APIRouter()

@router.post("/detect-weapon")
async def detect(request: Request):
    print(request)
    # # Obtener la imagen del request
    # data = await request.json()
    # img_data = data['image'].split(',', 1)[1]
    # img_data = base64.b64decode(img_data)
    # image = Image.open(io.BytesIO(img_data))

    # # Pasar la imagen al modelo YOLO
    # objetos_detectados = detectar_objeto(image)

    # # Si se detecta un objeto, enviar una notificación (esto es solo un ejemplo)
    # if objetos_detectados:
    #     send_whatsapp_message(objetos_detectados)

    # # Devolver una respuesta
    # return {'objetos_detectados': objetos_detectados}
