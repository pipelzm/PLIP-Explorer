# PLIP Explorer — Guide rapide

## Installation

Installez dist/chimerax_plipexplorer-0.1.0a4-py3-none-any.whl avec toolshed install dans ChimeraX. Quittez complètement ChimeraX, puis relancez-le. Ouvrez l’outil avec : ui tool show "PLIP Explorer".

## Langue

Choisissez Français dans le sélecteur de langue en haut du panneau. Le choix est mémorisé. Le changement de langue conserve le rapport, le site sélectionné, les filtres, les couleurs et la position de la caméra. Les identifiants scientifiques et les données exportées restent inchangés.

## Exemple sans installer PLIP

Choisissez Exemple → 1VSN → Charger l’exemple. Le site NFT:A:283 contient 13 interactions : 4 contacts hydrophobes, 7 liaisons hydrogène et 2 liaisons halogène. Décochez Liaison hydrogène : il doit rester 6 lignes visibles. Cochez-la de nouveau, puis cliquez sur une ligne pour centrer les résidus. Activez Distances 3D et cliquez sur Appliquer le style pour afficher les distances.

## Autre vérification

Dans 1EVE, E20:A:2001 contient 10 interactions : 5 contacts hydrophobes, 1 liaison hydrogène, 1 pont d’eau, 2 empilements π–π et 1 interaction cation–π. Chaque exemple ouvre un modèle distinct. Masquez le précédent si les structures se superposent. Le CSV inclut toutes les interactions du site, même les catégories masquées.

## Analyser vos complexes

Pour effectuer de nouveaux calculs, PLIP nécessite un environnement Python séparé. Indiquez son exécutable Python dans Moteur PLIP. Ouvrez un complexe compatible avec le format PDB contenant protéine et ligand, puis cliquez sur Analyser le complexe. Consultez README_ES.md pour la configuration. Les exemples sont précalculés et n’exécutent pas PLIP. De nouveaux calculs peuvent varier selon la protonation, la préparation et la version de PLIP.

## État des vérifications

L’utilisateur a confirmé l’ouverture de la version 0.1.0a2 dans ChimeraX 1.12 sur macOS M1. L’affichage et les nouvelles langues de la version 0.1.0a4 restent à vérifier dans cet environnement. Les boîtes de dialogue natives et les messages externes de PLIP, Open Babel ou ChimeraX peuvent conserver leur propre langue.
