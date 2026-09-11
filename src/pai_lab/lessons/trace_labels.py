"""Physical units of the plotted trace, independent of the scalar summary metric."""


def labels(identifier: str, units: str) -> tuple[str, str]:
    special = {
        "core-00": ("Capability index", "Availability (0 or 1)"),
        "core-02": ("Model index", "Pinned bytes match (0 or 1)"),
        "core-03": ("Model index", "Velocity coordinates (count)"),
        "core-04": ("Joint index", "Position (rad)"),
        "core-fr3-01": ("Joint index", "Position (rad)"),
        "core-enlight-01": ("Joint index", "Position (rad)"),
        "core-fr3-04": ("IK iteration", "Position error (m)"),
        "core-enlight-02": ("Configuration index", "Position error (m)"),
        "core-wuji-01": ("Pose index", "Joint-vector norm (rad)"),
        "core-dexterity-01": ("Property index", "Count"),
        "core-dexterity-02": ("Pose index", "Tip objective (m)"),
        "core-data-01": ("Transition index", "Angle (rad)"),
        "core-rl-01": ("PPO update", "Mean rollout reward"),
        "core-fr3-08": ("PPO update", "Mean rollout reward"),
        "core-il-01": ("Gradient step", "Torque MSE (Nm squared)"),
        "core-aloha-01": ("Time (s)", "First joint angle (rad)"),
        "core-vla-01": ("Action index", "Action (rad)"),
        "sim-g1-01": ("Evaluation step", "Mean reward"),
        "sim-wuji-01": ("Evaluation step", "Mean reward"),
        "sim-wuji-02": ("Evaluation step", "Mean reward"),
        "sim-vla-01": ("Gradient step", "SmolVLA loss"),
        "sim-vla-02": ("Action index", "Configured action units"),
        "sim-deploy-01": ("Test vector index", "Normalized first action"),
        "hw-common-01": ("Inference index", "Normalized first action"),
    }
    return special.get(identifier, ("Time (s)", units))
