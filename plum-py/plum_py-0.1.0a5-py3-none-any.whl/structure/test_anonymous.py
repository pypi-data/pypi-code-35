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
    +--------+--------+-------+--------+-----------+
    | Offset | Access | Value | Memory | Type      |
    +--------+--------+-------+--------+-----------+
    |        | x      |       |        | Structure |
    | 0      |   .m1  | 1     | 01     | UInt8     |
    | 1      |   .m2  | 2     | 02 00  | UInt16    |
    +--------+--------+-------+--------+-----------+
    """)


class TestInit(object):

    """Test initialization variants."""

    def test_init_dict(self):
        """Test initialization via dict (no defaults)."""
        s = Structure(dict(m1=UInt8(1), m2=UInt16(2)))

        assert getdump(s) == sample_dump

    def test_init_params(self):
        """Test initialization via parameters (no defaults)."""
        s = Structure(m1=UInt8(1), m2=UInt16(2))

        assert getdump(s) == sample_dump

    def test_init_combination(self):
        """Test initialization via dict and parameters.

        Verify members applied from both, keyword params win
        in conflict.

        """
        s = Structure(dict(m1=UInt8(1), m2=None), m2=UInt16(2))

        assert getdump(s) == sample_dump


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

    def test_untyped_set(self):
        with pytest.raises(TypeError) as trap:
            self.sample[0] = 1

        expected = Baseline("""
            value must be a plum type instance
            """)

        assert wrap_message(trap.value) == expected


class TestNameAccess(_TestNameAccess):

    # inherit test cases

    sample = Structure(m1=UInt8(1), m2=UInt16(2))
    sample_dump = sample_dump

    def test_untyped_set(self):
        with pytest.raises(TypeError) as trap:
            self.sample.m1 = 1

        expected = Baseline("""
            value must be a plum type instance
            """)

        assert wrap_message(trap.value) == expected

    def test_new_attributes(self):
        sample = Structure()
        sample.m1 = UInt8(1)
        sample.m2 = UInt16(2)
        assert getdump(sample) == self.sample_dump


class TestCompare(_TestCompare):

    # inherit test cases

    sample = Structure(m1=UInt8(1), m2=UInt16(2))
