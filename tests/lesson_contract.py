"""Thin-entrypoint contracts; measured integration lives in scripts/verify_course.py."""

import pytest

from pai_lab.catalog import resolve_lesson
from pai_lab.lessons import check_lesson, run_lesson
from pai_lab.readiness import gaps


def assert_contract(identifier, tmp_path):
    lesson = resolve_lesson(identifier)
    assert check_lesson(identifier) == []
    if lesson.implementation == "scaffolded":
        with pytest.raises(NotImplementedError):
            run_lesson(identifier, output_dir=tmp_path / "run")
        return
    missing = gaps(lesson)
    if missing:
        with pytest.raises(FileNotFoundError):
            run_lesson(identifier, output_dir=tmp_path / "run")
        assert not (tmp_path / "run").exists()
        return
    result = run_lesson(identifier, output_dir=tmp_path / "run")
    from pai_lab.lessons.evidence import validate_run

    assert result.lesson_id == lesson.id
    assert validate_run(identifier, tmp_path / "run") == []
