"""Both agent entry points must consume the same maintained learner contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_codex_and_claude_tutorial_wrappers_equal_canonical_workflow():
    workflow = (ROOT / "agent/workflow.md").read_text()
    wrappers = [
        (ROOT / family / "skills/tutorial-robotics/SKILL.md").read_text()
        for family in (".agents", ".claude")
    ]
    assert wrappers[0] == wrappers[1]
    assert wrappers[0].split("---", 2)[2].lstrip("\n") == workflow


def test_bootstrap_entry_wrappers_agree_and_reference_actual_workflow():
    paths = [ROOT / family / "skills/bootstrap-host/SKILL.md" for family in (".agents", ".claude")]
    assert paths[0].read_bytes() == paths[1].read_bytes()
    for path in paths:
        assert (path.parent / "../../../agent/workflow.md").resolve() == ROOT / "agent/workflow.md"
