from .blob import Variable, Tensor
from . import layer as nn
from .net import *

forward = sm.forward
optimize = sm.optimize
update = sm.update


def Session():
    """Use Session to imitation the tensorflow"""
    return sm


from .layers import *
from .ops import *
from . import contrib
