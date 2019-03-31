# flake8: noqa
__version__ = "0.1.1"

__all__ = [
    'datarecord',
    'CannotMutateRecordError',
]

from .record import datarecord
from .exceptions import CannotMutateRecordError
