# Repository instructions

- Keep this public repository simulation-only and Apache-2.0.
- Preserve `assets/vendor/wuji-description` and `deps/mujoco-ros2-core` as
  pinned, read-only submodules. Never edit or push vendor assets.
- Keep generated scenes, checkpoints, runs, datasets, and bags untracked.
- Policies and gestures must default to simulation. Do not add a Wuji SDK or
  hardware output path without a separately approved safety-gated adapter.
- The Hand 2 Beta 1 fingertip pads are not collision geometry; do not present
  contact policies as sim-to-real results.
- Use `terryum` and `terry.t.um@gmail.com` for GitHub and commits.
