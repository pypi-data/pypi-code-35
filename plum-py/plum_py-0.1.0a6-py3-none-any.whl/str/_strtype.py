# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import codecs

from .._plumtype import PlumType


class StrType(PlumType):

    """Str type metaclass.

    Create custom |Str| subclass. For example:

        >>> from plum.str import Str
        >>> class MyStr(Str, encoding='ascii', nbytes=4):
        ...     pass
        ...
        >>>

    :param str encoding: encoding name (see :mod:`codecs` standard encodings)
    :param str errors: error handling (e.g. ``'string'``, ``'ignore'``, ``'replace'``)
    :param int nbytes: size in number of bytes
    :param bytes pad: pad value, len(pad) must equal 1

    """

    def __new__(mcs, name, bases, namespace, encoding=None, errors=None, nbytes=None, pad=None, zero_termination=None):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, encoding=None, errors=None, nbytes=None, pad=None, zero_termination=None):
        super().__init__(name, bases, namespace)

        if encoding is None:
            encoding = cls._codecs_info.name

        if errors is None:
            errors = cls._errors

        if nbytes is None:
            nbytes = cls._nbytes
        else:
            assert nbytes > 0

        if pad is None:
            pad = cls._pad
        else:
            pad = bytes(pad)
            assert len(pad) == 1

        if zero_termination is None:
            zero_termination = cls._zero_termination

        cls._codecs_info = codecs.lookup(encoding)
        cls._errors = errors
        cls._nbytes = nbytes
        cls._pad = pad
        cls._zero_termination = zero_termination
