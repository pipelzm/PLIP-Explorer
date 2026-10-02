# PLIP Explorer — Quick start

## Install 0.1.0a4

Install dist/chimerax_plipexplorer-0.1.0a4-py3-none-any.whl using toolshed install in ChimeraX. Quit ChimeraX completely and restart it. Open Tools → Structure Analysis → PLIP Explorer, or run: ui tool show "PLIP Explorer".

## Language

Choose English in the Language / Idioma selector. The preference is saved. Switching language preserves the loaded report, selected site, filters, colors and camera. Scientific identifiers and exported fields remain unchanged. Native file dialogs and external PLIP/Open Babel/ChimeraX messages may use their own language.

## Try it without installing PLIP

Select Example → 1VSN → Load example. The bundled precomputed report contains 13 interactions at NFT:A:283: 4 hydrophobic contacts, 7 hydrogen bonds and 2 halogen bonds. Disable Hydrogen bond: 6 rows should remain visible. Re-enable it and click a row to focus and label its residues. Turn on 3D distances and click Apply style to test distance labels.

## Second example

Load 1EVE and choose E20:A:2001. Expect 10 interactions: 5 hydrophobic contacts, 1 hydrogen bond, 1 water bridge, 2 π–π stacks and 1 cation–π interaction. Water bridges use two segments; aromatic interactions use group centers. Other ligand sites also appear in this report. Each example opens a separate structure; hide the previous model if they overlap.

## Check export and sessions

Export CSV should produce 13 data rows plus a header for the 1VSN site. CSV includes hidden interaction categories. Save a test .cxs session, reopen it and check the structure, table and filters. Session restoration and rendering still need testing in native ChimeraX.

## Analyze your own complex

Set PLIP engine to the Python executable of a separate environment containing PLIP and Open Babel. Obtain its path with: python -c "import sys; print(sys.executable)". See README_ES.md for environment setup. Open one PDB-compatible model containing both protein and ligand, Refresh, select the complex and click Analyze complex. A new results folder should contain report.xml, plip.log and run.json, with status complete and the PLIP version in run.json.

## What the test establishes

The examples test import and visualization; loading them does not run PLIP. The reported counts are exact for the bundled XML files. Fresh analyses may differ with protonation, preparation or engine version. The panel uses PLIP data and native ChimeraX graphics; it does not import PyMOL PSE or PML files. The user confirmed panel startup in version 0.1.0a2 on ChimeraX 1.12/macOS M1. The new interface and graphics in 0.1.0a4 still require testing there.
