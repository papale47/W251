import paho.mqtt.client as mqtt
import os
import time

MQTT_HOST = 'mqtt'
MQTT_TOPIC = 'streaming'

REMOTE_MQTT_HOST = '3.18.110.190'
REMOTE_MQTT_TOPIC = 'streaming2'
REMOTE_MQTT_PORT = 1883


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, message):
    print("Message received.")
    remote_client.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
    msg = message.payload
    remote_client.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
    

client = mqtt.Client('receiving')
remote_client = mqtt.Client('forwarding')

client.on_connect = on_connect
client.on_message = on_message


client.connect(MQTT_HOST)
#remote_client.connect(REMOTE_MQTT_BROKER)

# Starting thread which will receive the frames
client.loop_forever()

