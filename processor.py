import paho.mqtt.client as mqtt
import boto3
import base64
import cv2
import os
import time
import numpy as np
import uuid

MQTT_HOST = 'mqtt'
MQTT_TOPIC =  'streaming2'

session = boto3.Session(aws_access_key_id='XXX', aws_secret_access_key='XXX')
s3_store = session.client('s3')

def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, message):
    try:
        img = base64.b64decode(message.payload)
        filename = 'hw3/' + str(uuid.uuid4().hex)
        s3_store.put_object(Body = img, Bucket = 'jgp-w251-hw3', Key = filename)
        print('Image stored.')

    except:
        print('Failed')

client = mqtt.Client('image_processor')
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST)

client.loop_forever()
