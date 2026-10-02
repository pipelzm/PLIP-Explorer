# PLIP Explorer — Kurzanleitung

## Installation

Installieren Sie die Datei dist/chimerax_plipexplorer-0.1.0a4-py3-none-any.whl mit toolshed install in ChimeraX. Beenden Sie ChimeraX vollständig und starten Sie es neu. Öffnen Sie das Werkzeug mit: ui tool show "PLIP Explorer".

## Sprache

Wählen Sie Deutsch im Sprachmenü oben. Die Einstellung wird gespeichert. Ein Sprachwechsel erhält den geladenen Bericht, die ausgewählte Bindungsstelle, Filter, Farben und die Kameraposition. Wissenschaftliche Kennungen und exportierte Daten bleiben unverändert.

## Beispiel ohne PLIP-Installation

Wählen Sie Beispiel → 1VSN → Beispiel laden. NFT:A:283 enthält 13 Wechselwirkungen: 4 hydrophobe Kontakte, 7 Wasserstoffbrücken und 2 Halogenbindungen. Deaktivieren Sie Wasserstoffbrücke: 6 Tabellenzeilen sollten sichtbar bleiben. Aktivieren Sie die Kategorie wieder und klicken Sie auf eine Zeile, um die Reste zu zentrieren. Mit 3D-Abstände und Stil anwenden können Sie Abstandsangaben einblenden.

## Weitere Prüfung

Im Beispiel 1EVE enthält E20:A:2001 10 Wechselwirkungen: 5 hydrophobe Kontakte, 1 Wasserstoffbrücke, 1 Wasserbrücke, 2 π–π-Stapelungen und 1 Kation–π-Wechselwirkung. Jedes Beispiel öffnet ein separates Modell. Blenden Sie das vorherige Modell bei Überlagerungen aus. CSV exportiert alle Wechselwirkungen der Bindungsstelle, auch ausgeblendete Kategorien.

## Eigene Komplexe analysieren

Für neue Berechnungen benötigt PLIP eine separate Python-Umgebung. Geben Sie deren Python-Programmdatei unter PLIP-Engine an. Öffnen Sie einen PDB-kompatiblen Komplex mit Protein und Ligand und klicken Sie auf Komplex analysieren. Hinweise zur Einrichtung stehen in README_ES.md. Die Beispiele sind vorberechnet und führen PLIP nicht aus. Neue Ergebnisse können je nach Protonierung, Vorbereitung und PLIP-Version abweichen.

## Prüfstatus

Version 0.1.0a2 wurde vom Benutzer in ChimeraX 1.12 auf macOS M1 geöffnet. Die Darstellung und die neuen Sprachen der Version 0.1.0a4 müssen dort noch geprüft werden. Native Dateidialoge und externe Meldungen von PLIP, Open Babel oder ChimeraX können ihre eigene Sprache verwenden.
