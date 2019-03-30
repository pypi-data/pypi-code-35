# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .._plum import Plum
from ._member import Member


class Varies(Plum):

    __member__ = None

    def __new__(cls, value):
        return value

    @classmethod
    def __create__(cls, value=None):
        return value

    @classmethod
    def __touchup__(cls, parent):
        member = cls.__member__
        type_key = parent[member.typekey]
        member_type = member.mapping[type_key]
        value = parent[member.name]
        parent[member.name] = member_type(value)

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        member = cls.__member__
        type_key = parent[member.typekey]
        member_type = member.mapping[type_key]
        item, offset, limit = member_type.__unpack__(memory, offset, limit, dump, parent)
        if not isinstance(item, member_type):
            item = member_type(item)
        return item, offset, limit


class TypeSwitchMember(Member):

    __slots__ = [
        'name',
        'cls',
        'mapping',
        'typekey',
    ]

    def __init__(self, typekey, mapping):
        self.typekey = typekey
        self.mapping = mapping
        self.name = None  # assigned during structure class construction
        self.cls = None  # assigned during structure class construction

    @property
    def default(self):
        return None

    @property
    def ignore(self):
        return False

    def finalize(self, name, cls, members):
        cls = type('Varies', (Varies,), {'__member__': self})
        super().finalize(name, cls, members)

    def __repr__(self):
        return f'TypeSwitchMember(name={self.name!r}, typekey={self.typekey!r})'


def switch_type(typekey, mapping):
    """Configure structure member type with mapping to another member.

    :param str typekey: name of member to use as type mapping key
    :param dict mapping: type lookup (key is ``typekey`` member, value is member type)
    :returns: structure member definition
    :rtype: TypeSwitchMember

    """
    return TypeSwitchMember(typekey, mapping)
