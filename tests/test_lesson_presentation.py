"""Guided results tie a learner's saved question to measured run evidence."""

import json
from pathlib import Path

import numpy as np
import pytest

from pai_lab.catalog import resolve_lesson
from pai_lab.cli import main
from pai_lab.lessons.presentation import _first_opposite_peak, present
from pai_lab.lessons.runner import run_lesson
from pai_lab.progress import load_progress
from pai_lab.readiness import gaps
from pai_lab.session import resume


@pytest.fixture
def state(tmp_path, monkeypatch):
    root = tmp_path / "learner"
    monkeypatch.setenv("PAL_LOCAL_DIR", str(root))
    return root


@pytest.fixture
def pendulums(tmp_path, state):
    missing = gaps(resolve_lesson("core-01"), prerequisites=False)
    if missing:
        pytest.skip("; ".join(missing))
    paths = [tmp_path / "low", tmp_path / "high"]
    for path, angle in zip(paths, (0.35, 0.70), strict=True):
        run_lesson("core-01", output_dir=path, parameters={"initial_angle_rad": angle})
    return paths


def test_pendulum_results_and_comprehension_resume(pendulums, capsys):
    low, high = pendulums
    baseline = ("core-01", "--run-dir", str(low))
    pair = (*baseline, "--comparison-run-dir", str(high))
    assert main(["lesson", "present", *pair, "--language", "ko", "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "awaiting_comprehension"
    page = Path(result["page"]).read_text()
    assert result["question"] in page
    assert result["question"].startswith("그래프의 0선 아래에서")
    assert 'id="play" type="button">재생</button>' in page
    assert 'id="seek" type="range" min="0" max="65" value="0"' in page
    assert page.count('id="jump" type="button">0.85초</button>') == 1
    assert "<table>" not in page
    replay = json.loads(page.split("const recording = ", 1)[1].split(";\n", 1)[0])
    assert replay["time"][43] == pytest.approx(0.85)
    assert "const interpolatedIndex = 43;" in page
    assert Path(result["images"][0]).read_bytes().startswith(b"\x89PNG")
    assert load_progress().completed == {}

    measurements = result["measurements"]
    assert measurements["observation_time_s"] == pytest.approx(1.28)
    times = []
    cases = zip((0.35, 0.70), pendulums, measurements["cases"], strict=True)
    for index, (angle, run, case) in enumerate(cases):
        with np.load(run / "replay.npz", allow_pickle=False) as state:
            times.append(state["time_s"])
            assert case["initial_angle_rad"] == angle
            peak = np.argmin(state["qpos"][:, 0])
            assert case["opposite_peak_rad"] == state["qpos"][peak, 0]
            assert case["opposite_peak_time_s"] == state["time_s"][peak]
            assert replay["angles"][index][43] == pytest.approx(state["qpos"][42:44, 0].mean())
    np.testing.assert_array_equal(*times)

    assert main(["course", "next", "--json"]) == 2
    assert json.loads(capsys.readouterr().out)["reason"] == "awaiting_comprehension"
    session_path = low.parent / "learner/session.json"
    original = session_path.read_text()
    altered = json.loads(original)
    altered["presentation"]["page_url"] = (low / "plot.png").as_uri()
    session_path.write_text(json.dumps(altered))
    assert not resume()["resume_available"]
    session_path.write_text(original)
    assert main(["course", "pause", "--json"]) == 0
    assert main(["course", "resume", "--json"]) == 0
    assert resume()["saved_state"]["presentation"] == {
        key: value for key, value in result.items() if key != "status"
    }
    assert main(["lesson", "finish", *baseline, "--json"]) == 2
    assert load_progress().completed == {}
    assert (
        main(
            [
                "lesson",
                "review",
                *pair,
                "--notes",
                "The learner identified the release angle and both minima.",
            ]
        )
        == 0
    )
    assert resume()["resume_phase"] == "awaiting_comprehension"
    assert main(["lesson", "finish", *baseline, "--json"]) == 0
    assert "core-01" in load_progress().completed
    assert resume()["resume_phase"] == "finished"
    capsys.readouterr()
    core_02_gaps = gaps(resolve_lesson("core-02"), prerequisites=False)
    next_status = main(["course", "next", "--json"])
    next_result = json.loads(capsys.readouterr().out)
    if core_02_gaps:
        assert next_status == 2
        assert next_result["reason"] == "no-eligible-lesson"
    else:
        assert next_status == 0
        assert next_result["id"] == "core-02"


def test_pendulum_peak_shortcut_uses_first_complete_opposite_swing():
    angles = np.array([0.4, 0.1, -0.2, -0.4, -0.2, 0.1, 0.4, 0.0, -0.5, -0.1])
    assert _first_opposite_peak(angles) == 3
    assert _first_opposite_peak(-angles) == 3
    assert _first_opposite_peak(angles[:4]) is None


def test_corrupt_evidence_and_wrong_comparison_cannot_be_presented(state, pendulums, tmp_path):
    low, high = pendulums
    wrong = tmp_path / "timestep"
    run_lesson("core-01", output_dir=wrong, variant=2)
    with pytest.raises(ValueError, match="only the initial angle"):
        present("core-01", low, wrong, "en")
    (high / "replay.npz").write_bytes(b"corrupt evidence")
    with pytest.raises(ValueError, match="checksum mismatch"):
        present("core-01", low, high, "en")
    assert not (state / "presentations").exists()


def test_core_02_03_04_results(pendulums, tmp_path):
    missing = gaps(resolve_lesson("core-03"), prerequisites=False)
    if missing:
        pytest.skip("; ".join(missing))
    sources, inventory, first, second = (
        tmp_path / name for name in ("sources", "models", "a", "b")
    )

    def finish(lesson, baseline, comparison=None):
        args = [lesson, "--run-dir", str(baseline)]
        compare = ["--comparison-run-dir", str(comparison)] if comparison else []
        assert main(["lesson", "present", *args, *compare]) == 0
        assert (
            main(["lesson", "review", *args, *compare, "--notes", "Learner requested completion."])
            == 0
        )
        assert main(["lesson", "finish", *args]) == 0

    finish("core-01", *pendulums)
    run_lesson("core-02", output_dir=sources)
    hashes = present("core-02", sources, None, "en")["measurements"]
    assert hashes["original_sha256"] != hashes["changed_sha256"]
    finish("core-02", sources)
    run_lesson("core-03", output_dir=inventory)
    models = present("core-03", inventory, None, "ko")["measurements"]
    assert models["g1"] == {"nq": 36, "nv": 35, "nu": 29}
    finish("core-03", inventory)
    for path, azimuth in zip((first, second), (135, 165), strict=True):
        run_lesson("core-04", output_dir=path, parameters={"camera_azimuth": azimuth})

    views = present("core-04", first, second, "en")
    assert views["measurements"] == {"camera_azimuth_deg": [135, 165], "same_saved_pose": True}
    assert len(views["images"]) == 2
    assert Path(views["images"][0]).read_bytes() != Path(views["images"][1]).read_bytes()
    finish("core-04", first, second)
