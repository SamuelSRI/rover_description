from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

from pathlib import Path


def generate_launch_description():
    pkg_path = Path(get_package_share_directory("rover_description"))
    urdf_path = pkg_path / "urdf" / "rover.urdf"

    robot_description = urdf_path.read_text()

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[
                {"robot_description": robot_description}
            ],
        )
    ])
