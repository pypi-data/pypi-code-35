# coding=utf-8
from __future__ import print_function

import numpy as np

from suanpan import path
from suanpan.utils import json


def _loads(obj, *args, **kwargs):
    return np.frombuffer(obj["data"], obj["dtype"]).reshape(obj["shape"])


def _load(fp, *args, **kwargs):
    return _loads(json.load(fp, *args, **kwargs))


def _loadf(file, *args, **kwargs):
    encoding = kwargs.pop("encoding", "utf-8")
    with open(file, "r", encoding=encoding) as file:
        return _load(file, *args, **kwargs)


def _dumps(npy, *args, **kwargs):
    return {"dtype": str(npy.dtype), "shape": npy.shape, "data": npy.tobytes()}


def _dump(npy, fp, *args, **kwargs):
    return json.dump(_dumps(npy, *args, **kwargs), fp)


def _dumpf(npy, file, *args, **kwargs):
    encoding = kwargs.pop("encoding", "utf-8")
    path.safeMkdirsForFile(file)
    with open(file, "w", encoding=encoding) as file:
        return _dump(npy, file, *args, **kwargs)


def load(file, *args, **kwargs):
    _l = _loadf if isinstance(file, str) else _load
    return _l(file, *args, **kwargs)


def dump(npy, file, *args, **kwargs):
    _d = _dumpf if isinstance(file, str) else _dump
    return _d(npy, file, *args, **kwargs)


loads = _loads
dumps = _dumps
