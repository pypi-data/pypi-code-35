from inspect import getfullargspec
from typing import Iterable, Callable

__all__ = 'run_in_kwargs',

def run_in_kwargs(kwargs: dict, func: Callable):
	return func(**{
        key: kwargs[key]
        for key in getfullargspec(func).args
    })
