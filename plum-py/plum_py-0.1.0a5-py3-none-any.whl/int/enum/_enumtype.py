# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer enumeration type metaclass."""

from enum import EnumMeta
from .. import IntType


class EnumType(IntType, EnumMeta):

    """Integer enumeration type metaclass.

    Create custom |Enum| subclass. For example:

        >>> from plum.int.enum import Enum
        >>> class Enum24(Enum, nbytes=3, byteorder='big'):
        ...     A = 1
        ...     B = 2
        ...     C = 3
        ...
        >>>

    :param int nbytes: number of memory bytes
    :param str byteorder: ``'big'`` or ``'little'``
    :param bool signed: signed integer

    """

    @classmethod
    def __prepare__(cls, name, bases, nbytes=None, byteorder=None, signed=None):
        # pylint: disable=arguments-differ
        # pylint: disable=unused-argument
        # pylint: disable=too-many-arguments
        return super().__prepare__(name, bases)

    def __new__(cls, name, bases, namespace, nbytes=None, byteorder=None, signed=None):
        # pylint: disable=signature-differs
        # pylint: disable=arguments-differ
        # pylint: disable=too-many-arguments
        return super().__new__(cls, name, bases, namespace,
                               nbytes=nbytes, byteorder=byteorder, signed=signed)

    def __init__(cls, name, bases, namespace, nbytes=None, byteorder=None, signed=None):
        # pylint: disable=too-many-arguments
        super().__init__(name, bases, namespace,
                         nbytes=nbytes, byteorder=byteorder, signed=signed)
