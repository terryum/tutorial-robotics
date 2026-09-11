# WS1 verification handoff

Use the exact learner-experience commit, including the merged WS1 baseline. No remote command is executed by this handoff. Ubuntu/ROS/GPU/Isaac results remain reader_test_required until the following commands produce measured evidence.

Core and offline verification:

```bash
sh bootstrap.sh --plan
sh bootstrap.sh --apply
source .venv/bin/activate
pal assets fetch mujoco-menagerie
pal assets fetch wuji-description-beta2
pal assets fetch flexiv-description
python scripts/verify_course.py --profile core --local-dir .local/development/ws1-core
```

This executes 25 Core lessons plus the generated candidate and offline sink. The script keeps learner progress untouched and stops on the first missing prerequisite/capability or failed experiment. Repeating it resumes only validated runs. Read the actual plots and renderings.

Prepare each optional stack manually in an independent environment; do not install sudo packages, drivers, CUDA, ROS, Isaac or large weights automatically. Install this checkout in the selected stack environment so pal resolves to this same code. Preserve vendor checkouts and write logs, caches and generated assets under .local/. Disable upload/telemetry and prepare model assets before launching.

| Profile | Required preparation | Verification command | Expected evidence |
|---|---|---|---|
| ROS | Ubuntu 24.04; sourced Jazzy; working rclpy, sensor_msgs, geometry_msgs, std_srvs, example_interfaces, tf2_ros, rosbag2_py; Python 3.12 | `python scripts/verify_course.py --profile ros --local-dir .local/development/ws1-ros` | Real DDS samples, reset service, action, TF, SQLite rosbag write/read equality |
| G1 GPU | Pinned Unitree MJLab and its documented mjlab 1.2.0 stack; CUDA arithmetic; prepared reference motion | `python scripts/verify_course.py --profile gpu --local-dir .local/development/ws1-gpu` | Initial/final checkpoints, tensor change, GPU evaluation rewards, actual rendered frame |
| Wuji GPU | Pinned Wuji MJLab supported Pixi environment with local prepared assets; no hardware/deploy tasks | Run its Python with this repository installed, then the GPU profile command | Registered reorientation task; saved/reloaded policy and finite measured rewards |
| SmolVLA | Pinned LeRobot source installed, CUDA, explicitly prepared local pretrained weights/tokenizer and LeRobot v3 dataset/videos | GPU profile after writing the local input JSON below | Real batch loss/backprop, policy+processor reload, loopback server action |
| Isaac | Prepared Isaac Sim with the adapter's documented 5.1 importer/Core API, NumPy/MuJoCo and this checkout installed | `python scripts/verify_course.py --profile isaac --local-dir .local/development/ws1-isaac` | Actual USD articulation, RGB/depth, mapped 20-joint MuJoCo/PhysX trace; RMSE < 0.15 rad |

Unitree, Wuji and LeRobot dependency sets may require separate environments. Do not merge their lockfiles. Use the same chosen local development session to resume the already verified Core artifacts, or run Core again in the new environment. A source revision change invalidates prior execution evidence.

Optional local inputs live in the selected PAL_LOCAL_DIR/stack-inputs directory:

```json
{
  "sim-g1-01.json": {
    "motion_file": "/absolute/path/to/prepared/reference_motion.npz"
  },
  "sim-vla-01.json": {
    "checkpoint": "/absolute/path/to/prepared/smolvla",
    "dataset_root": "/absolute/path/to/local/lerobot-dataset",
    "dataset_repo_id": "local/prepared-dataset"
  },
  "sim-vla-02.json": {
    "endpoint": "http://127.0.0.1:8080",
    "request_file": "/absolute/path/to/prepared/request.json",
    "action_dimension": 7,
    "action_limit": 1.0
  }
}
```

Create each named file with its inner object. These are examples, not credentials or live endpoints. The remote VLA elective requires explicit course inclusion and a prepared request appropriate for the configured service. The local SmolVLA server uses JSON tensor observations; an OpenPI/GR00T service needs a compatible contract/adapter before it can pass.

Expected failure behavior: missing stacks or input files return capability-unavailable, failed numerical criteria retain a failed run.json, and neither case writes completion. A short training pass never sets performance_verified true. Candidate generation does not promote a policy or authorize hardware.

Return the commit SHA, environment versions, .local/.../verification.json result counts, artifact checks and a non-secret review of the rendered images. Keep raw data, policies, device identity, network details and local paths out of shared Git evidence.
