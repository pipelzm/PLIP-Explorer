"""Packaging/API contract checks; these do not emulate the ChimeraX GUI."""
import ast
from email import message_from_bytes
import importlib.util
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def setup_metadata():
    tree = ast.parse((ROOT / "setup.py").read_text())
    setup = next(n for n in ast.walk(tree) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == "setup")
    return {k.arg: ast.literal_eval(k.value) for k in setup.keywords}


def bundle_fields(classifiers):
    classifier = next(c for c in classifiers if c.startswith("ChimeraX :: Bundle ::"))
    return [part.strip() for part in classifier.split("::")]


class BundleTests(unittest.TestCase):
    def test_lifecycle_metadata_has_required_hooks(self):
        metadata = setup_metadata()
        xml = ET.parse(ROOT / "bundle_info.xml").getroot()
        fields = bundle_fields(metadata["classifiers"])
        self.assertEqual(metadata["version"], xml.get("version"))
        self.assertEqual(fields[6], xml.get("customInit", ""))
        api_tree = ast.parse((ROOT / "src" / "__init__.py").read_text())
        api = next(n for n in api_tree.body if isinstance(n, ast.ClassDef) and n.name == "_API")
        methods = {n.name for n in api.body if isinstance(n, ast.FunctionDef)}
        if fields[6].lower() == "true":
            self.assertTrue({"initialize", "finish"} <= methods,
                            "customInit=true requires initialize and finish overrides")
        self.assertTrue({"start_tool", "get_class"} <= methods)

    def test_bundle_import_is_lazy_and_panel_dispatch_matches_api_v1(self):
        # Only the host base class is replaced. This checks our entry points,
        # not Qt widgets, host session management, or rendered graphics.
        toolshed = types.ModuleType("chimerax.core.toolshed")
        toolshed.BundleAPI = type("BundleAPI", (), {})
        modules = {"chimerax": types.ModuleType("chimerax"),
                   "chimerax.core": types.ModuleType("chimerax.core"),
                   "chimerax.core.toolshed": toolshed}
        name = "plip_bundle_contract"
        spec = importlib.util.spec_from_file_location(name, ROOT / "src" / "__init__.py")
        bundle = importlib.util.module_from_spec(spec)
        modules[name] = bundle
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(bundle)
            self.assertNotIn(name + ".tool", sys.modules)
            self.assertEqual(bundle.bundle_api.api_version, 1)
            class Panel:
                def __init__(self, session, tool_name):
                    self.session, self.name = session, tool_name
            tool_module = types.ModuleType(name + ".tool")
            tool_module.PLIPExplorer = Panel
            with patch.dict(sys.modules, {name + ".tool": tool_module}):
                session, info = object(), types.SimpleNamespace(name="PLIP Explorer")
                panel = bundle.bundle_api.start_tool(session, object(), info)
                self.assertIs(panel.session, session)
                self.assertEqual(panel.name, info.name)
                self.assertIs(bundle.bundle_api.get_class("PLIPExplorer"), Panel)

    def test_distributed_wheel_matches_source_and_metadata(self):
        metadata = setup_metadata()
        wheels = list((ROOT / "dist").glob(f'*{metadata["version"]}-*.whl'))
        self.assertEqual(len(wheels), 1, "Build the current wheel before this check")
        with ZipFile(wheels[0]) as wheel:
            meta_path = next(n for n in wheel.namelist() if n.endswith("/METADATA"))
            built = message_from_bytes(wheel.read(meta_path))
            self.assertEqual(built["Version"], metadata["version"])
            self.assertEqual(bundle_fields(built.get_all("Classifier")),
                             bundle_fields(metadata["classifiers"]))
            for source in (ROOT / "src").rglob("*.py"):
                target = "chimerax/plip_explorer/" + source.relative_to(ROOT / "src").as_posix()
                self.assertEqual(wheel.read(target), source.read_bytes(), target)
            for source in (ROOT / "src/docs/user/tools").glob("*.html"):
                target = "chimerax/plip_explorer/docs/user/tools/" + source.name
                self.assertEqual(wheel.read(target), source.read_bytes(), target)
            for source in (ROOT / "src/examples").rglob("*"):
                if source.is_file():
                    target = "chimerax/plip_explorer/" + source.relative_to(ROOT / "src").as_posix()
                    self.assertEqual(wheel.read(target), source.read_bytes(), target)


if __name__ == "__main__": unittest.main(verbosity=2)
