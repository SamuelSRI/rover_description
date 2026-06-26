# rover_description

ROS 2 robot description package for a tracked rover.

This package provides a minimal URDF and launch file for publishing the static TF tree of the rover using `robot_state_publisher`.

## TF tree

```text
odom
└── base_link
    ├── asdt1_link
    ├── imu_link
    └── gps_link
