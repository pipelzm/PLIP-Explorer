"""Scientific data/engine regression tests. Does not emulate ChimeraX GUI."""
import csv
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import types
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
# Load the independent core without executing the ChimeraX bundle initializer.
package = types.ModuleType("plip_test_core")
package.__path__ = [str(ROOT / "src")]
sys.modules[package.__name__] = package
from plip_test_core.report import (parse_report, KINDS, GROUP_KINDS,
    check_points, validate_pdb, csv_text)
from plip_test_core.engine import command, run_plip, Cancelled
from plip_test_core.render import validate_scene


def structure(path):
    """Read fixture coordinates for validation only; not a ChimeraX mock."""
    atoms = []
    for line in Path(path).read_text().splitlines():
        if line.startswith(("ATOM  ", "HETATM")):
            atoms.append(types.SimpleNamespace(serial_number=int(line[6:11]),
                coord=tuple(float(line[a:b]) for a, b in ((30,38),(38,46),(46,54)))))
    class Coordinates(list):
        @property
        def coords(self): return [a.coord for a in self]
    return types.SimpleNamespace(atoms=Coordinates(atoms))


def synthetic_report():
    root = ET.Element("report")
    ET.SubElement(root, "plipversion").text = "synthetic-test"
    bs = ET.SubElement(root, "bindingsite")
    ids = ET.SubElement(bs, "identifiers")
    for k, v in {"hetid":"LIG", "chain":"A", "position":"2"}.items():
        ET.SubElement(ids,k).text = v
    interactions = ET.SubElement(bs, "interactions")
    for kind in KINDS:
        node = ET.SubElement(ET.SubElement(interactions,kind),"interaction")
        d = {"resnr":"1", "reschain":"A", "restype":"ASP", "dist":"3.00",
             "dist_d-a":"3.00", "dist_h-a":"2.00", "dist_a-w":"2.50", "dist_d-w":"2.70",
             "centdist":"3.00", "don_angle":"160.00"}
        for k, v in d.items(): ET.SubElement(node,k).text = v
        for name, point in {"ligcoo":(0,0,0),"protcoo":(3,0,0),"watercoo":(1,2,0),
                            "metalcoo":(0,0,0),"targetcoo":(3,0,0)}.items():
            c = ET.SubElement(node,name)
            for k, v in zip("xyz",point): ET.SubElement(c,k).text = str(v)
    return ET.tostring(root,encoding="unicode")


class ReportTests(unittest.TestCase):
    def test_eight_types_and_no_lost_rows(self):
        report = parse_report(synthetic_report())
        self.assertEqual({r.kind for r in report.sites[0].interactions}, set(KINDS))
        self.assertFalse(report.warnings)

    def test_water_uses_two_legs(self):
        row = next(r for r in parse_report(synthetic_report()).sites[0].interactions if r.kind == "water_bridges")
        self.assertEqual(row.segments, (((0.,0.,0.),(1.,2.,0.)),((1.,2.,0.),(3.,0.,0.))))
        self.assertIn("A–W 2.50",row.distance)
        self.assertIn("D–W 2.70",row.distance)

    def test_hbond_reports_donor_acceptor_distance(self):
        row = next(r for r in parse_report(synthetic_report()).sites[0].interactions if r.kind == "hydrogen_bonds")
        self.assertEqual(row.distance, "D–A 3.00")

    def test_nonfinite_is_reported_and_omitted(self):
        report = parse_report(synthetic_report().replace("<x>0</x>","<x>nan</x>",1))
        self.assertEqual(len(report.sites[0].interactions),7)
        self.assertEqual(len(report.warnings),1)

    def test_unknown_type_is_not_silently_ignored(self):
        xml = synthetic_report().replace("</interactions>","<unknown><interaction/></unknown></interactions>")
        self.assertIn("no implementada",parse_report(xml).warnings[0])

    def test_wrong_xml_and_entities_rejected(self):
        for xml in ("<other/>","<!DOCTYPE report><report/>"):
            with self.assertRaises(ValueError): parse_report(xml)

    def test_empty_site_preserved(self):
        report = parse_report('<report><bindingsite><identifiers/><interactions/></bindingsite></report>')
        self.assertEqual(len(report.sites),1)
        self.assertEqual(len(report.sites[0].interactions),0)

    def test_1vsn_real_report_coordinate_identity(self):
        d = ROOT/"examples"/"1VSN"
        report = parse_report((d/"report.xml").read_text())
        model = structure(d/"1VSN.pdb")
        self.assertEqual(len(report.sites[0].interactions),13)
        self.assertEqual(check_points(report.sites[0],model.atoms.coords),(26,[]))
        validate_scene(model,report.sites[0])

    def test_1eve_real_report_group_centers(self):
        d = ROOT/"examples"/"1EVE"
        report = parse_report((d/"report.xml").read_text())
        model = structure(d/"1EVE.pdb")
        e20 = next(s for s in report.sites if s.key == "E20:A:2001")
        self.assertEqual(len(e20.interactions),10)
        self.assertEqual(sum(r.kind in GROUP_KINDS for r in e20.interactions),3)
        for site in report.sites: validate_scene(model,site)

    def test_mismatched_pdb_rejected(self):
        d = ROOT/"examples"/"1VSN"
        site = parse_report((d/"report.xml").read_text()).sites[0]
        model = structure(d/"1VSN.pdb")
        for atom in model.atoms: atom.coord = tuple(v+10 for v in atom.coord)
        with self.assertRaises(ValueError): validate_scene(model,site)

    def test_bad_center_rejected(self):
        d = ROOT/"examples"/"1EVE"
        report = parse_report((d/"report.xml").read_text())
        site = next(s for s in report.sites if s.key == "E20:A:2001")
        row = next(r for r in site.interactions if r.kind == "pi_stacks")
        row.points = ((999.,999.,999.),row.points[1])
        with self.assertRaises(ValueError): validate_scene(structure(d/"1EVE.pdb"),site)

    def test_csv_complete_and_unicode(self):
        site = parse_report(synthetic_report()).sites[0]
        rows = list(csv.reader(io.StringIO(csv_text(site))))
        self.assertEqual(len(rows),9)
        self.assertEqual(len(rows[0]),6)

    def test_input_scope_validation(self):
        good = (ROOT/"examples"/"1VSN"/"1VSN.pdb").read_text()
        validate_pdb(good)
        lines = good.splitlines()
        i = next(i for i,s in enumerate(lines) if s.startswith("ATOM  "))
        for column in (16,26):
            edited = list(lines); s = edited[i]; edited[i] = s[:column]+"A"+s[column+1:]
            with self.assertRaises(ValueError): validate_pdb("\n".join(edited))
        with self.assertRaises(ValueError): validate_pdb("HEADER empty\n")


class EngineTests(unittest.TestCase):
    def test_python_symlink_keeps_venv_path(self):
        with tempfile.TemporaryDirectory() as d:
            executable = Path(d)/"python"
            try: executable.symlink_to(sys.executable)
            except OSError: self.skipTest("Symlinks unavailable")
            args = command(str(executable),"input.pdb",d)
            self.assertEqual(args[0],str(executable))
            self.assertIn("--name",args)
            self.assertEqual(args[args.index("--name")+1],"report")

    def test_nohydro_and_spaces_are_separate_arguments(self):
        args = command(sys.executable,"space input.pdb","space output",False)
        self.assertTrue(args[-1] == "--nohydro")
        self.assertEqual(args[args.index("-f")+1],str(Path("space input.pdb").resolve()))

    def test_existing_result_protected(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/"report.xml").write_text("old")
            with self.assertRaises(ValueError):
                run_plip(sys.executable,"missing.pdb",d,threading.Event())

    @unittest.skipUnless(os.name == "posix", "POSIX subprocess fixture")
    def test_cancel_and_timeout_terminate_process(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            # Dedicated test executable; the production runner always uses shell=False.
            exe=d/"slow_python"
            exe.write_text(f'#!{sys.executable}\nimport time\ntime.sleep(30)\n')
            exe.chmod(0o755)
            inp=d/"input.pdb"; shutil.copy2(ROOT/"examples"/"1VSN"/"1VSN.pdb",inp)
            cancel=threading.Event();cancel.set()
            with self.assertRaises(Cancelled): run_plip(exe,inp,d/"cancel",cancel)
            with self.assertRaises(TimeoutError): run_plip(exe,inp,d/"timeout",threading.Event(),timeout=0.05)

    @unittest.skipUnless(os.environ.get("PLIP_TEST_PYTHON"), "Set PLIP_TEST_PYTHON for actual PLIP execution")
    def test_actual_engine_matches_independent_plip_nohydro(self):
        import json
        python = os.environ["PLIP_TEST_PYTHON"]
        with tempfile.TemporaryDirectory(prefix="plip test spaces ") as d:
            d=Path(d);source=ROOT/"examples"/"1VSN"/"1VSN.pdb"
            out=d/"plugin";out.mkdir();inp=out/"input.pdb";shutil.copy2(source,inp)
            report,pdb=run_plip(python,inp,out,threading.Event(),protonate=False)
            independent=d/"independent";independent.mkdir()
            subprocess.run([python,"-I","-m","plip.plipcmd","-f",str(inp),"-x","--name","report",
                            "-o",str(independent),"--nohydro"],check=True,capture_output=True)
            direct=parse_report((independent/"report.xml").read_text())
            self.assertEqual([(s.key,[r.data for r in s.interactions]) for s in report.sites],
                             [(s.key,[r.data for r in s.interactions]) for s in direct.sites])
            self.assertEqual(json.loads((out/"run.json").read_text())["status"],"complete")
            self.assertTrue(pdb.is_file())


if __name__ == "__main__": unittest.main(verbosity=2)
