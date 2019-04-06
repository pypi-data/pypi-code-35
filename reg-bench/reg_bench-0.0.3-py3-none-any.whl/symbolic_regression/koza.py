import sys
from functools import partial

import numpy as np

from .util import generate_uniform_data_set
from .util import generator_from_helper
from .util import poly


koza_func1 = partial(poly, i=4)


def koza_func2(x):
    return x ** 5 - 2.0 * x ** 3 + x


def koza_func3(x):
    return x ** 6 - 2.0 * x ** 4 + x ** 2


def _koza_helper(func, rng=np.random):
    train = generate_uniform_data_set(func, 20, (-1, 1), rng=rng)
    test = generate_uniform_data_set(func, 20, (-1, 1), rng=rng)
    return train, test


generator_from_helper(_koza_helper)
current_module = sys.modules[__name__]
all_problems = {name: getattr(current_module, name) for name in locals() if "generate_koza" in name}
