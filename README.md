# Tutorial Robotics

An action-first, source-pinned robotics curriculum that runs from a MacBook
foundation through GPU workstation training and, where supported, a separately
gated robot-runtime host.

This public repository is complete on its own. It contains the curriculum,
state, code, tests, and runbooks for publicly accessible robot ecosystems:

- Franka Research 3
- Unitree G1
- Wuji Hand 2
- Sharpa Wave
- ALOHA

Private target platforms are supported by the separate
`terryum/tutorial-robotics-private` overlay. The public repository never imports,
downloads, or requires that overlay.

## Start on a MacBook

```bash
git clone --recurse-submodules https://github.com/terryum/tutorial-robotics.git \
  ~/Codes/robotics/tutorial-robotics
cd ~/Codes/robotics/tutorial-robotics
uv sync --group dev
uv run pal doctor
uv run pal tutorial list
```

Then follow [`START_HERE.md`](START_HERE.md). The same Git history and shared
state move in this order:

```text
MacBook foundation -> WS2 simulation/training -> WS1 robot runtime
```

Machine-local paths, devices, network details, and credentials live in the
ignored `.local/` directory. Generated outputs, datasets, runs, bags, and
checkpoints are not committed.

## Repository layout

```text
src/                         public Python packages and the `pal` CLI
tutorials/<robot>/           robot-oriented tutorials
state/                       shared progress and phase gates
runbooks/                    MacBook, WS2, and WS1 handoff procedures
assets/vendor/               pinned redistributable vendor dependency only
external/                    ignored source/model downloads
ros2_ws/                     Wuji simulation and ROS 2 workspace
```

`mujoco-ros2-core` remains an independently versioned Apache-2.0 dependency.
Vendor assets retain their own licenses and are never rewritten.

## License

Original project code and documentation are Apache-2.0. Third-party models,
meshes, datasets, and repositories remain governed by their upstream licenses.

