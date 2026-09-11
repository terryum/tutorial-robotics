"""Regression tests for irreversible-looking learner-state mistakes."""

import json

import pytest

from pai_lab.cli import main
from pai_lab.local import local_root
from pai_lab.progress import load_progress


@pytest.fixture
def session(tmp_path, monkeypatch):
    monkeypatch.setenv("PAL_LOCAL_DIR", str(tmp_path / "learner"))
    return local_root()


def run_t00(path, seed=7):
    assert (
        main(["lesson", "run", "T00", "--output-dir", str(path), "--seed", str(seed), "--json"])
        == 0
    )


def review_t00(baseline, comparison):
    return main(
        [
            "lesson",
            "review",
            "T00",
            "--run-dir",
            str(baseline),
            "--comparison-run-dir",
            str(comparison),
            "--notes",
            "Host package capabilities are invariant under seed; inspected the actual host report.",
            "--json",
        ]
    )


def test_host_detection_does_not_initialize_state(session):
    assert main(["host", "detect", "--json"]) == 0
    assert not session.exists()


def test_init_preserves_legacy_completion(session):
    session.mkdir()
    original = {
        "through": "core",
        "completed": {"core-00": {"verification": "ci-checked", "run_dir": "legacy"}},
    }
    (session / "progress.json").write_text(json.dumps(original))
    assert main(["course", "init", "--through", "sim", "--json"]) == 0
    assert load_progress().completed == original["completed"]


def test_run_review_feedback_finish_and_reinit(session, tmp_path):
    baseline, comparison = tmp_path / "baseline", tmp_path / "comparison"
    run_t00(baseline)
    assert load_progress().completed == {}
    assert main(["lesson", "finish", "T00", "--run-dir", str(baseline), "--json"]) == 2
    run_t00(comparison, seed=8)
    assert review_t00(baseline, comparison) == 0
    assert main(["feedback", "add", "[개선점] 지금 바로 호스트 수치를 설명해줘", "--json"]) == 0
    feedback = json.loads((session / "feedback.json").read_text())[0]
    assert feedback["lesson"] == "core-00"
    assert feedback["urgency"] == "immediate"
    assert main(["lesson", "finish", "T00", "--run-dir", str(baseline), "--json"]) == 2
    assert (
        main(
            [
                "feedback",
                "resolve",
                feedback["id"],
                "--evidence",
                "Explained each measured capability; verified both runs.",
                "--json",
            ]
        )
        == 0
    )
    assert main(["lesson", "finish", "T00", "--run-dir", str(baseline), "--json"]) == 0
    complete = load_progress().completed.copy()
    assert main(["course", "init", "--json"]) == 0
    assert load_progress().completed == complete
    assert main(["feedback", "add", "After-lesson feedback", "--json"]) == 0
    assert json.loads((session / "feedback.json").read_text())[-1]["lesson"] == "core-00"
    # Existing evidence is preserved on accidental directory reuse.
    before = (baseline / "run.json").read_bytes()
    assert main(["lesson", "run", "T00", "--output-dir", str(baseline), "--json"]) != 0
    assert (baseline / "run.json").read_bytes() == before


@pytest.mark.parametrize("mutation", ["missing", "numeric", "identity", "blank_image"])
def test_corrupt_artifacts_never_finish(session, tmp_path, mutation):
    baseline, comparison = tmp_path / "baseline", tmp_path / "comparison"
    run_t00(baseline)
    run_t00(comparison, seed=8)
    assert review_t00(baseline, comparison) == 0
    if mutation == "missing":
        (baseline / "host-audit.json").unlink()
    elif mutation == "numeric":
        (baseline / "trace.csv").write_text("time_s,reference,observed\n0,1,nan\n")
    elif mutation == "identity":
        summary = json.loads((baseline / "summary.json").read_text())
        summary["lesson_id"] = "core-01"
        (baseline / "summary.json").write_text(json.dumps(summary))
    else:
        from PIL import Image

        Image.new("RGB", (480, 360)).save(baseline / "plot.png")
    assert main(["lesson", "check", "T00", "--run-dir", str(baseline), "--json"]) == 1
    assert main(["lesson", "finish", "T00", "--run-dir", str(baseline), "--json"]) == 2
    assert load_progress().completed == {}


def test_comparison_rejects_two_variables_and_same_run(session, tmp_path):
    baseline, comparison = tmp_path / "baseline", tmp_path / "comparison"
    run_t00(baseline)
    assert review_t00(baseline, baseline) == 2
    assert (
        main(
            [
                "lesson",
                "run",
                "T00",
                "--output-dir",
                str(comparison),
                "--seed",
                "8",
                "--samples",
                "96",
                "--json",
            ]
        )
        == 0
    )
    assert review_t00(baseline, comparison) == 2


def test_model_or_prerequisite_gap_never_completes(session, tmp_path):
    assert (
        main(["lesson", "run", "core-fr3-04", "--output-dir", str(tmp_path / "blocked"), "--json"])
        == 2
    )
    assert not (tmp_path / "blocked").exists()
    assert load_progress().completed == {}


def test_concurrent_feedback_is_not_lost(session):
    from concurrent.futures import ThreadPoolExecutor

    from pai_lab.feedback import add, items

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda i: add(f"feedback {i}", "T00"), range(20)))
    assert len(items()) == 20
    assert {item["id"] for item in items()} == {item["id"] for item in results}


def test_bootstrap_plan_without_python_or_uv_is_read_only(session):
    import os
    import subprocess

    from pai_lab.catalog import ROOT

    environment = {**os.environ, "PATH": "/usr/bin:/bin"}
    result = subprocess.run(
        ["/bin/sh", str(ROOT / "bootstrap.sh"), "--plan"],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Environment:" in result.stdout
    assert "uv: missing" in result.stdout
    assert not session.exists()
