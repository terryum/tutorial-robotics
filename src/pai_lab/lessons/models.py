"""Pinned vendor models. Derived models are written only into a run directory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import mujoco
import numpy as np
from scipy.spatial.transform import Rotation

from pai_lab.catalog import ROOT

MODEL_PATHS = {
    "fr3": ("mujoco-menagerie", "franka_fr3/scene.xml"),
    "g1": ("mujoco-menagerie", "unitree_g1/scene.xml"),
    "aloha": ("mujoco-menagerie", "aloha/scene.xml"),
    "sharpa": ("mujoco-menagerie", "sharpa_wave/scene_right.xml"),
    "wuji": ("wuji-description", "hand2/hand2_beta2/body/mjcf/right.xml"),
}


def provenance(name: str) -> dict[str, Any]:
    lock = json.loads((ROOT / "assets/model-lock.json").read_text())
    entry = lock["models"][name]
    base = ROOT / ".cache/assets" / entry["destination"]
    for relative, expected in entry["files"].items():
        path = base / relative
        if not path.is_file():
            raise FileNotFoundError(
                f"{name}: missing {relative}; pal assets fetch {entry['bundle']}"
            )
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"{name}: modified vendor file {relative}; use a clean pinned cache")
    return {
        "model": name,
        "revision": entry["revision"],
        "license": entry["license"],
        "files_digest": hashlib.sha256(
            json.dumps(entry["files"], sort_keys=True).encode()
        ).hexdigest(),
    }


def load(name: str, output: Path | None = None) -> tuple[Any, Any, dict[str, Any]]:
    receipt = provenance(name)
    if name == "enlight":
        if output is None:
            raise ValueError("Enlight conversion requires a run output directory")
        path = enlight_xml(output)
    else:
        bundle, relative = MODEL_PATHS[name]
        path = ROOT / ".cache/assets" / bundle / relative
    model = mujoco.MjModel.from_xml_path(str(path))
    data = mujoco.MjData(model)
    if model.nkey:
        mujoco.mj_resetDataKeyframe(model, data, 0)
    mujoco.mj_forward(model, data)
    receipt.update(nq=model.nq, nv=model.nv, nu=model.nu, nbody=model.nbody)
    return model, data, receipt


def scalar_yaml(path: Path) -> dict[str, Any]:
    """Read the pinned vendor's mapping-only numeric configuration; reject other YAML."""
    result: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, result)]
    for line in path.read_text().splitlines():
        text = line.split("#", 1)[0].rstrip()
        if not text.strip():
            continue
        indent = len(text) - len(text.lstrip())
        key, value = text.strip().split(":", 1)
        while stack[-1][0] >= indent:
            stack.pop()
        if value.strip():
            stack[-1][1][key] = float(value)
        else:
            child: dict[str, Any] = {}
            stack[-1][1][key] = child
            stack.append((indent, child))
    return result


def enlight_parameters() -> dict[str, Any]:
    base = ROOT / ".cache/assets/flexiv-description/config/Enlight-L"
    return {
        key: scalar_yaml(base / filename)[section]
        for key, filename, section in (
            ("kinematics", "default_kinematics.yaml", "kinematics"),
            ("inertia", "inertia_parameters.yaml", "inertia_parameters"),
            ("limits", "joint_limits.yaml", "joint_limits"),
            ("initial", "initial_positions.yaml", "initial_positions"),
        )
    }


def enlight_xml(output: Path) -> Path:
    parameters = enlight_parameters()
    root = ET.Element("mujoco", model="Enlight-L-public-draft")
    ET.SubElement(root, "compiler", angle="radian")
    ET.SubElement(root, "option", timestep="0.002", integrator="implicitfast")
    assets = ET.SubElement(root, "asset")
    world = ET.SubElement(root, "worldbody")
    ET.SubElement(world, "light", pos="0 0 2")
    parent = world
    for i in range(1, 8):
        name = f"joint{i}"
        k = parameters["kinematics"][name]
        inertia = parameters["inertia"][f"link{i}"]
        limits = parameters["limits"][name]
        quat = Rotation.from_euler("xyz", [k[a] for a in ("roll", "pitch", "yaw")]).as_quat()
        parent = ET.SubElement(
            parent,
            "body",
            name=f"link{i}",
            pos=" ".join(str(k[a]) for a in ("x", "y", "z")),
            quat=" ".join(map(str, quat[[3, 0, 1, 2]])),
        )
        ET.SubElement(
            parent,
            "joint",
            name=name,
            axis="0 0 1",
            range=f"{limits['lower']} {limits['upper']}",
            damping="0.1",
        )
        tensor = inertia["inertia"]
        ET.SubElement(
            parent,
            "inertial",
            mass=str(inertia["mass"]),
            pos=" ".join(str(inertia["origin"][a]) for a in ("x", "y", "z")),
            fullinertia=" ".join(
                str(tensor[a]) for a in ("ixx", "iyy", "izz", "ixy", "ixz", "iyz")
            ),
        )
        mesh = ROOT / f".cache/assets/flexiv-description/meshes/Enlight-L/collision/link{i}.stl"
        ET.SubElement(assets, "mesh", name=f"mesh{i}", file=str(mesh))
        ET.SubElement(parent, "geom", type="mesh", mesh=f"mesh{i}", rgba="0.65 0.72 0.85 1")
    k = parameters["kinematics"]["link7_to_flange"]
    ET.SubElement(
        parent, "site", name="attachment_site", pos=" ".join(str(k[a]) for a in ("x", "y", "z"))
    )
    actuator = ET.SubElement(root, "actuator")
    for i in range(1, 8):
        ET.SubElement(
            actuator,
            "motor",
            joint=f"joint{i}",
            gear="1",
            ctrllimited="true",
            ctrlrange=f"-{parameters['limits'][f'joint{i}']['effort']} {parameters['limits'][f'joint{i}']['effort']}",
        )
    key = ET.SubElement(root, "keyframe")
    ET.SubElement(
        key,
        "key",
        name="home",
        qpos=" ".join(str(parameters["initial"][f"joint{i}"]) for i in range(1, 8)),
    )
    path = output / "enlight-draft.xml"
    ET.ElementTree(root).write(path, encoding="unicode")
    return path


def enlight_fk(q: np.ndarray) -> np.ndarray:
    matrix = np.eye(4)
    p = enlight_parameters()["kinematics"]
    for i in range(1, 9):
        k = p[f"joint{i}"] if i < 8 else p["link7_to_flange"]
        origin = np.eye(4)
        origin[:3, :3] = Rotation.from_euler(
            "xyz", [k[a] for a in ("roll", "pitch", "yaw")]
        ).as_matrix()
        origin[:3, 3] = [k[a] for a in ("x", "y", "z")]
        rotation = np.eye(4)
        if i < 8:
            rotation[:3, :3] = Rotation.from_rotvec([0, 0, q[i - 1]]).as_matrix()
        matrix = matrix @ origin @ rotation
    return matrix


def inventory(model: Any) -> dict[str, Any]:
    return {
        "nq": model.nq,
        "nv": model.nv,
        "nu": model.nu,
        "joint_names": [model.joint(i).name for i in range(model.njnt)],
        "joint_ranges": model.jnt_range.tolist(),
        "body_names": [model.body(i).name for i in range(model.nbody)],
        "mass_kg": float(model.body_mass.sum()),
        "ngeom": model.ngeom,
        "site_names": [model.site(i).name for i in range(model.nsite)],
    }
