# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from ..int import Int
from ._member import Member


def __touchup__(cls, value, parent):
    if value is None:
        dims = getattr(parent, cls._member.dimsmember)
        try:
            dims = [int(dims)]
        except TypeError:
            dims = list(dims)

        value = cls._member.cls._make_instance(None, dims)

    return value


def __unpack__(cls, memory, offset, limit, dump, parent):
    dims = getattr(parent, cls._member.dimsmember)

    try:
        dims = (int(dims),)
    except TypeError:
        dims = tuple(int(d) for d in dims)

    return cls.__original_unpack__(memory, offset, limit, dump, None, dims)


class ArrayMember(Member):

    __slots__ = [
        'name',
        'cls',
        'dimsmember'
    ]

    def __init__(self, dimsmember):
        self.dimsmember = dimsmember
        self.name = None  # assigned during structure class construction
        self.cls = None  # assigned during structure class construction

    @property
    def default(self):
        return None

    @property
    def ignore(self):
        return False

    def finalize(self, name, cls, members):
        namespace = {
            '_member': self,
            '__touchup__': classmethod(__touchup__),
            '__unpack__': classmethod(__unpack__),
            '__original_unpack__': cls.__unpack__,
        }
        dims_cls = members[self.dimsmember].cls
        if issubclass(dims_cls, Int):
            dims = (None,)
        else:
            dims = [None] * dims_cls._dims[0]
        cls = type(cls)(cls.__name__, (cls,), namespace, dims=dims)
        super().finalize(name, cls, members)

    def __repr__(self):
        return ('ArrayMember('
                f'name={self.name!r},'
                f'cls={self.cls!r},'
                f'dimsmember={self.dimsmember!r},'
                ')')


def transfer_dims(*, dimsmember):
    """Configure array structure member to follow dims structure member.

    :param str dimsmember: dims member name
    :returns: structure member definition
    :rtype: ArrayMember

    """
    return ArrayMember(dimsmember)
