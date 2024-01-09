import os

from cv_bridge import CvBridge
from sensor_msgs.msg import Image

from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


class FaceDetection(Node):
    def __init__(self):
        super().__init__("face_detection")
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, 
            "/image_raw", 
            self.face_detection_callback, 
            10)
    
    def face_detection_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # mono2d body detection
        mono2d_body_pub_topic_arg = DeclareLaunchArgument(
            'mono2d_body_pub_topic',
            default_value='/hobot_mono2d_body_detection',
            description='mono2d body ai message publish topic')
        mono2d_body_det_node = Node(
            package='mono2d_body_detection',
            executable='mono2d_body_detection',
            output='screen',
            parameters=[
                {"ai_msg_pub_topic_name": LaunchConfiguration(
                    'mono2d_body_pub_topic')}
            ],
            arguments=['--ros-args', '--log-level', 'warn']
        )