from fastapi import APIRouter
from .import notification, detect

api_router = APIRouter()

api_router.include_router(notification.router, prefix="/notification")
api_router.include_router(detect.router, prefix="/detect")
