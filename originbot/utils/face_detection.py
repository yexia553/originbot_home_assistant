import rclpy
from rclpy.node import Node
from ai_msgs.msg import PerceptionTargets
from cv_bridge import CvBridge
import time

from api_connection import APIConnection

BabyMonitorMapping = {
    # 这里的k-v要根据后端Django中的值来确定
    "face": "看不到脸",
    "body": "不在摄像头范围内",
}


class FaceDetectionListener(Node):
    """
    检测宝宝的脸是不是在摄像头中
    """
    def __init__(self):
        super().__init__("face_detection")
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            PerceptionTargets, "hobot_mono2d_body_detection", self.listener_callback, 10
        )
        self.conn = APIConnection()
        self.timer = time.time()
        self.counter = 0

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
        if disappeared_targets_list:
            self.sending_notification(disappeared_targets_list)

    def sending_notification(self, disappeared_targets_list):
        for item in disappeared_targets_list:
            if BabyMonitorMapping.get(item):
                event = BabyMonitorMapping.get(item)
                if self.counter == 0:
                    # 这里baby的ID是模拟的，应该去数据库中查
                    data = {"event": event, "baby": "6b56979a-b2b9-11ee-920d-f12e14f97477"} 
                    self.conn.post_data(item=data, api="api/monitor/face-detection/")
                    self.counter += 1
                    self.timer = time.time()
                else:
                    if time.time() - self.timer >= 60.0:
                        # 60秒不重复发消钉钉消息
                        data = {"event": event, "baby": "6b56979a-b2b9-11ee-920d-f12e14f97477"}
                        self.conn.post_data(item=data, api="api/monitor/face-detection/")
                        self.timer = time.time()
                        self.counter += 1


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
