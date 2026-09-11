"""Isaac 6 must never call its removed legacy URDF Kit command."""
import sys
from types import ModuleType, SimpleNamespace

from pai_lab.lessons.isaac_adapter import import_urdf


def test_six_uses_direct_importer_and_explicit_output(monkeypatch, tmp_path):
    def module(name):
        value=ModuleType(name);monkeypatch.setitem(sys.modules,name,value)
        if '.' in name:
            parent,child=name.rsplit('.',1)
            setattr(sys.modules[parent],child,value)
        return value
    for name in ['omni','omni.usd','isaacsim','isaacsim.core','isaacsim.core.utils','isaacsim.core.utils.extensions','isaacsim.asset','isaacsim.asset.importer','isaacsim.asset.importer.urdf','pxr']:
        module(name)
    sys.modules['isaacsim.core.utils.extensions'].enable_extension=lambda name: None
    called=[]
    api=sys.modules['isaacsim.asset.importer.urdf']
    api.URDFImporterConfig=lambda **kwargs: kwargs
    class Importer:
        def __init__(self,config):called.append(config)
        def import_urdf(self):return str(tmp_path/'derived.usda')
    api.URDFImporter=Importer
    stage=SimpleNamespace(Traverse=lambda:[SimpleNamespace(HasAPI=lambda schema:True,GetPath=lambda:'/Robot')])
    sys.modules['pxr'].Usd=SimpleNamespace(Stage=SimpleNamespace(Open=lambda path:stage))
    sys.modules['pxr'].UsdPhysics=SimpleNamespace(ArticulationRootAPI=object)
    actual,root,version=import_urdf(tmp_path/'source.urdf',tmp_path/'derived.usda',fix_base=False)
    assert actual is stage and root=='/Robot' and version=='6.0-direct-importer'
    assert called[0]['usd_path']==str(tmp_path/'derived.usda')
    assert called[0]['fix_base'] is False and called[0]['merge_fixed_joints'] is False
