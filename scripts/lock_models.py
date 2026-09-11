"""Record exact model bytes from already pinned read-only caches; deliberate maintainer action."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = json.loads((ROOT / "assets/sources.json").read_text())["bundles"]
MODELS = {
    "fr3": ("mujoco-menagerie", ["franka_fr3"], "Apache-2.0"),
    "g1": ("mujoco-menagerie", ["unitree_g1"], "BSD-3-Clause"),
    "aloha": ("mujoco-menagerie", ["aloha"], "BSD-3-Clause"),
    "sharpa": ("mujoco-menagerie", ["sharpa_wave"], "Apache-2.0"),
    "wuji": ("wuji-description-beta2", ["hand2/hand2_beta2/body"], "MIT"),
    "enlight": (
        "flexiv-description",
        ["config/Enlight-L", "meshes/Enlight-L", "urdf/common"],
        "Apache-2.0",
    ),
}


def main():
    models = {}
    for name, (bundle, folders, license_name) in MODELS.items():
        source = SOURCES[bundle]
        base = ROOT / ".cache/assets" / source["destination"]
        actual = subprocess.check_output(
            ["git", "-C", str(base), "rev-parse", "HEAD"], text=True
        ).strip()
        if actual != source["revision"]:
            raise ValueError(f"{name}: wrong commit {actual}")
        files = set()
        for folder in folders:
            files.update(p for p in (base / folder).rglob("*") if p.is_file())
        files.update(p for p in base.glob("LICENSE*") if p.is_file())
        models[name] = {
            "bundle": bundle,
            "destination": source["destination"],
            "revision": actual,
            "license": license_name,
            "files": {
                str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(files)
            },
        }
    (ROOT / "assets/model-lock.json").write_text(
        json.dumps({"schema_version": 1, "models": models}, indent=2) + "\n"
    )
    print("Locked", len(models), "public models; vendor files unchanged")


if __name__ == "__main__":
    main()
