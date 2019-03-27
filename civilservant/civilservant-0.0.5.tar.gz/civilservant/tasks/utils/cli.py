from invoke.program import Program

from .namespace import namespace
from ... import __version__


program = Program(
    name="CivilServant Library Loader",
    namespace=namespace,
    binary="cs",
    version=__version__.__version__
)

