# compat2.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,R1717,W0122,W0613

# Standard library imports
import re


###
# Functions
###
def _ex_type_str(exobj):  # pragma: no cover
    """Return a string corresponding to the exception type."""
    regexp = re.compile(r"<(?:\bclass\b|\btype\b)\s+'?([\w|\.]+)'?>")
    exc_type = str(exobj)
    if regexp.match(exc_type):
        exc_type = regexp.match(exc_type).groups()[0]
        exc_type = exc_type[11:] if exc_type.startswith("exceptions.") else exc_type
    if "." in exc_type:
        exc_type = exc_type.split(".")[-1]
    return exc_type


def _get_ex_msg(obj):
    """Get exception message."""
    return obj.value.args[0] if hasattr(obj, "value") else obj.args[0]


def _get_func_code(obj):
    """Get funcion code."""
    return obj.func_code


def _raise_exception(exception_object):
    """Raise exception with short traceback."""
    raise exception_object


def _readlines(fname):
    """Read all lines from file."""
    with open(fname, "r") as fobj:
        return fobj.readlines()


def _rwtb(extype, exmsg, extb):  # pragma: no cover
    """Raise Python 2 exception with traceback."""
    exec("raise extype, exmsg, extb")


def _unicode_char(char):  # pragma: no cover
    """Return true if character is Unicode (non-ASCII) character."""
    try:
        char.encode("ascii")
    except UnicodeDecodeError:
        return True
    return False


# Largely from From https://stackoverflow.com/questions/956867/
# how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python
# with Python 2.6 compatibility changes
def _unicode_to_ascii(obj):  # pragma: no cover
    """Convert to ASCII."""
    # pylint: disable=E0602
    if isinstance(obj, dict):
        return dict(
            [
                (_unicode_to_ascii(key), _unicode_to_ascii(value))
                for key, value in obj.items()
            ]
        )
    if isinstance(obj, list):
        return [_unicode_to_ascii(element) for element in obj]
    if isinstance(obj, unicode):
        return obj.encode("utf-8")
    return obj
