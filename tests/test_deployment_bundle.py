import json

from pai_lab.bundle import validate_bundle
from pai_lab.catalog import ROOT

SAMPLE = ROOT / "examples/sim-deploy-01/sample_candidate/manifest.json"


def test_sample_candidate_is_complete_and_deterministic() -> None:
    assert validate_bundle(SAMPLE) == []


def test_sample_candidate_checkout_preserves_checksum_bytes() -> None:
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    assert "examples/sim-deploy-01/sample_candidate/*.json -text" in attributes


def test_candidate_rejects_checksum_mismatch(tmp_path) -> None:
    manifest = json.loads(SAMPLE.read_text(encoding="utf-8"))
    manifest["policy"]["path"] = "policy.json"
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (tmp_path / "policy.json").write_text("{}", encoding="utf-8")
    assert "policy checksum mismatch" in validate_bundle(tmp_path / "manifest.json")
