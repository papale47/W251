
from facenet_pytorch import MTCNN  
import torch
from torch.utils.data import DataLoader
import cv2
import paho.mqtt.client as mqtt
import base64
import time
import os


MQTT_BROKER = 'mqtt'
MQTT_TOPIC = 'streaming'


# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(keep_all=True, device=device)

# Phao-MQTT Clinet
client = mqtt.Client()

# Connect
client.connect(MQTT_BROKER)
counter = 0
try:
    while True:
        if counter == 0:
            start = time.time()
        if counter == 120:
            end = time.time()
            seconds = end - start
            fps = counter/seconds
            print("Estimated frames per second : {0}".format(fps))

        ret, frame = cap.read()
        resized = cv2.resize(frame, (1280, 720))
        boxes, probs, landmarks = mtcnn.detect(resized, landmarks=True)
        for box in boxes:
            x1 = int(box[0])
            y1 = int(box[1])
            x2 = int(box[2])
            y2 = int(box[3])
            face = resized[y1:y2, x1:x2]
            rc, jpg = cv2.imencode('.jpg', face)
            msg = base64.b64encode(jpg)
            client.publish(MQTT_TOPIC, payload=msg, qos=0, retain=False)
        counter += 1
        

except:
    cap.release()
    client.disconnect()
    print("\nAll Done...")
