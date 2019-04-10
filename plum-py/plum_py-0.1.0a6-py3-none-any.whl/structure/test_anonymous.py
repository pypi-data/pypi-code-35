# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure usage (no pre-defined members)."""

import pytest
from baseline import Baseline

from plum import (
    ExcessMemoryError,
    calcsize,
    getdump,
    pack,
    unpack,
)

from plum.int.little import UInt16, UInt8
from plum.structure import Structure

from ..tests.utils import wrap_message
from .test_features import TestCompare as _TestCompare
from .test_features import TestIndexAccess as _TestIndexAccess
from .test_features import TestNameAccess as _TestNameAccess


sample_dump = Baseline("""
    +--------+-------------+-------+--------+-----------+
    | Offset | Access      | Value | Memory | Type      |
    +--------+-------------+-------+--------+-----------+
    |        | x           |       |        | Structure |
    | 0      |   [0] (.m1) | 1     | 01     | UInt8     |
    | 1      |   [1] (.m2) | 2     | 02 00  | UInt16    |
    +--------+-------------+-------+--------+-----------+
    """)


class TestInit(object):

    """Test initialization variants."""

    def test_init_pos_args(self):
        """Test initialization via positional arguments."""
        s = Structure(UInt8(1), UInt16(2))

        expected_dump = Baseline("""
            +--------+--------+-------+--------+-----------+
            | Offset | Access | Value | Memory | Type      |
            +--------+--------+-------+--------+-----------+
            |        | x      |       |        | Structure |
            | 0      |   [0]  | 1     | 01     | UInt8     |
            | 1      |   [1]  | 2     | 02 00  | UInt16    |
            +--------+--------+-------+--------+-----------+
            """)

        assert getdump(s) == expected_dump

    def test_init_kw_args(self):
        """Test initialization via keyword arguments."""
        s = Structure(m1=UInt8(1), m2=UInt16(2))

        assert getdump(s) == sample_dump

    def test_init_combination(self):
        """Test initialization via positional and keyword arguments."""
        s = Structure(UInt8(1), m2=UInt16(2))

        expected_dump = Baseline("""
            +--------+-------------+-------+--------+-----------+
            | Offset | Access      | Value | Memory | Type      |
            +--------+-------------+-------+--------+-----------+
            |        | x           |       |        | Structure |
            | 0      |   [0]       | 1     | 01     | UInt8     |
            | 1      |   [1] (.m2) | 2     | 02 00  | UInt16    |
            +--------+-------------+-------+--------+-----------+
            """)

        assert getdump(s) == expected_dump


class TestUtilities:

    def test_calcsize(self):
        assert calcsize(Structure(m1=UInt8(1), m2=UInt16(2))) == 3

    def test_dump(self):
        s = Structure(m1=UInt8(1), m2=UInt16(2))
        assert getdump(s) == sample_dump

    def test_pack_builtins(self):
        assert pack(Structure, {'m1': UInt8(1), 'm2': UInt16(2)}) == b'\x01\x02\x00'

    def test_pack_instance(self):
        s = Structure(m1=UInt8(1), m2=UInt16(2))
        assert pack(s) == b'\x01\x02\x00'

    def test_unpack(self):
        s = unpack(Structure, b'')

        expected_dump = Baseline("""
            +--------+--------+-------+--------+-----------+
            | Offset | Access | Value | Memory | Type      |
            +--------+--------+-------+--------+-----------+
            |        | x      |       |        | Structure |
            +--------+--------+-------+--------+-----------+
            """)

        assert getdump(s) == expected_dump

    def test_unpack_excess(self):
        with pytest.raises(ExcessMemoryError) as trap:
            unpack(Structure, b'\x01')

        expected = Baseline("""


            +--------+-----------------+-------+--------+-----------+
            | Offset | Access          | Value | Memory | Type      |
            +--------+-----------------+-------+--------+-----------+
            |        | x               |       |        | Structure |
            | 0      | <excess memory> |       | 01     |           |
            +--------+-----------------+-------+--------+-----------+

            1 unconsumed memory bytes
            """)

        assert wrap_message(trap.value) == expected


class TestIndexAccess(_TestIndexAccess):

    # inherit test cases

    sample = Structure(m1=UInt8(1), m2=UInt16(2))
    sample_dump = sample_dump


class TestNameAccess(_TestNameAccess):

    sample = Structure(m1=UInt8(1), m2=UInt16(2))
    sample_dump = sample_dump


class TestCompare(_TestCompare):

    # inherit test cases

    sample = Structure(m1=UInt8(1), m2=UInt16(2))
