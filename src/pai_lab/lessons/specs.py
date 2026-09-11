"""Catalog operation names and artifact contracts."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LessonSpec:
    operation: str
    artifact: str
    metric: str
    units: str


LESSON_SPECS: dict[str, LessonSpec] = {
    "core-00": LessonSpec("host-audit", "host-audit.json", "available_capability_count", "count"),
    "core-01": LessonSpec("pendulum-integrator", "pendulum-state.csv", "energy_drift", "joule"),
    "core-02": LessonSpec("source-pin-audit", "source-pins.json", "valid_source_ratio", "ratio"),
    "core-03": LessonSpec("asset-schema", "model-inventory.json", "valid_model_ratio", "ratio"),
    "core-04": LessonSpec("deterministic-render", "frame.pgm", "rendered_joint_count", "count"),
    "core-fr3-01": LessonSpec("fr3-anatomy", "fr3-joints.json", "joint_count", "count"),
    "core-fr3-02": LessonSpec("joint-pd", "pd-response.csv", "tracking_error", "rad"),
    "core-fr3-03": LessonSpec("gravity-feedforward", "gravity-torque.csv", "tracking_error", "rad"),
    "core-fr3-04": LessonSpec("jacobian-ik", "jacobian.json", "ik_residual", "meter"),
    "core-fr3-05": LessonSpec(
        "operational-space", "task-space-response.csv", "pose_error", "meter"
    ),
    "core-fr3-06": LessonSpec(
        "contact-friction", "friction-sweep.csv", "mean_normal_force", "newton"
    ),
    "core-fr3-07": LessonSpec(
        "reach-environment", "reach-rollout.csv", "terminal_distance", "meter"
    ),
    "core-fr3-08": LessonSpec("fr3-ppo", "ppo-learning.csv", "reward_gain", "reward"),
    "core-enlight-01": LessonSpec(
        "enlight-kinematics", "enlight-frames.json", "frame_count", "count"
    ),
    "core-enlight-02": LessonSpec(
        "cross-format-validation", "cross-format.json", "max_fk_error", "meter"
    ),
    "core-wuji-01": LessonSpec("hand-synergy", "named-poses.json", "pose_count", "count"),
    "core-wuji-02": LessonSpec(
        "virtual-tactile", "tactile-grid.csv", "mean_contact_force", "newton"
    ),
    "core-dexterity-01": LessonSpec(
        "hand-comparison", "hand-comparison.json", "shared_joint_ratio", "ratio"
    ),
    "core-dexterity-02": LessonSpec(
        "hand-retarget", "retargeted-demo.csv", "retarget_error", "meter"
    ),
    "core-rl-01": LessonSpec("continuous-ppo", "policy-update.csv", "objective_gain", "reward"),
    "core-g1-01": LessonSpec("g1-playback", "g1-motion.csv", "loop_error", "rad"),
    "core-data-01": LessonSpec("episode-dataset", "episode.jsonl", "transition_count", "count"),
    "core-il-01": LessonSpec("behavioral-cloning", "bc-loss.csv", "loss_reduction", "loss"),
    "core-aloha-01": LessonSpec("act-contract", "act-schema.json", "action_dimension", "count"),
    "core-vla-01": LessonSpec(
        "vla-protocol", "vla-request-response.json", "schema_fields", "count"
    ),
    "sim-ros-01": LessonSpec("ros-graph-qos-tf", "ros-graph.json", "received_state_error", "rad"),
    "sim-ros-02": LessonSpec(
        "ros-joint-bridge", "joint-state-bridge.csv", "received_state_error", "rad"
    ),
    "sim-ros-03": LessonSpec(
        "mcap-record-replay", "record-replay.json", "received_state_error", "rad"
    ),
    "sim-ros-04": LessonSpec(
        "embodiment-api", "embodiment-contract.json", "received_state_error", "rad"
    ),
    "sim-g1-01": LessonSpec(
        "gpu-motion-imitation", "motion-imitation.csv", "evaluation_reward", "reward"
    ),
    "sim-wuji-01": LessonSpec(
        "gpu-inhand-ppo", "inhand-learning.csv", "evaluation_reward", "reward"
    ),
    "sim-vla-01": LessonSpec("smolvla-finetune", "finetune-metrics.csv", "loss_reduction", "loss"),
    "sim-vla-02": LessonSpec("remote-vla", "remote-inference.json", "roundtrip_time", "second"),
    "sim-isaac-01": LessonSpec(
        "isaac-import", "import-contract.json", "imported_joint_count", "count"
    ),
    "sim-isaac-02": LessonSpec(
        "isaac-synthetic-data", "synthetic-camera.json", "imported_joint_count", "count"
    ),
    "sim-cross-01": LessonSpec("sim-to-sim", "sim-parity.csv", "state_rmse", "rad"),
    "sim-deploy-01": LessonSpec(
        "deployment-bundle", "bundle-verification.json", "test_vector_error", "normalized"
    ),
    "sim-enlight-01": LessonSpec(
        "ros-fake-hardware", "fake-hardware.json", "received_state_error", "rad"
    ),
    "sim-enlight-02": LessonSpec(
        "contact-candidate", "contact-candidate.json", "mean_normal_force", "newton"
    ),
    "sim-wuji-02": LessonSpec(
        "dexterity-candidate", "dexterity-candidate.json", "evaluation_reward", "reward"
    ),
    "hw-common-01": LessonSpec(
        "offline-command-sink", "command-sink.json", "emitted_command_count", "count"
    ),
}
