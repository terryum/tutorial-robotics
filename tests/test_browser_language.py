import importlib.util
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("open_lesson", ROOT / "scripts/open_lesson.py")
browser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(browser)


def saved(language):
    return {"browser": "chrome", "language": language, "tab_id": 42}


@pytest.mark.parametrize(
    "state,conversation,live,force,expected,mode",
    [
        (None, "ko", "en", False, "ko", "force"),
        (None, "en", "ko", False, "en", "force"),
        (saved("en"), "en", "ko", False, "ko", "preserve"),
        (saved("ko"), "ko", "en", False, "en", "preserve"),
        (saved("en"), "ko", None, False, "en", "preserve"),
        (saved("ko"), "en", None, False, "ko", "preserve"),
        (saved("ko"), "en", "ko", True, "en", "force"),
    ],
)
def test_language_precedence_and_receipt(
    tmp_path, monkeypatch, state, conversation, live, force, expected, mode
):
    state_file = tmp_path / "browser.json"
    if state:
        state_file.write_text(json.dumps(state))

    def chrome(command, **kwargs):
        fallback, lesson, tab, actual_mode = command[2:]
        assert actual_mode == mode
        assert tab == ("42" if state else "")
        selected = fallback if actual_mode == "force" or live is None else live
        return SimpleNamespace(
            stdout=(
                f"language={selected}\nurl={browser.DOCS_URL}{selected}/lessons/{lesson}.md\n"
                f"tab_id=42\nreused=true\ntitle={lesson}.md at main\n"
            )
        )

    monkeypatch.setattr(browser.subprocess, "run", chrome)
    result = browser.open_lesson("core-01", conversation, state_file, force_language=force)
    assert result["language"] == expected
    assert json.loads(state_file.read_text())["language"] == expected
    assert result["url"].endswith(f"/{expected}/lessons/core-01.md")


def test_failed_navigation_preserves_language_state(tmp_path, monkeypatch):
    state_file = tmp_path / "browser.json"
    previous = json.dumps(saved("ko"))
    state_file.write_text(previous)

    def failed(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "osascript")

    monkeypatch.setattr(browser.subprocess, "run", failed)
    with pytest.raises(subprocess.CalledProcessError):
        browser.open_lesson("core-01", "en", state_file)
    assert state_file.read_text() == previous


def test_unverified_page_does_not_replace_state(tmp_path, monkeypatch):
    state_file = tmp_path / "browser.json"
    previous = json.dumps(saved("ko"))
    state_file.write_text(previous)
    monkeypatch.setattr(
        browser.subprocess,
        "run",
        lambda *a, **kw: SimpleNamespace(
            stdout="language=en\nurl=https://github.com/login\ntitle=Sign in\ntab_id=42\n"
        ),
    )
    with pytest.raises(ValueError, match="verify"):
        browser.open_lesson("core-01", "en", state_file)
    assert state_file.read_text() == previous
