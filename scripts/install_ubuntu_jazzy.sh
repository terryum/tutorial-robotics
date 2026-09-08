#!/usr/bin/env bash
# Native Ubuntu 24.04 packages for offline MuJoCo/ROS development.
# Run with sudo or pkexec; review the package list before running.
set -euo pipefail
source /etc/os-release
[[ "$ID" == ubuntu && "$VERSION_ID" == 24.04 && "$(uname -m)" == x86_64 ]]
[[ "$EUID" == 0 ]] || { echo 'Run with sudo or pkexec.' >&2; exit 1; }
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-remove build-essential cmake python3-dev python3-venv curl ca-certificates libglfw3 libosmesa6 mesa-utils xvfb x11-utils python3-pyqt5
ros_source_deb=$(mktemp --suffix=.deb)
trap 'rm -f "$ros_source_deb"' EXIT
curl -fsSL https://github.com/ros-infrastructure/ros-apt-source/releases/download/1.2.0/ros2-apt-source_1.2.0.noble_all.deb -o "$ros_source_deb"
echo "0804d9b13db770eb87019be414cd78378835228ad5fa801fc88758596dd8f7e5  $ros_source_deb" | sha256sum -c -
dpkg -i "$ros_source_deb"
apt-get update
apt-get install -y --no-remove ros-jazzy-desktop ros-dev-tools ros-jazzy-rmw-cyclonedds-cpp ros-jazzy-rosbag2-storage-mcap ros-jazzy-joint-state-publisher-gui
