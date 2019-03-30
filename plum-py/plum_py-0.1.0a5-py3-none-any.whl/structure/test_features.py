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
    +--------+--------+-------+--------+--------+
    | Offset | Access | Value | Memory | Type   |
    +--------+--------+-------+--------+--------+
    |        | x      |       |        | Custom |
    | 0      |   .m1  | 1     | 01     | UInt8  |
    | 1      |   .m2  | 2     | 02 00  | UInt16 |
    +--------+--------+-------+--------+--------+
    """)


class TestInit(object):

    @staticmethod
    def test_init_dict():
        """Test initialization via dict (no defaults)."""
        c = Custom(dict(m1=1, m2=2))

        assert getdump(c) == sample_dump

    @staticmethod
    def test_init_dict_default():
        """Test initialization via dict (use defaults)."""
        c = Custom(dict(m1=1))

        expected_dump = Baseline("""
            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            |        | x      |       |        | Custom |
            | 0      |   .m1  | 1     | 01     | UInt8  |
            | 1      |   .m2  | 39304 | 88 99  | UInt16 |
            +--------+--------+-------+--------+--------+
            """)

        assert getdump(c) == expected_dump

    @staticmethod
    def test_init_params():
        """Test initialization via parameters (no defaults)."""
        c = Custom(m1=1, m2=2)

        assert getdump(c) == sample_dump

    @staticmethod
    def test_init_params_default():
        """Test initialization via parameters (use defaults)."""
        c = Custom(m1=1)

        expected_dump = Baseline("""
            +--------+--------+-------+--------+--------+
            | Offset | Access | Value | Memory | Type   |
            +--------+--------+-------+--------+--------+
            |        | x      |       |        | Custom |
            | 0      |   .m1  | 1     | 01     | UInt8  |
            | 1      |   .m2  | 39304 | 88 99  | UInt16 |
            +--------+--------+-------+--------+--------+
            """)

        assert getdump(c) == expected_dump

    @staticmethod
    def test_init_combination():
        """Test initialization via dict and parameters.

        Verify members applied from both, keyword params win
        in conflict.

        """
        c = Custom(dict(m1=0, m2=2), m1=1)

        assert getdump(c) == sample_dump


class TestIndexAccess:

    sample = Custom(m1=1, m2=2)
    sample_dump = sample_dump

    def test_valid_lookup(self):
        assert self.sample[0] is self.sample.m1
        assert self.sample[1] is self.sample.m2

    def test_valid_set(self):
        cls = type(self.sample)
        sample = cls(m1=UInt8(0), m2=UInt16(2))
        sample[0] = UInt8(1)
        assert getdump(sample) == self.sample_dump

    def test_invalid_lookup(self):
        with pytest.raises(KeyError) as trap:
            self.sample[2]
        assert str(trap.value) == '2'

    def test_invalid_set_index(self):
        with pytest.raises(KeyError) as trap:
            self.sample[2] = UInt16(2)
        assert str(trap.value) == '2'

    def test_untyped_set(self):
        cls = type(self.sample)
        sample = cls(m1=UInt8(0), m2=UInt16(2))
        sample[0] = 1
        assert getdump(sample) == self.sample_dump


class TestNameAccess:

    sample = Custom(m1=1, m2=2)
    sample_dump = sample_dump

    def test_valid_lookup(self):
        assert self.sample.m1 == 1
        assert type(self.sample.m1) is UInt8
        assert self.sample.m2 == 2
        assert type(self.sample.m2) is UInt16

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

    def test_untyped_set(self):
        cls = type(self.sample)
        sample = cls(m1=UInt8(0), m2=UInt16(2))
        sample.m1 = 1
        assert getdump(sample) == self.sample_dump


class TestCompare:

    sample = Custom(m1=1, m2=2)

    def test_versus_dict(self):
        assert self.sample == dict(m1=1, m2=2)
        assert not (self.sample != dict(m1=1, m2=2))

    def test_extra_member(self):
        assert self.sample != dict(m1=1, m2=2, m3=3)
        assert not (self.sample == dict(m1=1, m2=2, m3=3))

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
        assert self.sample == dict(m1=1, m2=99)
        assert not (self.sample != dict(m1=1, m2=99))

    def test_default_members(self):
        assert getdump(self.sample) == sample_dump
