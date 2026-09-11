"""Discovery boundary for private or third-party lesson providers."""

from __future__ import annotations

from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Protocol


class LessonProvider(Protocol):
    name: str

    def lessons(self) -> tuple[Any, ...]: ...

    def run(self, identifier: str, output_dir: Path, samples: int = 64, **options: Any) -> Any: ...

    def check(self, identifier: str) -> list[str]: ...

    def requires_comparison(self, identifier: str) -> bool: ...

    def validate_run(self, identifier: str, output_dir: Path) -> list[str]: ...


def discover_lesson_providers() -> tuple[LessonProvider, ...]:
    providers: list[LessonProvider] = []
    for entry_point in entry_points(group="pai_lab.lesson_providers"):
        factory = entry_point.load()
        providers.append(factory())
    return tuple(providers)


def provider_for(identifier: str) -> LessonProvider | None:
    for provider in discover_lesson_providers():
        if any(str(lesson.id).lower() == identifier.lower() for lesson in provider.lessons()):
            return provider
    return None


def extended_catalog() -> tuple[Any, ...]:
    """Return provider metadata without contaminating the 49-node public catalog."""

    return tuple(
        lesson for provider in discover_lesson_providers() for lesson in provider.lessons()
    )
