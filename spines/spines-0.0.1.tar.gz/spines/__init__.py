# -*- coding: utf-8 -*-
"""
Spines

Skeletons for parameterized models.
"""
from .base import Model
from .parameters import Parameter
from .parameters import BoundedParameter

__all__ = [
    # Base
    'Model',
    # Parameters
    'Parameter',
    'BoundedParameter',
]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
