"""Fail closed on v1 publication invariants."""

from __future__ import annotations

import json
import re

from pai_lab.catalog import ROOT, load_catalog, validate_catalog

PLACEHOLDERS = re.compile(r"pending implementation|todo\b|tbd\b|agent must generate", re.IGNORECASE)
SECRET_PATTERNS = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}"
)


def main() -> int:
    errors = validate_catalog()
    if (ROOT / ".gitmodules").exists():
        errors.append(".gitmodules must not exist in the standalone public repository")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if 'path = "../mujoco-ros2-core"' in pyproject:
        errors.append("sibling mujoco-ros2-core path dependency remains")
    release = json.loads((ROOT / "curriculum/catalog.json").read_text(encoding="utf-8"))["release"]
    scaffolded = [lesson.id for lesson in load_catalog() if lesson.implementation == "scaffolded"]
    if not str(release).endswith("-dev") and scaffolded:
        errors.append("stable release blocked by scaffolded lessons: " + ", ".join(scaffolded))
    publishing = (ROOT / "state/PUBLISHING.md").read_text(encoding="utf-8")
    for lesson in load_catalog():
        row_expected = f"| {lesson.id} | `{lesson.verification}` | {lesson.implementation} |"
        if row_expected not in publishing:
            errors.append(f"{lesson.id}: publishing state disagrees with catalog")
    for lesson in load_catalog():
        en = (ROOT / "docs/en/lessons" / f"{lesson.id}.md").read_text(encoding="utf-8")
        ko = (ROOT / "docs/ko/lessons" / f"{lesson.id}.md").read_text(encoding="utf-8")
        for text, language in ((en, "en"), (ko, "ko")):
            if PLACEHOLDERS.search(text):
                errors.append(f"{lesson.id}/{language}: placeholder text")
            headings = [line for line in text.splitlines() if line.startswith("## ")]
            expected_headings = [
                "## Reader route",
                "## Learning goals",
                "## Preflight",
                "## Action",
                "## Expected",
                "## How it works",
                "## Code connection",
                "## Try it",
                "## Recovery",
                "## Checkpoint",
                "## Next lesson",
            ]
            if lesson.implementation == "implemented":
                expected_headings.insert(expected_headings.index("## How it works"), "## Observe")
            if headings != expected_headings:
                errors.append(f"{lesson.id}/{language}: heading parity mismatch")
    agent = (ROOT / ".agents/skills/tutorial-robotics/SKILL.md").read_text(encoding="utf-8")
    claude = (ROOT / ".claude/skills/tutorial-robotics/SKILL.md").read_text(encoding="utf-8")
    if agent != claude:
        errors.append("Codex and Claude skill wrappers differ")
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if (
            not path.is_file()
            or any(
                part in {".git", ".venv", ".local", ".cache", "vendor", "__pycache__"}
                for part in relative.parts
            )
            or path.suffix.lower() in {".png", ".jpg", ".pdf"}
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if SECRET_PATTERNS.search(text):
            errors.append(f"possible secret: {relative}")
    if errors:
        print("\n".join(errors))
        return 1
    print("release structure valid; external reader/hardware evidence is still badge-gated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
