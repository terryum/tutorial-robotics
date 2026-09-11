"""Version-specific URDF import; callers must create SimulationApp first.

6.0 removes URDFParseAndImportFile. Both routes explicitly write outside vendor
sources. The returned stage must still pass model-specific parity checks.
"""

from pathlib import Path
from typing import Any


def import_urdf(source: Path, output: Path, *, fix_base: bool = True) -> tuple[Any, str, str]:
    import omni.usd
    from isaacsim.core.utils.extensions import enable_extension

    enable_extension("isaacsim.asset.importer.urdf")
    import isaacsim.asset.importer.urdf as api

    if hasattr(api, "URDFImporter") and hasattr(api, "URDFImporterConfig"):
        config = api.URDFImporterConfig(
            urdf_path=str(source.resolve()),
            usd_path=str(output.resolve()),
            fix_base=fix_base,
            merge_fixed_joints=False,
            merge_mesh=False,
        )
        path = api.URDFImporter(config).import_urdf()
        if not path:
            raise RuntimeError("Isaac 6 importer produced no USD path")
        from pxr import Usd, UsdPhysics

        stage = Usd.Stage.Open(str(path))
        if stage is None:
            raise RuntimeError("cannot reopen imported USD")
        roots = [prim for prim in stage.Traverse() if prim.HasAPI(UsdPhysics.ArticulationRootAPI)]
        if len(roots) != 1:
            raise RuntimeError("expected exactly one imported articulation")
        return stage, str(roots[0].GetPath()), "6.0-direct-importer"
    import omni.kit.commands

    ok, config = omni.kit.commands.execute("URDFCreateImportConfig")
    if not ok:
        raise RuntimeError("Isaac 5.1 importer configuration failed")
    config.set_fix_base(fix_base)
    config.set_merge_fixed_joints(False)
    config.set_import_inertia_tensor(True)
    ok, root = omni.kit.commands.execute(
        "URDFParseAndImportFile",
        urdf_path=str(source.resolve()),
        import_config=config,
        dest_path=str(output.resolve()),
        get_articulation_root=True,
    )
    if not ok:
        raise RuntimeError("Isaac 5.1 URDF import failed")
    from pxr import Usd

    stage = Usd.Stage.Open(str(output.resolve()))
    if stage is None:
        raise RuntimeError("cannot reopen imported USD")
    return stage, str(root), "5.1-kit-importer"
