import os
import cv2
import numpy as np
from channels.generic.websocket import WebsocketConsumer
import time
from datetime import datetime


class BabyCare(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()
        self.file_index = 0
        self.out = None
        self.out = self.get_new_videowriter()
        self.count = 0

    def get_new_videowriter(self):
        return cv2.VideoWriter(
            f"output_{datetime.now().strftime('%Y-%m-%d----%H:%M:%S')}.avi",
            cv2.VideoWriter_fourcc(*"XVID"),
            30.0,
            (640, 480),
        )

    def connect(self):
        self.accept()

    def disconnect(self, code):
        return super().disconnect(code)

    def receive(self, text_data=None, bytes_data=None):
        try:
            if bytes_data:
                # Decode JPEG frame into an image
                img_array = np.frombuffer(bytes_data, dtype=np.dtype("uint8"))
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                # Write the image into the video file
                self.out.write(img)
                self.count += 1

                # Broadcast the received binary data to all connected WebSockets
                self.send(bytes_data=bytes_data)

                # Check if 5 seconds have passed
                if time.time() - self.start_time >= 60:
                    # If so, release the current VideoWriter and start a new one
                    self.out.release()
                    self.file_index += 1
                    print(f"收到了{self.count}帧图片")
                    self.out = self.get_new_videowriter()
                    self.start_time = time.time()

        except Exception as e:
            # Handle or log any exceptions that occur during processing
            print(f"Error while processing frames: {e}")
