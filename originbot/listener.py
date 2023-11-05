import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import paho.mqtt.client as mqtt
import base64


class CameraListener(Node):
    def __init__(self):
        super().__init__('camera_listener')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, 'compressed_image', self.listener_callback, 10
        )

        # Initialize the MQTT client
        self.client = mqtt.Client()
        self.client.connect(
            "192.168.0.120", 1883, 60
        )  # if your mqtt server is running on a different machine, change localhost to its IP address.

    def listener_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # Convert the image to JPEG
        ret, jpeg = cv2.imencode('.jpg', cv_image)

        if not ret:
            raise Exception('Could not encode image!')

        b64_string = base64.b64encode(jpeg.tobytes()).decode('utf-8')

        # Publish the encoded string via MQTT
        self.client.publish("robot/camera/image_raw", b64_string)
        print("sent a image to mqtt server")


def main(args=None):
    rclpy.init(args=args)

    camera_listener = CameraListener()

    rclpy.spin(camera_listener)

    # Destroy the node explicitly
    camera_listener.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
