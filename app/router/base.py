from fastapi import APIRouter
from .import notification

api_router = APIRouter()

api_router.include_router(notification.router, prefix="/notification")
