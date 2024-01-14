import rclpy
from rclpy.node import Node
from ai_msgs.msg import PerceptionTargets
from cv_bridge import CvBridge

from api_connection import APIConnection


class FaceDetectionListener(Node):
    def __init__(self):
        super().__init__("face_detection")
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            PerceptionTargets, "hobot_mono2d_body_detection", self.listener_callback, 10
        )
        self.conn = APIConnection()

    def listener_callback(self, msg):
        targets = msg.targets
        disappeared_targets = msg.disappeared_targets
        targets_list = []
        disappeared_targets_list = []
        if disappeared_targets:
            for item in disappeared_targets:
                disappeared_targets_list.append(item.rois[0].type)
        if targets:
            for item in targets:
                targets_list.append(item.rois[0].type)
        print(f"检测到的对象如下：{targets_list}")
        print(f"消失的对象如下：{disappeared_targets_list}")
        if "face" in disappeared_targets_list:
            data = {"event": "看不到脸", "baby": "6b56979a-b2b9-11ee-920d-f12e14f97477"}
            self.conn.post_data(item=data, api="api/monitor/face-detection/")


def main(args=None):
    rclpy.init(args=args)
    try:
        face_detection_listener = FaceDetectionListener()

        rclpy.spin(face_detection_listener)
    except KeyboardInterrupt:
        print("终止运行")
    finally:
        face_detection_listener.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
