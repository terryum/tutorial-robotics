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
        intro = (
            f"이 수업에서는 **{title}**의 재현 가능한 최소 기준선을 만들고, "
            "상태·기준값·관측값의 흐름을 수치 artifact로 검사합니다."
        )
        goals = (
            "- capability와 선행 수업을 실행 전에 확인합니다.\n"
            "- 고정 seed로 기준 trace를 만들고 SHA-256으로 기록합니다.\n"
            "- 외부 GPU, ROS 2 또는 실제 장비 검증이 필요한 범위를 badge와 분리합니다."
        )
        expected = (
            "exit code `0`과 함께 `summary.json`, `trace.csv`, `lesson-report.md`가 생성됩니다. "
            "`summary.json`의 `metric_value`는 유한하고 같은 seed에서 재현되어야 합니다."
        )
        recovery = (
            f"먼저 `pal lesson check {lesson['id']} --json`을 실행합니다. capability가 없으면 "
            f"`pal setup verify --stage {lesson['stage']} --json`의 missing 목록을 따르고, 시스템 패키지나 firmware는 자동 설치하지 않습니다."
        )
        explanation = (
            "공통 runner는 20 ms 간격의 정규화된 기준 신호와 관측 신호를 생성합니다. "
            "평균 절대 추종 오차 $E=\\frac{1}{N}\\sum_i |r_i-y_i|$를 계산하고, CSV 바이트의 SHA-256을 checkpoint로 사용합니다. "
            "이 값은 인터페이스와 재현성 smoke를 검증하며 실제 로봇 정확도나 센서 힘을 의미하지 않습니다."
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
        intro = (
            f"You will build a reproducible minimum baseline for **{title}** and inspect the flow "
            "from reference state to observed state through numeric artifacts."
        )
        goals = (
            "- Check capabilities and prerequisites before execution.\n"
            "- Produce a seeded trace and record its SHA-256 digest.\n"
            "- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge."
        )
        expected = (
            "Exit code `0` creates `summary.json`, `trace.csv`, and `lesson-report.md`. "
            "`metric_value` in `summary.json` must be finite and repeatable for the same seed."
        )
        recovery = (
            f"Run `pal lesson check {lesson['id']} --json` first. If a capability is unavailable, follow "
            f"the missing list from `pal setup verify --stage {lesson['stage']} --json`; do not auto-install system packages or firmware."
        )
        explanation = (
            "The common runner samples normalized reference and observed signals every 20 ms. "
            "It computes mean absolute tracking error $E=\\frac{1}{N}\\sum_i |r_i-y_i|$ and uses the CSV byte-level SHA-256 as a checkpoint. "
            "This validates interface and reproducibility plumbing; it is not evidence of real robot accuracy or sensor force."
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

{warning}

## Learning goals

{goals}

## Preflight

```bash
pal host detect --json
pal setup verify --stage {lesson['stage']} --json
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
    return f'''from pai_lab.lessons import check_lesson, run_lesson


def test_{lesson_id.replace("-", "_")}_contract(tmp_path) -> None:
    result = run_lesson("{lesson_id}", output_dir=tmp_path, seed=7, samples=16)
    assert result.lesson_id == "{lesson_id}"
    assert result.metric_value >= 0.0
    assert {{path.name for path in tmp_path.iterdir()}} == {{"summary.json", "trace.csv", "lesson-report.md"}}
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
        lines.append(
            f"| {lesson['id']} | `{lesson['verification']}` | implemented | catalog/doc/entrypoint/smoke contract |"
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
