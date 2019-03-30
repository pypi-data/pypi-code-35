# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from plum import Memory, dump, getdump, pack, unpack
from plum.int.little import UInt16, UInt8
from plum.structure import Structure, Member
from plum.int.bitfields import BitFields, bitfield

m = Memory(b'123')

unpack(UInt16, b'\x00\x01\x02')

