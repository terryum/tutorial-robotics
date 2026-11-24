"""Build a standalone results page from verified lesson evidence."""

from __future__ import annotations

import base64
import json
from hashlib import sha256
from html import escape
from pathlib import Path
from typing import Any
from uuid import uuid4

import numpy as np

from pai_lab.catalog import resolve_lesson
from pai_lab.lessons.evidence import comparison_errors, validate_run
from pai_lab.lessons.observation import compare_runs, inspect_run
from pai_lab.local import local_root

QUESTIONS = {
    "core-01": (
        (
            "Below the zero line, which curve reaches a lower minimum? "
            "What do you see in the replay that shows its pendulum rose higher on the opposite side?"
        ),
        (
            "그래프의 0선 아래에서 어느 곡선의 최솟값이 더 낮나요? "
            "그 곡선에 해당하는 진자가 반대편에서 더 높이 올라갔다는 것을 재생 화면에서 어떻게 알 수 있나요?"
        ),
    ),
    "core-02": (
        "Which byte changed, and what happened to the SHA-256 digest?",
        "어느 바이트를 바꿨고, SHA-256 해시는 어떻게 달라졌나요?",
    ),
    "core-03": (
        "Which model has different nq and nv counts, and what does each count represent?",
        "어느 모델에서 nq와 nv가 다르고, 각 수는 무엇을 세나요?",
    ),
    "core-04": (
        "Which camera input changed, and what in the saved state shows the FR3 pose stayed fixed?",
        "카메라 입력 중 어떤 값을 바꿨고, 저장된 상태에서 FR3 자세가 같다는 것을 어떻게 확인할 수 있나요?",
    ),
}
GENERIC_QUESTION = (
    "What did you change, and which measurement supports your explanation?",
    "무엇을 바꿨고, 어떤 측정값이 설명을 뒷받침하나요?",
)


def _artifact(run: Path, name: str) -> Path:
    path = run / name
    hashes = json.loads((run / "run.json").read_text())["artifacts"]
    if (
        not path.resolve().is_relative_to(run.resolve())
        or name not in hashes
        or sha256(path.read_bytes()).hexdigest() != hashes[name]
    ):
        raise ValueError(f"missing or invalid presentation evidence: {name}")
    return path


def _data(run: Path, name: str = "experiment.json") -> dict[str, Any]:
    value = json.loads(_artifact(run, name).read_text())
    if not isinstance(value, dict):
        raise TypeError(f"expected an object in {name}")
    return value


def _state(run: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    with np.load(_artifact(run, "replay.npz"), allow_pickle=False) as saved:
        return saved["time_s"], saved["qpos"], saved["qvel"]


def _first_opposite_peak(angles: np.ndarray) -> int | None:
    signed = angles * np.sign(angles[0])
    previous, current, following = signed[:-2], signed[1:-1], signed[2:]
    turning_points = np.flatnonzero((current < 0) & (previous > current) & (current <= following))
    return int(turning_points[0] + 1) if turning_points.size else None


def _pendulums(a: Path, b: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    ae, be = _data(a), _data(b)
    ap, bp = ae["payload"], be["payload"]
    angle = "initial_angle_rad"
    fixed = ("dt_s", "gravity_m_s2", "initial_angular_velocity_rad_s", "observation_time_s")
    a_params, b_params = ae["parameters"], be["parameters"]
    if (
        a_params[angle] == b_params[angle]
        or ae["variant"] != be["variant"]
        or any(
            a_params.get(k) != b_params.get(k)
            for k in (a_params.keys() | b_params.keys()) - {angle}
        )
        or any(ap[k] != bp[k] for k in (*fixed, "pivot_position_m"))
        or _artifact(a, "replay.mjb").read_bytes() != _artifact(b, "replay.mjb").read_bytes()
    ):
        raise ValueError("pendulum presentation requires changing only the initial angle")
    at, aq, _ = _state(a)
    bt, bq, _ = _state(b)
    if not np.array_equal(at, bt):
        raise ValueError("pendulum presentation requires matching recorded times")
    cases = []
    peaks = []
    for payload, positions in ((ap, aq), (bp, bq)):
        angles = positions[:, 0]
        opposite = _first_opposite_peak(angles)
        peaks.append(opposite)
        observed = opposite is not None
        cases.append(
            {
                "initial_angle_rad": float(angles[0]),
                "opposite_peak_rad": float(angles[opposite]) if observed else None,
                "opposite_peak_time_s": float(at[opposite]) if observed else None,
                "opposite_tip_z_m": payload["tip_positions_m"][opposite][2] if observed else None,
            }
        )
    return (
        {"cases": cases, **{k: ap[k] for k in fixed}},
        {
            "time": at.tolist(),
            "angles": [aq[:, 0].tolist(), bq[:, 0].tolist()],
            "tips": [ap["tip_positions_m"], bp["tip_positions_m"]],
            "pivot": ap["pivot_position_m"],
            "peaks": peaks,
        },
    )


def _angle_plot(path: Path, replay: dict[str, Any], measurements: dict[str, Any]) -> None:
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    figure = Figure(figsize=(8, 3.3), layout="constrained")
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    for angles, case, color in zip(
        replay["angles"], measurements["cases"], ("#175aa8", "#ac5225"), strict=True
    ):
        axis.plot(replay["time"], angles, color=color, label=f"{angles[0]:.2f} rad")
        if case["opposite_peak_rad"] is not None:
            axis.scatter(case["opposite_peak_time_s"], case["opposite_peak_rad"], color=color)
    axis.axhline(0, color="#68778b", linewidth=0.8)
    axis.set(xlabel="Time (s)", ylabel="qpos[0] (rad)")
    axis.grid(alpha=0.2)
    axis.legend(title="Release angle")
    figure.savefig(path, dpi=130)


def _image(path: Path, caption: str) -> str:
    png = base64.b64encode(path.read_bytes()).decode("ascii")
    label = escape(caption)
    return (
        f'<figure><img src="data:image/png;base64,{png}" alt="{label}">'
        f"<figcaption>{label}</figcaption></figure>"
    )


def _table(headers: tuple[str, ...], rows: list[tuple[object, ...]]) -> str:
    heading = "".join(f"<th>{escape(header)}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(str(value))}</td>" for value in row) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{heading}</tr></thead><tbody>{body}</tbody></table>"


def _comparison_frame(replay: dict[str, Any]) -> tuple[dict[str, Any], int | None, bool]:
    first, second = replay["peaks"]
    if first is None or second is None:
        return replay, None, False

    left, half_step = divmod(first + second, 2)
    if not half_step:
        return replay, left, False

    position = left + 1
    timeline = {}
    for key in ("time", "angles", "tips"):
        values = np.asarray(replay[key])
        axis = 0 if key == "time" else 1
        interpolated = (values.take(left, axis=axis) + values.take(position, axis=axis)) / 2
        timeline[key] = np.insert(values, position, interpolated, axis=axis).tolist()
    return {**replay, **timeline}, position, True


def _replay_markup(replay: dict[str, Any], ko: bool) -> str:
    replay, comparison_index, interpolated = _comparison_frame(replay)
    play, pause, time_label = (
        ("재생", "일시 정지", "관측 시각") if ko else ("Play", "Pause", "Recorded time")
    )
    frames = "".join(
        f'<figure><canvas id="pendulum-{index}" width="360" height="236" aria-label="{angles[0]:.2f} rad"></canvas>'
        f'<figcaption>{angles[0]:.2f} rad · <output id="angle-{index}"></output></figcaption></figure>'
        for index, angles in enumerate(replay["angles"])
    )
    shortcut = ""
    if comparison_index is not None:
        time = f"{replay['time'][comparison_index]:.3f}".rstrip("0").rstrip(".")
        time_text = f"{time}초" if ko else f"{time} s"
        shortcut = f'<button id="jump" type="button">{time_text}</button>'
    interpolated_label = " (보간)" if ko else " (interpolated)"
    return f"""
<div class="pair">{frames}</div>
<div class="controls">
<button id="play" type="button">{play}</button>
<label for="seek">{time_label}</label>
<input id="seek" type="range" min="0" max="{len(replay["time"]) - 1}" value="0">
<output id="time"></output>
{shortcut}
</div>
<script>
const recording = {json.dumps(replay, allow_nan=False)};
const seek = document.getElementById("seek");
const button = document.getElementById("play");
const comparisonIndex = {json.dumps(comparison_index)};
const interpolatedIndex = {json.dumps(comparison_index if interpolated else None)};
const interpolatedLabel = {json.dumps(interpolated_label)};
const colors = ["#175aa8", "#ac5225"];
const t = recording.time;
const pivot = recording.pivot;
const radius = Math.max(...recording.tips.map(tips =>
    Math.hypot(tips[0][0] - pivot[0], tips[0][2] - pivot[2])));
let playing = false;

function draw(index) {{
    seek.value = index;
    document.getElementById("time").value = t[index].toFixed(3) + " s" +
        (index === interpolatedIndex ? interpolatedLabel : "");
    recording.tips.forEach((tips, side) => {{
        const canvas = document.getElementById("pendulum-" + side);
        const ctx = canvas.getContext("2d");
        const scale = 160 / radius;
        const x = 180 + (tips[index][0] - pivot[0]) * scale;
        const y = 40 - (tips[index][2] - pivot[2]) * scale;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#c2cbd8";
        ctx.beginPath(); ctx.moveTo(180, 40); ctx.lineTo(180, 216); ctx.stroke();
        ctx.lineWidth = 5;
        ctx.strokeStyle = colors[side];
        ctx.beginPath(); ctx.moveTo(180, 40); ctx.lineTo(x, y); ctx.stroke();
        ctx.fillStyle = colors[side];
        ctx.beginPath(); ctx.arc(x, y, 12, 0, 2 * Math.PI); ctx.fill();
        ctx.fillStyle = "#17273c";
        ctx.beginPath(); ctx.arc(180, 40, 6, 0, 2 * Math.PI); ctx.fill();
        document.getElementById("angle-" + side).value =
            recording.angles[side][index].toFixed(3) + " rad";
    }});
}}
let playback;
function stop() {{
    playing = false;
    cancelAnimationFrame(playback);
    button.textContent = {json.dumps(play)};
}}
function jumpTo(index) {{ stop(); draw(index); }}
seek.addEventListener("input", () => jumpTo(Number(seek.value)));
document.getElementById("jump")?.addEventListener("click", () => jumpTo(comparisonIndex));
button.addEventListener("click", () => {{
    if (playing) {{ stop(); return; }}
    let index = Number(seek.value);
    if (index === t.length - 1) index = 0;
    draw(index);
    const start = performance.now() - 1000 * t[index];
    playing = true;
    button.textContent = {json.dumps(pause)};
    function tick(now) {{
        while (index + 1 < t.length && t[index + 1] <= (now - start) / 1000) index++;
        draw(index);
        if (index === t.length - 1) stop();
        else playback = requestAnimationFrame(tick);
    }}
    playback = requestAnimationFrame(tick);
}});
draw(0);
document.documentElement.dataset.replayReady = "true";
</script>
"""


def present(
    identifier: str,
    baseline: Path,
    comparison: Path | None,
    language: str,
) -> dict[str, Any]:
    lesson = resolve_lesson(identifier)
    identifier = lesson.id
    if comparison is None and identifier in {"core-01", "core-04"}:
        raise ValueError("this results page needs baseline and comparison runs")
    errors = (
        comparison_errors(identifier, baseline, comparison)
        if comparison is not None
        else validate_run(identifier, baseline)
    )
    if errors:
        raise ValueError("; ".join(errors))

    ko = language == "ko"
    question = QUESTIONS.get(identifier, GENERIC_QUESTION)[ko]
    title = f"{identifier} · " + ("실험 결과" if ko else "Lesson results")
    picture_paths: list[tuple[Path, str]] = []
    replay = None
    details = ""
    if identifier == "core-01" and comparison is not None:
        measurements, replay = _pendulums(baseline, comparison)
    elif identifier == "core-02":
        measurements = _data(baseline, "source-pins.json")["hash_comparison"]
        details = f"<p><code>{escape(measurements['path'])}</code></p>" + _table(
            ("기록", "바이트 위치", "바이트 값", "SHA-256")
            if ko
            else ("Record", "Byte offset", "Byte value", "SHA-256"),
            [
                (
                    label,
                    measurements["byte_offset"],
                    measurements[f"{key}_byte"],
                    measurements[f"{key}_sha256"],
                )
                for key, label in zip(
                    ("original", "changed"),
                    ("원본", "복사본") if ko else ("Original", "Copy"),
                    strict=True,
                )
            ],
        )
        picture_paths.append(
            (_artifact(baseline, "plot.png"), "소스 검사" if ko else "Source checks")
        )
    elif identifier == "core-03":
        inventory = _data(baseline, "model-inventory.json")
        measurements = {
            name: {key: model[key] for key in ("nq", "nv", "nu")}
            for name, model in inventory.items()
            if "nq" in model
        }
        if not measurements:
            raise ValueError("model inventory contains no measured dimensions")
        details = _table(
            ("모델" if ko else "Model", "nq", "nv", "nu"),
            [
                (name, counts["nq"], counts["nv"], counts["nu"])
                for name, counts in measurements.items()
            ],
        )
        picture_paths.append(
            (_artifact(baseline, "frame.png"), "모델 렌더링" if ko else "Model rendering")
        )
    elif identifier == "core-04" and comparison is not None:
        a, b = _data(baseline), _data(comparison)
        angles = [run["parameters"]["camera_azimuth"] for run in (a, b)]
        if (
            angles[0] == angles[1]
            or a["variant"] != b["variant"]
            or not all(
                np.array_equal(x, y)
                for x, y in zip(_state(baseline), _state(comparison), strict=True)
            )
            or _artifact(baseline, "replay.mjb").read_bytes()
            != _artifact(comparison, "replay.mjb").read_bytes()
        ):
            raise ValueError("camera presentation requires the same saved FR3 model and pose")
        measurements = {"camera_azimuth_deg": angles, "same_saved_pose": True}
        details = (
            "<p>"
            + (
                "<code>qpos</code>와 <code>qvel</code>이 두 기록에서 같습니다."
                if ko
                else "The recorded <code>qpos</code> and <code>qvel</code> match."
            )
            + "</p>"
        )
        for run, angle in zip((baseline, comparison), angles, strict=True):
            picture_paths.append((_artifact(run, "frame.png"), f"{angle:g}°"))
    else:
        measured_runs = [baseline, comparison] if comparison is not None else [baseline]
        observations = [inspect_run(identifier, run) for run in measured_runs]
        measurements = dict(zip(("baseline", "comparison"), observations))
        details = _table(
            ("측정 항목", "측정값", "단위") if ko else ("Metric", "Value", "Unit"),
            [(item["metric"], item["value"], item["units"]) for item in observations],
        )
        for run, label in zip(
            measured_runs, ("기준", "비교") if ko else ("Baseline", "Comparison")
        ):
            picture_paths.append((_artifact(run, "plot.png"), label))
            if "frame.png" in json.loads((run / "run.json").read_text())["artifacts"]:
                picture_paths.append((_artifact(run, "frame.png"), label))
    output = local_root() / "presentations" / identifier / uuid4().hex
    output.mkdir(parents=True)
    if replay is not None:
        image = output / "angle-comparison.png"
        _angle_plot(image, replay, measurements)
        picture_paths.append((image, "시간에 따른 각도" if ko else "Recorded angle over time"))
    elif comparison is not None and identifier != "core-04":
        compare_runs(identifier, baseline, comparison, output / "comparison")
        picture_paths.append(
            (output / "comparison" / "comparison.png", "비교 그래프" if ko else "Comparison plot")
        )
    page = output / "index.html"
    page.write_text(
        f"""<!doctype html>
<html lang="{language}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script>
try {{
    const savedMode = localStorage.getItem("tutorial-robotics-results-color-mode");
    if (savedMode === "light" || savedMode === "dark") {{
        document.documentElement.dataset.colorMode = savedMode;
    }}
}} catch {{ /* File URLs may not have persistent storage. */ }}
</script>
<style>
:root {{ color-scheme: light dark; }}
:root[data-color-mode="light"] {{ color-scheme: light; }}
:root[data-color-mode="dark"] {{ color-scheme: dark; }}
body {{ margin: 32px auto; padding: 0 16px; max-width: 1000px; color: #17273c;
       color: light-dark(#17273c, #e1e9f3); background: #fafbfc;
       background: light-dark(#fafbfc, #15202d); font: 17px/1.55 system-ui, sans-serif; }}
header {{ display: flex; align-items: baseline; gap: 12px; justify-content: space-between; }}
h1 {{ font-size: 1.8rem; margin: 0 0 .2em; }}
.appearance {{ margin-inline-start: auto; text-align: end; font-size: .9em; white-space: nowrap; }}
.appearance select {{ font: inherit; border-radius: .25rem; padding: .2em; }}
figure {{ margin: 0; min-width: 0; }}
img, canvas {{ width: 100%; height: auto; display: block; background: white; border-radius: 8px; }}
figcaption {{ margin: .4em 0 1em; text-align: center; }}
.pair {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }}
.controls {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 18px; }}
input {{ flex: 1; min-width: 100px; }}
button {{ font: inherit; padding: .2em .7em; }}
table {{ width: 100%; border-collapse: collapse; background: white;
        background: light-dark(white, #1d2a39); }}
th, td {{ padding: .45em; text-align: left; border: 1px solid #ccd5e0;
         border-color: light-dark(#ccd5e0, #475b71); overflow-wrap: anywhere; }}
@media (max-width: 540px) {{ body {{ font-size: 14px; }} }}
</style>
</head>
<body>
<header>
<h1>{title}</h1>
<div class="appearance" hidden>
<label for="color-mode">{"테마" if ko else "Theme"}</label>
<select id="color-mode">
<option value="auto">{"시스템 설정" if ko else "System"}</option>
<option value="light">{"라이트" if ko else "Light"}</option>
<option value="dark">{"다크" if ko else "Dark"}</option>
</select>
</div>
</header>
<script>
{{
    const mode = document.getElementById("color-mode");
    const root = document.documentElement;
    mode.value = root.dataset.colorMode || "auto";
    mode.addEventListener("change", () => {{
        root.dataset.colorMode = mode.value;
        try {{
            localStorage.setItem("tutorial-robotics-results-color-mode", mode.value);
        }} catch {{ /* The current page can still apply the choice. */ }}
    }});
    mode.parentElement.hidden = false;
}}
</script>
<p>{escape(lesson.title_ko if ko else lesson.title)}</p>
{_replay_markup(replay, ko) if replay else ""}
<div class="{"pair" if identifier == "core-04" else ""}">
{"".join(_image(path, label) for path, label in picture_paths)}
</div>
{details}
<h2>{"이해 확인" if ko else "Check your understanding"}</h2>
<p>{escape(question)}</p>
</body>
</html>
""",
        encoding="utf-8",
    )
    return {
        "lesson": identifier,
        "page": str(page),
        "page_url": page.as_uri(),
        "title": title,
        "page_sha256": sha256(page.read_bytes()).hexdigest(),
        "images": [str(path.resolve()) for path, _ in picture_paths],
        "measurements": measurements,
        "question": question,
        "language": language,
    }
