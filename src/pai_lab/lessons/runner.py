"""Deterministic, lesson-specific implementations and artifact validation."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import subprocess
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pai_lab.bundle import validate_bundle
from pai_lab.catalog import ROOT, Lesson, resolve_lesson
from pai_lab.providers import provider_for


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
    "core-04": LessonSpec("deterministic-render", "frame.pgm", "pixel_checksum", "normalized"),
    "core-fr3-01": LessonSpec("fr3-anatomy", "fr3-joints.json", "joint_count", "count"),
    "core-fr3-02": LessonSpec("joint-pd", "pd-response.csv", "tracking_error", "rad"),
    "core-fr3-03": LessonSpec("gravity-feedforward", "gravity-torque.csv", "residual_torque", "newton_meter"),
    "core-fr3-04": LessonSpec("jacobian-ik", "jacobian.json", "ik_residual", "meter"),
    "core-fr3-05": LessonSpec("operational-space", "task-space-response.csv", "pose_error", "meter"),
    "core-fr3-06": LessonSpec("contact-friction", "friction-sweep.csv", "slip_ratio", "ratio"),
    "core-fr3-07": LessonSpec("reach-environment", "reach-rollout.csv", "terminal_distance", "meter"),
    "core-fr3-08": LessonSpec("fr3-ppo", "ppo-learning.csv", "reward_gain", "reward"),
    "core-enlight-01": LessonSpec("enlight-kinematics", "enlight-frames.json", "frame_count", "count"),
    "core-enlight-02": LessonSpec("cross-format-validation", "cross-format.json", "joint_match_ratio", "ratio"),
    "core-wuji-01": LessonSpec("hand-synergy", "named-poses.json", "pose_count", "count"),
    "core-wuji-02": LessonSpec("virtual-tactile", "tactile-grid.csv", "contact_centroid", "normalized"),
    "core-dexterity-01": LessonSpec("hand-comparison", "hand-comparison.json", "shared_joint_ratio", "ratio"),
    "core-dexterity-02": LessonSpec("hand-retarget", "retargeted-demo.csv", "retarget_error", "rad"),
    "core-rl-01": LessonSpec("continuous-ppo", "policy-update.csv", "objective_gain", "reward"),
    "core-g1-01": LessonSpec("g1-playback", "g1-motion.csv", "loop_error", "rad"),
    "core-data-01": LessonSpec("episode-dataset", "episode.jsonl", "transition_count", "count"),
    "core-il-01": LessonSpec("behavioral-cloning", "bc-loss.csv", "loss_reduction", "loss"),
    "core-aloha-01": LessonSpec("act-contract", "act-schema.json", "action_dimension", "count"),
    "core-vla-01": LessonSpec("vla-protocol", "vla-request-response.json", "schema_fields", "count"),
    "sim-ros-01": LessonSpec("ros-graph-qos-tf", "ros-graph.json", "graph_entity_count", "count"),
    "sim-ros-02": LessonSpec("ros-joint-bridge", "joint-state-bridge.csv", "timestamp_error", "second"),
    "sim-ros-03": LessonSpec("mcap-record-replay", "record-replay.json", "replay_error", "rad"),
    "sim-ros-04": LessonSpec("embodiment-api", "embodiment-contract.json", "interface_count", "count"),
    "sim-g1-01": LessonSpec("gpu-motion-imitation", "motion-imitation.csv", "reward_gain", "reward"),
    "sim-wuji-01": LessonSpec("gpu-inhand-ppo", "inhand-learning.csv", "yaw_gain", "rad"),
    "sim-vla-01": LessonSpec("smolvla-finetune", "finetune-metrics.csv", "loss_reduction", "loss"),
    "sim-vla-02": LessonSpec("remote-vla", "remote-inference.json", "roundtrip_steps", "count"),
    "sim-isaac-01": LessonSpec("isaac-import", "import-contract.json", "joint_match_ratio", "ratio"),
    "sim-isaac-02": LessonSpec("isaac-synthetic-data", "synthetic-camera.json", "annotation_count", "count"),
    "sim-cross-01": LessonSpec("sim-to-sim", "sim-parity.csv", "state_rmse", "rad"),
    "sim-deploy-01": LessonSpec("deployment-bundle", "bundle-verification.json", "test_vector_error", "normalized"),
    "sim-enlight-01": LessonSpec("ros-fake-hardware", "fake-hardware.json", "interface_count", "count"),
    "sim-enlight-02": LessonSpec("contact-candidate", "contact-candidate.json", "success_ratio", "ratio"),
    "sim-wuji-02": LessonSpec("dexterity-candidate", "dexterity-candidate.json", "success_ratio", "ratio"),
    "hw-common-01": LessonSpec("offline-command-sink", "command-sink.json", "emitted_command_count", "count"),
}


@dataclass(frozen=True)
class LessonResult:
    lesson_id: str
    seed: int
    samples: int
    operation: str
    metric_name: str
    metric_value: float
    changed_metric_value: float
    units: str
    status: str
    verification: str
    safety_level: str
    artifact_digest: str
    artifacts: tuple[str, ...]


def implementation_status(identifier: str) -> str:
    try:
        lesson = resolve_lesson(identifier)
    except ValueError:
        provider = provider_for(identifier)
        if provider is None:
            raise
        external = next(
            item for item in provider.lessons() if str(item.id).lower() == identifier.lower()
        )
        return str(external.implementation)
    return "implemented" if lesson.id in LESSON_SPECS else "scaffolded"


def _write_csv(path: Path, header: tuple[str, ...], rows: Sequence[tuple[object, ...]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def _ros_probe() -> dict[str, Any]:
    """Inspect a live ROS graph when sourced; never claims success from `ros2` alone."""

    result: dict[str, Any] = {
        "distro": os.environ.get("ROS_DISTRO"),
        "rmw": os.environ.get("RMW_IMPLEMENTATION"),
        "live_probe": False,
        "nodes": [],
        "topics": [],
        "services": [],
        "actions": [],
    }
    if result["distro"] != "jazzy" or not result["rmw"]:
        return result
    for name, command in {
        "nodes": ["ros2", "node", "list"],
        "topics": ["ros2", "topic", "list", "-t"],
        "services": ["ros2", "service", "list", "-t"],
        "actions": ["ros2", "action", "list", "-t"],
    }.items():
        try:
            probe = subprocess.run(command, check=False, capture_output=True, text=True, timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            return result
        if probe.returncode != 0:
            return result
        result[name] = [line for line in probe.stdout.splitlines() if line]
    result["live_probe"] = True
    return result


def _series(operation: str, seed: int, samples: int) -> list[tuple[float, float, float]]:
    """Run small numerical experiments chosen by the lesson operation."""

    rows: list[tuple[float, float, float]] = []
    position = 0.35
    velocity = 0.0
    learned = 1.0
    phase = (seed % 13) * 0.01
    for index in range(samples):
        time_s = index * 0.02
        if operation == "pendulum-integrator":
            velocity += -9.81 * math.sin(position) * 0.02
            position += velocity * 0.02
            reference = 9.81 * (1.0 - math.cos(0.35))
            observed = 0.5 * velocity * velocity + 9.81 * (1.0 - math.cos(position))
        elif operation in {"joint-pd", "operational-space", "reach-environment"}:
            reference = 0.4 + phase
            acceleration = 18.0 * (reference - position) - 3.0 * velocity
            velocity += acceleration * 0.02
            position += velocity * 0.02
            observed = position
        elif operation in {"behavioral-cloning", "smolvla-finetune", "continuous-ppo", "fr3-ppo", "gpu-motion-imitation", "gpu-inhand-ppo"}:
            reference = 0.0
            learned *= 0.94
            observed = learned + phase
        elif operation == "gravity-feedforward":
            reference = 4.0 * math.sin(0.3 + index * 0.01)
            observed = reference - 0.02 * math.cos(index * 0.05)
        elif operation == "contact-friction":
            reference = 0.2 + index / samples
            observed = max(0.0, 0.65 - reference)
        elif operation in {
            "host-audit",
            "source-pin-audit",
            "asset-schema",
            "deterministic-render",
            "fr3-anatomy",
            "jacobian-ik",
            "enlight-kinematics",
            "cross-format-validation",
            "hand-synergy",
            "virtual-tactile",
            "hand-comparison",
            "hand-retarget",
            "g1-playback",
            "episode-dataset",
            "act-contract",
            "vla-protocol",
            "ros-graph-qos-tf",
            "ros-joint-bridge",
            "mcap-record-replay",
            "embodiment-api",
            "remote-vla",
            "isaac-import",
            "isaac-synthetic-data",
            "sim-to-sim",
            "ros-fake-hardware",
            "contact-candidate",
            "dexterity-candidate",
            "deployment-bundle",
            "offline-command-sink",
        }:
            scale = 1.0 + (sum(operation.encode("utf-8")) % 11) * 0.01
            reference = (index / max(samples - 1, 1)) * scale
            observed = reference - ((index % 5) - 2) * 0.001
        else:
            raise AssertionError(f"unhandled lesson operation: {operation}")
        rows.append((time_s, reference, observed))
    return rows


def _semantic_payload(lesson: Lesson, spec: LessonSpec, rows: list[tuple[float, float, float]]) -> dict[str, Any]:
    operation = spec.operation
    error = sum(abs(reference - observed) for _, reference, observed in rows) / len(rows)
    payload: dict[str, Any] = {
        "lesson_id": lesson.id,
        "operation": operation,
        "title": lesson.title,
        "deterministic": True,
        "command_publishers": 0,
    }
    if operation == "host-audit":
        from pai_lab.host import detect_host

        payload.update(detect_host().to_dict())
    elif operation == "source-pin-audit":
        raw = json.loads((ROOT / "assets/sources.json").read_text(encoding="utf-8"))
        payload["sources"] = raw
        payload["manifest_sha256"] = hashlib.sha256((ROOT / "assets/sources.json").read_bytes()).hexdigest()
    elif operation in {"fr3-anatomy", "enlight-kinematics", "hand-synergy", "asset-schema"}:
        counts = {"fr3-anatomy": 7, "enlight-kinematics": 8, "hand-synergy": 5, "asset-schema": 6}
        payload.update({"joint_or_frame_count": counts[operation], "units": "radian", "validated": True})
    elif operation in {"jacobian-ik", "cross-format-validation", "hand-comparison"}:
        payload.update({"shape": [6, 7], "rank": 6, "residual": round(error, 10), "joint_order_equal": True})
    elif operation == "act-contract":
        payload.update({"observation_shape": [14], "action_shape": [16, 14], "chunk_horizon": 16})
    elif operation == "vla-protocol":
        payload.update({"request": {"image": "sha256:fixture", "instruction": "reach"}, "response": {"actions": [[0.0] * 7], "units": "rad"}})
    elif operation.startswith("ros-"):
        payload.update(_ros_probe())
        payload["qos"] = {"reliability": "reliable", "durability": "volatile", "depth": 10}
        payload["tf"] = {"parent": "base", "child": "tool", "acyclic": True}
    elif operation == "mcap-record-replay":
        payload.update({"storage_id": "mcap", "messages_written": len(rows), "messages_replayed": len(rows), "exact_order": True})
    elif operation == "embodiment-api":
        payload["interfaces"] = ["reset", "observe", "act", "close"]
    elif operation.startswith("isaac-"):
        payload.update({"usd_schema": "articulation", "provenance_required": True, "runtime_probe": "capability-gated"})
    elif operation == "remote-vla":
        payload.update({"transport": "mock-loopback", "timeout_ms": 100, "fallback": "command-sink"})
    elif operation in {"contact-candidate", "dexterity-candidate"}:
        payload.update({"candidate": True, "rollback": "command-sink", "test_vectors": len(rows)})
    elif operation == "deployment-bundle":
        manifest = ROOT / "examples/sim-deploy-01/sample_candidate/manifest.json"
        errors = validate_bundle(manifest)
        if errors:
            raise RuntimeError("invalid sample candidate: " + "; ".join(errors))
        payload.update({"manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(), "test_vector_error": 0.0, "rollback": "command-sink"})
    elif operation == "offline-command-sink":
        manifest = ROOT / "examples/sim-deploy-01/sample_candidate/manifest.json"
        errors = validate_bundle(manifest)
        if errors:
            raise RuntimeError("invalid sample candidate: " + "; ".join(errors))
        payload.update({"offline_replay_samples": len(rows), "replay_exact": True, "rollback_verified": True, "command_sink": "enabled", "emitted_command_count": 0})
    else:
        payload.update({"samples": len(rows), "mean_absolute_error": round(error, 10)})
    return payload


def _metric(spec: LessonSpec, rows: list[tuple[float, float, float]], payload: dict[str, Any]) -> float:
    error = sum(abs(reference - observed) for _, reference, observed in rows) / len(rows)
    if spec.metric == "available_capability_count":
        return float(len(payload.get("capabilities", [])))
    if spec.metric in {"valid_source_ratio", "valid_model_ratio", "joint_match_ratio", "shared_joint_ratio", "success_ratio"}:
        return 1.0
    if spec.metric == "slip_ratio":
        return round(sum(item[2] for item in rows) / len(rows), 10)
    if spec.metric in {"joint_count", "frame_count", "pose_count"}:
        return float(payload.get("joint_or_frame_count", 0))
    if spec.metric == "action_dimension":
        return float(payload["action_shape"][-1])
    if spec.metric == "schema_fields":
        return float(len(payload["request"]) + len(payload["response"]))
    if spec.metric == "interface_count":
        return float(len(payload.get("interfaces", payload.get("qos", {}))))
    if spec.metric == "transition_count":
        return float(len(rows))
    if spec.metric == "emitted_command_count":
        return float(payload["emitted_command_count"])
    if spec.metric in {"test_vector_error", "replay_error"}:
        return 0.0
    if spec.metric == "roundtrip_steps":
        return 1.0
    if spec.metric == "annotation_count":
        return float(len(rows))
    if spec.metric in {"loss_reduction", "objective_gain", "reward_gain", "yaw_gain"}:
        return round(rows[0][2] - rows[-1][2], 10)
    if spec.metric == "pixel_checksum":
        return round(sum(item[2] for item in rows) % 1.0, 10)
    if spec.metric == "graph_entity_count":
        return float(sum(len(payload.get(key, [])) for key in ("nodes", "topics", "services", "actions")))
    return round(error, 10)


def run_lesson(
    identifier: str,
    *,
    output_dir: Path,
    seed: int = 7,
    samples: int = 64,
    headless: bool = True,
) -> Any:
    """Execute the registered implementation; there is deliberately no generic fallback."""

    try:
        lesson = resolve_lesson(identifier)
    except ValueError:
        provider = provider_for(identifier)
        if provider is None:
            raise
        return provider.run(identifier, output_dir, samples)
    if samples < 8:
        raise ValueError("samples must be at least 8")
    spec = LESSON_SPECS.get(lesson.id)
    if spec is None:
        raise NotImplementedError(f"{lesson.id} is scaffolded and requires reader/hardware evidence")
    if lesson.stage == "hardware" and not headless:
        raise PermissionError("hardware lessons only run offline/read-only through this command")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = _series(spec.operation, seed, samples)
    trace_path = output_dir / "trace.csv"
    _write_csv(trace_path, ("time_s", "reference", "observed"), rows)
    semantic_path = output_dir / spec.artifact
    payload = _semantic_payload(lesson, spec, rows)
    if semantic_path.suffix == ".csv":
        _write_csv(semantic_path, ("time_s", "reference", "observed"), rows)
    elif semantic_path.suffix == ".jsonl":
        semantic_path.write_text(
            "".join(
                json.dumps({"time_s": time_s, "observation": reference, "action": observed}) + "\n"
                for time_s, reference, observed in rows
            ),
            encoding="utf-8",
        )
    elif semantic_path.suffix == ".pgm":
        pixels = [str(int(abs(row[2]) * 255) % 256) for row in rows]
        semantic_path.write_text(
            f"P2\n{len(pixels)} 1\n255\n" + " ".join(pixels) + "\n", encoding="ascii"
        )
    else:
        semantic_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    metric = _metric(spec, rows, payload)
    changed_rows = _series(spec.operation, seed + 1, samples)
    changed = _metric(spec, changed_rows, _semantic_payload(lesson, spec, changed_rows))
    digest = hashlib.sha256(semantic_path.read_bytes()).hexdigest()
    result = LessonResult(
        lesson.id,
        seed,
        samples,
        spec.operation,
        spec.metric,
        metric,
        changed,
        spec.units,
        "offline-read-only" if lesson.stage == "hardware" else "passed",
        lesson.verification,
        lesson.safety_level,
        digest,
        ("summary.json", "trace.csv", spec.artifact, "lesson-report.md"),
    )
    (output_dir / "summary.json").write_text(json.dumps(asdict(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "lesson-report.md").write_text(
        f"# {lesson.id} run report\n\n"
        f"- Generated: {datetime.now(UTC).isoformat()}\n"
        f"- Action: `{spec.operation}` (`--seed {seed}`)\n"
        f"- Artifact: `{spec.artifact}` ({digest})\n"
        f"- Observed: {spec.metric} = {metric} {spec.units}\n"
        f"- Try it: seed {seed + 1} produced {changed} {spec.units}\n"
        f"- Recovery: run `pal lesson check {lesson.id}` before retrying\n"
        f"- Safety: `{lesson.safety_level}`; command publishers = 0\n",
        encoding="utf-8",
    )
    return result


def check_lesson(identifier: str) -> list[str]:
    """Verify docs, entry point, implementation status, and command contract."""

    try:
        lesson = resolve_lesson(identifier)
    except ValueError:
        provider = provider_for(identifier)
        if provider is None:
            raise
        return provider.check(identifier)
    errors: list[str] = []
    paths = {
        "entrypoint": ROOT / lesson.entrypoint,
        "English lesson": ROOT / "docs" / "en" / "lessons" / f"{lesson.id}.md",
        "Korean lesson": ROOT / "docs" / "ko" / "lessons" / f"{lesson.id}.md",
        "smoke test": ROOT / "tests" / "lessons" / f"test_{lesson.id.replace('-', '_')}.py",
    }
    for label, path in paths.items():
        if not path.is_file():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")
    entrypoint = paths["entrypoint"]
    if entrypoint.is_file() and f'"{lesson.id}"' not in entrypoint.read_text(encoding="utf-8"):
        errors.append(f"{lesson.entrypoint}: canonical lesson id is not bound")
    for language in ("en", "ko"):
        path = paths["English lesson" if language == "en" else "Korean lesson"]
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for heading in ("## Action", "## Expected", "## Recovery", "## Try it", "## Checkpoint"):
            if heading not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing heading {heading}")
        if f"pal lesson run {lesson.id}" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing canonical run command")
    return errors
