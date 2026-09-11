"""One read-only gate for selection, execution, and completion."""

from pathlib import Path

from pai_lab.catalog import ROOT, Lesson
from pai_lab.host import detect_host
from pai_lab.progress import load_progress


def gaps(lesson: Lesson, *, prerequisites: bool = True) -> list[str]:
    host = detect_host()
    errors = []
    platforms = {host.platform_id} | set(host.capabilities)
    if not platforms.intersection(lesson.platforms):
        errors.append(f"platform {host.platform_id}; requires {', '.join(lesson.platforms)}")
    for capability in lesson.capabilities:
        if capability not in host.capabilities:
            errors.append(
                f"capability {capability}; inspect pal setup verify --profile "
                + (
                    "ros"
                    if "ros" in capability
                    else "isaac"
                    if "isaac" in capability
                    else "gpu"
                    if "cuda" in capability
                    else "core"
                )
            )
    if lesson.implementation != "implemented":
        errors.append("reader_test_required: device adapter is scaffolded")
    models = required_models(lesson.id)
    if models:
        from pai_lab.lessons.models import provenance

        for model in models:
            try:
                provenance(model)
            except (FileNotFoundError, ValueError) as error:
                errors.append(str(error))
    if prerequisites:
        completed = load_progress().completed
        for identifier in lesson.prerequisites:
            if identifier not in completed:
                errors.append(f"prerequisite {identifier}; run and finish it first")
            elif completion_gaps(identifier):
                errors.append(
                    f"prerequisite {identifier} has stale or unverified evidence; rerun and finish it"
                )
    return errors


def completion_gaps(identifier: str) -> list[str]:
    from pai_lab.feedback import pending
    from pai_lab.lessons.evidence import validate_run

    entry = load_progress().completed.get(identifier)
    if not entry or not entry.get("run_dir"):
        return ["no completed run"]
    path = Path(entry["run_dir"])
    if not path.is_absolute():
        path = ROOT / path
    errors = validate_run(identifier, path)
    if not (path / "review.json").is_file():
        errors.append("completed run has no review; legacy record preserved but unverified")
    if pending(identifier):
        errors.append("unresolved feedback")
    return errors


def required_models(identifier: str) -> tuple[str, ...]:
    if identifier in {"core-02", "core-03"}:
        return ("fr3", "enlight", "wuji", "sharpa", "g1", "aloha")
    if identifier.startswith("core-fr3") or identifier == "core-04":
        return ("fr3",)
    if identifier.startswith("core-enlight") or identifier in {"sim-enlight-01", "sim-enlight-02"}:
        return ("enlight",)
    if identifier.startswith("core-dexterity"):
        return ("wuji", "sharpa")
    if identifier.startswith(("core-wuji", "sim-isaac")) or identifier == "sim-cross-01":
        return ("wuji",)
    if identifier == "core-g1-01":
        return ("g1",)
    if identifier == "core-aloha-01":
        return ("aloha",)
    return ()
