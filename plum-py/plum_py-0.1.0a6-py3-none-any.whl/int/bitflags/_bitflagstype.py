# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""BitFlags type metaclass."""

from enum import IntFlag
import math

from plum.int.bitfields import BitFieldsType, bitfield


class BitFlagsType(BitFieldsType):

    """BitFlags type metaclass.

    Create custom |BitFlags| subclass. For example:

        >>> from plum.int.bitflags import BitFlags
        >>> class MyFlags(BitFlags, nbytes=1, byteorder='big', fill=0, ignore=0x80):
        ...     RED = 1
        ...     GREEN = 2
        ...     BLUE = 4
        ...
        >>>

    :param int nbytes: number of memory bytes
    :param str byteorder: ``'big'`` or ``'little'``
    :param int fill: default value (integer basis before applying bit field values)
    :param int ignore: mask applied during comparison to ignore bit fields
    :param IntFlag flag: bit field enumeration (or ``True`` when members in namespace)

    """

    def __new__(mcs, name, bases, namespace, nbytes=None, byteorder=None,
                fill=None, ignore=None, flag=None):
        # pylint: disable=unused-argument
        return super().__new__(mcs, name, bases, namespace, nbytes, byteorder,
                               fill, ignore)

    def __init__(cls, name, bases, namespace, nbytes=None, byteorder=None,
                 fill=None, ignore=None, flag=None):

        if flag is None:
            flag = cls._flag_cls
        elif flag is True:
            member_def = {}
            for flag_name, flag_val in namespace.items():
                if flag_name.isupper():
                    member_def[flag_name] = flag_val
                    delattr(cls, flag_name)
            flag = IntFlag(name, member_def)

        if flag is not None:
            try:
                valid = issubclass(flag, IntFlag)
            except TypeError:
                valid = False

            if valid:
                try:
                    cls.__annotations__
                except AttributeError:
                    cls.__annotations__ = {}
                else:
                    raise TypeError(
                        "subclass may not contain bitfield definitions (or any annotation)"
                        " when 'flag' argument specifies an integer flag enumeration")

                for member in flag:
                    cls.__annotations__[member.name.lower()] = bool
                    setattr(cls, member.name.lower(),
                            bitfield(pos=int(math.log(member, 2)), size=1, default=False))
            else:
                raise TypeError(
                    'invalid enum, expected IntFlag subclass or True')

        super().__init__(name, bases, namespace, nbytes, byteorder, fill, ignore)
        cls._flag_cls = flag

    def __getattr__(cls, name):
        # IntFlag members are uppercase
        if name.isupper():
            flag_cls = cls._flag_cls
            if flag_cls:
                try:
                    return getattr(flag_cls, name)
                except AttributeError:
                    pass

        return super().__getattribute__(name)

    def __iter__(self):
        return iter(self._flag_cls)

    def __getitem__(self, name):
        return self._flag_cls[name]
