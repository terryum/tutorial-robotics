from __future__ import annotations

import json

import pai_lab.cli as cli_module
from pai_lab.host import CapabilityEvidence, HostProfile


def test_user_capability_list_cannot_enable_runtime(tmp_path, monkeypatch) -> None:
    fake_root = tmp_path
    local = fake_root / ".local"
    local.mkdir()
    (local / "capabilities.json").write_text(
        json.dumps({"capabilities": ["robot-runtime", "nvidia-cuda"]}), encoding="utf-8"
    )
    profile = HostProfile(
        "Test",
        "x86_64",
        "3.12.0",
        "test-x86_64",
        ("python-3.12",),
        {"python-3.12": CapabilityEvidence("available", "test")},
        {},
    )
    monkeypatch.setattr(cli_module, "ROOT", fake_root)
    monkeypatch.setattr(cli_module, "detect_host", lambda: profile)
    capabilities = cli_module._local_capabilities()
    assert "python-3.12" in capabilities
    assert "robot-runtime" not in capabilities
    assert "nvidia-cuda" not in capabilities


def test_even_pal_receipt_cannot_self_authorize_protected_capability(tmp_path, monkeypatch) -> None:
    local = tmp_path / ".local"
    local.mkdir()
    (local / "capabilities.json").write_text(
        json.dumps({
            "schema_version": 2,
            "source": "pal-verify",
            "verified_capabilities": ["robot-runtime", "custom-offline-tool"],
        }),
        encoding="utf-8",
    )
    profile = HostProfile("Test", "x86_64", "3.12.0", "test", (), {}, {})
    monkeypatch.setattr(cli_module, "ROOT", tmp_path)
    monkeypatch.setattr(cli_module, "detect_host", lambda: profile)
    capabilities = cli_module._local_capabilities()
    assert "custom-offline-tool" in capabilities
    assert "robot-runtime" not in capabilities
