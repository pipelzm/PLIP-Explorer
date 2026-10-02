"""Catalog, controller-state and offline-example checks; no native GUI test."""
import ast
from collections import Counter
from pathlib import Path
from string import Formatter
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
package = types.ModuleType("plip_language_test")
package.__path__ = [str(ROOT / "src")]
sys.modules[package.__name__] = package
from plip_language_test.i18n import CATALOG, LANGUAGES, message, translate
from plip_language_test.report import KINDS, parse_report, csv_text


class LanguageTests(unittest.TestCase):
    def test_catalog_covers_ui_and_preserves_placeholders(self):
        def fields(text):
            return {key for _, key, _, _ in Formatter().parse(text) if key is not None}
        for source, translations in CATALOG.items():
            self.assertEqual(set(translations), set(LANGUAGES) - {"es"}, source)
            for language, text in translations.items():
                self.assertTrue(text)
                self.assertEqual(fields(text), fields(source), source)
                values = {key: "__" + key + "__" for key in fields(source)}
                self.assertEqual(translate(source, language, **values), text.format(**values))
        sources = {value[0] for value in KINDS.values()}
        for filename in ("tool.py", "report.py", "engine.py", "render.py"):
            tree = ast.parse((ROOT / "src" / filename).read_text())
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call): continue
                name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
                offset = 1 if name == "text_widget" else 0
                if name in {"tr", "label", "button", "checkbox", "set_status", "text_widget", "message",
                            "ValueError", "RuntimeError", "TimeoutError", "Cancelled"} and len(node.args) > offset:
                    arg = node.args[offset]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str): sources.add(arg.value)
        self.assertFalse(sources - CATALOG.keys(), sources - CATALOG.keys())

    def test_nested_errors_and_paths_translate_without_altering_values(self):
        err = ValueError(message("Falta {field}", field="ligcoo"))
        warning = message("Interacción {uid} omitida: {error}", uid="2:water_bridges:0", error=err)
        self.assertEqual(translate(warning, "en"), "Interaction 2:water_bridges:0 omitted: Missing ligcoo")
        self.assertIn("Interação", translate(warning, "pt"))
        path = "/tmp/results {original}/plip.log"
        for language in LANGUAGES:
            result = translate(message("PLIP terminó con código {code}. Revisa {path}", code=2, path=path), language)
            self.assertIn(path, result)
            self.assertIn("2", result)
        self.assertEqual(translate("Cancelar", "unknown"), "Cancelar")

    def test_language_change_preserves_loaded_state_without_redrawing(self):
        # Execute the actual controller method with tiny view adapters, not Qt.
        tree = ast.parse((ROOT / "src/tool.py").read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "PLIPExplorer")
        names = {"tr", "set_status", "change_language", "help_for_language"}
        body = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in names]
        namespace = {"translate": translate, "message": message, "KINDS": KINDS}
        exec(compile(ast.Module(body=body, type_ignores=[]), "tool_controller", "exec"), namespace)
        class View:
            def setText(self, value): self.text = value
            def setHorizontalHeaderLabels(self, value): self.headers = value
            def currentRow(self): return 4
            def selectRow(self, value): self.selected = value
        panel = types.SimpleNamespace(language="es", settings=types.SimpleNamespace(),
            language_combo=types.SimpleNamespace(currentData=lambda: "en"),
            site_combo=types.SimpleNamespace(currentIndex=lambda: 2),
            report=object(), table=View(), status=View(), _texts=[],
            groups={"hydrogen_bonds": types.SimpleNamespace(deleted=False, name="")},
            colors={"hydrogen_bonds": [55, 135, 240, 255]}, model=object(),
            _status_message=message("PLIP {version} · {count} interacciones{warnings}",
                                    version="2.4.0", count=13, warnings=""))
        panel.tr = types.MethodType(namespace["tr"], panel)
        panel.help_for_language = types.MethodType(namespace["help_for_language"], panel)
        seen = []
        panel.populate_sites = lambda i: seen.append(i)
        panel.populate_table = lambda: seen.append("table")
        old = (panel.report, panel.model, panel.groups, panel.colors)
        for language in LANGUAGES:
            with self.subTest(language=language):
                panel.language_combo.currentData = lambda: language
                seen.clear()
                namespace["change_language"](panel)
                self.assertEqual(seen, [2, "table"])
                self.assertEqual(panel.table.selected, 4)
                self.assertEqual(panel.settings.language, language)
                suffix = "" if language == "es" else "_" + language
                filename = "plip_explorer" + suffix + ".html"
                self.assertEqual(panel.help, "help:user/tools/" + filename)
                self.assertTrue((ROOT / "src/docs/user/tools" / filename).is_file())
                self.assertEqual(panel.status.text, translate(panel._status_message, language))
                self.assertEqual(panel.table.headers[0], translate("Interacción", language))
                self.assertEqual(panel.groups["hydrogen_bonds"].name, "PLIP · " + translate("Puente de hidrógeno", language))
                for before, after in zip(old, (panel.report, panel.model, panel.groups, panel.colors)):
                    self.assertIs(before, after)

    def test_packaged_examples_match_reference_and_csv_is_language_independent(self):
        expected = {
            "1VSN": ("NFT:A:283", {"hydrophobic_interactions": 4, "hydrogen_bonds": 7, "halogen_bonds": 2}),
            "1EVE": ("E20:A:2001", {"hydrophobic_interactions": 5, "hydrogen_bonds": 1,
                "water_bridges": 1, "pi_stacks": 2, "pi_cation_interactions": 1})}
        for name, (key, counts) in expected.items():
            for filename in ("report.xml", name + ".pdb"):
                self.assertEqual((ROOT / "src/examples" / name / filename).read_bytes(),
                                 (ROOT / "examples" / name / filename).read_bytes())
            report = parse_report((ROOT / "src/examples" / name / "report.xml").read_text())
            self.assertEqual(report.warnings, [])
            site = next(s for s in report.sites if s.key == key)
            self.assertEqual(dict(Counter(i.kind for i in site.interactions)), counts)
            before = csv_text(site)
            for lang in LANGUAGES:
                for row in site.interactions: translate(KINDS[row.kind][0], lang)
                self.assertEqual(csv_text(site), before)


if __name__ == "__main__": unittest.main(verbosity=2)
