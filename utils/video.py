#agregar codigo de video aca

import os
import cv2
import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import shutil


def process_video_test(video_path):
    video = cv2.VideoCapture(video_path)

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) == 27:
            break
        cv2.waitKey(25)
    video.release()
    cv2.destroyAllWindows()


def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (224, 224))
    normalized_frame = resized_frame / 255.0
    preprocessed_frame = tf.expand_dims(normalized_frame, axis=0)
    return preprocessed_frame


def process_video(video_path, model):
    video = cv2.VideoCapture(video_path)
    detections = []

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break

        processed_frame = preprocess_frame(frame)

        features = model(processed_frame)

        probabilities = tf.nn.softmax(features)

        class_id = tf.argmax(probabilities, axis=1)
        class_label = class_id.numpy()[0]

        cv2.imshow('Video', frame)

        if class_label == 1:
            detections.append("Pistol or handggun detected!")

        if cv2.waitKey(1) == 27:
            break

        cv2.waitKey(25)

    video.release()
    cv2.destroyAllWindows()

    # Print the detections
    if len(detections) > 0:
        print("Detections:")
        for detection in detections:
            print(detection)
    else:
        print("No pistol or handgun detected.")



trackers = {
    'csrt' : cv2.legacy.TrackerCSRT_create,  # hight accuracy ,slow
    'mosse' : cv2.legacy.TrackerMOSSE_create,  # fast, low accuracy
    'kcf' : cv2.legacy.TrackerKCF_create,   # moderate accuracy and speed
    'medianflow' : cv2.legacy.TrackerMedianFlow_create,
    'mil' : cv2.legacy.TrackerMIL_create,
    'tld' : cv2.legacy.TrackerTLD_create,
    'boosting' : cv2.legacy.TrackerBoosting_create,
}



def process_video_v2(video_path, model):
    video = cv2.VideoCapture(video_path)
    detections = []
    tracker = cv2.TrackerKCF_create()  # Create an object tracker
    initialized = False  # Flag to track if the tracker is initialized
    cv2.TrackerMOSSE_create()
    while True:
        ret, frame = video.read()

        if not ret:
            break

        if not initialized:
            bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
            tracker.init(frame, bbox)  # Initialize the tracker with the selected bounding box
            initialized = True

        # Update the tracker
        success, bbox = tracker.update(frame)

        if success:
            detections.append("Pistol or handgun detected!")
            x, y, w, h = [int(coord) for coord in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) == 27:
            break

        cv2.waitKey(25)

    video.release()
    cv2.destroyAllWindows()

    # Print the detections
    if len(detections) > 0:
        print("Detections:")
        for detection in detections:
            print(detection)
    else:
        print("No pistol or handgun detected.")
