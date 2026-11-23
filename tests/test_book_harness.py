"""Exercise dependency and resume boundaries; these fixtures are not native-agent evidence."""

import importlib.util
import json
import subprocess
import sys

from pai_lab.catalog import ROOT

RUNTIME = ROOT / ".agents/skills/harness/scripts/run.py"


def call(project, *args, ok=True):
    result = subprocess.run(
        [sys.executable, str(RUNTIME), "--project", str(project), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if ok:
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)
    assert result.returncode != 0
    return result.stderr


def task(identifier, inputs, dependencies=()):
    return {
        "id": identifier,
        "role": "harness_worker",
        "inputs": inputs,
        "dependencies": list(dependencies),
        "ownership": [f"out/{identifier}.txt"],
        "context": {"decisions": [], "skill_paths": []},
        "acceptance": ["fixture artifact recorded"],
        "required": True,
    }


def fixture_plan(tmp_path, tasks):
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps({"objective": "dependency boundary test fixture", "tasks": tasks}))
    return path


def complete_fixture(tmp_path, identifier):
    # Synthetic IDs here exercise the ledger only; live native tests run separately.
    call(
        tmp_path,
        "start",
        "--run",
        "one",
        "--task",
        identifier,
        "--agent-id",
        f"test-fixture-{identifier}",
    )
    output = tmp_path / f"out/{identifier}.txt"
    output.parent.mkdir(exist_ok=True)
    output.write_text(identifier)
    result = tmp_path / f"{identifier}-result.json"
    result.write_text(
        json.dumps(
            {
                "run_id": "one",
                "task_id": identifier,
                "status": "completed",
                "summary": "unit fixture only",
                "artifacts": [f"out/{identifier}.txt"],
                "checks": [
                    {
                        "name": "fixture bytes",
                        "status": "passed",
                        "required": True,
                        "evidence": f"fixture output contains {identifier}",
                    }
                ],
                "issues": [],
            }
        )
    )
    call(tmp_path, "result", "--run", "one", "--task", identifier, "--result-file", str(result))
    call(
        tmp_path,
        "agent",
        "--run",
        "one",
        "--agent-id",
        f"test-fixture-{identifier}",
        "--state",
        "idle",
        "--evidence",
        "synthetic lifecycle fixture",
    )


def test_missing_input_cannot_dispatch_downstream(tmp_path):
    plan = fixture_plan(
        tmp_path, [task("upstream", ["absent.txt"]), task("consumer", [], ["upstream"])]
    )
    # Refuse initialization or dispatch before a consumer can run.
    result = subprocess.run(
        [
            sys.executable,
            str(RUNTIME),
            "--project",
            str(tmp_path),
            "init",
            "--plan-file",
            str(plan),
            "--run-id",
            "missing",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        call(
            tmp_path,
            "start",
            "--run",
            "missing",
            "--task",
            "consumer",
            "--agent-id",
            "test-fixture-consumer",
            ok=False,
        )
    else:
        assert "absent.txt" in result.stderr
    assert not (tmp_path / "out/consumer.txt").exists()


def test_resume_only_invalidates_changed_input_and_consumers(tmp_path):
    for name in ("a", "b"):
        (tmp_path / f"{name}.txt").write_text(name)
    plan = fixture_plan(
        tmp_path, [task("a", ["a.txt"]), task("b", ["b.txt"]), task("consumer", [], ["a"])]
    )
    call(tmp_path, "init", "--plan-file", str(plan), "--run-id", "one")
    for identifier in ("a", "b", "consumer"):
        complete_fixture(tmp_path, identifier)
    old = (tmp_path / ".harness/runs/one/plan.json").read_bytes()
    (tmp_path / "a.txt").write_text("changed")
    call(tmp_path, "resume", "--run", "one", "--new-run", "two")
    resumed = json.loads((tmp_path / ".harness/runs/two/plan.json").read_text())
    states = {row["id"]: row["status"] for row in resumed["tasks"]}
    assert states == {"a": "pending", "b": "completed", "consumer": "pending"}
    assert (tmp_path / ".harness/runs/one/plan.json").read_bytes() == old


def test_book_manifest_matches_catalog_and_authored_goals():
    spec = importlib.util.spec_from_file_location("book_spec", ROOT / "scripts/book_spec.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    actual = module.build()
    saved = json.loads((ROOT / "curriculum/book-spec.json").read_text())
    assert actual == saved
    assert len({lesson["id"] for lesson in actual["lessons"]}) == len(
        json.loads((ROOT / "curriculum/catalog.json").read_text())["lessons"]
    )
    for lesson in actual["lessons"]:
        for relative in lesson["implementation_sources"] + [lesson["test"]]:
            assert (ROOT / relative).is_file(), relative
        assert set(lesson["question"]) == {"en", "ko"}
        assert set(lesson["objectives"]) == {"en", "ko"}
        for template in lesson["concept_chapters"]:
            for language in ("en", "ko"):
                assert (ROOT / template.format(language=language)).is_file()


def test_scoped_production_selects_only_changed_lesson_or_concept_consumers():
    spec = importlib.util.spec_from_file_location("book_plan", ROOT / "scripts/book_plan.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    narrow = module.make_plan("scoped", ["core-fr3-02"], [])
    assert {row["id"] for row in narrow["tasks"]} == {
        "lesson-core-fr3-02",
        "review-lesson-core-fr3-02",
        "integrated-qa",
    }
    topics = json.loads((ROOT / "curriculum/book-topics.json").read_text())
    shared = module.make_plan("shared", [], ["kinematics"])
    selected = {row["id"][7:] for row in shared["tasks"] if row["id"].startswith("lesson-")}
    expected = {
        identifier
        for identifier, row in topics.items()
        if row[0] == "kinematics"
        or any(
            "concepts/kinematics.md"
            in (ROOT / f"docs/{language}/lessons/{identifier}.md").read_text()
            for language in ("en", "ko")
        )
    }
    assert selected == expected
