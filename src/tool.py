"""Dockable Qt interface for PLIP Explorer 0.1.0a4."""
from pathlib import Path
import json
import os
import tempfile
import threading
from datetime import datetime

from chimerax.core.tools import ToolInstance
from chimerax.core.settings import Settings
from chimerax.core.commands import run, StringArg
from chimerax.ui import MainToolWindow
from Qt.QtCore import Qt, QTimer
from Qt.QtGui import QColor, QBrush
from Qt.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QCheckBox, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QDoubleSpinBox, QGroupBox,
    QColorDialog, QAbstractItemView, QScrollArea, QWidget)

from .report import KINDS, parse_report, csv_text, validate_pdb
from .engine import run_plip, Cancelled
from . import render
from .i18n import LANGUAGES, message, translate


class ExplorerSettings(Settings):
    AUTO_SAVE = {"python_path": "", "output_dir": str(Path.home()/"Documents"/"PLIP_Explorer"),
                 "language": "es"}


class PLIPExplorer(ToolInstance):
    SESSION_ENDURING = False
    SESSION_SAVE = True
    help = "help:user/tools/plip_explorer.html"

    def __init__(self, session, tool_name="PLIP Explorer"):
        super().__init__(session, tool_name)
        self._alive = True
        self._busy = False
        self._cancel = None
        self.report = None
        self.model = None
        self.groups = {}
        self._digest = None
        self._stale = False
        self._run_dir = ""
        self._source_model = None
        self.colors = {k: list(v[1]) for k, v in KINDS.items()}
        self.settings = ExplorerSettings(session, "PLIP Explorer")
        self.language = self.settings.language if self.settings.language in LANGUAGES else "es"
        self.help = self.help_for_language()
        self._texts = []
        self._status_message = "Selecciona un complejo que contenga proteína y ligando."
        self.tool_window = MainToolWindow(self)
        self._build_ui()
        self.refresh_models()
        self.timer = QTimer(self.tool_window.ui_area)
        self.timer.timeout.connect(self.check_geometry)
        self.timer.start(2000)

    def tr(self, source, **values):
        return translate(source, self.language, **values)

    def help_for_language(self):
        suffix = "" if self.language == "es" else "_" + self.language
        return "help:user/tools/plip_explorer" + suffix + ".html"

    def text_widget(self, widget, source, method="setText"):
        self._texts.append((widget, source, method))
        getattr(widget, method)(self.tr(source))
        return widget

    def label(self, source):
        return self.text_widget(QLabel(), source)

    def button(self, source):
        return self.text_widget(QPushButton(), source)

    def checkbox(self, source):
        return self.text_widget(QCheckBox(), source)

    def set_status(self, source, **values):
        self._status_message = message(source, **values) if values else source
        self.status.setText(self.tr(self._status_message))

    def change_language(self, *args):
        self.language = self.language_combo.currentData()
        self.settings.language = self.language
        self.help = self.help_for_language()
        for widget, source, method in self._texts:
            getattr(widget, method)(self.tr(source))
        self.table.setHorizontalHeaderLabels([self.tr(s) for s in
            ("Interacción", "Residuo", "Distancia (Å)", "Ángulos (°)")])
        if self.report:
            index = self.site_combo.currentIndex()
            self.populate_sites(index)
            selected = self.table.currentRow()
            self.populate_table()
            if selected >= 0: self.table.selectRow(selected)
        # Change names only; preserve geometry, filters, colors and camera.
        for kind, group in self.groups.items():
            if not group.deleted:
                group.name = "PLIP · " + self.tr(KINDS[kind][0])
        self.status.setText(self.tr(self._status_message))

    def _build_ui(self):
        area = self.tool_window.ui_area
        outer = QVBoxLayout(area)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        content = QWidget(); layout = QVBoxLayout(content)
        scroll.setWidget(content); outer.addWidget(scroll)
        title = QLabel("PLIP Explorer · 0.1.0a4")
        title.setStyleSheet("font-size: 17px; font-weight: 600; margin-bottom: 4px;")
        layout.addWidget(title)
        language_row = QHBoxLayout()
        language_row.addWidget(self.label("Idioma"))
        self.language_combo = QComboBox()
        for code, name in LANGUAGES.items(): self.language_combo.addItem(name, code)
        self.language_combo.setCurrentIndex(self.language_combo.findData(self.language))
        language_row.addWidget(self.language_combo); language_row.addStretch(1)
        layout.addLayout(language_row)
        subtitle = self.label("Interacciones proteína–ligando · análisis local")
        layout.addWidget(subtitle)

        config = self.text_widget(QGroupBox(), "Análisis", "setTitle")
        form = QFormLayout(config)
        self.model_combo = QComboBox()
        row = QHBoxLayout(); row.addWidget(self.model_combo, 1)
        refresh = self.button("Actualizar"); refresh.clicked.connect(self.refresh_models)
        row.addWidget(refresh); form.addRow(self.label("Complejo"), row)
        self.python_path = QLineEdit(self.settings.python_path)
        self.text_widget(self.python_path, "Python del entorno PLIP", "setPlaceholderText")
        row = QHBoxLayout(); row.addWidget(self.python_path, 1)
        browse = self.button("Elegir…"); browse.clicked.connect(self.choose_python)
        row.addWidget(browse); form.addRow(self.label("Motor PLIP"), row)
        self.output_path = QLineEdit(self.settings.output_dir)
        row = QHBoxLayout(); row.addWidget(self.output_path, 1)
        browse_out = self.button("Carpeta…"); browse_out.clicked.connect(self.choose_output)
        row.addWidget(browse_out); form.addRow(self.label("Resultados"), row)
        self.protonate = self.checkbox("Añadir hidrógenos polares con PLIP")
        self.protonate.setChecked(True); form.addRow(self.protonate)
        layout.addWidget(config)

        row = QHBoxLayout()
        self.analyze_button = self.button("Analizar complejo")
        self.analyze_button.clicked.connect(self.analyze)
        self.cancel_button = self.button("Cancelar")
        self.cancel_button.setEnabled(False); self.cancel_button.clicked.connect(self.cancel)
        self.import_button = self.button("Importar XML + PDB…")
        self.import_button.clicked.connect(self.import_report)
        for widget in (self.analyze_button, self.cancel_button, self.import_button):
            row.addWidget(widget)
        layout.addLayout(row)
        row = QHBoxLayout()
        row.addWidget(self.label("Ejemplo"))
        self.example_combo = QComboBox()
        for name in ("1VSN", "1EVE"): self.example_combo.addItem(name)
        row.addWidget(self.example_combo)
        self.example_button = self.button("Cargar ejemplo")
        self.example_button.clicked.connect(self.load_example)
        row.addWidget(self.example_button); row.addStretch(1)
        layout.addLayout(row)
        example_note = self.label("Resultados precalculados; no requieren instalar PLIP.")
        example_note.setWordWrap(True); layout.addWidget(example_note)
        self.status = QLabel(self.tr(self._status_message))
        self.status.setWordWrap(True); layout.addWidget(self.status)

        self.site_combo = QComboBox()
        self.site_combo.currentIndexChanged.connect(self.draw)
        layout.addWidget(self.site_combo)
        filters = self.text_widget(QGroupBox(), "Mostrar interacciones", "setTitle")
        filters_layout = QVBoxLayout(filters)
        self.checkboxes = {}
        for kind, (name, color) in KINDS.items():
            row = QHBoxLayout()
            checkbox = self.checkbox(name); checkbox.setChecked(True)
            checkbox.toggled.connect(lambda checked, k=kind: self.filter_kind(k, checked))
            self.checkboxes[kind] = checkbox; row.addWidget(checkbox, 1)
            button = self.button("Color…")
            button.clicked.connect(lambda checked=False, k=kind: self.choose_color(k))
            row.addWidget(button); filters_layout.addLayout(row)
        layout.addWidget(filters)

        row = QHBoxLayout()
        row.addWidget(self.label("Radio de línea (Å)"))
        self.radius = QDoubleSpinBox(); self.radius.setRange(0.02, 0.3)
        self.radius.setDecimals(3); self.radius.setSingleStep(0.01); self.radius.setValue(0.055)
        row.addWidget(self.radius)
        self.distance_labels = self.checkbox("Distancias 3D")
        row.addWidget(self.distance_labels)
        style = self.button("Aplicar estilo"); style.clicked.connect(self.draw)
        row.addWidget(style); layout.addLayout(row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels([self.tr(s) for s in
            ("Interacción", "Residuo", "Distancia (Å)", "Ángulos (°)")])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setMinimumHeight(180)
        self.table.cellClicked.connect(self.focus)
        layout.addWidget(self.table, 1)
        note = self.label("Pulsa una fila para centrar y etiquetar sus residuos.\n"
                      "Las líneas representan el análisis guardado; no son un cálculo dinámico.")
        note.setWordWrap(True); layout.addWidget(note)

        row = QHBoxLayout()
        csv = self.button("Exportar CSV…"); csv.clicked.connect(self.export_csv)
        save = self.button("Guardar sesión…"); save.clicked.connect(self.save_session)
        logs = self.button("Ver bitácora"); logs.clicked.connect(self.show_log)
        for w in (csv, save, logs): row.addWidget(w)
        layout.addLayout(row)
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.tool_window.manage("side")

    def error(self, exc):
        self.set_status(exc)
        text = self.tr(exc)
        self.session.logger.warning("PLIP Explorer: " + text)
        QMessageBox.warning(self.tool_window.ui_area, "PLIP Explorer", text)

    def refresh_models(self):
        from chimerax.atomic import AtomicStructure
        old = self.model_combo.currentData()
        self.model_combo.clear()
        for model in self.session.models.list(type=AtomicStructure):
            self.model_combo.addItem(f"#{model.id_string} · {model.name}", model)
        for i in range(self.model_combo.count()):
            if self.model_combo.itemData(i) is old:
                self.model_combo.setCurrentIndex(i)

    def choose_python(self):
        path, _ = QFileDialog.getOpenFileName(self.tool_window.ui_area, self.tr("Seleccionar Python del entorno PLIP"),
                                            options=QFileDialog.Option.DontResolveSymlinks)
        if path: self.python_path.setText(path)

    def choose_output(self):
        path = QFileDialog.getExistingDirectory(self.tool_window.ui_area, self.tr("Carpeta de resultados"))
        if path: self.output_path.setText(path)

    def set_busy(self, busy):
        self._busy = busy
        self.analyze_button.setEnabled(not busy)
        self.import_button.setEnabled(not busy)
        self.example_button.setEnabled(not busy)
        self.cancel_button.setEnabled(busy)

    def analyze(self):
        if self._busy: return
        try:
            model = self.model_combo.currentData()
            if model is None or model.deleted:
                raise ValueError("Abre y selecciona un complejo molecular.")
            if any(len(r.chain_id) > 1 or r.number < -999 or r.number > 9999 for r in model.residues):
                raise ValueError("Esta versión necesita cadenas de un carácter y numeración compatible con PDB.")
            if model.num_atoms > 99999:
                raise ValueError("Selecciona un complejo de menos de 100 000 átomos.")
            python = self.python_path.text().strip()
            if not Path(python).expanduser().is_file():
                raise ValueError("Configura la ruta al Python del entorno PLIP (consulta la guía).")
            self.settings.python_path = python
            root = Path(self.output_path.text()).expanduser()
            root.mkdir(parents=True, exist_ok=True)
            self.settings.output_dir = str(root)
            directory = Path(tempfile.mkdtemp(prefix=datetime.now().strftime("%Y%m%d_%H%M%S_"), dir=root))
            self._run_dir = str(directory)
            self._source_model = model
            input_pdb = directory / "input.pdb"
            # Export this atomic model only, never child marker/pseudobond models
            # left by an earlier analysis. Include only the current coordinate set.
            from chimerax.pdb.pdb import save_pdb
            save_pdb(self.session, str(input_pdb), models=[model], all_coordsets=False)
            validate_pdb(input_pdb.read_text(encoding="utf-8"))
            protonate = self.protonate.isChecked()
            self._cancel = threading.Event()
            cancel_event = self._cancel
            self.set_busy(True)
            self.set_status("PLIP está analizando el complejo… Puedes seguir usando ChimeraX.")
            def worker():
                try:
                    result = run_plip(python, input_pdb, directory, cancel_event, protonate)
                    callback = lambda result=result: self.finished(result, None)
                except Exception as exc:
                    callback = lambda exc=exc: self.finished(None, exc)
                if self._alive:
                    self.session.ui.thread_safe(callback)
            threading.Thread(target=worker, name="PLIP Explorer", daemon=True).start()
        except Exception as exc:
            self.set_busy(False); self.error(exc)

    def cancel(self):
        if self._cancel:
            self._cancel.set()
            self.set_status("Cancelando PLIP…")

    def finished(self, result, error):
        if not self._alive: return
        self.set_busy(False)
        if isinstance(error, Cancelled):
            self.set_status("Análisis cancelado. La bitácora se conserva.")
        elif error:
            self.error(error)
        else:
            try:
                self.load_result(*result)
                if self._source_model is not None and not self._source_model.deleted:
                    self._source_model.display = False
            except Exception as exc: self.error(exc)

    def import_report(self):
        xml, _ = QFileDialog.getOpenFileName(self.tool_window.ui_area, self.tr("Informe PLIP"), filter="PLIP XML (*.xml)")
        if not xml: return
        try:
            report = parse_report(Path(xml).read_text(encoding="utf-8"))
            pdb, _ = QFileDialog.getOpenFileName(self.tool_window.ui_area,
                self.tr("PDB original/corregido utilizado por PLIP"), str(Path(xml).parent), "PDB (*.pdb)")
            if not pdb: return
            self.load_result(report, Path(pdb))
            self._run_dir = str(Path(xml).parent)
        except Exception as exc: self.error(exc)

    def load_example(self):
        if self._busy: return
        name = self.example_combo.currentText()
        if name not in ("1VSN", "1EVE"): return
        try:
            directory = Path(__file__).parent / "examples" / name
            report = parse_report((directory / "report.xml").read_text(encoding="utf-8"))
            self.load_result(report, directory / (name + ".pdb"))
            self._run_dir = str(directory)
            self.session.logger.info(self.tr("Ejemplo precalculado {name}: no se ejecutó el motor PLIP.", name=name))
            if self.model is not None: run(self.session, "view " + self.model.atomspec, log=False)
        except Exception as exc: self.error(exc)

    def load_result(self, report, pdb):
        from chimerax.atomic import AtomicStructure
        opened = run(self.session, f"open {StringArg.unparse(str(pdb))}")
        models = [m for m in opened if isinstance(m, AtomicStructure)]
        if len(models) != 1:
            self.session.models.close(opened)
            raise ValueError("Se requiere un único modelo en el PDB analizado.")
        model = models[0]
        try:
            for site in report.sites:
                render.validate_scene(model, site)
        except Exception:
            self.session.models.close(opened); raise
        render.close_groups(self.session, self.groups)
        self.groups = {}
        model.name = "PLIP · " + self.tr("estructura analizada")
        self.model = model; self.report = report
        self._digest = render.fingerprint(model); self._stale = False
        self.populate_sites()
        for warning in report.warnings: self.session.logger.warning(self.tr(warning))
        self.refresh_models()
        if self.report.sites: self.draw()
        else: self.set_status("PLIP no detectó ligandos analizables. Consulta plip.log.")

    def populate_sites(self, index=0):
        self.site_combo.blockSignals(True)
        self.site_combo.clear()
        for site in self.report.sites:
            self.site_combo.addItem(self.tr("{site} · {count} interacciones", site=site.key, count=len(site.interactions)))
        self.site_combo.setCurrentIndex(index)
        self.site_combo.blockSignals(False)

    def current_site(self):
        index = self.site_combo.currentIndex()
        return self.report.sites[index] if self.report and 0 <= index < len(self.report.sites) else None

    def draw(self, *args):
        site = self.current_site()
        if site is None: return
        try:
            self.check_geometry()
            if self._stale:
                raise ValueError("La geometría cambió o el modelo se cerró. Ejecuta un nuevo análisis.")
            # Validate before replacing an existing valid scene.
            render.validate_scene(self.model, site)
            new_groups = render.build_scene(self.session, self.model, site, self.colors,
                                            self.radius.value(), self.distance_labels.isChecked(), self.language)
            render.close_groups(self.session, self.groups)
            self.groups = new_groups
            for kind, cb in self.checkboxes.items(): self.filter_kind(kind, cb.isChecked())
            self.populate_table()
            warnings = message(" · {count} advertencias (Log)", count=len(self.report.warnings)) if self.report.warnings else ""
            self.set_status("PLIP {version} · {count} interacciones{warnings}",
                            version=self.report.version, count=len(site.interactions), warnings=warnings)
        except Exception as exc: self.error(exc)

    def populate_table(self):
        site = self.current_site()
        self._rows = site.interactions if site else []
        self.table.setRowCount(len(self._rows))
        for i, interaction in enumerate(self._rows):
            distance = interaction.distance
            if interaction.kind == "pi_stacks":
                distance = self.tr("Centros {distance}", distance=interaction.data.get("centdist", interaction.data.get("cent_dist", "?")))
            for j, value in enumerate((self.tr(KINDS[interaction.kind][0]), interaction.residue,
                                       distance, interaction.angle)):
                item = QTableWidgetItem(value)
                if j == 0: item.setForeground(QBrush(QColor(*self.colors[interaction.kind])))
                item.setToolTip(json.dumps(interaction.data, ensure_ascii=False, indent=2))
                self.table.setItem(i, j, item)
            self.table.setRowHidden(i, not self.checkboxes[interaction.kind].isChecked())
        self.table.resizeColumnsToContents()

    def filter_kind(self, kind, checked):
        model = self.groups.get(kind)
        if model is not None and not model.deleted:
            model.display = checked and not self._stale
        for i, row in enumerate(getattr(self, "_rows", [])):
            if row.kind == kind: self.table.setRowHidden(i, not checked)

    def choose_color(self, kind):
        color = QColorDialog.getColor(QColor(*self.colors[kind]), self.tool_window.ui_area)
        if color.isValid():
            self.colors[kind] = list(color.getRgb())
            self.draw()

    def focus(self, row, column):
        self.check_geometry()
        if self._stale: return
        try: render.focus_row(self.session, self.model, self.current_site(), self._rows[row])
        except Exception as exc: self.error(exc)

    def check_geometry(self):
        if self.report is None or self._stale: return
        if render.fingerprint(self.model) != self._digest:
            self._stale = True
            for model in self.groups.values():
                if not model.deleted: model.display = False
            self.set_status("Geometría o numeración modificada: interacciones ocultas. Vuelve a analizar.")

    def export_csv(self):
        site = self.current_site()
        if site is None: return
        self.check_geometry()
        if self._stale:
            self.error("Recalcula el análisis antes de exportar una estructura modificada."); return
        path, _ = QFileDialog.getSaveFileName(self.tool_window.ui_area, self.tr("Exportar interacciones"), "plip_interactions.csv", "CSV (*.csv)")
        if path:
            try: Path(path).write_text(csv_text(site), encoding="utf-8-sig")
            except Exception as exc: self.error(exc)

    def save_session(self):
        path, _ = QFileDialog.getSaveFileName(self.tool_window.ui_area, self.tr("Guardar sesión ChimeraX"), "plip_session.cxs", "ChimeraX (*.cxs)")
        if path:
            try: run(self.session, "save " + StringArg.unparse(path))
            except Exception as exc: self.error(exc)

    def show_log(self):
        if not self._run_dir:
            self.set_status("Todavía no hay una ejecución."); return
        logfile = Path(self._run_dir)/"plip.log"
        self.session.logger.info(self.tr("Resultados PLIP: {path}", path=self._run_dir))
        if logfile.is_file():
            self.session.logger.info(logfile.read_text(encoding="utf-8", errors="replace")[-30000:])
        run(self.session, "ui tool show Log", log=False)

    def take_snapshot(self, session, flags):
        self.check_geometry()
        return {"version": 1, "xml": self.report.xml if self.report else None,
                "model": self.model, "groups": self.groups, "digest": self._digest,
                "stale": self._stale, "site": self.site_combo.currentIndex(),
                "colors": self.colors, "radius": self.radius.value(),
                "labels": self.distance_labels.isChecked(), "run_dir": self._run_dir,
                "filters": {k: cb.isChecked() for k, cb in self.checkboxes.items()}}

    @classmethod
    def restore_snapshot(cls, session, data):
        tool = cls(session)
        if data.get("version") != 1:
            raise ValueError("Versión de sesión PLIP Explorer no compatible.")
        tool.model = data.get("model"); tool.groups = data.get("groups", {})
        tool._digest = data.get("digest"); tool._stale = data.get("stale", False)
        tool.colors = data.get("colors", tool.colors)
        tool.radius.setValue(data.get("radius", 0.055))
        tool.distance_labels.setChecked(data.get("labels", False))
        tool._run_dir = data.get("run_dir", "")
        if data.get("xml"):
            tool.report = parse_report(data["xml"]); tool.populate_sites()
            tool.site_combo.blockSignals(True)
            tool.site_combo.setCurrentIndex(data.get("site", 0))
            tool.site_combo.blockSignals(False)
            for kind, value in data.get("filters", {}).items():
                if kind in tool.checkboxes: tool.checkboxes[kind].setChecked(value)
            tool.populate_table()
            tool.set_status("Sesión PLIP restaurada." if not tool._stale else "Análisis desactualizado; vuelve a analizar.")
        return tool

    def delete(self):
        self._alive = False
        self.timer.stop()
        if self._cancel: self._cancel.set()
        super().delete()
