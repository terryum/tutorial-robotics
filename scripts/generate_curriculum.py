"""Generate mirrored lesson pages, thin entry points, tests, and indexes.

The JSON catalog is authoritative. Generated files are committed so GitHub can
render and review them without running this script.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any

from pai_lab.lessons.runner import LESSON_SPECS

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "curriculum" / "catalog.json").read_text(encoding="utf-8"))
LESSONS: list[dict[str, Any]] = CATALOG["lessons"]


def _csv(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) or "None"


def _next(lesson: dict[str, Any]) -> str:
    index = LESSONS.index(lesson) + 1
    if index == len(LESSONS):
        return "Course complete"
    following = LESSONS[index]
    return f"[{following['id']}](./{following['id']}.md) — {following['title']}"


def _page(lesson: dict[str, Any], language: str) -> str:
    is_ko = language == "ko"
    title = lesson["title_ko"] if is_ko else lesson["title"]
    aliases = _csv(lesson["aliases"])
    prerequisites = _csv(lesson["prerequisites"])
    capabilities = _csv(lesson["capabilities"])
    platforms = _csv(lesson["platforms"])
    safety = lesson["safety_level"]
    verification = lesson["verification"]
    implementation = lesson["implementation"]
    spec = LESSON_SPECS.get(lesson["id"])
    operation = spec.operation if spec else "reader-hardware-gate"
    artifact = spec.artifact if spec else "no run artifact until the gate is implemented"
    metric = spec.metric if spec else "not applicable"
    profile = (
        "runtime-offline"
        if lesson["id"] == "hw-common-01"
        else "isaac"
        if "isaac-sim" in lesson["capabilities"]
        else "gpu"
        if "nvidia-cuda" in lesson["capabilities"]
        else "ros"
        if "ros2-jazzy" in lesson["capabilities"]
        else "hardware"
        if lesson["stage"] == "hardware"
        else "core"
    )
    warning = (
        "이 entrypoint는 명령을 전송하지 않는 offline/read-only 계약만 실행합니다. 실제 motion에는 새로운 실행 카드와 명시적 승인이 필요합니다."
        if is_ko and lesson["stage"] == "hardware"
        else "This entry point only exercises an offline/read-only contract. Real motion requires a fresh run card and explicit approval."
        if lesson["stage"] == "hardware"
        else "이 수업은 실제 하드웨어 명령을 전송하지 않습니다."
        if is_ko
        else "This lesson never emits a hardware command."
    )
    if is_ko:
        intro = f"이 수업은 **{title}**을 `{operation}` 구현과 `{artifact}` artifact로 검사합니다."
        goals = (
            "- capability와 선행 수업을 실행 전에 확인합니다.\n"
            f"- `{operation}`이 만든 `{artifact}`를 직접 검사합니다.\n"
            "- 외부 GPU, ROS 2 또는 실제 장비 검증이 필요한 범위를 badge와 분리합니다."
        )
        expected = (
            f"`{implementation}` 수업은 exit code `0`과 함께 `{artifact}`, `summary.json`, "
            "`trace.csv`, `lesson-report.md`를 생성합니다. scaffolded 수업은 exit code `2`와 "
            "`reader_test_required`를 반환하며 실행 artifact를 만들지 않습니다."
        )
        recovery = (
            f"먼저 `pal lesson check {lesson['id']} --json`을 실행합니다. capability가 없으면 "
            f"`pal setup verify --profile {profile} --json`의 missing 목록을 따르고, 시스템 패키지나 firmware는 자동 설치하지 않습니다."
        )
        explanation = (
            f"runner는 catalog ID를 고유한 `{operation}`에 dispatch하고 `{metric}`을 계산합니다. "
            f"검사는 범용 성공 신호가 아니라 `{artifact}`의 수업별 schema와 SHA-256을 사용합니다. "
            "외부 runtime capability가 필요한 수업은 실제 host probe 없이 완료로 표시되지 않습니다."
        )
        try_it = (
            f"`pal lesson run {lesson['id']} --headless --seed 8 --samples 96`로 seed와 표본 수를 바꿉니다. "
            "새 artifact의 digest와 `changed_metric_value`가 달라지되 schema는 같아야 합니다."
        )
        checkpoint = (
            "`pal lesson check`는 양언어 heading, canonical 명령, entrypoint와 lesson별 test를 검사합니다. "
            f"출판 badge는 `{verification}`이며 local 완료 여부와 독립적입니다."
        )
        next_text = "과정의 다음 catalog 항목: " + _next(lesson)
    else:
        intro = f"This lesson checks **{title}** through the `{operation}` implementation and its `{artifact}` artifact."
        goals = (
            "- Check capabilities and prerequisites before execution.\n"
            f"- Inspect the `{artifact}` produced by `{operation}`.\n"
            "- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge."
        )
        expected = (
            f"An `implemented` lesson exits `0` and creates `{artifact}`, `summary.json`, `trace.csv`, "
            "and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and "
            "does not create a run artifact."
        )
        recovery = (
            f"Run `pal lesson check {lesson['id']} --json` first. If a capability is unavailable, follow "
            f"the missing list from `pal setup verify --profile {profile} --json`; do not auto-install system packages or firmware."
        )
        explanation = (
            f"The runner dispatches this catalog ID to the unique `{operation}` operation and computes "
            f"`{metric}`. Verification uses the lesson-specific `{artifact}` schema and SHA-256, not a "
            "generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe."
        )
        try_it = (
            f"Run `pal lesson run {lesson['id']} --headless --seed 8 --samples 96`. "
            "The digest and `changed_metric_value` should change while the artifact schema stays fixed."
        )
        checkpoint = (
            "`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. "
            f"The publication badge is `{verification}` and is independent of local completion."
        )
        next_text = "Next catalog item: " + _next(lesson)
    return f"""# {lesson['id']} — {title}

{intro}

| Field | Value |
|---|---|
| Stage / track | `{lesson['stage']}` / `{lesson['track']}` |
| Legacy alias | {aliases} |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | {platforms} |
| Capabilities | {capabilities} |
| Prerequisites | {prerequisites} |
| Safety | `{safety}` |
| Verification | `{verification}` |
| Implementation | `{implementation}` |

{warning}

## Learning goals

{goals}

## Preflight

```bash
pal host detect --json
pal setup verify --profile {profile} --json
pal lesson check {lesson['id']} --json
```

## Action

```bash
pal lesson run {lesson['id']} --headless --seed 7 --samples 64
```

The same thin entry point is available as `python {lesson['entrypoint']} --headless`.

## Expected

{expected}

## Recovery

{recovery}

## How it works

{explanation}

Source references: {_csv(lesson['source_refs'])}. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

{try_it}

## Checkpoint

{checkpoint}

Expected artifacts: {_csv(lesson['expected_artifacts'])}.

## Next lesson

{next_text}
"""


def _entrypoint(lesson_id: str) -> str:
    return f'''"""Thin entry point for {lesson_id}."""

from __future__ import annotations

import argparse
from pathlib import Path

from pai_lab.catalog import ROOT
from pai_lab.lessons import run_lesson


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--output-dir", type=Path, default=ROOT / ".local/runs/{lesson_id}/manual")
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()
    result = run_lesson(
        "{lesson_id}",
        output_dir=args.output_dir,
        seed=args.seed,
        samples=args.samples,
        headless=args.headless,
    )
    print(f"lesson={{result.lesson_id}} metric={{result.metric_value}} digest={{result.artifact_digest}}")


if __name__ == "__main__":
    main()
'''


def _test(lesson_id: str) -> str:
    scaffolded = lesson_id in {
        "hw-common-02",
        "hw-fr3-01",
        "hw-wuji-01",
        "hw-wuji-02",
        "hw-enlight-01",
        "hw-enlight-02",
        "hw-enlight-03",
        "hw-enlight-wuji-01",
    }
    if scaffolded:
        return f'''import pytest

from pai_lab.lessons import check_lesson, implementation_status, run_lesson


def test_{lesson_id.replace("-", "_")}_contract(tmp_path) -> None:
    assert implementation_status("{lesson_id}") == "scaffolded"
    with pytest.raises(NotImplementedError):
        run_lesson("{lesson_id}", output_dir=tmp_path, seed=7, samples=16)
    assert check_lesson("{lesson_id}") == []
'''
    return f'''from pai_lab.lessons import check_lesson, run_lesson


def test_{lesson_id.replace("-", "_")}_contract(tmp_path) -> None:
    result = run_lesson("{lesson_id}", output_dir=tmp_path, seed=7, samples=16)
    assert result.lesson_id == "{lesson_id}"
    assert result.metric_value >= 0.0
    assert {{path.name for path in tmp_path.iterdir()}} == set(result.artifacts)
    assert check_lesson("{lesson_id}") == []
'''


def _index(language: str) -> str:
    title = "수업 목록" if language == "ko" else "Lesson index"
    intro = (
        "Stage 안에서는 선행 수업과 capability로 다음 수업을 선택합니다. 장비 이름은 순서를 결정하지 않습니다."
        if language == "ko"
        else "Prerequisites and capabilities select the next lesson; machine names never define the order."
    )
    rows = [f"# {title}\n\n{intro}\n\n| # | Lesson | Stage | Track | Verification |\n|---:|---|---|---|---|"]
    for lesson in LESSONS:
        label = lesson["title_ko"] if language == "ko" else lesson["title"]
        rows.append(
            f"| {lesson['order']} | [{lesson['id']}](lessons/{lesson['id']}.md) — {label} | "
            f"`{lesson['stage']}` | `{lesson['track']}` | `{lesson['verification']}` |"
        )
    return "\n".join(rows) + "\n"


def _legacy_redirects() -> None:
    mapping_path = ROOT / "migration" / "tutorial-id-map.csv"
    if not mapping_path.is_file():
        return
    lookup = {alias: lesson for lesson in LESSONS for alias in lesson["aliases"]}
    with mapping_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    old_paths = {row["legacy_id"]: row["public_path"] for row in rows}
    new_rows: list[dict[str, str]] = []
    for alias, lesson in lookup.items():
        public_path = old_paths.get(alias, f"tutorials/legacy/{alias}.md")
        path = ROOT / public_path
        path.parent.mkdir(parents=True, exist_ok=True)
        relative_en = Path(os.path.relpath(ROOT / "docs/en/lessons" / f"{lesson['id']}.md", path.parent))
        relative_ko = Path(os.path.relpath(ROOT / "docs/ko/lessons" / f"{lesson['id']}.md", path.parent))
        lesson = lookup[alias]
        path.write_text(
            f"# {alias} moved to {lesson['id']}\n\n"
            f"This legacy ID remains valid in `pal` for v1.x. Continue with "
            f"[{lesson['id']} (English)]({relative_en}) or [한국어]({relative_ko}).\n\n"
            f"```bash\npal lesson run {alias} --headless\n```\n",
            encoding="utf-8",
        )
        new_rows.append(
            {
                "legacy_id": alias,
                "canonical_id": lesson["id"],
                "public_path": public_path,
                "canonical_en": f"docs/en/lessons/{lesson['id']}.md",
                "canonical_ko": f"docs/ko/lessons/{lesson['id']}.md",
            }
        )
    with mapping_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=("legacy_id", "canonical_id", "public_path", "canonical_en", "canonical_ko"),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(new_rows)


def _publishing_state() -> None:
    path = ROOT / "state" / "PUBLISHING.md"
    if path.exists():
        return
    lines = [
        "# Curriculum publishing state",
        "",
        "This shared file tracks repository publication evidence. Learner progress is local in `.local/progress.json`.",
        "",
        "| ID | Verification | Status | Evidence |",
        "|---|---|---|---|",
    ]
    for lesson in LESSONS:
        status = (
            "scaffolded"
            if lesson["id"] in {
                "hw-common-02",
                "hw-fr3-01",
                "hw-wuji-01",
                "hw-wuji-02",
                "hw-enlight-01",
                "hw-enlight-02",
                "hw-enlight-03",
                "hw-enlight-wuji-01",
            }
            else "implemented"
        )
        lines.append(
            f"| {lesson['id']} | `{lesson['verification']}` | {status} | lesson-specific deterministic artifact contract |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    for language in ("en", "ko"):
        lesson_root = ROOT / "docs" / language / "lessons"
        lesson_root.mkdir(parents=True, exist_ok=True)
        for lesson in LESSONS:
            (lesson_root / f"{lesson['id']}.md").write_text(_page(lesson, language), encoding="utf-8")
        (ROOT / "docs" / language / "index.md").write_text(_index(language), encoding="utf-8")
    test_root = ROOT / "tests" / "lessons"
    test_root.mkdir(parents=True, exist_ok=True)
    for lesson in LESSONS:
        entrypoint = ROOT / lesson["entrypoint"]
        entrypoint.parent.mkdir(parents=True, exist_ok=True)
        entrypoint.write_text(_entrypoint(lesson["id"]), encoding="utf-8")
        (test_root / f"test_{lesson['id'].replace('-', '_')}.py").write_text(_test(lesson["id"]), encoding="utf-8")
    _legacy_redirects()
    _publishing_state()
    print(f"generated {len(LESSONS)} bilingual lessons, entry points, and tests")


if __name__ == "__main__":
    main()
