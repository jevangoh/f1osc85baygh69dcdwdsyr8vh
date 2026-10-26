from importlib.metadata import version, PackageNotFoundError
from .f1osc85baygh69dcdwdsyr8vh import f1osc85baygh69dcdwdsyr8vh as _

try:
    __version__ = version("f1osc85baygh69dcdwdsyr8vh")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["_", "__version__"]
