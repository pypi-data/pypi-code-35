import sys
from functools import partial

import numpy as np

from .util import generate_evenly_spaced_data_set
from .util import generate_uniform_data_set
from .util import generator_from_helper

"""
Sets of "Improving Symbolic Regression with Interval Arithmetic and Linear Scaling" by Maarten Keijzer
DOI: 10.1007/3-540-36599-0_7
"""


def keijzer_func4(x):
    return 0.3 * x * np.sin(2.0 * np.pi * x)


def keijzer_func5(x):
    sx = np.sin(x)
    cx = np.cos(x)
    return x ** 3 * np.exp(-x) * cx * sx * (sx ** 2 * cx - 1.0)


def keijzer_func6(x, y, z):
    return 30.0 * x * z / ((x - 10.0) * y ** 2)


def keijzer_func7(x):
    f = lambda n: sum(1.0 / i for i in range(1, int(n)))
    if any(x < 0):
        raise ValueError
    if isinstance(x, np.ndarray):
        return np.array([f(n) for n in x])
    else:
        return f(x)


def keijzer_func8(x):
    return np.log(x)


def keijzer_func9(x):
    return np.sqrt(x)


def keijzer_func10(x):
    return np.arcsinh(x)


def keijzer_func11(x, y):
    return x ** y


def keijzer_func12(x, y):
    return x * y + np.sin((x - 1.0) * (y - 1.0))


def keijzer_func13(x, y):
    return x ** 4 - x ** 3 + 0.5 * y ** 2 - y


def keijzer_func14(x, y):
    return 6.0 * np.sin(x) * np.cos(x)


def keijzer_func15(x, y):
    return 8.0 / (2.0 + x ** 2 + y ** 2)


def keijzer_func16(x, y):
    return x ** 3 / 3.0 + y ** 3 / 2.0 - y - x


def _keijzer1_3_helper(step, ranges):
    return generate_evenly_spaced_data_set(keijzer_func4, step, ranges)


def generate_keijzer1():
    ranges = (-1, 1)
    train = _keijzer1_3_helper(0.1, ranges)
    test = _keijzer1_3_helper(0.001, ranges)
    return train, test


def generate_keijzer2():
    ranges = (-2, 2)
    train = _keijzer1_3_helper(0.1, ranges)
    test = _keijzer1_3_helper(0.001, ranges)
    return train, test


def generate_keijzer3():
    ranges = (-4, 4)
    train = _keijzer1_3_helper(0.1, ranges)
    test = _keijzer1_3_helper(0.001, ranges)
    return train, test


def generate_keijzer4():
    train = generate_evenly_spaced_data_set(keijzer_func5, 0.05, (0, 10))
    test = generate_evenly_spaced_data_set(keijzer_func5, 0.05, (0.05, 10.05))
    return train, test


def generate_keijzer5(rng=np.random):
    ranges = [(-1, 1), (1, 2), (-1, 1)]
    train = generate_uniform_data_set(keijzer_func6, 1000, ranges, rng=rng)
    test = generate_uniform_data_set(keijzer_func6, 10000, ranges, rng=rng)
    return train, test


def generate_keijzer6():
    train = generate_evenly_spaced_data_set(keijzer_func7, 1.0, (1, 50))
    test = generate_evenly_spaced_data_set(keijzer_func7, 1.0, (1, 120))
    return train, test


def generate_keijzer7():
    train = generate_evenly_spaced_data_set(keijzer_func8, 1.0, (1, 100))
    test = generate_evenly_spaced_data_set(keijzer_func8, 0.01, (1, 100))
    return train, test


def generate_keijzer8():
    train = generate_evenly_spaced_data_set(keijzer_func9, 1.0, (0, 100))
    test = generate_evenly_spaced_data_set(keijzer_func9, 0.01, (0, 100))
    return train, test


def generate_keijzer9():
    train = generate_evenly_spaced_data_set(keijzer_func10, 1.0, (0, 100))
    test = generate_evenly_spaced_data_set(keijzer_func10, 0.01, (0, 100))
    return train, test


def generate_keijzer10(rng=np.random):
    train = generate_uniform_data_set(keijzer_func11, 100, (0, 1), rng=rng)
    test = generate_evenly_spaced_data_set(keijzer_func11, 0.01, (0, 1))
    return train, test


def _keijzer11_15_helper(func, rng=np.random):
    train = generate_uniform_data_set(func, 20, (-3, 3), rng=rng)
    test = generate_evenly_spaced_data_set(func, 0.01, (-3, 3))
    return train, test


generator_from_helper(_keijzer11_15_helper, shift=-1, i=list(range(12, 16)))

current_module = sys.modules[__name__]
all_problems = {name: getattr(current_module, name) for name in locals() if "generate_keijzer" in name}
