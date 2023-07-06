import base64
import subprocess
import aiohttp
from fastapi import WebSocket, WebSocketDisconnect
import cv2
from fastapi import APIRouter
from app.utils.modelling import run_object_detection
from app.utils.notification import send_whatsapp_message
from app.utils.video import draw_rectangles, predict

router = APIRouter()

message_sent = False
@router.websocket("/ws")
async def get_stream(websocket: WebSocket):
    global message_sent

    await websocket.accept()

    while True:
        try:
            cap = cv2.VideoCapture(1)

            while True:
                success, frame = cap.read()
                if not success:
                    break
                else:
                    # aqui va la funcion que recibe el frma y hace la prediccion
                    detections = predict(frame)
                    frame_copy = frame.copy()

                    draw_rectangles(frame, detections)

                    #Transmision
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_base64 = base64.b64encode(buffer).decode('utf-8')
                    await websocket.send_bytes(frame_base64)

                    # envía un mensaje
                    if not message_sent and any(detection[4] > 0.7 for detection in detections):
                        send_whatsapp_message(frame_copy)
                        message_sent = True

        except WebSocketDisconnect:
            print("Client disconnected")
            message_sent = False
            await websocket.accept()
