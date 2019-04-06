import collections
import inspect
import sys
from functools import partial
from inspect import getframeinfo
from inspect import getmodulename
from inspect import stack
from itertools import repeat

import numpy as np
import toolz


def poly(x, i):
    return np.sum(x ** j for j in range(1, i + 1))


test_data = collections.namedtuple("TestData", "data target")


def generate_data_set(testfunction, num_points, dist, params):

    dim = len(inspect.getfullargspec(testfunction).args)

    if isinstance(params, dict):
        dist_ = lambda size, params: dist(size=size, **params)
    else:
        dist_ = nd_dist_factory(dist)

    data = dist_(size=(dim, num_points), params=params)
    target = testfunction(*data)
    return test_data(data=data, target=target)


def nd_dist_factory(dist):
    return lambda size, params: np.array(
        [dist(size=s, **p) for s, p in zip(repeat(size[1], times=size[0]), params)]
    )


def generate_uniform_data_set(testfunction, num_points, ranges, rng=np.random):
    to_dict = lambda range_: dict(low=range_[0], high=range_[1])
    params = (to_dict(range_) for range_ in ranges) if toolz.isiterable(ranges[0]) else to_dict(ranges)
    return generate_data_set(testfunction, num_points, rng.uniform, params)


def isiterable(x):
    try:
        iter(x)
        return True
    except TypeError:
        return False


def generate_evenly_spaced_data_set(testfunction, step_sizes, ranges):

    dim = len(inspect.getfullargspec(testfunction).args)
    if len(ranges) == 2 and not isiterable(ranges[0]):
        ranges = repeat(ranges, times=dim)
    else:
        if dim != len(ranges):
            raise ValueError

    if isinstance(step_sizes, float):
        step_sizes = repeat(step_sizes, times=dim)
    else:
        if dim != len(step_sizes):
            raise ValueError
    grid = np.meshgrid(
        *[
            np.linspace(l, u, (u - l) / step_size + 1, endpoint=True)
            for (l, u), step_size in zip(ranges, step_sizes)
        ]
    )

    data = np.array([g.flatten() for g in grid])
    return test_data(data=data, target=testfunction(*data))


def generator_from_helper(helper, shift=0, i=()):
    caller = getframeinfo(stack()[1][0])  # find current_module by looking up caller in stack
    name = getmodulename(caller.filename)
    current_module = [mod for mname, mod in sys.modules.items() if name == mname.split(".")[-1]][0]
    context = dir(current_module)
    for f, fname in (
        (getattr(current_module, func), func) for func in context if "{}_func".format(name) in func
    ):
        f_ = partial(helper, func=f)
        n = int(fname.split("_func")[-1])
        if n in i or not i:
            generator_name = "generate_{}{}".format(name, n + shift)
            if generator_name not in context:
                setattr(current_module, generator_name, f_)  # register generator function in current_module
