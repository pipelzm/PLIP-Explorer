"""PLIP Explorer: a native ChimeraX bundle."""
from chimerax.core.toolshed import BundleAPI


class _API(BundleAPI):
    # No custom lifecycle initialization is needed. The bundle metadata must
    # leave customInit unset; GUI imports occur only when the tool is opened.
    api_version = 1

    @staticmethod
    def start_tool(session, bi, ti):
        from .tool import PLIPExplorer
        return PLIPExplorer(session, ti.name)

    @staticmethod
    def get_class(class_name):
        if class_name == "PLIPExplorer":
            from .tool import PLIPExplorer
            return PLIPExplorer
        raise ValueError(f"Clase desconocida: {class_name}")


bundle_api = _API()
