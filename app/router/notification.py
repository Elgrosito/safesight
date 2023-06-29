from fastapi import APIRouter

from app.utils.notification import send_whatsapp_message

router = APIRouter()

@router.post("/webhook")
async def handle_webhook():
    return send_whatsapp_message()
