from ._version import get_versions
from .contexts import cd
from .prompting import error, prompt, status, success
from .unix import cp, ln_s

__all__ = ["prompt", "status", "success", "error", "cp", "cd", "ln_s"]


__version__ = get_versions()["version"]
del get_versions
