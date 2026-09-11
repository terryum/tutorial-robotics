"""Record consumed prerequisite executions without mutating their evidence."""

import hashlib
from contextvars import ContextVar
from pathlib import Path

inputs: ContextVar[list[dict[str, str]] | None] = ContextVar("lesson_inputs", default=None)


def record(identifier: str, path: Path) -> None:
    active = inputs.get()
    if active is not None:
        active.append(
            {
                "lesson": identifier,
                "run_dir": str(path.resolve()),
                "receipt_sha256": hashlib.sha256((path / "run.json").read_bytes()).hexdigest(),
            }
        )
