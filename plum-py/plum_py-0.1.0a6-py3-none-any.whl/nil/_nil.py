# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .._plum import Plum
from ._niltype import NilType


class Nil(Plum, metaclass=NilType):

    """Do not interpret memory bytes."""

    _nbytes = 0

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        try:
            dump.cls = cls
        except AttributeError:
            pass  # dump must be None
        else:
            dump.value = 'nil'

        return nil, offset, limit

    @classmethod
    def __pack__(cls, memory, offset, object, dump):
        try:
            dump.cls = cls
        except AttributeError:
            pass  # dump must be None
        else:
            dump.value = 'nil'

        return offset

    def __str__(self):
        return 'Nil()'

    def __baserepr__(self):
        return 'Nil()'

    def __repr__(self):
        return self.__baserepr__()

    def __eq__(self, other):
        return (other is self) or (other is None)

    def __ne__(self, other):
        return (other is not self) and (other is not None)


Nil.__module__ = 'plum'  # FUTURE - do this for every type

nil = Nil()
