from tests.lesson_contract import assert_contract


def test_core_fr3_02_contract(tmp_path):
    assert_contract("core-fr3-02", tmp_path)
