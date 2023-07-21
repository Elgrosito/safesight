from ultralytics import YOLO
import cv2

model = YOLO('best.pt')

def predict(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #results = model(rgb_frame)
    results = model(rgb_frame, conf=0.5)

    # Process results list
    boxes = results[0].boxes
    return boxes

def draw_rectangles(frame, boxes):
    classes = ['pistol', 'knife']
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        cls = int(box.cls)
        conf = box.conf[0]

        # Conversión de coordenadas y clase a int
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

        # Dibuja el rectángulo
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Dibuja el texto
        label = f"{classes[cls]}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

        return conf
