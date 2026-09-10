from glob import glob

from setuptools import find_packages, setup

package_name = "wuji_hand2_tutorial"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Terry Um",
    maintainer_email="terry.t.um@gmail.com",
    description="Simulation-only ROS 2 examples for Wuji Hand 2.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "mujoco_robot_node = wuji_hand2_tutorial.mujoco_robot_node:main",
            "verification_command_publisher = wuji_hand2_tutorial.verification_command_publisher:main",
        ]
    },
)
