import math
from hanamusume.oglm_solver import OGLMSolver

def linear(x):
    return x
class LinearSolver(OGLMSolver):
    def __init__(self, *args, **kwargs):
        kwargs['pred'] = lambda dec: dec
        OGLMSolver.__init__(self, *args, **kwargs)

def sigmoid(x):
    return 1. / (1. + math.exp(-x))
class LogisticSolver(OGLMSolver):
    def __init__(self, *args, **kwargs):
        kwargs['pred'] = lambda dec: sigmoid(dec)
        OGLMSolver.__init__(self, *args, **kwargs)

def exponential(x):
    return math.exp(min(x,5))
class PoissonSolver(OGLMSolver):
    def __init__(self, *args, **kwargs):
        kwargs['pred'] = lambda dec: exponential(x)
        OGLMSolver.__init__(self, *args, **kwargs)
