"""Helper functions for paths manipulation."""
import os
from contextlib import contextmanager
import inspect


def get_cfp(real: bool = False, fdir: bool = False) -> str:
    """Return caller's current file path.

    Args:
        real: if True, return full path, otherwise relative path
            (default: {False})
        fdir: file's directory path will be returned instead
            (default: {False}).
    """
    frame = inspect.stack()[1]
    p = frame[0].f_code.co_filename
    if real:
        p = os.path.realpath(p)
    if fdir:
        p = os.path.dirname(p)
    return p


@contextmanager
def chdir_tmp(path):
    """Change current working directory temporarily."""
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)
