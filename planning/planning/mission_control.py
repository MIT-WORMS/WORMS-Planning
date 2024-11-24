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

from messages.msg import Command # type: ignore

class MissionControl(Node):
    def __init__(self):
        super().__init__("Mission_Control")

        self.publisher = self.create_publisher(Command, 'mission_control_command_topic', 10)

        time.sleep(3)

        msg = Command()
        msg.duration = 10
        msg.action = 'forward'
        self.publisher.publish(msg)


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