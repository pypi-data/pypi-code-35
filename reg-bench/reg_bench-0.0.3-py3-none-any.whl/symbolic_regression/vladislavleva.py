import sys

import numpy as np

from .util import generate_evenly_spaced_data_set
from .util import generate_uniform_data_set


def vladislavleva_func1(x, y):
    return np.exp(-1.0 * (x - 1) ** 2) / (1.2 + (y - 2.5) ** 2)


def vladislavleva_func2(x):
    sx = np.sin(x)
    cx = np.cos(x)
    return np.exp(-x) * x ** 3 * cx * sx * (cx * sx ** 2 - 1.0)


def vladislavleva_func3(x, y):
    return vladislavleva_func2(x) * (y - 5)


def vladislavleva_func4(x, y, z, w, v):
    return 10.0 / (5 + np.sum((i - 3) ** 2 for i in [x, y, z, w, v]))


def vladislavleva_func5(x, y, z):
    return 30 * (x - 1) * (z - 1) / (y ** 2 * (x - 10))


def vladislavleva_func6(x, y):
    return 6 * np.sin(x) * np.cos(y)


def vladislavleva_func7(x, y):
    return (x - 3) * (y - 3) + 2 * np.sin((x - 4) * (y - 4))


def vladislavleva_func8(x, y):
    return ((x - 3) ** 4 + (y - 3) ** 3 - (y - 3)) / ((y - 2) ** 4 + 10.0)


def generate_vladislavleva1(rng=np.random):
    train = generate_uniform_data_set(vladislavleva_func1, 100, (0.3, 4), rng=rng)
    test = generate_evenly_spaced_data_set(vladislavleva_func1, 0.1, (-0.2, 4.2))
    return train, test


def generate_vladislavleva2():
    train = generate_evenly_spaced_data_set(vladislavleva_func2, 0.1, (0.05, 10.0))
    test = generate_evenly_spaced_data_set(vladislavleva_func2, 0.05, (-0.5, 10.5))
    return train, test


def generate_vladislavleva3():
    train = generate_evenly_spaced_data_set(vladislavleva_func3, [0.1, 2.0], [(0.05, 10.0), (0.05, 10.05)])
    test = generate_evenly_spaced_data_set(vladislavleva_func3, [0.05, 0.5], (-0.5, 10.5))
    return train, test


def generate_vladislavleva4(rng=np.random):
    train = generate_uniform_data_set(vladislavleva_func4, 1024, (0.05, 6.05), rng=rng)
    test = generate_uniform_data_set(vladislavleva_func4, 5000, (-0.25, 6.35), rng=rng)
    return train, test


def generate_vladislavleva5(rng=np.random):
    train = generate_uniform_data_set(vladislavleva_func5, 300, [(0.05, 2), (1, 2), (0.05, 2)], rng=rng)
    test = generate_evenly_spaced_data_set(
        vladislavleva_func5, [0.15, 0.1, 0.15], [(-0.05, 2.1), (0.95, 2.05), (-0.05, 2.1)]
    )
    return train, test


def generate_vladislavleva6(rng=np.random):
    train = generate_uniform_data_set(vladislavleva_func6, 30, (0.1, 5.9), rng=rng)
    test = generate_evenly_spaced_data_set(vladislavleva_func6, 0.02, (-0.05, 6.05))
    return train, test


def generate_vladislavleva7(rng=np.random):
    train = generate_uniform_data_set(vladislavleva_func7, 300, (0.05, 6.05), rng=rng)
    test = generate_uniform_data_set(vladislavleva_func7, 1000, (-0.25, 6.35), rng=rng)
    return train, test


def generate_vladislavleva8(rng=np.random):
    train = generate_uniform_data_set(vladislavleva_func8, 50, (0.05, 6.05), rng=rng)
    test = generate_evenly_spaced_data_set(vladislavleva_func8, 0.02, (-0.25, 6.35))
    return train, test


current_module = sys.modules[__name__]
all_problems = {name: getattr(current_module, name) for name in locals() if "generate_vladislavleva" in name}
