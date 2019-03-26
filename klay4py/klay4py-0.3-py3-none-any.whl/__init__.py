from .__version__ import __title__, __description__, __url__, __copyright__
from .__version__ import __author__, __author_email__, __license__, __version__

from .jvm import init_jvm
from .klay import Klay

__all__ = ['jvm', 'Klay']