"""Generate equivalent Codex and Claude wrappers from the common workflow."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / "agent/workflow.md").read_text(encoding="utf-8")
HEADER = """---
name: tutorial-robotics
description: Run the public capability-first Tutorial Robotics curriculum safely.
---

"""


def main() -> None:
    content = HEADER + WORKFLOW
    for path in (
        ROOT / ".agents/skills/tutorial-robotics/SKILL.md",
        ROOT / ".claude/skills/tutorial-robotics/SKILL.md",
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print("synchronized Codex and Claude skill wrappers")


if __name__ == "__main__":
    main()
