"""Native ChimeraX scene objects, built only on the GUI thread."""
import hashlib
import math
from .report import KINDS, GROUP_KINDS, check_points
from .i18n import message, translate


def fingerprint(model):
    if model is None or model.deleted:
        return "closed"
    digest = hashlib.sha256(model.atoms.coords.tobytes())
    digest.update(str(model.num_atoms).encode())
    # Renumbering changes the table-to-residue mapping even if coordinates do not.
    digest.update(repr([(r.name, r.chain_id, r.number, r.insertion_code)
                        for r in model.residues]).encode())
    return digest.hexdigest()


def validate_scene(model, site):
    checked, bad = check_points(site, model.atoms.coords)
    if bad:
        raise ValueError(message("El PDB no coincide con {count} interacción(es) del XML. Selecciona la estructura analizada por PLIP.", count=len(bad)))
    serials = {}
    for atom in model.atoms:
        serials.setdefault(atom.serial_number, []).append(atom)
    for row in site.interactions:
        if row.kind not in GROUP_KINDS:
            continue
        for field, point in zip(("lig_idx_list", "prot_idx_list"), row.points):
            indices = row.data.get(field, [])
            if not indices or any(len(serials.get(n, [])) != 1 for n in indices):
                raise ValueError("El informe de grupos requiere IDs atómicos únicos y el PDB original/corregido de PLIP.")
            atoms = [serials[n][0] for n in indices]
            center = tuple(sum(float(a.coord[d]) for a in atoms)/len(atoms) for d in range(3))
            if math.dist(center, point) > 0.035:
                raise ValueError(message("No coincide el centro geométrico de {uid}. Usa el PDB original/corregido del informe.", uid=row.uid))


def residue_atoms(model, site, row=None):
    refs = set()
    extra_serials = set()
    for interaction in ([row] if row is not None else site.interactions):
        for field in ("water_idx", "metal_idx", "target_idx"):
            if interaction.data.get(field):
                extra_serials.add(int(interaction.data[field]))
    if row is not None:
        d = row.data
        refs.add((d.get("reschain", ""), str(d.get("resnr", ""))))
        refs.add((d.get("reschain_lig", ""), str(d.get("resnr_lig", ""))))
    else:
        for r in site.interactions:
            d = r.data
            refs.add((d.get("reschain", ""), str(d.get("resnr", ""))))
            refs.add((d.get("reschain_lig", ""), str(d.get("resnr_lig", ""))))
    ident = site.identifiers
    refs.add((ident.get("chain", ""), str(ident.get("position", ""))))
    from chimerax.atomic import Atoms
    return Atoms([a for r in model.residues for a in r.atoms
                  if (r.chain_id, str(r.number)) in refs or a.serial_number in extra_serials])


def show_pocket(session, model, site):
    from chimerax.core.commands import run
    run(session, f"hide {model.atomspec} atoms", log=False)
    run(session, f"cartoon {model.atomspec}", log=False)
    atoms = residue_atoms(model, site)
    if len(atoms):
        atoms.displays = True
        atoms.draw_modes = atoms[0].STICK_STYLE
        # Backbone atoms remain visible alongside cartoons.
        run(session, f"cartoon {model.atomspec} suppress false", log=False)


def build_scene(session, model, site, colors=None, radius=0.055, labels=False, language="es"):
    validate_scene(model, site)
    from chimerax.markers import MarkerSet
    from chimerax.core.commands import run
    groups = {}
    try:
        for kind, (title, default_color) in KINDS.items():
            rows = [r for r in site.interactions if r.kind == kind]
            if not rows:
                continue
            markers = MarkerSet(session, name="PLIP · " + translate(title, language))
            model.add([markers])
            groups[kind] = markers
            group = markers.pseudobond_group(translate("interacciones PLIP", language))
            group.dashes = 6
            rgba = tuple((colors or {}).get(kind, default_color))
            for row in rows:
                for p, q in row.segments:
                    # Marker coordinates are the actual PLIP endpoints, including
                    # group centers; they are not guessed from neighboring atoms.
                    a = markers.create_marker(p, rgba, 0.07)
                    b = markers.create_marker(q, rgba, 0.07)
                    pb = group.new_pseudobond(a, b)
                    pb.color = rgba
                    pb.halfbond = False
                    pb.radius = radius
            if labels:
                run(session, f"label {group.atomspec} pseudobonds", log=False)
        show_pocket(session, model, site)
        return groups
    except Exception:
        close_groups(session, groups)
        raise


def close_groups(session, groups):
    models = [m for m in groups.values() if not m.deleted]
    if models:
        session.models.close(models)


def focus_row(session, model, site, row):
    from chimerax.core.commands import run
    session.selection.clear()
    atoms = residue_atoms(model, site, row)
    if not len(atoms):
        return
    atoms.selecteds = True
    atoms.displays = True
    run(session, "view sel", log=False)
    run(session, "label sel residues", log=False)
