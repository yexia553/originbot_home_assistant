"""
从MQTT server接收数据，并存到数据库中
"""
from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
import base64
import cv2
import numpy as np
from subprocess import Popen, PIPE
from monitor.models import ImageModel


command = [
    'ffmpeg',
    '-y',  # Overwrite output files
    '-f',
    'image2pipe',  # Image format (png, jpeg)
    '-r',
    '10',  # Framerate (fps)
    '-i',
    '-',  # Input comes from pipe
    '-vcodec',
    'libx264',
    '-pix_fmt',
    'yuv420p',  # codec and pixel format suitable for most players
    '-preset',
    'ultrafast',
    '-tune',
    'zerolatency',
    '-f',
    'flv',  # FLV is a common container format
    "rtmp://10.11.12.173:1935/live/test",
]
ffmpeg_pipe = Popen(command, stdin=PIPE)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("robot/camera/image_raw")


def on_message(client, userdata, msg):
    jpg_original = base64.b64decode(msg.payload)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    image_buffer = cv2.cvtColor(cv2.imdecode(jpg_as_np, flags=1), cv2.COLOR_BGR2RGB)

    ret, frame = cv2.imencode('.png', image_buffer)  # or '.jpg'
    print("####################################")
    print(frame)
    if not ret:
        raise Exception('Failed to encode image')

    ffmpeg_pipe.stdin.write(frame.tobytes())

    # def save_image_to_db(image_buffer):
    #     encoded_string = base64.b64encode(
    #         cv2.imencode('.jpg', image_buffer)[1]
    #     ).decode()
    #     img_obj = ImageModel(data=encoded_string)
    #     img_obj.save()

    # save_image_to_db(
    #     image_buffer
    # )  # call this function to save image data into database
    # print("saved a image successfully.")


# def on_message(client, userdata, msg):
#     print(msg.topic + " received")
#     jpg_original = base64.b64decode(msg.payload)
#     jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
#     image_buffer = cv2.imdecode(jpg_as_np, flags=1)

#     def save_image_to_db(image_buffer):
#         encoded_string = base64.b64encode(
#             cv2.imencode('.jpg', image_buffer)[1]
#         ).decode()
#         img_obj = ImageModel(data=encoded_string)
#         img_obj.save()

#     save_image_to_db(
#         image_buffer
#     )  # call this function to save image data into database
#     print("saved a image successfully.")


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("10.11.12.173", 1883, 60)

        client.loop_forever()
