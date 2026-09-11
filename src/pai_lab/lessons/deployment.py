"""Candidate bundles built from measured policies; no live command transport exists."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np

from pai_lab.catalog import ROOT
from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.learning import previous_run
from pai_lab.local import write_json


def policy_action(bundle: Path, observation: np.ndarray) -> np.ndarray:
    manifest = json.loads((bundle / "manifest.json").read_text())
    policy = bundle / manifest["policy"]["path"]
    if hashlib.sha256(policy.read_bytes()).hexdigest() != manifest["policy"]["sha256"]:
        raise ValueError("policy checksum mismatch")
    weights = np.load(policy)["weights"]
    x = np.append(np.clip(observation, -5, 5), 1.0)
    if x.shape[0] != weights.shape[0]:
        raise ValueError("observation dimension mismatch")
    action = np.tanh(x @ weights)
    if not np.isfinite(action).all() or np.max(np.abs(action)) > 1:
        raise ValueError("nonfinite or out-of-bounds action")
    return np.asarray(action)


def validate_candidate(bundle: Path) -> list[str]:
    errors = []
    try:
        manifest = json.loads((bundle / "manifest.json").read_text())
        if manifest.get("schema_version") != 2 or manifest.get("rollback") != "command-sink":
            errors.append("unsupported manifest or rollback")
        if manifest.get("promotion") != "candidate-only":
            errors.append("this course only creates candidates")
        for relative, digest in manifest["files"].items():
            path = (bundle / relative).resolve()
            if not path.is_relative_to(bundle.resolve()):
                errors.append("bundle path escape")
            elif not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f"bundle checksum mismatch: {relative}")
        for vector in manifest["test_vectors"]:
            actual = policy_action(bundle, np.array(vector["observation"]))
            if not np.allclose(actual, vector["action"], atol=1e-12, rtol=0):
                errors.append("test vector mismatch")
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(str(error))
    return errors


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    if identifier == "sim-deploy-01":
        source = previous_run("core-fr3-08")
        from pai_lab.lessons.evidence import validate_run

        errors = validate_run("core-fr3-08", source)
        if errors:
            raise ValueError("source policy evidence: " + "; ".join(errors))
        bundle = output / "sample_candidate"
        bundle.mkdir()
        for name in ("policy.npz", "policy-contract.json", "experiment.json", "run.json"):
            shutil.copyfile(source / name, bundle / name)
        weights = np.load(bundle / "policy.npz")["weights"]
        rng = np.random.default_rng(seed)
        vectors = []
        for _ in range(samples):
            x = rng.uniform(-0.1, 0.1, weights.shape[0] - 1)
            vectors.append(
                {"observation": x.tolist(), "action": np.tanh(np.append(x, 1.0) @ weights).tolist()}
            )
        hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in bundle.iterdir()}
        manifest = {
            "schema_version": 2,
            "lesson_id": identifier,
            "promotion": "candidate-only",
            "policy": {"path": "policy.npz", "sha256": hashes["policy.npz"]},
            "files": hashes,
            "test_vectors": vectors,
            "observation_order": [
                "q_minus_home[7]",
                "qvel_times_0.1[7]",
                "world_target_error_times_10[3]",
            ],
            "action_order": [f"fr3_joint{i}_normalized_delta" for i in range(1, 8)],
            "units": "bounded normalized delta; simulator applies 0.03 rad",
            "normalization": "see observation_order",
            "frame": "world",
            "rate_hz": 50,
            "rollback": "command-sink",
            "lock_sha256": hashlib.sha256((ROOT / "uv.lock").read_bytes()).hexdigest(),
            "performance_verified": False,
        }
        write_json(bundle / "manifest.json", manifest)
        errors = validate_candidate(bundle)
        rows = [
            (
                float(i),
                float(v["action"][0]),
                float(policy_action(bundle, np.array(v["observation"]))[0]),
            )
            for i, v in enumerate(vectors)
        ]
        return Experiment(
            rows,
            max(abs(a - b) for _, a, b in rows),
            {
                "bundle": "sample_candidate/manifest.json",
                "errors": errors,
                "performance_verified": False,
            },
            {
                "bundle_valid": not errors,
                "actual_trained_policy": bool(np.linalg.norm(weights) > 0),
            },
            files=["sample_candidate"],
        )
    if identifier == "hw-common-01":
        bundle = previous_run("sim-deploy-01") / "sample_candidate"
        errors = validate_candidate(bundle)
        if errors:
            raise ValueError("; ".join(errors))
        manifest = json.loads((bundle / "manifest.json").read_text())
        sink = []
        for vector in manifest["test_vectors"]:
            action = policy_action(bundle, np.array(vector["observation"]))
            sink.append(action.tolist())  # Intentionally no publisher, socket, SDK, or callback.
        replay = [
            policy_action(bundle, np.array(v["observation"])).tolist()
            for v in manifest["test_vectors"]
        ]
        write_json(output / "inference.json", {"actions": sink, "replay": replay})
        rows = [
            (float(i), float(a[0]), float(b[0]))
            for i, (a, b) in enumerate(zip(sink, replay, strict=True))
        ]
        return Experiment(
            rows,
            0.0,
            {
                "command_sink": "enabled",
                "emitted_command_count": 0,
                "inference_count": len(sink),
                "manifest_sha256": hashlib.sha256(
                    (bundle / "manifest.json").read_bytes()
                ).hexdigest(),
                "replay_exact": sink == replay,
            },
            {"deterministic_inference": sink == replay, "nonempty_inference": len(sink) > 0},
            files=["inference.json"],
        )
    if identifier in {"sim-enlight-02", "sim-wuji-02"}:
        from pai_lab.lessons.gpu import candidate

        return candidate(identifier, output, seed, samples, variant)
    raise ValueError(identifier)
