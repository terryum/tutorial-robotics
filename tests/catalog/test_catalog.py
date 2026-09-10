from pai_lab.assets import check_sources
from pai_lab.catalog import load_catalog, resolve_lesson, validate_catalog


def test_catalog_has_exact_stage_counts_and_closed_graph() -> None:
    lessons = load_catalog()
    assert len(lessons) == 49
    assert {stage: sum(item.stage == stage for item in lessons) for stage in ("core", "sim", "hardware")} == {
        "core": 25,
        "sim": 15,
        "hardware": 9,
    }
    assert validate_catalog() == []
    assert check_sources() == []
    assert sum(item.implementation == "implemented" for item in lessons) == 41
    assert sum(item.implementation == "scaffolded" for item in lessons) == 8


def test_legacy_aliases_resolve_to_canonical_lessons() -> None:
    assert resolve_lesson("T00").id == "core-00"
    assert resolve_lesson("T38A").id == "hw-enlight-wuji-01"
    assert resolve_lesson("T42B").id == "hw-wuji-02"
