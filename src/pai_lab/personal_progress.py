"""Explicit, local-only JSON bridge to an optional learner-owned helper.

No helper, Git, or network operation occurs without an enabled registration.
The helper owns durable queuing; this module never exports raw evidence.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from pai_lab.catalog import ROOT, load_catalog
from pai_lab.local import local_root, write_json

_snapshots: dict[str, dict[str, Any]] = {}


def configuration(root: Path = ROOT) -> dict[str, Any] | None:
    # An override always denotes a developer/verification session, even if it
    # happens to point at the registered directory.
    if any(
        os.environ.get(key)
        for key in ("PAL_LOCAL_DIR", "PAL_PRIVATE_LOCAL_DIR", "PAL_PUBLIC_LOCAL_DIR")
    ):
        return None
    path = root / ".local/personal-progress.json"
    if not path.is_file():
        return None
    raw = json.loads(path.read_text())
    if raw.get("enabled") is not True or Path(raw["registered_root"]).resolve() != root.resolve():
        return None
    command = raw.get("helper")
    if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
        raise ValueError("personal progress helper must be an argument list")
    return dict(raw)


def exchange(
    operation: str = "sync", *, root: Path = ROOT, scope: str = "public"
) -> dict[str, Any] | None:
    config = configuration(root)
    if config is None:
        return None
    cache = root / ".local/personal-progress-cache.json"
    try:
        result = subprocess.run(
            config["helper"],
            input=json.dumps(
                {
                    "schema_version": 1,
                    "operation": operation,
                    "root": str(root.resolve()),
                    "scope": scope,
                }
            ),
            capture_output=True,
            text=True,
            timeout=180,
            check=True,
        )
        value = json.loads(result.stdout)
        if value.get("schema_version") != 1 or not isinstance(value.get("lessons"), list):
            raise ValueError("invalid personal progress response")
        write_json(cache, value)
    except (OSError, ValueError, subprocess.SubprocessError):
        value = (
            json.loads(cache.read_text())
            if cache.exists()
            else {"schema_version": 1, "lessons": []}
        )
        value["sync"] = {
            **value.get("sync", {}),
            "status": "pending",
            "reason": "helper unavailable; local completion retained",
        }
        print("personal progress: 동기화 대기 (local completion retained)", file=sys.stderr)
    _snapshots[str(root)] = value
    return dict(value)


def snapshot(root: Path = ROOT) -> dict[str, Any] | None:
    if configuration(root) is None:
        return None
    if str(root) not in _snapshots:
        cache = root / ".local/personal-progress-cache.json"
        _snapshots[str(root)] = json.loads(cache.read_text()) if cache.exists() else {"lessons": []}
    return _snapshots[str(root)]


def shared_entry(
    identifier: str, *, root: Path = ROOT, scope: str = "public"
) -> dict[str, Any] | None:
    value = snapshot(root)
    if value:
        for row in value["lessons"]:
            if row["scope"] == scope and row["id"] == identifier and row["completed"]:
                return dict(row)
    return None


def overlay(completed: dict[str, Any], *, root: Path = ROOT, scope: str = "public") -> None:
    value = snapshot(root)
    if value:
        for row in value["lessons"]:
            if row["scope"] == scope and row["completed"] and row["id"] not in completed:
                # No invented run_dir: shared learning is not a local artifact.
                completed[row["id"]] = {**row, "shared": True}


def shared_feedback(identifier: str, *, root: Path = ROOT, scope: str = "public") -> bool:
    value = snapshot(root)
    return bool(
        value
        and any(
            row["scope"] == scope and row["id"] == identifier and row.get("unresolved_feedback")
            for row in value["lessons"]
        )
    )


def shared_gaps(identifier: str, *, root: Path = ROOT, scope: str = "public") -> list[str] | None:
    row = shared_entry(identifier, root=root, scope=scope)
    if row is None:
        return None
    errors = []
    digests = row.get("verified_digests", [])
    compatible_history = False
    if scope == "public" and digests:
        from pai_lab.lessons.evidence import CORE_HISTORY
        from pai_lab.lessons.runner import implementation_digest

        prior, current = CORE_HISTORY.get(identifier, ("", ""))
        digest = implementation_digest(identifier)
        compatible_history = prior in digests and current == digest
        if digest not in digests and not compatible_history:
            errors.append("this checkout has changed; revalidate the lesson on this environment")
    if row.get("needs_review") and not compatible_history:
        errors.append("shared completion retained; current source version needs revalidation")
    if row.get("unresolved_feedback"):
        errors.append("unresolved shared feedback; resume the originating environment")
    return errors


def notify() -> None:
    exchange("sync")


def _progress_counts(rows: list[dict[str, Any]]) -> dict[str, int | float]:
    completed = sum(bool(row["completed"]) for row in rows)
    return {
        "completed": completed,
        "total": len(rows),
        "percent": 100 * completed / len(rows) if rows else 0,
    }


def _learning_summary(value: dict[str, Any]) -> dict[str, Any]:
    diagnostics = {lesson.id: lesson.stage for lesson in load_catalog() if lesson.diagnostic}
    rows = [
        row for row in value["lessons"] if row["scope"] != "public" or row["id"] not in diagnostics
    ]
    if len(rows) == len(value["lessons"]):
        return value
    result = {**value, **_progress_counts(rows), "lessons": rows}
    if groups := value.get("groups"):
        filtered_groups = dict(groups)
        for stage in groups.keys() & diagnostics.values():
            stage_rows = [
                row for row in rows if row["scope"] == "public" and row.get("stage") == stage
            ]
            filtered_groups[stage] = {**groups[stage], **_progress_counts(stage_rows)}
        result["groups"] = filtered_groups
    if "verified_completed" in value:
        result["verified_completed"] = sum(
            bool(row["completed"])
            and bool(row.get("current_version_verified", not row.get("needs_review")))
            for row in rows
        )
    return result


def summary() -> dict[str, Any]:
    value = snapshot()
    if value is not None:
        from pai_lab.progress import load_progress

        if not load_progress().path:
            return _learning_summary(value)
    from pai_lab.paths import selected_lessons
    from pai_lab.progress import load_progress
    from pai_lab.readiness import completion_gaps

    completed = load_progress().completed
    rows = [
        {
            "id": lesson.id,
            "scope": "public",
            "stage": lesson.stage,
            "completed": lesson.id in completed,
            "needs_review": bool(completion_gaps(lesson.id)) if lesson.id in completed else False,
        }
        for lesson in selected_lessons()
    ]
    verified = sum(bool(row["completed"]) and not row["needs_review"] for row in rows)
    return {
        "schema_version": 1,
        **_progress_counts(rows),
        "verified_completed": verified,
        "path": load_progress().path,
        "path_complete": bool(rows) and verified == len(rows),
        "lessons": rows,
        "sync": {"status": "disabled"},
        "state_directory": str(local_root()),
    }
