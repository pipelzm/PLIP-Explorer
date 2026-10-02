"""Local PLIP execution with cancellation, timeout and durable run folders."""
import json
import os
from pathlib import Path
import subprocess
import time
from .report import parse_report, validate_pdb
from .i18n import message


class Cancelled(RuntimeError):
    pass


def command(python, input_pdb, output_dir, protonate=True):
    python = Path(python).expanduser()
    if not python.is_file():
        raise ValueError("Selecciona el ejecutable Python del entorno que contiene PLIP.")
    # Keep the venv executable path: resolving its symlink would select the
    # system interpreter and lose the PLIP environment.
    args = [os.path.abspath(python), "-I", "-m", "plip.plipcmd", "-f",
            str(Path(input_pdb).resolve()), "-x", "--name", "report", "-o", str(Path(output_dir).resolve())]
    if not protonate:
        args.append("--nohydro")
    return args


def run_plip(python, input_pdb, output_dir, cancel, protonate=True, timeout=600):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    if (output / "report.xml").exists():
        raise ValueError("La carpeta ya contiene un informe; usa una carpeta de ejecución nueva.")
    validate_pdb(Path(input_pdb).read_text(encoding="utf-8"))
    args = command(python, input_pdb, output_dir, protonate)
    env = dict(os.environ)
    for key in ("PYTHONHOME", "PYTHONPATH", "LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH"):
        env.pop(key, None)
    started = time.monotonic()
    provenance = {"command": args, "protonate": protonate, "timeout_seconds": timeout,
                  "input": str(Path(input_pdb).resolve()), "status": "running"}
    manifest = output / "run.json"
    manifest.write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    try:
        with (output / "plip.log").open("w", encoding="utf-8") as log:
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            with subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT,
                                  stdin=subprocess.DEVNULL, env=env, shell=False,
                                  cwd=str(output), creationflags=flags) as proc:
                try:
                    while proc.poll() is None:
                        if cancel.wait(0.15):
                            raise Cancelled("Análisis cancelado.")
                        if time.monotonic() - started > timeout:
                            raise TimeoutError(message("PLIP superó {seconds} segundos.", seconds=timeout))
                except BaseException:
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        proc.kill(); proc.wait()
                    raise
                if proc.returncode:
                    raise RuntimeError(message("PLIP terminó con código {code}. Revisa {path}", code=proc.returncode, path=output / 'plip.log'))
        if cancel.is_set():
            raise Cancelled("Análisis cancelado.")
        xml_path = output / "report.xml"
        if not xml_path.is_file():
            raise RuntimeError("PLIP no produjo report.xml. Revisa plip.log.")
        report = parse_report(xml_path.read_text(encoding="utf-8"))
        # Use the exact corrected input named by PLIP, not a possibly renumbered
        # OpenBabel protonated export. Report endpoints are heavy-atom coordinates.
        analyzed = Path(report.pdbfile)
        if not analyzed.is_absolute():
            analyzed = output / analyzed
        allowed = output.resolve()
        if not analyzed.is_file() or not analyzed.resolve().is_relative_to(allowed):
            if report.pdbfile and Path(report.pdbfile).resolve() == Path(input_pdb).resolve():
                analyzed = Path(input_pdb)
            else:
                raise RuntimeError("No se encontró la estructura exacta indicada por PLIP.")
        provenance.update(status="complete", plip_version=report.version,
                          analyzed_pdb=str(analyzed), warnings=report.warnings)
        return report, analyzed
    except Exception as exc:
        provenance.update(status="cancelled" if isinstance(exc, Cancelled) else "failed", error=str(exc))
        raise
    finally:
        provenance["elapsed_seconds"] = round(time.monotonic()-started, 3)
        manifest.write_text(json.dumps(provenance, indent=2), encoding="utf-8")
