"""
independent chemical symbols
"""


__version__ = '1.0.0'
def version():
    return __version__


import os
BASEDIR = os.path.dirname(os.path.abspath(__file__))

from atomtools.atomtools import *
