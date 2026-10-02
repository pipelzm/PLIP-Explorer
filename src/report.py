"""PLIP XML reader. Standard library only; no ChimeraX or PLIP imports."""
from dataclasses import dataclass, field
import csv
import io
import math
import xml.etree.ElementTree as ET
from .i18n import message


KINDS = {
    "hydrophobic_interactions": ("Contacto hidrofóbico", (150, 150, 150, 255)),
    "hydrogen_bonds": ("Puente de hidrógeno", (55, 135, 240, 255)),
    "water_bridges": ("Puente de agua", (80, 200, 230, 255)),
    "salt_bridges": ("Puente salino", (235, 190, 30, 255)),
    "pi_stacks": ("Apilamiento π–π", (75, 190, 110, 255)),
    "pi_cation_interactions": ("Interacción catión–π", (245, 145, 45, 255)),
    "halogen_bonds": ("Enlace de halógeno", (30, 200, 160, 255)),
    "metal_complexes": ("Coordinación metálica", (175, 100, 220, 255)),
}
GROUP_KINDS = {"salt_bridges", "pi_stacks", "pi_cation_interactions"}


def _tree(node):
    if not list(node):
        return (node.text or "").strip()
    if all(c.tag == "idx" for c in node):
        return [int(c.text) for c in node]
    return {c.tag: _tree(c) for c in node}


def _coord(data, key):
    d = data[key]
    p = tuple(float(d[a]) for a in ("x", "y", "z"))
    if not all(math.isfinite(v) for v in p):
        raise ValueError("Coordenada no finita")
    return p


@dataclass
class Interaction:
    uid: str
    kind: str
    data: dict
    points: tuple

    @property
    def residue(self):
        d = self.data
        return f"{d.get('restype', '?')} {d.get('reschain', '')}:{d.get('resnr', '?')}"

    @property
    def distance(self):
        d = self.data
        if self.kind == "water_bridges":
            return f"A–W {d.get('dist_a-w', '?')}; D–W {d.get('dist_d-w', '?')}"
        if self.kind == "hydrogen_bonds":
            return f"D–A {d.get('dist_d-a', '?')}"
        if self.kind == "pi_stacks":
            return f"Centros {d.get('centdist', d.get('cent_dist', '?'))}"
        return d.get("dist", "?")

    @property
    def angle(self):
        return "; ".join(f"{key}: {self.data[key]}" for key in
                         ("don_angle", "acc_angle", "water_angle", "angle")
                         if key in self.data)

    @property
    def segments(self):
        # Water bridges are TWO legs, never a fictitious protein–ligand line.
        if self.kind == "water_bridges":
            return ((self.points[0], self.points[2]),
                    (self.points[2], self.points[1]))
        return ((self.points[0], self.points[1]),)


@dataclass
class Site:
    key: str
    identifiers: dict
    interactions: list = field(default_factory=list)


@dataclass
class Report:
    xml: str
    version: str
    pdbfile: str
    sites: list
    warnings: list


def parse_report(xml):
    if isinstance(xml, bytes):
        xml = xml.decode("utf-8-sig")
    if len(xml) > 30_000_000:
        raise ValueError("El XML supera el límite de 30 MB de esta versión.")
    if "<!DOCTYPE" in xml.upper() or "<!ENTITY" in xml.upper():
        raise ValueError("El informe no debe contener DTD ni entidades XML.")
    root = ET.fromstring(xml)
    if root.tag != "report":
        raise ValueError("No es un informe XML de PLIP (falta <report>).")
    sites, warnings = [], []
    for index, bs in enumerate(root.findall("bindingsite")):
        ident = _tree(bs.find("identifiers")) if bs.find("identifiers") is not None else {}
        if not isinstance(ident, dict):
            ident = {}
            warnings.append(message("Sitio {index}: faltan identificadores del ligando.", index=index + 1))
        key = ":".join(str(ident.get(k, "?")) for k in ("hetid", "chain", "position"))
        if any(s.key == key for s in sites):
            key += f" [sitio {index + 1}]"
        site = Site(key, ident)
        containers = bs.find("interactions")
        if containers is None:
            warnings.append(message("{key}: falta el bloque interactions.", key=key))
            containers = []
        for container in containers:
            if container.tag not in KINDS:
                if len(container):
                    warnings.append(message("Categoría no implementada: {kind}.", kind=container.tag))
                continue
            for n, entry in enumerate(container):
                uid = f"{index}:{container.tag}:{n}"
                try:
                    data = _tree(entry)
                    keys = ("metalcoo", "targetcoo") if container.tag == "metal_complexes" else ("ligcoo", "protcoo")
                    if container.tag == "water_bridges":
                        keys += ("watercoo",)
                    points = tuple(_coord(data, k) for k in keys)
                    for field_name in ("resnr", "restype", "reschain"):
                        if field_name not in data:
                            raise ValueError(message("Falta {field}", field=field_name))
                    site.interactions.append(Interaction(uid, container.tag, data, points))
                except (KeyError, ValueError, TypeError) as exc:
                    warnings.append(message("Interacción {uid} omitida: {error}", uid=uid, error=exc))
        sites.append(site)
    return Report(xml, root.findtext("plipversion", message("desconocida")),
                  root.findtext("pdbfile", ""), sites, warnings)


def csv_text(site):
    out = io.StringIO(newline="")
    writer = csv.writer(out)
    writer.writerow(["site", "interaction", "residue", "distance_A", "angles_deg", "PLIP_fields_json"])
    import json
    for row in site.interactions:
        writer.writerow([site.key, row.kind, row.residue, row.distance, row.angle,
                         json.dumps(row.data, ensure_ascii=False, sort_keys=True)])
    return out.getvalue()


def validate_pdb(text):
    """Fail clearly on inputs outside the first release's PDB scope."""
    records = [s for s in text.splitlines() if s.startswith(("ATOM  ", "HETATM"))]
    if not records:
        raise ValueError("La entrada no contiene átomos PDB.")
    if sum(s.startswith("MODEL ") for s in text.splitlines()) > 1:
        raise ValueError("Exporta un único modelo/conformación antes de analizar.")
    if len(records) > 99999:
        raise ValueError("Esta versión requiere un complejo de menos de 100 000 átomos.")
    if any(len(s) < 54 for s in records):
        raise ValueError("Registro PDB incompleto.")
    if any(s[16].strip() for s in records):
        raise ValueError("Resuelve las conformaciones alternativas y exporta una sola antes de analizar.")
    if any(s[26].strip() for s in records):
        raise ValueError("Esta versión requiere residuos sin códigos de inserción. Usa una copia renumerada.")
    for s in records:
        try:
            int(s[6:11]); int(s[22:26])
            xyz = [float(s[a:b]) for a, b in ((30, 38), (38, 46), (46, 54))]
            if not all(math.isfinite(v) for v in xyz):
                raise ValueError()
        except ValueError:
            raise ValueError("Numeración o coordenadas incompatibles con PDB estándar.") from None
    if not any(s.startswith("HETATM") and s[17:20].strip() not in {"HOH", "WAT", "DOD"} for s in records):
        raise ValueError("Falta un ligando en registros HETATM. El complejo debe incluir proteína y ligando.")


def check_points(site, coords, tolerance=0.025):
    """Validate atom endpoints against a structure; centers have no atom equivalent."""
    # Spatial hashing avoids an interactions × atoms distance matrix.
    from itertools import product
    cells = {}
    for xyz in coords:
        xyz = tuple(float(v) for v in xyz)
        cell = tuple(math.floor(v / tolerance) for v in xyz)
        cells.setdefault(cell, []).append(xyz)
    bad, checked = [], 0
    for row in site.interactions:
        if row.kind in GROUP_KINDS:
            continue
        for point in row.points:
            checked += 1
            cell = tuple(math.floor(v / tolerance) for v in point)
            candidates = (p for delta in product((-1, 0, 1), repeat=3)
                          for p in cells.get(tuple(a+b for a, b in zip(cell, delta)), []))
            if not any(math.dist(point, p) <= tolerance for p in candidates):
                bad.append(row.uid)
    return checked, sorted(set(bad))
