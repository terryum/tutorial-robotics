import hashlib

from pai_lab.catalog import ROOT
from pai_lab.lessons.physics import source_hash_comparison
from tests.lesson_contract import assert_contract


def test_core_02_contract(tmp_path):
    assert_contract("core-02", tmp_path)


def test_hash_experiment_modifies_one_byte_in_memory():
    path = ROOT / "assets/sources.json"
    original = path.read_bytes()
    comparison = source_hash_comparison(original)
    offset = comparison["byte_offset"]
    changed = original[:offset] + bytes([comparison["changed_byte"]]) + original[offset + 1 :]
    assert original[offset] == comparison["original_byte"]
    assert sum(before != after for before, after in zip(original, changed, strict=True)) == 1
    assert hashlib.sha256(original).hexdigest() == comparison["original_sha256"]
    assert hashlib.sha256(changed).hexdigest() == comparison["changed_sha256"]
    assert comparison["original_sha256"] != comparison["changed_sha256"]
    assert path.read_bytes() == original
