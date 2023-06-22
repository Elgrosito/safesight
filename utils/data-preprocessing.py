import csv
import cv2
import os

def preprocess_video_frames(video_path, csv_file):
    labels = []
    boxes = []
    frame_list = []
    none = {}

    cap = cv2.VideoCapture(video_path)

    with open(csv_file) as csvfile:
        rows = csv.reader(csvfile)
        next(iter(rows))  # Skip the header row

        for i, row in enumerate(rows):
            ret, frame = cap.read()

            if not ret:
                none[i] = f"Frame {i} could not be read"
                continue

            # Resize the frame to (224, 224) and normalize it by dividing by 255.0
            frame = cv2.resize(frame, (224,224)).astype("float") / 255.0

            # Append it to the list of frames
            frame_list.append(frame)

            # Fetch and store the label for the frame
            labels.append(int(row[3]))

            # Fetch the bounding box coordinates, scale them to [0, 1] by dividing by 224, and store them
            boxes.append([
                float(row[4])/224,
                float(row[5])/224,
                float(row[6])/224,
                float(row[7])/224,
            ])

    return labels, boxes, frame_list, none
