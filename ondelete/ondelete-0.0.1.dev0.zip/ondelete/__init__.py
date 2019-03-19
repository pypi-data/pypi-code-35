"""
OnDelete

Roger D. Serwy
2019-03-19

"""

from __future__ import print_function
from ._version import __version__

__all__ = ['OnDelete']


class OnDelete:
    _debug = False

    def __init__(self, func=None, debug=None):
        if debug is not None:
            self._debug = debug
        if self._debug:
            print('New OnDelete: %r' % self)
        self._func = func
            
    def __call__(self, func):
        self._func = func  # via decorator

    def __del__(self):
        if self._debug:
            print('OnDelete: %r' % self)
        self.clean()

    def clean(self):
        func, self._func = self._func, None
        if callable(func):
            func()

