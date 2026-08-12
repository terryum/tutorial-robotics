# Repository instructions

- Keep this repository public, Apache-2.0, and free of credentials, serial
  numbers, private addresses, calibration, bags, datasets, and checkpoints.
- Preserve `assets/vendor/wuji-description` and `deps/mujoco-ros2-core` as
  pinned, read-only submodules. Never edit or push vendor assets.
- Use the official Wuji Hand 2 Beta 1 MJCF and ROS URDF directly; generated
  scenes and caches stay untracked.
- Keep setup, model inspection, ROS 2 examples, and small verification motions
  here. Learning baselines belong in `wuji-hand2-motion-baselines`.
- Simulation commands must never connect to hardware. A future hardware
  adapter starts read-only and requires identity, safety, limits,
  acknowledgement, timeout, stale-command, fault, and E-stop gates.
- Use `terryum` and `terry.t.um@gmail.com` for GitHub and commits.
