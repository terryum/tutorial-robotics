"""Durable teaching phase receipts. Resume inspection never actuates hardware."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from pai_lab.catalog import ROOT, resolve_lesson
from pai_lab.local import local_root, write_json


def update_session(**changes: Any) -> dict[str, Any]:
    path = local_root() / "session.json"
    previous = json.loads(path.read_text()) if path.exists() else {}
    # A new lesson must not inherit explanation or comparison from the last one.
    if changes.get("lesson", previous.get("lesson")) != previous.get("lesson"):
        previous = {}
    if "phase" in changes and changes["phase"] != "paused":
        previous.pop("resume_phase", None)
    from pai_lab.progress import load_progress

    previous.update(changes, saved_at=datetime.now(UTC).isoformat(), path=load_progress().path)
    phase = previous.get("phase", "select")
    previous["next_action"] = {
        "running": "wait for execution; preserve interruption evidence",
        "inspect": "inspect numeric artifacts, explain, then run one comparison",
        "awaiting_comprehension": "reopen the saved results and ask the saved question; await the learner",
        "reviewed": "check feedback and finish the reviewed baseline",
        "finished": "stop; await a request for the next lesson",
        "paused": "inspect course resume before continuing",
    }.get(phase, "inspect saved state before continuing")
    write_json(path, previous)
    return dict(previous)


def pause() -> dict[str, Any]:
    path = local_root() / "session.json"
    value = json.loads(path.read_text()) if path.exists() else {}
    if value.get("phase") == "paused":
        return value
    return update_session(phase="paused", resume_phase=value.get("phase", "select"))


def resume(source: Path | None = None, identifier: str | None = None) -> dict[str, Any]:
    path = source or local_root() / "session.json"
    if path.is_dir():
        path = path / "run.json"
    if not path.is_file():
        raise ValueError("no saved session or run; select a lesson first")
    value = json.loads(path.read_text())
    if not value.get("lesson"):
        if identifier:
            raise ValueError("saved state has no lesson")
        return {
            "lesson": None,
            "saved_state": value,
            "resume_phase": "select",
            "next_action": "select a lesson with course next",
            "automatic_execution": False,
            "resume_available": True,
        }
    lesson = resolve_lesson(str(value.get("lesson", "")))
    if identifier and lesson.id != resolve_lesson(identifier).id:
        raise ValueError("resume lesson mismatch")
    phase = value.get("phase", value.get("status", "inspect"))
    if phase == "paused":
        phase = value.get("resume_phase", "select")
    action = "inspect saved artifacts and continue explanation/comparison"
    if phase in {"running", "interrupted", "failed"}:
        action = "restart short simulation in a fresh run; inspect training checkpoint separately"
    if phase == "finished":
        action = "select the next eligible lesson with course next"
    if lesson.stage == "hardware":
        action = "inspect only; fresh device readiness and per-run approval required"
    evidence_errors: list[str] = []
    run_path = value.get("run_dir")
    if run_path and phase != "awaiting_comprehension":
        candidate = Path(run_path)
        candidate = candidate if candidate.is_absolute() else ROOT / candidate
        if (candidate / "run.json").exists() and (candidate / "summary.json").exists():
            from pai_lab.lessons.evidence import validate_run

            evidence_errors = validate_run(lesson.id, candidate, history=phase == "finished")
    elif path.name == "run.json" and value.get("status") == "executed":
        from pai_lab.lessons.evidence import validate_run

        evidence_errors = validate_run(lesson.id, path.parent)
    if phase == "awaiting_comprehension":
        from pai_lab.lessons.evidence import comparison_errors, validate_run

        action = "reopen the saved results and ask the saved question; await the learner"
        try:
            results = value["presentation"]
            page = Path(results["page"])
            presentation_root = local_root() / "presentations" / lesson.id
            if (
                not page.resolve().is_relative_to(presentation_root)
                or results["page_url"] != page.resolve().as_uri()
                or sha256(page.read_bytes()).hexdigest() != results["page_sha256"]
            ):
                evidence_errors.append("saved results page changed")
            baseline = Path(value["baseline_run"])
            comparison = value.get("comparison_run")
            evidence_errors += (
                comparison_errors(lesson.id, baseline, Path(comparison))
                if comparison
                else validate_run(lesson.id, baseline)
            )
        except (OSError, TypeError, KeyError) as error:
            evidence_errors.append(f"saved results are unavailable: {error}")
    if evidence_errors:
        action = (
            "preserve saved evidence and restart with compatible current code/model/environment"
        )
    return {
        "evidence_errors": evidence_errors,
        "lesson": lesson.id,
        "saved_state": value,
        "resume_phase": phase,
        "next_action": action,
        "automatic_execution": False,
        "resume_available": lesson.stage != "hardware" and not evidence_errors,
    }
