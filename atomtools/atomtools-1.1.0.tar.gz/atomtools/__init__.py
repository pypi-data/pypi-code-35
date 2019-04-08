"""
independent chemical symbols
"""


__version__ = '1.1.0'
def version():
    return __version__


import os
BASEDIR = os.path.dirname(os.path.abspath(__file__))

# from atomtools.atomtools import get_distance_matrix, input_standard_pos_transform
from atomtools.tools import *

