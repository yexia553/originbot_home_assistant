"""
OriginBot的元动作，以便让大模型决定应该调用哪个动作
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
import math
import time


# 描述每个action的作用和参数说明，用于帮助LLM判断应该调用哪个action
meta_action_description = {
    "originbot_turning": {
        "description": "控制originbot原地转弯",
        "params": {
            "angular_speed": {
                "type": "float",
                "description": "角速度（弧度/秒），假设原地左转，正数表示左转，复数表示右转",
                "default": 0.5,
            },
            "target_angle": {
                "type": "float",
                "description": "需要转弯的总角度",
                "default": 5,
            },
        },
    },
}


class OriginBotTruning(Node):
    def __init__(self, angular_speed=1, target_angle=5):
        super().__init__("originbot")
        self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.timer = self.create_timer(1.0, self.left_turn)

    def left_turn(self):
        target_angle = math.radians(self.target_angle)
        duration = target_angle / self.angular_speed  # 计算转向所需时间

        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = self.angular_speed

        # 开始转向
        end_time = time.time() + duration
        while time.time() < end_time:
            self.publisher_.publish(twist)

        # 停止机器人
        twist.angular.z = 0.0
        self.publisher_.publish(twist)

        # 停止Node
        self.timer.cancel()  # 停止定时器


def originbot_turning(angular_speed=1.0, target_angle=5.0, args=None):
    rclpy.init(args=args)
    originbot = OriginBotTruning(angular_speed, target_angle)
    rclpy.spin(originbot)
    originbot.destroy_node()
    rclpy.shutdown()
