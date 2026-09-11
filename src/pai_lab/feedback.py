"""Durable feedback shared by both agents in the current local session."""

import fcntl
import json
from collections.abc import Callable
from datetime import UTC, datetime
from functools import wraps
from typing import Any
from uuid import uuid4

from pai_lab.catalog import resolve_lesson
from pai_lab.local import local_root, write_json


def serialized[**P, T](function: Callable[P, T]) -> Callable[P, T]:
    @wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        path = local_root() / "feedback.lock"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            return function(*args, **kwargs)

    return wrapped


def items() -> list[dict[str, Any]]:
    path = local_root() / "feedback.json"
    return list(json.loads(path.read_text()) if path.exists() else [])


def current_lesson() -> str:
    path = local_root() / "session.json"
    if not path.exists():
        raise ValueError("no current lesson; supply --lesson ID")
    return str(json.loads(path.read_text())["lesson"])


@serialized
def add(text: str, identifier: str | None = None, urgent: bool = False) -> dict[str, Any]:
    if not text.strip():
        raise ValueError("feedback must not be empty")
    lesson = resolve_lesson(identifier or current_lesson())
    value = {
        "id": uuid4().hex,
        "lesson": lesson.id,
        "original": text,
        "received_at": datetime.now(UTC).isoformat(),
        "urgency": "immediate" if urgent or "지금 바로" in text else "batch",
        "status": "open",
        "resolution": None,
    }
    write_json(local_root() / "feedback.json", [*items(), value])
    return value


@serialized
def resolve(identifier: str, evidence: str) -> dict[str, Any]:
    if not evidence.strip():
        raise ValueError("resolution requires a change and verification description")
    values = items()
    value = next((item for item in values if item["id"] == identifier), None)
    if value is None:
        raise ValueError("unknown feedback ID")
    value.update(status="resolved", resolution=evidence, resolved_at=datetime.now(UTC).isoformat())
    write_json(local_root() / "feedback.json", values)
    return value


def pending(lesson: str) -> list[dict[str, Any]]:
    return [item for item in items() if item["lesson"] == lesson and item["status"] != "resolved"]
