import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    gait_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('brain_package'), 'launch', 'launch.py')])
    )
    mission_control = Node(package="planning",
                    executable="mission_control")
    
    return LaunchDescription([gait_launch, mission_control])