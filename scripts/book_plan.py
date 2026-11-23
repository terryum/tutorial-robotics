"""Create full or scoped book-production packets; does not spawn agents or touch progress."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from pai_lab.lessons.dependencies import engine

ROOT = Path(__file__).resolve().parents[1]


def make_plan(run_id: str, lessons: list[str], concepts: list[str]) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
        raise ValueError("Run ID must contain letters, digits, underscores or hyphens")
    catalog = json.loads((ROOT / "curriculum/catalog.json").read_text())["lessons"]
    topics = json.loads((ROOT / "curriculum/book-topics.json").read_text())
    by_id = {row["id"]: row for row in catalog}
    known_concepts = {row[0] for row in topics.values()}
    if set(lessons) - by_id.keys() or set(concepts) - known_concepts:
        raise ValueError("Unknown lesson or concept")
    full = not lessons and not concepts
    selected_concepts = known_concepts if full else set(concepts)
    selected = (
        set(by_id)
        if full
        else set(lessons)
        | {
            identifier
            for identifier, topic in topics.items()
            if topic[0] in selected_concepts
            or any(
                f"concepts/{concept}.md"
                in (ROOT / f"docs/{language}/lessons/{identifier}.md").read_text()
                for concept in selected_concepts
                for language in ("en", "ko")
            )
        }
    )
    tasks = []

    def add(identifier: str, role: str, dependencies: list[str], inputs: list[str], decision: str):
        tasks.append(
            {
                "id": identifier,
                "role": role,
                "dependencies": dependencies,
                "ownership": [f".harness/runs/{run_id}/task-{identifier}/outputs"],
                "inputs": ["agent/book-contract.md", "curriculum/catalog.json", *inputs],
                "context": {
                    "decisions": [decision],
                    "skill_paths": [
                        ".agents/skills/robotics-lesson-authoring/SKILL.md",
                        ".agents/skills/robotics-book-review/SKILL.md",
                    ],
                },
                "acceptance": [
                    "Source-grounded bilingual output; required checks have actual evidence"
                ],
                "required": True,
            }
        )

    for concept in sorted(selected_concepts):
        task_id = "concept-" + concept
        add(
            task_id,
            "harness_worker",
            [],
            ["src/pai_lab/lessons"],
            f"Draft both languages for concept {concept}; output only, never learner execution",
        )
        add(
            "review-" + task_id,
            "harness_reviewer",
            [task_id],
            [],
            "Review read-only; parent records reviewer findings and requires correction before integration",
        )
    review_ids = []
    for row in sorted(catalog, key=lambda item: item["order"]):
        identifier = row["id"]
        if identifier not in selected:
            continue
        concept = topics[identifier][0]
        deps = [
            "review-concept-" + changed
            for changed in sorted(selected_concepts)
            if changed == concept
            or any(
                f"concepts/{changed}.md"
                in (ROOT / f"docs/{language}/lessons/{identifier}.md").read_text()
                for language in ("en", "ko")
            )
        ]
        task_id = "lesson-" + identifier
        add(
            task_id,
            "harness_worker",
            deps,
            [
                row["entrypoint"],
                f"src/pai_lab/lessons/{engine(identifier)}.py",
                "src/pai_lab/lessons/runner.py",
                f"tests/lessons/test_{identifier.replace('-', '_')}.py",
            ],
            f"Draft {identifier} in Korean then English; include summary and both language reviews",
        )
        review = "review-" + task_id
        add(
            review,
            "harness_reviewer",
            [task_id],
            [],
            "Read actual source and bilingual draft; product edits prohibited",
        )
        review_ids.append(review)
    add(
        "integrated-qa",
        "harness_qa",
        review_ids,
        [],
        "After parent integrates reviewed outputs and refreshes summaries, check actual README-linked book, build, artifacts and Harness completion",
    )
    return {"objective": "Source-grounded bilingual robotics book production", "tasks": tasks}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--changed-lesson", action="append", default=[])
    parser.add_argument("--changed-concept", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = make_plan(args.run_id, args.changed_lesson, args.changed_concept)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {len(plan['tasks'])} task packets to {args.output}")


if __name__ == "__main__":
    main()
