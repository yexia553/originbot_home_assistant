import rclpy
from rclpy.node import Node
from ai_msgs.msg import PerceptionTargets
from cv_bridge import CvBridge


class FaceDetectionListener(Node):
    def __init__(self):
        super().__init__('face_detection')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            PerceptionTargets, 'hobot_mono2d_body_detection', self.listener_callback, 10
        )

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
        print(f"新增的对象如下：{targets_list}")
        print(f"消失的对象如下：{disappeared_targets_list}")


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


if __name__ == '__main__':
    main()
