# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from ._member import Member
from ..int import Int


def __touchup__(cls, value, parent):
    if value is None:
        array = getattr(parent, cls._member.arraymember)
        dims_cls = cls._member.cls
        if array is None:
            # both dims and array members not provided
            if issubclass(dims_cls, Int):
                value = 0
            else:
                value = [0] * dims_cls._dims[0]
        else:
            if issubclass(dims_cls, Int):
                value = len(array)
            else:
                value = []
                for i in range(dims_cls._dims[0]):
                    value.append(len(array))
                    array = array[0]
    return value


class DimsMember(Member):

    __slots__ = [
        'name',
        'cls',
        'arraymember'
    ]

    def __init__(self, arraymember):
        self.arraymember = arraymember
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
        return ('DimsMember('
                f'name={self.name!r},'
                f'cls={self.cls!r},'
                f'arraymember={self.arraymember!r},'
                ')')


def measure_dims(*, arraymember):
    """Configure dims structure member to follow dims of array structure member.

    :param str arraymember: array member name
    :returns: structure member definition
    :rtype: DimsMember

    """
    return DimsMember(arraymember)
