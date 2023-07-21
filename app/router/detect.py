import base64
from fastapi import WebSocket, WebSocketDisconnect
import cv2
from fastapi import APIRouter
from app.utils.notification import send_whatsapp_message
from app.utils.video import draw_rectangles, predict

router = APIRouter()

message_sent = False
@router.websocket("/ws")
async def get_stream(websocket: WebSocket):
    global message_sent

    await websocket.accept()

    current_channel = 9
    while True:
        channel = await websocket.receive_text()  #recibo canal enviado desde el front
        channel = int(channel)
        if channel != current_channel:
            message_sent = False
            current_channel = channel
        try:
            cap = cv2.VideoCapture(channel)

            while True:
                success, frame = cap.read()
                if not success:
                    break
                else:
                    # Recibe el frma y hace la prediccion
                    detections = predict(frame)

                    conf = draw_rectangles(frame, detections)

                    #Transmision
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_base64 = base64.b64encode(buffer).decode('utf-8')
                    await websocket.send_bytes(frame_base64)

                    # envía un mensaje
                    if not message_sent and conf is not None and conf > 0.7:
                        frame_copy = frame.copy()
                        send_whatsapp_message(frame_copy)
                        message_sent = True

        except WebSocketDisconnect:
            print("Client disconnected")
            message_sent = False
            await websocket.accept()
