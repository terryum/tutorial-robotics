from pai_lab.assets import check_sources
from pai_lab.catalog import load_catalog, resolve_lesson, validate_catalog


def test_catalog_extends_original_lessons_and_has_closed_graph() -> None:
    lessons = load_catalog()
    assert len(lessons) >= 49
    counts = {
        stage: sum(item.stage == stage for item in lessons) for stage in ("core", "sim", "hardware")
    }
    assert all(
        counts[stage] >= minimum
        for stage, minimum in {"core": 25, "sim": 15, "hardware": 9}.items()
    )
    assert validate_catalog() == []
    assert check_sources() == []
    assert sum(item.implementation == "implemented" for item in lessons) >= 41
    assert sum(item.implementation == "scaffolded" for item in lessons) >= 8


def test_legacy_aliases_resolve_to_canonical_lessons() -> None:
    assert resolve_lesson("T00").id == "core-00"
    assert resolve_lesson("T38A").id == "hw-enlight-wuji-01"
    assert resolve_lesson("T42B").id == "hw-wuji-02"


def test_original_ids_and_aliases_are_preserved():
    import json

    from pai_lab.catalog import ROOT

    original = json.loads((ROOT / "curriculum/legacy-ids.json").read_text())
    assert len(original) == 49
    for identifier, aliases in original.items():
        assert resolve_lesson(identifier).aliases == tuple(aliases)
