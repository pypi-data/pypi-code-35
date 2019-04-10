# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .. import Plum, calcsize
from ._member import Member


def __touchup__(cls, value, parent):
    size_member = cls._member

    if value is None:
        sized_object = getattr(parent, size_member.sizedmember)

        if sized_object is None:
            # both size and sized member not provided
            value = 0

        else:
            if not isinstance(sized_object, Plum):
                names, types, _has_touchups = type(parent).__plum_internals__
                so_cls = types[names.index(size_member.sizedmember)]
                sized_object = so_cls(sized_object)
                setattr(parent, size_member.sizedmember, sized_object)

            value = calcsize(sized_object) // size_member.scalefactor

    return value


class SizeMember(Member):

    __slots__ = [
        'name',
        'cls',
        'scalefactor',
        'sizedmember',
    ]

    def __init__(self, sizedmember, scalefactor):
        self.sizedmember = sizedmember
        self.scalefactor = scalefactor
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
        }
        cls = type(cls)(cls.__name__, (cls,), namespace)
        super().finalize(name, cls, members)

    def __repr__(self):
        return ('SizeMember('
                f'sizedmember={self.sizedmember!r},'
                f'scalefactor={self.scalefactor!r},'
                ')')


def measure_size(*, sizedmember, scalefactor=1):
    """Configure size structure member to follow size of associated structure member.

    :param str sizedmember: sized object member name
    :param int scalefactor: number of bytes per units of size
    :returns: structure member definition
    :rtype: SizeMember

    """
    return SizeMember(sizedmember, scalefactor)
