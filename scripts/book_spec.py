"""Build the source-grounded, bilingual production manifest without learner state."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pai_lab.lessons.dependencies import engine

ROOT = Path(__file__).resolve().parents[1]


def goals(text: str) -> str:
    match = re.search(
        r"^## Learning goals\s*\n(.*?)(?=\n\s*\n|\n## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    if not match or not match[1].strip():
        raise ValueError("Missing authored Learning goals paragraph")
    return " ".join(match[1].split())


def build(root: Path = ROOT) -> dict:
    catalog = json.loads((root / "curriculum/catalog.json").read_text())["lessons"]
    topics = json.loads((root / "curriculum/book-topics.json").read_text())
    if {row["id"] for row in catalog} != set(topics):
        raise ValueError("Book topics must cover the catalog exactly once")
    lessons = []
    for row in sorted(catalog, key=lambda item: item["order"]):
        identifier = row["id"]
        concept, question_en, question_ko = topics[identifier]
        source = (
            "src/pai_lab/hardware/run_card.py"
            if row["stage"] == "hardware" and row["implementation"] == "scaffolded"
            else f"src/pai_lab/lessons/{engine(identifier)}.py"
        )
        lessons.append(
            {
                "id": identifier,
                "question": {"en": question_en, "ko": question_ko},
                "objectives": {
                    language: goals((root / f"docs/{language}/lessons/{identifier}.md").read_text())
                    for language in ("en", "ko")
                },
                "prerequisites": row["prerequisites"],
                "prerequisite_concepts": [concept],
                "implementation_sources": [
                    row["entrypoint"],
                    "src/pai_lab/lessons/runner.py",
                    source,
                ],
                "test": f"tests/lessons/test_{identifier.replace('-', '_')}.py",
                "environment": {key: row[key] for key in ("platforms", "capabilities")},
                "observe": row["expected_artifacts"],
                "verification": row["verification"],
                "implementation": row["implementation"],
                "evidence_scope": "catalog publication badge; local execution not asserted by this manifest",
                "concept_chapters": [f"docs/{{language}}/concepts/{concept}.md"],
            }
        )
    return {"schema_version": 1, "lesson_count": len(lessons), "lessons": lessons}


def main() -> None:
    target = ROOT / "curriculum/book-spec.json"
    manifest = build()
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(
        f"wrote {target.relative_to(ROOT)}: {manifest['lesson_count']} bilingual lesson specifications"
    )


if __name__ == "__main__":
    main()
