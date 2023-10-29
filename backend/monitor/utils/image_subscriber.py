import paho.mqtt.client as mqtt
import base64
import cv2
import numpy as np


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("robot/camera/image_raw")  # the topic you subscribed in ROS node.


def on_message(client, userdata, msg):
    print(msg.topic + " received")
    jpg_original = base64.b64decode(msg.payload)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    image_buffer = cv2.imdecode(jpg_as_np, flags=1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect to the broker
client.connect("192.168.0.120", 1883, 60)

client.loop_start()
