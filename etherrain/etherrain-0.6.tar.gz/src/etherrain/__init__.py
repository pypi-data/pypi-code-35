import sys

__version__ = "0.6"

__uri__ = 'https://github.com/hpeyerl/etherrain'
__title__ = "etherrain"
__description__ = 'Interface Library for QuickSmart Etherrain/8 irrigation controller'
__doc__ = __description__ + " <" + __uri__ + ">"
__author__ = 'Herb Peyerl'
__email__ = 'hpeyerl+etherrain@beer.org'
__license__ = "MIT"

__copyright__ = "Copyright (c) 2017 Herb Peyerl"

from .etherrain import EtherRain

if __name__ == '__main__': print(__version__)
