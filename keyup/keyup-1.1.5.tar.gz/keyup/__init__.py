from keyup._version import __version__ as version

__author__ = 'Blake Huber'
__version__ = version
__email__ = "blakeca00@gmail.com"

from keyup import logd

# global logger
logger = logd.getLogger(__version__)
