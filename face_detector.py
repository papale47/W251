import cv2
import paho.mqtt.client as mqtt
import base64
import time
import os


MQTT_BROKER = 'mqtt'
MQTT_TOPIC = 'streaming'


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
# Phao-MQTT Clinet

client = mqtt.Client()
# Connect
client.connect(MQTT_BROKER)
try:
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            face = frame[y:y+h, x:x+w]
            rc, jpg = cv2.imencode('.jpg', face)
            msg = base64.b64encode(jpg)
            client.publish(MQTT_TOPIC, payload=msg, qos=0, retain=False)
        
except:
    cap.release()
    client.disconnect()
    print("\nAll Done...")
