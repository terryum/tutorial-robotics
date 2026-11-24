"""Shared pytest configuration and local capability fixtures."""

import sys

import pytest


@pytest.fixture(scope="session")
def native_macos_gl():
    if sys.platform != "darwin":
        return
    import mujoco
    from mujoco.cgl.cgl import CGLError

    try:
        model = mujoco.MjModel.from_xml_string("<mujoco/>")
        with mujoco.Renderer(model, height=16, width=16):
            pass
    except CGLError as error:
        pytest.skip(f"native macOS OpenGL context unavailable: {error}")


@pytest.fixture(autouse=True)
def isolated_learner_state(tmp_path, monkeypatch):
    monkeypatch.setenv("PAL_LOCAL_DIR", str(tmp_path / "learner-state"))
