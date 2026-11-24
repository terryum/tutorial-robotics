"""Compare frame and episode splits on a completed scripted Enlight BC run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from pai_lab.lessons.evidence import validate_run


def compare_splits(run_dir: Path) -> dict:
    errors = validate_run("core-enlight-04", run_dir)
    if errors:
        raise ValueError("Invalid Enlight BC run: " + "; ".join(errors))
    records = json.loads((run_dir / "demonstrations.json").read_text(encoding="utf-8"))
    evaluation = json.loads((run_dir / "evaluation.json").read_text(encoding="utf-8"))
    train = [row["episode"] for row in records if row["split"] == "train"]
    validation = [row["episode"] for row in records if row["split"] == "validation"]
    if not train or not validation:
        raise ValueError("Both training and validation demonstration frames are required")

    # Keep the test episodes aside and match the original numbers of frames in both splits.
    seed = 7
    shuffled = np.random.default_rng(seed).permutation(train + validation)
    frame_overlap = len(set(shuffled[: len(train)]) & set(shuffled[len(train) :]))
    episode_overlap = len(set(train) & set(validation))
    if frame_overlap == 0 or episode_overlap != 0:
        raise ValueError("Expected overlap only in the random frame split")

    return {
        "frame_split_seed": seed,
        "train_frames": len(train),
        "validation_frames": len(validation),
        "train_episodes": len(set(train)),
        "validation_episodes": len(set(validation)),
        "shared_episodes_frame_split": frame_overlap,
        "shared_episodes_episode_split": episode_overlap,
        "validation_action_mse": evaluation["validation_mse"],
        "test_action_mse": evaluation["test_mse"],
        "closed_loop_successes": evaluation["successes"],
        "closed_loop_attempts": len(evaluation["episodes"]),
        "closed_loop_seed": evaluation["seed"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = compare_splits(args.run_dir)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
