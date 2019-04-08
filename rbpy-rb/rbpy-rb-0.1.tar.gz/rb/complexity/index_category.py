from enum import Enum

from rb.complexity.surface.factory import create as surface
from rb.complexity.syntax.factory import create as syntax


class IndexCategory(Enum):
    SURFACE: surface
    SYNTAX: syntax
