# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Interpret memory bytes as a structure with uniquely named and typed members."""

from ._measure_dims import measure_dims
from ._measure_size import measure_size
from ._member import Member, member
from ._limit_size import limit_size
from ._structure import Structure
from ._structuretype import StructureType
from ._switch_type import Varies, switch_type
from ._transfer_dims import transfer_dims
