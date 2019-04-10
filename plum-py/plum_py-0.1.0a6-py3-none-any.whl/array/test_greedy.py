# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from baseline import Baseline

from .. import getdump
from ..int.little import UInt16
from ..tests.conformance import BasicConformance
from . import Array as _Array


class Array(_Array, item_cls=UInt16):
    pass


class TestArray(BasicConformance):

    """Test basic API conformance and utility usage."""

    bindata = b'\x00\x00\x01\x00\x02\x00\x03\x00'

    cls = Array

    cls_nbytes = None

    dump = Baseline("""
    +--------+--------+-------+--------+--------+
    | Offset | Access | Value | Memory | Type   |
    +--------+--------+-------+--------+--------+
    |        | x      |       |        | Array  |
    | 0      |   [0]  | 0     | 00 00  | UInt16 |
    | 2      |   [1]  | 1     | 01 00  | UInt16 |
    | 4      |   [2]  | 2     | 02 00  | UInt16 |
    | 6      |   [3]  | 3     | 03 00  | UInt16 |
    +--------+--------+-------+--------+--------+
    """)

    greedy = True

    retval_str = Baseline("""
        [0, 1, 2, 3]
        """)

    retval_repr = Baseline("""
        Array([0, 1, 2, 3])
        """)

    value = [0, 1, 2, 3]

    unpack_cls = list

    unpack_excess = 'N/A'

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+--------+
        | Offset | Access | Value                | Memory | Type   |
        +--------+--------+----------------------+--------+--------+
        |        | x      |                      |        | Array  |
        | 0      |   [0]  | 0                    | 00 00  | UInt16 |
        | 2      |   [1]  | 1                    | 01 00  | UInt16 |
        | 4      |   [2]  | 2                    | 02 00  | UInt16 |
        | 6      |   [3]  | <insufficient bytes> | 03     | UInt16 |
        +--------+--------+----------------------+--------+--------+

        InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
        needed, only 1 available), dump above shows interrupted progress
        """)


sample = Array(TestArray.value)


class TestIndexAccess:

    """Test __setitem__ and __getitem__ usages."""

    def test_valid_lookup(self):
        assert sample[0] == 0
        assert sample[1] == 1
        assert isinstance(sample[0], int)

    def test_valid_set(self):
        a = Array([0, 1, 2, 99])
        a[3] = UInt16(3)
        assert getdump(a) == TestArray.dump

    def test_invalid_lookup(self):
        with pytest.raises(IndexError) as trap:
            sample[4]
        assert str(trap.value) == 'list index out of range'

    def test_invalid_set_index(self):
        a = Array(TestArray.value)
        with pytest.raises(IndexError) as trap:
            a[4] = 0
        assert str(trap.value) == 'list assignment index out of range'

    def test_untyped_set(self):
        a = Array([0, 1, 2, 99])
        a[3] = 3
        assert getdump(a) == TestArray.dump


class TestCompare:

    def test_versus_list(self):
        assert sample == TestArray.value
        assert not (sample != TestArray.value)

    def test_versus_same(self):
        assert sample == sample
        assert not (sample != sample)

    def test_versus_dissimiliar(self):
        assert sample != [[0, 1, 2], [3, 4, 5]]
