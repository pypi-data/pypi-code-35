# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from baseline import Baseline

from plum import getdump

from ..int.little import UInt16, UInt8
from ..sequence import Sequence
from ..tests.conformance import BasicConformance


class Custom(Sequence, types=(UInt8, UInt16)):

    """Sample Structure class."""


class TestBasic(BasicConformance):

    """Test basic API conformance and utility usage."""

    bindata = b'\x01\x02\x00'

    cls = Custom

    cls_nbytes = 3

    dump = Baseline("""
            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            |        | x      |       |        | Custom |
            | 0      |   [0]  | 1     | 01     | UInt8  |
            | 1      |   [1]  | 2     | 02 00  | UInt16 |
            +--------+--------+-------+--------+--------+
            """)

    retval_str = Baseline("""
        [1, 2]
        """)

    retval_repr = Baseline("""
        Custom([1, 2])
        """)

    value = [1, 2]

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+--------+
        | Offset | Access          | Value | Memory | Type   |
        +--------+-----------------+-------+--------+--------+
        |        | x               |       |        | Custom |
        | 0      |   [0]           | 1     | 01     | UInt8  |
        | 1      |   [1]           | 2     | 02 00  | UInt16 |
        | 3      | <excess memory> |       | 99     |        |
        +--------+-----------------+-------+--------+--------+

        1 unconsumed memory bytes (4 available, 3 consumed)
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+--------+
        | Offset | Access | Value                | Memory | Type   |
        +--------+--------+----------------------+--------+--------+
        |        | x      |                      |        | Custom |
        | 0      |   [0]  | 1                    | 01     | UInt8  |
        | 1      |   [1]  | <insufficient bytes> | 02     | UInt16 |
        +--------+--------+----------------------+--------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
        needed, only 1 available), dump above shows interrupted progress
        """)

    def test_init_non_generator(self):
        """Test initialization via non-generator tuple."""
        c = Custom((1, 2))

        assert getdump(c) == self.dump

    def test_init_generator(self):
        """Test initialization via generator."""
        c = Custom(range(1, 3))

        assert getdump(c) == self.dump
