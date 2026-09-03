from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WUJI_MODEL = (
    ROOT
    / "assets/vendor/wuji-description/hand2/hand2_beta1/body/mjcf/left.xml"
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    if WUJI_MODEL.is_file():
        return
    missing_vendor = pytest.mark.skip(
        reason="pinned Wuji model is not initialized; fetch it in the model tutorial"
    )
    for item in items:
        path = Path(str(item.path))
        if "wuji_motion" in path.parts or "wuji_setup" in path.parts:
            item.add_marker(missing_vendor)
