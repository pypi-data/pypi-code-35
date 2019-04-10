# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from baseline import Baseline

from plum import (
    ExcessMemoryError,
    InsufficientMemoryError,
    calcsize,
    getdump,
    pack,
    unpack,
)

from plum.int.little import UInt16, UInt8
from plum.structure import Structure, member

from ..tests.utils import wrap_message


class Custom(Structure):

    m1: UInt8
    m2: UInt16 = 0x9988


sample_dump = Baseline("""
    +--------+-------------+-------+--------+--------+
    | Offset | Access      | Value | Memory | Type   |
    +--------+-------------+-------+--------+--------+
    |        | x           |       |        | Custom |
    | 0      |   [0] (.m1) | 1     | 01     | UInt8  |
    | 1      |   [1] (.m2) | 2     | 02 00  | UInt16 |
    +--------+-------------+-------+--------+--------+
    """)


class TestInit(object):

    @staticmethod
    def test_init_pos():
        """Test initialization positional arguments."""
        c = Custom(1, 2)
        assert getdump(c) == sample_dump

    @staticmethod
    def test_init_pos_default():
        """Test initialization via keyword arguments (use defaults)."""
        c = Custom(1)

        expected_dump = Baseline("""
            +--------+-------------+-------+--------+--------+
            | Offset | Access      | Value | Memory | Type   |
            +--------+-------------+-------+--------+--------+
            |        | x           |       |        | Custom |
            | 0      |   [0] (.m1) | 1     | 01     | UInt8  |
            | 1      |   [1] (.m2) | 39304 | 88 99  | UInt16 |
            +--------+-------------+-------+--------+--------+
            """)

        assert getdump(c) == expected_dump

    @staticmethod
    def test_init_keyword():
        """Test initialization via keyword arguments (no defaults)."""
        c = Custom(m1=1, m2=2)
        assert getdump(c) == sample_dump

    @staticmethod
    def test_init_keyword_default():
        """Test initialization via keyword arguments (use defaults)."""
        c = Custom(m1=1)

        expected_dump = Baseline("""
            +--------+-------------+-------+--------+--------+
            | Offset | Access      | Value | Memory | Type   |
            +--------+-------------+-------+--------+--------+
            |        | x           |       |        | Custom |
            | 0      |   [0] (.m1) | 1     | 01     | UInt8  |
            | 1      |   [1] (.m2) | 39304 | 88 99  | UInt16 |
            +--------+-------------+-------+--------+--------+
            """)

        assert getdump(c) == expected_dump

    @staticmethod
    def test_init_combination():
        """Test initialization via positional and keyword arguments.

        Verify members applied from both, keyword params win
        in conflict.

        """
        c = Custom(1, m2=2)
        assert getdump(c) == sample_dump


class TestIndexAccess:

    sample = Custom(m1=1, m2=2)
    sample_dump = sample_dump

    def test_valid_lookup(self):
        assert self.sample[0] == 1
        assert self.sample[1] == 2

    def test_valid_set(self):
        cls = type(self.sample)
        sample = cls(m1=UInt8(0), m2=UInt16(2))
        sample[0] = UInt8(1)
        assert getdump(sample) == self.sample_dump

    def test_invalid_lookup(self):
        with pytest.raises(IndexError) as trap:
            self.sample[2]

        assert str(trap.value) == 'list index out of range'

    def test_invalid_set_index(self):
        with pytest.raises(IndexError) as trap:
            self.sample[2] = UInt16(2)

        assert str(trap.value) == 'list assignment index out of range'


class TestNameAccess:

    sample = Custom(m1=1, m2=2)
    sample_dump = sample_dump

    def test_valid_lookup(self):
        assert self.sample.m1 == 1
        assert self.sample.m2 == 2

    def test_valid_set(self):
        cls = type(self.sample)
        sample = cls(m1=UInt8(0), m2=UInt16(2))
        sample.m1 = UInt8(1)
        assert getdump(sample) == self.sample_dump

    def test_invalid_lookup(self):
        with pytest.raises(AttributeError) as trap:
            self.sample.m3

        clsname = type(self.sample).__name__
        assert str(trap.value) == f"{clsname!r} object has no attribute 'm3'"

    def test_invalid_set(self):
        cls = type(self.sample)
        sample = cls(m1=UInt8(0), m2=UInt16(2))
        with pytest.raises(AttributeError) as trap:
            sample.m3 = 0

        assert str(trap.value) == f"{cls.__name__!r} object has no attribute 'm3'"


class TestCompare:

    sample = Custom(m1=1, m2=2)

    def test_versus_list(self):
        assert self.sample == [1, 2]
        assert not (self.sample != [1, 2])

    def test_extra_member(self):
        assert self.sample != [1, 2, 3]
        assert not (self.sample == [1, 2, 3])

    def test_versus_same(self):
        cls = type(self.sample)
        assert self.sample == cls(m1=UInt8(1), m2=UInt16(2))
        assert not (self.sample != cls(m1=UInt8(1), m2=UInt16(2)))


class TestMember:

    """Test direct use of 'member' definition."""

    class Custom(Structure):
        m1: UInt8
        m2: UInt16 = member(default=2, ignore=True)

    Custom.__name__ = 'Custom'

    sample = Custom(m1=1, m2=2)

    def test_ignored_members(self):
        assert self.sample == self.Custom(m1=1, m2=99)
        assert not (self.sample != self.Custom(m1=1, m2=99))

    def test_default_members(self):
        sample = self.Custom(m1=1)
        assert getdump(sample) == sample_dump
