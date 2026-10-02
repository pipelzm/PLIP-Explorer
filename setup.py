"""Build the pure-Python bundle without requiring ChimeraX on the build host."""
from setuptools import setup

setup(
    name="ChimeraX-PLIPExplorer", version="0.1.0a4",
    description="Native PLIP interaction explorer for UCSF ChimeraX (alpha)",
    long_description="Local PLIP analysis, XML import and native ChimeraX interaction visualization.",
    license="MIT", python_requires=">=3.10",
    packages=["chimerax.plip_explorer"],
    package_dir={"chimerax.plip_explorer": "src"},
    package_data={"chimerax.plip_explorer": ["docs/user/tools/*.html", "examples/*/*.pdb", "examples/*/*.xml"]},
    install_requires=["ChimeraX-Core", "ChimeraX-UI", "ChimeraX-Atomic", "ChimeraX-Markers", "ChimeraX-StdCommands", "ChimeraX-Label", "ChimeraX-PDB"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: ChimeraX",
        "Programming Language :: Python :: 3",
        "ChimeraX :: Bundle :: Structure Analysis :: 1,1 :: chimerax.plip_explorer :: ::",
        "ChimeraX :: Tool :: PLIP Explorer :: Structure Analysis :: Analyze and explore PLIP interactions",
    ],
)
