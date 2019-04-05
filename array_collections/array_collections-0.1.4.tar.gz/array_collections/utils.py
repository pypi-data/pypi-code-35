# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:42:49 2018

This module includes classes and functions relating arrays.

@author: Guest Group
"""
import numpy as np

__all__ = ('same_type', 'dim')

ndarray = np.ndarray
asarray = np.asarray
integer = np.integer

def dim(string):
    """Return string with gray ansicolor coding."""
    return '\x1b[37m\x1b[22m' + string + '\x1b[0m'


# %% Functions for array like objects

def same_type(iterable, type_):
    """Raise TypeError if any item in iterable is not an instance of type_."""
    # Make sure iterable is in a tuple
    if not isinstance(iterable, type_):
        # Check that all are type_ instances
        for s in iterable:
            if not isinstance(s, type_):
                raise TypeError(f"Only '{type_.__name__}' objects are valid elements, not '{type(s).__name__}' objects.")


                
                