"""Explicit, model-bound external arm demonstrations with episode-level splits."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


def load_demonstrations(path: Path, model: str) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text())
    if payload.get("model") != model or payload.get("schema_version") != 1:
        raise ValueError("external dataset model/schema mismatch")
    rows: list[dict[str, Any]] = payload["rows"]
    splits: dict[int, str] = {}
    for row in rows:
        episode, split = row["episode"], row["split"]
        if split not in {"train", "validation", "test"}:
            raise ValueError("explicit train/validation/test split required")
        if episode in splits and splits[episode] != split:
            raise ValueError("episode leakage across splits")
        splits[episode] = split
        observation, action = np.asarray(row["observation"]), np.asarray(row["action"])
        if (
            observation.shape != (17,)
            or action.shape != (7,)
            or not np.isfinite(observation).all()
            or not np.isfinite(action).all()
        ):
            raise ValueError("finite model-specific 17-observation/7-action rows required")
    if set(splits.values()) != {"train", "validation", "test"}:
        raise ValueError("three nonempty episode splits required")
    return rows
