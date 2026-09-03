# ROS 2 Development Environment

ROS 2 fundamentals may run on either:

- macOS arm64 through a supported RoboStack/Pixi Jazzy environment
- Ubuntu 24.04 x86_64 through native ROS 2 Jazzy

Use semantic environment role `ros2-dev`. Vendor drivers/fake hardware that officially require Ubuntu must declare `ubuntu_24_04_x86_64` and `ros2_jazzy_native` capabilities.

Prefer CycloneDDS on Mac when Fast DDS/RViz compatibility is unstable. Core code and message contracts must remain portable.
