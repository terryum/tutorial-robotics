"""Independent learner or developer sessions; never shared publication state."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from pai_lab.catalog import ROOT


def local_root() -> Path:
    return Path(os.environ.get("PAL_LOCAL_DIR", str(ROOT / ".local"))).resolve()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=path.name + ".",
        suffix=".tmp",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)
