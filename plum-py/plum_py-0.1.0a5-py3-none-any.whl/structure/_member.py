# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class Member:

    __slots__ = [
        'default',
        'name',
        'cls',
        'ignore',
    ]

    def __init__(self, default=None, ignore=None):

        self.default = default
        self.ignore = ignore
        self.name = None  # assigned during structure class construction
        self.cls = None  # assigned during structure class construction

    def finalize(self, name, cls, members):
        self.name = name
        self.cls = cls

    def __repr__(self):
        return ('Member('
                f'name={self.name!r},'
                f'cls={self.cls!r},'
                f'default={self.default!r},'
                f'ignore={self.ignore!r},'
                ')')

    def __get__(self, obj, type=None):
        if obj is None:
            return self

        return obj[self.name]

    def __set__(self, obj, value):
        obj[self.name] = value


# TODO: look at dataclass implementation as to why this should be a function
#       rather than just leaving user instantiate class directly
#       (has something to do with IDE introspection/hints)
def member(*, default=None, ignore=False):
    """Create structure member definition.

    :param int default: initial value when unspecified
    :param bool ignore: ignore member during comparisons
    :returns: structure member definition
    :rtype: Member

    """
    return Member(default, ignore)
