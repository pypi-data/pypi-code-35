import numpy as np
from toolz.itertoolz import iterate
from toolz.itertoolz import take

from .maps import all_maps


def generate_map_data(problem, x0, t, params):
    f = problem(params)
    x = take(iterate(f, x0), t + 1)
    x = np.array(x)
    return x[:-1], x[1:]
