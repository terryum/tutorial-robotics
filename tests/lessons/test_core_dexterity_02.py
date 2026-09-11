from tests.lesson_contract import assert_contract


def test_core_dexterity_02_contract(tmp_path):
    assert_contract("core-dexterity-02", tmp_path)
