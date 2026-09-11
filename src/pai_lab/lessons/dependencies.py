"""Semantic lesson fingerprints. Old receipts retain their original global digest.

Only literal identifier branches are pruned. Unknown conditions remain, so a
shared helper change conservatively invalidates every lesson that uses it.
"""

from __future__ import annotations

import ast
import hashlib
import json
import tomllib
from dataclasses import asdict
from typing import Any

from pai_lab.catalog import ROOT, resolve_lesson
from pai_lab.readiness import required_models


def engine(identifier: str) -> str:
    lesson = resolve_lesson(identifier)
    if identifier in {
        "core-rl-01",
        "core-fr3-07",
        "core-fr3-08",
        "core-data-01",
        "core-il-01",
        "core-aloha-01",
        "core-vla-01",
    }:
        return "learning"
    if lesson.track in {"wuji", "dexterity", "g1"} and lesson.stage == "core":
        return "hands"
    if lesson.stage == "core":
        return "physics"
    if identifier in {"sim-deploy-01", "hw-common-01", "sim-enlight-02", "sim-wuji-02"}:
        return "deployment"
    return "stacks"


class Specialize(ast.NodeTransformer):
    def __init__(self, identifier: str):
        self.identifier = identifier

    def visit_If(self, node: ast.If) -> Any:
        test = node.test
        if (
            isinstance(test, ast.Compare)
            and isinstance(test.left, ast.Name)
            and test.left.id == "identifier"
            and len(test.ops) == 1
        ):
            try:
                value = ast.literal_eval(test.comparators[0])
                operation = test.ops[0]
                match = (
                    self.identifier == value
                    if isinstance(operation, ast.Eq)
                    else self.identifier != value
                    if isinstance(operation, ast.NotEq)
                    else self.identifier in value
                    if isinstance(operation, ast.In)
                    else None
                )
                if match is not None:
                    return [self.visit(item) for item in (node.body if match else node.orelse)]
            except (ValueError, TypeError):
                pass
        return self.generic_visit(node)


def semantic_source(source: str, identifier: str) -> str:
    tree = Specialize(identifier).visit(ast.parse(source))
    # Omit unused local helpers from a specialized dispatcher.
    definitions = {
        node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    }
    if "run" in definitions:
        used = {"run"}
        while True:
            referenced = {
                node.id
                for name in used
                for node in ast.walk(definitions[name])
                if isinstance(node, ast.Name)
            }
            extended = used | (referenced & definitions.keys())
            if extended == used:
                break
            used = extended
        tree.body = [
            node
            for node in tree.body
            if not isinstance(node, (ast.FunctionDef, ast.ClassDef)) or node.name in used
        ]
    return ast.dump(tree, include_attributes=False)


def dependency_manifest(identifier: str) -> dict[str, str]:
    lesson = resolve_lesson(identifier)
    selected = engine(lesson.id)
    modules = {
        "lessons/runner.py",
        "lessons/inputs.py",
        "lessons/experiment.py",
        "lessons/parameters.py",
        "lessons/dependencies.py",
        "lessons/observation.py",
        "lessons/trace_labels.py",
        f"lessons/{selected}.py",
    }
    if required_models(lesson.id) or selected in {"physics", "hands", "learning"}:
        modules |= {"lessons/models.py"}
    if selected == "physics" and lesson.id == "core-00":
        modules.add("host.py")
    if selected in {"hands", "learning", "deployment"}:
        modules |= {"lessons/physics.py"}
    if selected == "deployment":
        modules |= {"bundle.py", "lessons/learning.py", "lessons/hands.py"}
    if selected == "stacks":
        modules |= {
            "lessons/ros.py",
            "lessons/gpu.py",
            "lessons/isaac.py",
            "lessons/isaac_adapter.py",
            "lessons/vla.py",
            "bundle.py",
            "lessons/models.py",
            "lessons/learning.py",
            "lessons/physics.py",
        }
    result = {}
    for name in sorted(modules):
        source = (ROOT / "src/pai_lab" / name).read_text()
        result[f"src/pai_lab/{name}"] = hashlib.sha256(
            semantic_source(source, lesson.id).encode()
        ).hexdigest()
    # Titles, translations and publishing badges are not experiment inputs.
    metadata = asdict(lesson)
    selected_metadata = {
        key: metadata[key]
        for key in ("id", "capabilities", "platforms", "implementation", "expected_artifacts")
    }
    result["catalog:lesson"] = hashlib.sha256(
        json.dumps(selected_metadata, sort_keys=True).encode()
    ).hexdigest()
    lock = json.loads((ROOT / "assets/model-lock.json").read_text())
    for model in required_models(lesson.id):
        result[f"model:{model}"] = hashlib.sha256(
            json.dumps(lock["models"][model], sort_keys=True).encode()
        ).hexdigest()
    lock_packages = tomllib.loads((ROOT / "uv.lock").read_text())["package"]
    by_name = {package["name"]: package for package in lock_packages}
    active = {item["name"] for item in by_name["pai-lab"]["dependencies"]}
    if selected == "stacks":
        active |= {"torch", "lerobot", "stable-baselines3"} & by_name.keys()
    while True:
        dependencies = {
            item["name"]
            for name in active
            for item in by_name.get(name, {}).get("dependencies", [])
        }
        if dependencies <= active:
            break
        active |= dependencies
    result["runtime-lock"] = hashlib.sha256(
        json.dumps(
            [by_name[name] for name in sorted(active) if name in by_name], sort_keys=True
        ).encode()
    ).hexdigest()
    return result


def dependency_digest(identifier: str) -> str:
    return hashlib.sha256(
        json.dumps(dependency_manifest(identifier), sort_keys=True).encode()
    ).hexdigest()
