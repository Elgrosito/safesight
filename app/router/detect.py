import base64
import subprocess
import aiohttp
from fastapi import WebSocket, WebSocketDisconnect
import time
import cv2
from fastapi import APIRouter
from app.utils.sockets import sio_server
from app.utils.modelling import run_object_detection
from app.utils.notification import send_whatsapp_message

router = APIRouter()

@router.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        cap = cv2.VideoCapture(1)

        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                #detection
                # command = "python yolov5/detect.py --source 0 --conf 0.25 --weights yolov5/runs/train/exp4/weights/best.pt"
                # process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # out, _ = process.communicate(input=frame.tobytes())
                # process.wait()

                # # Obtener el output
                # detection_output = out.decode()

                # # Process the detection results
                # lines = detection_output.strip().split("\n")
                # results = []
                # for line in lines[1:]:
                #     if line.startswith("image"):
                #         break
                #     items = line.split()
                #     label = items[0]
                #     confidence = float(items[1])
                #     xmin, ymin, xmax, ymax = map(int, items[2:6])
                #     results.append({
                #         "label": label,
                #         "confidence": confidence,
                #         "bbox": (xmin, ymin, xmax, ymax)
                #     })

                # #Visualize the detection results on the frame
                # for result in results:
                #     label = result["label"]
                #     confidence = result["confidence"]
                #     xmin, ymin, xmax, ymax = result["bbox"]

                #     cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                #     cv2.putText(frame, f"{label}: {confidence:.2f}", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                #Transmision
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                await websocket.send_bytes(frame_base64)

    except WebSocketDisconnect:
        print("Client disconnected")
