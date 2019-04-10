# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from baseline import Baseline

from .. import getdump
from ..int.little import UInt16
from ..tests.conformance import BasicConformance
from . import Array


class Array2x2(Array, dims=(2,2), item_cls=UInt16):

    """Sample dimensioned Array."""


class TestArray2x2(BasicConformance):

    """Test basic API conformance and utility usage."""

    bindata = b'\x00\x00\x01\x00\x00\x01\x01\x01'

    cls = Array2x2

    cls_nbytes = 8

    dump = Baseline("""
        +--------+---------+-------+--------+----------+
        | Offset | Access  | Value | Memory | Type     |
        +--------+---------+-------+--------+----------+
        |        | x       |       |        | Array2x2 |
        |        |   [0]   |       |        |          |
        | 0      |     [0] | 0     | 00 00  | UInt16   |
        | 2      |     [1] | 1     | 01 00  | UInt16   |
        |        |   [1]   |       |        |          |
        | 4      |     [0] | 256   | 00 01  | UInt16   |
        | 6      |     [1] | 257   | 01 01  | UInt16   |
        +--------+---------+-------+--------+----------+
        """)

    retval_str = Baseline("""
        [[0, 1], [256, 257]]
        """)

    retval_repr = Baseline("""
        Array2x2([[0, 1], [256, 257]])
        """)

    value = [[0x0000, 0x0001], [0x0100, 0x0101]]

    unpack_cls = list

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+----------+
        | Offset | Access          | Value | Memory | Type     |
        +--------+-----------------+-------+--------+----------+
        |        | x               |       |        | Array2x2 |
        |        |   [0]           |       |        |          |
        | 0      |     [0]         | 0     | 00 00  | UInt16   |
        | 2      |     [1]         | 1     | 01 00  | UInt16   |
        |        |   [1]           |       |        |          |
        | 4      |     [0]         | 256   | 00 01  | UInt16   |
        | 6      |     [1]         | 257   | 01 01  | UInt16   |
        | 8      | <excess memory> |       | 99     |          |
        +--------+-----------------+-------+--------+----------+

        1 unconsumed memory bytes
        """)

    unpack_shortage = Baseline("""


        +--------+---------+----------------------+--------+----------+
        | Offset | Access  | Value                | Memory | Type     |
        +--------+---------+----------------------+--------+----------+
        |        | x       |                      |        | Array2x2 |
        |        |   [0]   |                      |        |          |
        | 0      |     [0] | 0                    | 00 00  | UInt16   |
        | 2      |     [1] | 1                    | 01 00  | UInt16   |
        |        |   [1]   |                      |        |          |
        | 4      |     [0] | 256                  | 00 01  | UInt16   |
        | 6      |     [1] | <insufficient bytes> | 01     | UInt16   |
        +--------+---------+----------------------+--------+----------+

        InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
        needed, only 1 available), dump above shows interrupted progress
        """)


sample = Array2x2(TestArray2x2.value)


class TestIndexAccess:

    """Test __setitem__ and __getitem__ usages."""

    def test_valid_lookup(self):
        assert sample[0] == [0x0000, 0x0001]
        assert sample[1] == [0x0100, 0x0101]
        assert isinstance(sample[0], Array)

    def test_valid_set(self):
        a = Array2x2([[0x0000, 0x0001], [0x0100, 0x9999]])
        a[1][1] = UInt16(0x0101)
        assert getdump(a) == TestArray2x2.dump

    def test_invalid_lookup(self):
        with pytest.raises(IndexError) as trap:
            sample[3]
        assert str(trap.value) == 'list index out of range'

        with pytest.raises(IndexError) as trap:
            sample[0][3]
        assert str(trap.value) == 'list index out of range'

    def test_invalid_set_index(self):
        a = Array2x2([[0, 0], [0, 0]])
        with pytest.raises(IndexError) as trap:
            a[1][3] = 0
        assert str(trap.value) == 'list assignment index out of range'

    def test_untyped_set(self):
        a = Array2x2([[0x0000, 0x0001], [0x0100, 0x9999]])
        a[1][1] = 0x0101
        assert getdump(a) == TestArray2x2.dump


class TestCompare:

    def test_versus_list(self):
        assert sample == TestArray2x2.value
        assert not (sample != TestArray2x2.value)

    def test_versus_same(self):
        assert sample == sample
        assert not (sample != sample)

    def test_versus_dissimiliar(self):
        assert sample != [0, 1]
        assert sample != [[0, 1, 2], [3, 4, 5]]
