"""Dispatch external-stack lessons without numerical fallback."""

from pathlib import Path

from pai_lab.lessons.experiment import Experiment


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    if identifier.startswith("sim-ros-") or identifier == "sim-enlight-01":
        from pai_lab.lessons.ros import run as experiment
    elif identifier in {"sim-g1-01", "sim-wuji-01"}:
        from pai_lab.lessons.gpu import run as experiment
    elif identifier.startswith("sim-vla-"):
        from pai_lab.lessons.vla import run as experiment
    elif identifier.startswith("sim-isaac-") or identifier == "sim-cross-01":
        from pai_lab.lessons.isaac import run as experiment
    else:
        raise ValueError(f"unregistered external lesson: {identifier}")
    return experiment(identifier, output, seed, samples, variant)
