"""Epoch-boundary checkpoints and portable numeric training bundles (no pickle)."""

from __future__ import annotations

import hashlib
import json
import signal
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import numpy as np

from pai_lab.catalog import ROOT
from pai_lab.local import write_json


def sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def identity(env: Any, algorithm: str, seed: int, learning_rate: float) -> dict[str, Any]:
    files = [
        "src/pai_lab/training.py",
        "src/pai_lab/lessons/arm.py",
        "src/pai_lab/lessons/models.py",
        "src/pai_lab/lessons/learning.py",
        "src/pai_lab/lessons/isaac_tasks.py",
        "src/pai_lab/lessons/isaac_adapter.py",
        "uv.lock",
    ]
    return {
        "model": env.name,
        "source": env.source,
        "engine": getattr(env, "engine", "MuJoCo"),
        "runtime_version": getattr(env, "runtime_version", "test-runtime"),
        "algorithm": algorithm,
        "seed": seed,
        "learning_rate": learning_rate,
        "code": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in files},
        "observation": "q-home[7],0.1*qvel[7],10*(world_target-tcp)[3]",
        "action": "bounded joint position delta=0.03*tanh(action)",
        "normalization": {"clip": [-5, 5], "adaptive": False},
        "control_dt_s": 0.02,
    }


@contextmanager
def termination_flag() -> Iterator[list[bool]]:
    stop = [False]

    def handler(signum: int, frame: Any) -> None:
        stop[0] = True

    previous = {s: signal.signal(s, handler) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        yield stop
    finally:
        for s, old in previous.items():
            signal.signal(s, old)


def save_checkpoint(output: Path, state: dict[str, Any]) -> Path:
    checkpoint = output / "checkpoints" / f"epoch-{state['epoch']:06d}.json"
    write_json(checkpoint, {"state": state, "sha256": sha(state)})
    return checkpoint


def read_checkpoint(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    state = value["state"]
    if sha(state) != value["sha256"] or state["schema_version"] != 1:
        raise ValueError("checkpoint checksum/schema mismatch")
    if set(state) != {
        "schema_version",
        "identity",
        "epoch",
        "weights",
        "optimizer",
        "rng",
        "rows",
        "data_sha256",
    }:
        raise ValueError("unrecognized checkpoint fields")
    weights = np.asarray(state["weights"], dtype=float)
    value_weights = np.asarray(state["optimizer"]["value_weights"], dtype=float)
    momentum = np.asarray(state["optimizer"]["momentum"], dtype=float)
    if (
        weights.shape != (18, 7)
        or momentum.shape != weights.shape
        or value_weights.shape != (18,)
        or not all(np.isfinite(a).all() for a in (weights, momentum, value_weights))
        or not isinstance(state["epoch"], int)
        or state["epoch"] < 1
    ):
        raise ValueError("invalid checkpoint numeric state")
    return dict(state)


def latest_checkpoint(path: Path) -> dict[str, Any]:
    if path.is_file():
        return read_checkpoint(path)
    for candidate in sorted((path / "checkpoints").glob("epoch-*.json"), reverse=True):
        try:
            return read_checkpoint(candidate)
        except (OSError, ValueError, KeyError, TypeError):
            continue
    raise ValueError("no valid checkpoint")


def transfer_export(source: Path, destination: Path) -> None:
    state = latest_checkpoint(source)
    data = (
        json.loads((source / "demonstrations.json").read_text())
        if (source / "demonstrations.json").exists()
        else None
    )
    if state["data_sha256"] != sha(data):
        raise ValueError("dataset checksum mismatch")
    payload = {"checkpoint": state, "demonstrations": data}
    if destination.exists():
        raise ValueError("export destination already exists")
    write_json(destination, {"schema_version": 1, "payload": payload, "sha256": sha(payload)})


def transfer_import(source: Path, destination: Path) -> None:
    bundle = json.loads(source.read_text())
    payload = bundle["payload"]
    if bundle["schema_version"] != 1 or sha(payload) != bundle["sha256"]:
        raise ValueError("transfer checksum/schema mismatch")
    state = payload["checkpoint"]
    if sha(payload["demonstrations"]) != state["data_sha256"]:
        raise ValueError("transfer dataset mismatch")
    if destination.exists():
        raise ValueError("import destination must be new")
    # Fixed filenames only: no extraction, paths, host configuration, or approval receipts.
    destination.mkdir(parents=True)
    checkpoint = save_checkpoint(destination, state)
    read_checkpoint(checkpoint)
    if payload["demonstrations"] is not None:
        write_json(destination / "demonstrations.json", payload["demonstrations"])


def train(
    env: Any,
    output: Path,
    *,
    algorithm: str = "bc",
    seed: int = 7,
    epochs: int = 16,
    learning_rate: float = 0.01,
    resume_from: Path | None = None,
    stop_after: int | None = None,
) -> dict[str, Any]:
    from pai_lab.lessons.arm import demonstrations, evaluate
    from pai_lab.lessons.learning import generalized_advantage

    if algorithm not in {"bc", "ppo"} or not 1 <= epochs <= 100000:
        raise ValueError("algorithm bc/ppo and epochs 1..100000 required")
    if not np.isfinite(learning_rate) or not 0 < learning_rate <= 0.1:
        raise ValueError("learning rate must be (0,0.1]")
    output.mkdir(parents=True, exist_ok=True)
    contract = identity(env, algorithm, seed, learning_rate)
    rng = np.random.default_rng(seed)
    weights = rng.normal(0, 0.01, (18, 7))
    momentum, value_weights = np.zeros_like(weights), np.zeros(18)
    rows: list[Any] = []
    start = 0
    data = None
    resumed = latest_checkpoint(resume_from) if resume_from else None
    if resumed:
        assert resume_from is not None
        if resumed["identity"] != contract:
            raise ValueError("incompatible code/model/environment/training configuration")
        weights = np.array(resumed["weights"])
        momentum = np.array(resumed["optimizer"]["momentum"])
        value_weights = np.array(resumed["optimizer"]["value_weights"])
        rng.bit_generator.state = resumed["rng"]
        rows, start = resumed["rows"], resumed["epoch"]
        if epochs < start:
            raise ValueError("requested total epochs precede checkpoint progress")
        source = resume_from.parent.parent if resume_from.is_file() else resume_from
        if algorithm == "bc":
            data = json.loads((source / "demonstrations.json").read_text())
        if sha(data) != resumed["data_sha256"]:
            raise ValueError("incompatible demonstration data")
    if algorithm == "bc":
        data = data if data is not None else demonstrations(env)
        write_json(output / "demonstrations.json", data)
        train_rows = [r for r in data if r["split"] == "train"]
        validation = [r for r in data if r["split"] == "validation"]
        test = [r for r in data if r["split"] == "test"]
        x = np.array([r["observation"] + [1.0] for r in train_rows])
        y = np.array([r["action"] for r in train_rows])
        # Normalize feature covariance with a fixed preconditioner; optimizer state remains explicit.
        preconditioner = np.linalg.inv(x.T @ x / len(x) + 1e-4 * np.eye(18))
    with termination_flag() as stop:
        for epoch in range(start, epochs):
            # Episodes restart at an update boundary, so no mid-episode hidden state is lost.
            env.rng = np.random.default_rng(seed + epoch)
            if algorithm == "bc":
                gradient = preconditioner @ (x.T @ (x @ weights - y) / len(x))
                momentum = 0.9 * momentum + gradient
                weights -= learning_rate * momentum
                metric = float(np.mean((x @ weights - y) ** 2))
            else:
                obs = env.reset()
                xs, actions, means, rewards, values, next_values, terminals, boundaries = (
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                )
                sigma = 0.3
                for _ in range(128):
                    feature = np.append(np.clip(obs, -5, 5), 1.0)
                    mean = feature @ weights
                    action = mean + rng.normal(0, sigma, 7)
                    following, reward, terminal, boundary = env.step(action)
                    xs.append(feature)
                    actions.append(action)
                    means.append(mean)
                    rewards.append(reward)
                    values.append(float(feature @ value_weights))
                    next_values.append(
                        float(np.append(np.clip(following, -5, 5), 1.0) @ value_weights)
                    )
                    terminals.append(terminal)
                    boundaries.append(terminal or boundary)
                    obs = env.reset() if terminal or boundary else following
                x, y, old = np.array(xs), np.array(actions), np.array(means)
                advantages = generalized_advantage(
                    np.array(rewards),
                    np.array(values),
                    np.array(next_values),
                    np.array(terminals),
                    np.array(boundaries),
                )
                returns = advantages + values
                advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
                for _ in range(4):
                    mean = x @ weights
                    ratio = np.exp(
                        np.clip(
                            -0.5
                            * np.sum(((y - mean) / sigma) ** 2 - ((y - old) / sigma) ** 2, axis=1),
                            -20,
                            20,
                        )
                    )
                    active = ((advantages >= 0) & (ratio <= 1.2)) | (
                        (advantages < 0) & (ratio >= 0.8)
                    )
                    gradient = (
                        x.T
                        @ ((active * advantages * ratio)[:, None] * (y - mean) / sigma**2)
                        / len(x)
                    )
                    weights += learning_rate * gradient / max(1.0, np.linalg.norm(gradient))
                value_weights = np.linalg.solve(x.T @ x + 0.01 * np.eye(18), x.T @ returns)
                metric = float(np.mean(rewards))
            rows.append((float(epoch), 0.0, metric))
            state = {
                "schema_version": 1,
                "identity": contract,
                "epoch": epoch + 1,
                "weights": weights.tolist(),
                "optimizer": {
                    "momentum": momentum.tolist(),
                    "value_weights": value_weights.tolist(),
                },
                "rng": rng.bit_generator.state,
                "rows": rows,
                "data_sha256": sha(data),
            }
            save_checkpoint(output, state)
            if stop[0] or (stop_after is not None and epoch + 1 >= stop_after):
                return {"status": "interrupted", "epoch": epoch + 1, "rows": rows}
    evaluation = evaluate(env, weights)
    if algorithm == "bc":
        for name, subset in (("validation", validation), ("test", test)):
            xv = np.array([r["observation"] + [1.0] for r in subset])
            yv = np.array([r["action"] for r in subset])
            evaluation[name + "_mse"] = float(np.mean((xv @ weights - yv) ** 2))
    np.savez(output / "policy.npz", weights=weights, value_weights=value_weights)
    write_json(output / "evaluation.json", evaluation)
    write_json(output / "training-contract.json", contract)
    return {
        "status": "trained",
        "epoch": epochs,
        "rows": rows,
        "evaluation": evaluation,
        "finite_policy": bool(np.isfinite(weights).all()),
        "performance_verified": evaluation["performance_verified"],
        "training_scope": "simulation-candidate",
        "source": env.source,
    }
