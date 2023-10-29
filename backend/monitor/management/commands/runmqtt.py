from django.core.management.base import BaseCommand, CommandError
import paho.mqtt.client as mqtt
import base64
import cv2
import numpy as np
from monitor.models import ImageModel  # importing the model


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("robot/camera/image_raw")  # the topic you subscribed in ROS node.


def on_message(client, userdata, msg):
    print(msg.topic + " received")
    jpg_original = base64.b64decode(msg.payload)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    image_buffer = cv2.imdecode(jpg_as_np, flags=1)

    def save_image_to_db(image_buffer):
        encoded_string = base64.b64encode(
            cv2.imencode('.jpg', image_buffer)[1]
        ).decode()  # encode image to base64 string
        img_obj = ImageModel(data=encoded_string)  # creating a new model instance
        img_obj.save()  # saving the model

    save_image_to_db(
        image_buffer
    )  # call this function to save image data into database
    print("saved a image successfully.")


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("192.168.0.120", 1883, 60)

        client.loop_forever()
