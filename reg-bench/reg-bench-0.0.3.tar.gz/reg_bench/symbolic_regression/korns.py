import sys
from functools import partial

import numpy as np

from .util import generate_uniform_data_set
from .util import generator_from_helper


"""
Sets of "Accuracy in Symbolic Regression" by Korns
DOI: 10.1007/978-1-4614-1770-5_8
"""


def korns_func1(x0, x1, x2, x3, x4):
    return 1.57 + 24.3 * x3


def korns_func2(x0, x1, x2, x3, x4):
    return 0.23 + 14.2 * (x3 + x1) / (3.0 * x4)


def korns_func3(x0, x1, x2, x3, x4):
    return -5.41 + 4.9 * (x3 - x0 + x1 / x4) / (3.0 * x4)


def korns_func4(x0, x1, x2, x3, x4):
    return -2.3 + 0.13 * np.sin(x2)


def korns_func5(x0, x1, x2, x3, x4):
    return 3.0 + 2.13 * np.log(x4)


def korns_func6(x0, x1, x2, x3, x4):
    return 1.3 + 0.13 * np.sqrt(x0)


def korns_func7(x0, x1, x2, x3, x4):
    return 213.809_408_89 - 213.809_408_89 * np.exp(-0.547_237_485_42 * x0)


def korns_func8(x0, x1, x2, x3, x4):
    return 6.87 + 11.0 * np.sqrt(7.23 * x0 * x3 * x4)


def korns_func9(x0, x1, x2, x3, x4):
    return np.sqrt(x0) / np.log(x1) * np.exp(x2) / x3 ** 2


def korns_func10(x0, x1, x2, x3, x4):
    return 0.81 + 24.3 * (2.0 * x1 + 3.0 * x2 * x3) / (4.0 * x3 ** 3 + 5.0 * x4 ** 4)


def korns_func11(x0, x1, x2, x3, x4):
    return 6.87 + 11.0 * np.cos(7.23 * x0 ** 3)


def korns_func12(x0, x1, x2, x3, x4):
    return 2.0 - 2.1 * np.cos(9.8 * x0) * np.sin(1.3 * x4)


def korns_func13(x0, x1, x2, x3, x4):
    return 32.0 - 3.0 * np.tan(x0) / np.tan(x1) * np.tan(x2) / np.tan(x3)


def korns_func14(x0, x1, x2, x3, x4):
    return 22.0 - 4.2 * (np.cos(x0) - np.tan(x1)) * np.tanh(x2) / np.sin(x3)


def korns_func15(x0, x1, x2, x3, x4):
    return 12.0 - 6.0 * np.tan(x0) / np.exp(x1) * (np.log(x2) - np.tan(x3))


def _korns_helper(func, rng=np.random):
    train = generate_uniform_data_set(func, 1000, (-50, 50), rng=rng)
    test = generate_uniform_data_set(func, 1000, (-50, 50), rng=rng)
    return train, test


generator_from_helper(_korns_helper)
current_module = sys.modules[__name__]
all_problems = {name: getattr(current_module, name) for name in locals() if "generate_korns" in name}
