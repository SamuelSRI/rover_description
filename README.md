# rover_description

ROS 2 robot description package for a rover platform.

This package contains the URDF/Xacro description of a rover equipped with:

* a chassis
* a rear circular radar platform
* 20 ARS5 radar modules arranged in a circle
* an AS-DT1 LiDAR
* an IMU
* a GPS antenna

The model is designed for visualization in RViz and for publishing the robot TF tree using `robot_state_publisher`.

## Features

* Full rover visual model using URDF/Xacro
* rover body with separated left and right tracks
* Approximation of track chamfers at the front and rear
* Rear circular platform mounted on top of the rover
* 20 radar modules placed around the platform
* Radar links matching the frame IDs published by the radar node
* Sensor frames for LiDAR, IMU and GPS
* Compatible with ROS 2 and RViz

## Robot dimensions

Main rover dimensions:

```text
Length: 1.18 m
Width: 0.80 m
Top height: 0.44 m
```

Rear circular platform:

```text
Diameter: 0.80 m
Thickness: 0.02 m
Rear edge aligned with the rear of the rover
```

Radar modules:

```text
Number of modules: 20
Module height: 0.13 m
Module width: 0.09 m
Module depth: 0.04 m
Radar ring diameter: 0.68 m
Radar center height: 0.10 m above the platform
```

## Radar layout

The radar modules are placed in a circle on the rear platform.

The radar links are named to match the `frame_id` used by the ARS5 radar node:

```text
radar_110_link
radar_111_link
...
radar_129_link
```

The front-facing radar is:

```text
radar_117_link
```

Radar indexing convention:

```text
radar_117_link = front of the rover

Going to the right side:
117 -> 118 -> 119 -> 120 ...

Going to the left side:
117 -> 116 -> 115 -> 114 ...
```

This allows the radar point cloud topics to match the URDF frames directly.

Example radar node output:

```text
/radar/r117/points frame_id = radar_117_link
/radar/r118/points frame_id = radar_118_link
/radar/r111/points frame_id = radar_111_link
```

## TF frames

The main frame is:

```text
base_link
```

Sensor frames:

```text
as_dt1_link
imu_link
gps_link
radar_110_link
radar_111_link
...
radar_129_link
```

Example TF tree:

```text
base_link
├── as_dt1_link
├── imu_link
├── gps_link
├── radar_110_link
├── radar_111_link
├── ...
└── radar_129_link
```

## Package structure

Recommended package structure:

```text
_rover_description
├── CMakeLists.txt
├── package.xml
├── launch
│ └── display.launch.py
├── rviz
│ └── _rover.rviz
└── urdf
 └── _rover.urdf.xacro
```

## Dependencies

Install the required ROS 2 packages:

```bash
sudo apt update
sudo apt install ros-$ROS_DISTRO-xacro ros-$ROS_DISTRO-robot-state-publisher ros-$ROS_DISTRO-joint-state-publisher-gui
```

Optional but recommended for visualization:

```bash
sudo apt install ros-$ROS_DISTRO-rviz2
```

## Build

Clone the package into your ROS 2 workspace:

```bash
cd ~/ros2_ws/src
git clone <your_repository_url>
```

Build the workspace:

```bash
cd ~/ros2_ws
colcon build --packages-select _rover_description
source install/setup.bash
```

## Generate URDF from Xacro

To manually generate the URDF file:

```bash
ros2 run xacro xacro ~/ros2_ws/src/_rover_description/urdf/_rover.urdf.xacro > /tmp/_rover.urdf
```

Or, if `xacro` is available directly:

```bash
xacro ~/ros2_ws/src/_rover_description/urdf/_rover.urdf.xacro > /tmp/_rover.urdf
```

## Launch robot description

Example launch command:

```bash
ros2 launch _rover_description display.launch.py
```

This should start:

* `robot_state_publisher`
* optionally `joint_state_publisher_gui`
* RViz

## Example display.launch.py

Create this file:

```text
launch/display.launch.py
```

With this content:

```python
from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
 pkg_share = FindPackageShare("_rover_description")

 xacro_file = PathJoinSubstitution([
 pkg_share,
 "urdf",
 "_rover.urdf.xacro"
 ])

 robot_description = {
 "robot_description": Command([
 "xacro ",
 xacro_file
 ])
 }

 return LaunchDescription([
 Node(
 package="robot_state_publisher",
 executable="robot_state_publisher",
 name="robot_state_publisher",
 parameters=[robot_description],
 output="screen"
 ),

 Node(
 package="joint_state_publisher_gui",
 executable="joint_state_publisher_gui",
 name="joint_state_publisher_gui",
 output="screen"
 ),

 Node(
 package="rviz2",
 executable="rviz2",
 name="rviz2",
 output="screen"
 )
 ])
```

## CMakeLists.txt install rules

Make sure your `CMakeLists.txt` installs the URDF and launch folders:

```cmake
cmake_minimum_required(VERSION 3.8)
project(_rover_description)

find_package(ament_cmake REQUIRED)

install(
 DIRECTORY urdf launch rviz
 DESTINATION share/${PROJECT_NAME}
)

ament_package()
```

If you do not have an `rviz` folder yet, either create it or remove `rviz` from the install rule.

## package.xml dependencies

Example `package.xml` dependencies:

```xml
<?xml version="1.0"?>
<package format="3">
 <name>_rover_description</name>
 <version>0.1.0</version>
 <description>URDF/Xacro robot description for a rover with LiDAR, GPS, IMU and 20 radar modules.</description>

 <maintainer email="your_email@example.com">Your Name</maintainer>
 <license>MIT</license>

 <buildtool_depend>ament_cmake</buildtool_depend>

 <exec_depend>xacro</exec_depend>
 <exec_depend>robot_state_publisher</exec_depend>
 <exec_depend>joint_state_publisher_gui</exec_depend>
 <exec_depend>rviz2</exec_depend>

 <export>
 <build_type>ament_cmake</build_type>
 </export>
</package>
```

## Verify TF frames

After launching the robot description, check that the radar frames exist:

```bash
ros2 run tf2_ros tf2_echo base_link radar_117_link
```

Check another radar:

```bash
ros2 run tf2_ros tf2_echo base_link radar_111_link
```

If the transform is published correctly, the radar node point clouds can be displayed in RViz using their matching `frame_id`.

## Verify radar point clouds

Example radar topics:

```bash
ros2 topic list | grep radar
```

Check one radar point cloud:

```bash
ros2 topic echo /radar/r117/points --once
```

The message should contain:

```yaml
header:
 frame_id: radar_117_link
```

For another radar:

```bash
ros2 topic echo /radar/r111/points --once
```

Expected frame:

```yaml
header:
 frame_id: radar_111_link
```

## RViz setup

In RViz:

1. Set `Fixed Frame` to:

```text
base_link
```

or, if localization is running:

```text
odom
```

2. Add the robot model:

```text
Add -> RobotModel
```

3. Add radar point clouds:

```text
Add -> PointCloud2
```

Example topics:

```text
/radar/r117/points
/radar/r118/points
/radar/r111/points
```

4. Add TF display:

```text
Add -> TF
```

This allows you to verify that all radar frames are correctly positioned around the platform.

## Notes

The rover shape is approximated using simple URDF geometries such as boxes and cylinders.

The track chamfers and body chamfers are visual approximations. For a more accurate model, the chassis and tracks should be replaced by mesh files such as `.stl` or `.dae`.

The radar modules are represented as boxes with a colored front face to make their orientation visible in RViz.

## License

This project is released under the MIT License.
