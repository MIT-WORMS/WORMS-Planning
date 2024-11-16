import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Joy
from std_msgs.msg import String
from rclpy.executors import MultiThreadedExecutor
from rclpy.context import Context
import numpy as np
import pandas as pd
import subprocess
import platform
import os
import time
import sys
import signal

from messages.msg import Readiness

class MissionControl(Node):
    def __init__(self):
        super().__init__("Mission_Control")
        self.get_logger().info("Mission Control Initialized testing")

        self.active_dict = {}
        self.active_dict_delay = {}
        self.readiness_subscriber = self.create_subscription(Readiness, 'readiness_communication_topic', self.readiness_communication_callback, 10)

        self.publish_action = False
        self.publisher = self.create_publisher(String, 'mission_control_commands', 10)

        self.timer = self.create_timer(0.01, self.timer_callback)

    def readiness_communication_callback(self, msg):
        if msg.status == "Active":
            self.active_dict[msg.sender] = True
        else:
            self.active_dict[msg.sender] = False
        self.active_dict_delay[msg.sender] = time.time()

    def timer_callback(self):
        publish_action = True
        for i in self.active_dict.values():
            if not i:
                publish_action = False
        for i in self.active_dict_delay.values():
            if time.time() - i > 0.2: # twice the config_time_step
                publish_action = False

        self.publish_action = publish_action

        if self.publish_action:
            # self.get_logger().info("Ready to publish")
            pass


def main(args=None):
    """
    Initializes ROS, creates 'Mission_control' node.
    """
    rclpy.init(args=args)

    node = MissionControl()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()