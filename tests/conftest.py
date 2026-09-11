"""Shared pytest configuration intentionally has no asset-dependent skips."""

import pytest


@pytest.fixture(autouse=True)
def isolated_learner_state(tmp_path, monkeypatch):
    monkeypatch.setenv("PAL_LOCAL_DIR", str(tmp_path / "learner-state"))
