"""
Data Record Module.
"""
from .code_generation import process_class


def datarecord(_cls=None):
    """
    Wrapper class to handle the decorator being called with or without parens
    """

    def wrap(cls):
        return process_class(cls)

    return wrap if _cls is None else wrap(_cls)
