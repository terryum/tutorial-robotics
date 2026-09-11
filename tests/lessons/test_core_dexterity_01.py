from tests.lesson_contract import assert_contract


def test_core_dexterity_01_contract(tmp_path):
    assert_contract("core-dexterity-01", tmp_path)
