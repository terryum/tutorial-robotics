# Model Formats in This Curriculum

| Format | Main role | Typical backend | Important contents |
|---|---|---|---|
| URDF/Xacro | kinematics and ROS description | ROS 2, MoveIt, robot_state_publisher | link tree, joints, axes, limits, mass/inertia, visual/collision |
| MJCF/XML | native dynamics and contact model | MuJoCo, MJX, mjlab | actuators, sensors, contact, friction, solver parameters, keyframes |
| USD/USDA/USDC | composed 3D scene and physics asset | Isaac Sim, Isaac Lab | articulation, drives, materials, cameras, lights, scene composition |
| SRDF | semantic planning configuration | MoveIt 2 | planning groups, end-effectors, disabled collisions |
| SDF | robot/world simulation | Gazebo | world, models, sensors, plugins, physics-engine settings |

## Friction must be qualified

- **joint damping:** velocity-proportional resistance
- **joint friction/frictionloss:** internal joint or transmission resistance
- **contact friction:** tangential resistance between two surfaces
- **torsional/rolling friction:** resistance to twisting or rolling at contact

A value copied between MuJoCo and PhysX is not guaranteed to create the same behavior. Always validate with a defined experiment.

## Source-of-truth policy

Do not nominate one universal master format.

- URDF: frame/joint naming and ROS kinematic contract
- MJCF: MuJoCo experiment contract
- USD: Isaac scene and sensor contract
- real hardware measurements: ultimate dynamic truth

Native vendor files remain immutable. Converted files live under `generated_assets/` with conversion metadata and source commit.
