import sys
from functools import partial

import numpy as np

from .util import generate_evenly_spaced_data_set
from .util import generate_uniform_data_set
from .util import generator_from_helper
from .util import poly


nguyen_func1 = partial(poly, i=3)
nguyen_func3 = partial(poly, i=5)
nguyen_func4 = partial(poly, i=6)


def nguyen_func5(x):
    return np.sin(x ** 2) * np.cos(x) - 1.0


def nguyen_func6(x):
    return np.sin(x) + np.sin(x + x ** 2)


def nguyen_func7(x):
    return np.log(x + 1) + np.log(x ** 2 + 1)


def nguyen_func8(x):
    return np.sqrt(x)


def nguyen_func9(x, y):
    return np.sin(x) + np.sin(y ** 2)


def nguyen_func10(x, y):
    return 2.0 * np.sin(x) * np.cos(y)


def _nguyen1_6_helper(func, rng=np.random):
    train = generate_uniform_data_set(func, 20, (-1, 1), rng=rng)
    test = generate_uniform_data_set(func, 20, (-1, 1), rng=rng)
    return train, test


generator_from_helper(_nguyen1_6_helper, i=(1, 3, 4, 5, 6))


def generate_nguyen7(rng=np.random):
    train = generate_uniform_data_set(nguyen_func7, 20, (0, 2), rng=rng)
    test = generate_uniform_data_set(nguyen_func7, 20, (0, 2), rng=rng)
    return train, test


def generate_nguyen8(rng=np.random):
    train = generate_uniform_data_set(nguyen_func8, 20, (0, 4), rng=rng)
    test = generate_uniform_data_set(nguyen_func8, 20, (0, 4), rng=rng)
    return train, test


def _nguyen9_10_helper(func, rng=np.random):
    train = generate_uniform_data_set(func, 100, (-1, 1), rng=rng)
    test = generate_uniform_data_set(func, 100, (-1, 1), rng=rng)
    return train, test


generator_from_helper(_nguyen9_10_helper, i=(9, 10))

current_module = sys.modules[__name__]
all_problems = {name: getattr(current_module, name) for name in locals() if "generate_nguyen" in name}
