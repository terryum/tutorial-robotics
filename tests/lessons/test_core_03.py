from tests.lesson_contract import assert_contract


def test_core_03_contract(tmp_path):
    assert_contract("core-03", tmp_path)
