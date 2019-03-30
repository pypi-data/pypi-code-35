# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from ._member import Member
from ..int import Int


def __create__(cls, value=None):
    if value is not None:
        value = cls(value)
    return value


def __touchup__(cls, parent):
    dims_name = cls._member.name
    if parent[dims_name] is None:
        array = parent[cls._member.arraymember]
        dims_cls = cls._member.cls
        if array is None:
            # both dims and array members not provided
            if issubclass(dims_cls, Int):
                parent[dims_name] = 0
            else:
                parent[dims_name] = [0] * len(dims_cls._dims)
        else:
            if issubclass(dims_cls, Int):
                parent[dims_name] = len(array)
            else:
                parent[dims_name] = array._dims


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
            '__create__': classmethod(__create__),
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
