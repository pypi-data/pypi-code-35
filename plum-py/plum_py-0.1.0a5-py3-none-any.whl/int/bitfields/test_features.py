# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from enum import IntEnum

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

from plum.int.bitfields import BitFields, bitfield

from ...tests.utils import wrap_message


class MyEnum(IntEnum):

    A = 1
    B = 2


class MyBits(BitFields, nbytes=2, fill=0x0):

    f1: int = bitfield(pos=0, size=8, default=0xab)
    f2: MyEnum = bitfield(pos=8, size=4)
    f3: bool = bitfield(pos=12, size=1)


class TestInit(object):

    """Test constructor."""

    @staticmethod
    def test_init_default():
        i = MyBits()
        assert i == 0

    expected_dump = Baseline("""
        +---------+--------+----------+--------+--------+
        | Offset  | Access | Value    | Memory | Type   |
        +---------+--------+----------+--------+--------+
        | 0       | x      | 4608     | 00 12  | MyBits |
        |  [0:7]  |   .f1  | 0        |        | int    |
        |  [8:11] |   .f2  | MyEnum.B |        | MyEnum |
        |  [12]   |   .f3  | True     |        | bool   |
        +---------+--------+----------+--------+--------+
        """)

    def test_dict(self):
        """Test initialization with fields in dict argument."""
        m = MyBits(dict(f1=0, f2=2, f3=1))

        assert getdump(m) == self.expected_dump

    def test_kwargs(self):
        """Test initialization with fields as keyword arguments."""
        m = MyBits(f1=0, f2=2, f3=1)

        assert getdump(m) == self.expected_dump

    def test_dict_and_kwargs(self):
        """Test initialization with fields in dict and keyword arguments."""
        m = MyBits(dict(f1=0), f2=2, f3=1)

        assert getdump(m) == self.expected_dump

    expected_dump_with_default = Baseline("""
        +---------+--------+----------+--------+--------+
        | Offset  | Access | Value    | Memory | Type   |
        +---------+--------+----------+--------+--------+
        | 0       | x      | 4779     | ab 12  | MyBits |
        |  [0:7]  |   .f1  | 171      |        | int    |
        |  [8:11] |   .f2  | MyEnum.B |        | MyEnum |
        |  [12]   |   .f3  | True     |        | bool   |
        +---------+--------+----------+--------+--------+
        """)

    def test_dict_with_defaults(self):
        """Test initialization with kwargs with some defaults."""
        m = MyBits(dict(f2=2, f3=1))

        assert getdump(m) == self.expected_dump_with_default

    def test_kwargs_with_defaults(self):
        """Test initialization with kwargs with some defaults."""
        m = MyBits(f2=2, f3=1)

        assert getdump(m) == self.expected_dump_with_default

    def test_extra_arg(self):
        """Test too many positional arguments."""
        expected_message = Baseline("""
            MyBits expected at most 1 arguments, got 2
            """)

        with pytest.raises(TypeError) as trap:
            MyBits(1, 2)

        assert str(trap.value) == expected_message

    def test_bad_dict_single(self):
        """Test unknown bit field name in dict."""
        expected_message = Baseline("""
            MyBits() got 1 unexpected bit field: 'f4'
            """)

        with pytest.raises(TypeError) as trap:
            MyBits(dict(f1=0, f2=0, f3=0, f4=0))

        assert str(trap.value) == expected_message

    def test_bad_dict_multiple(self):
        """Test unknown bit field names in dict."""
        expected_message = Baseline("""
            MyBits() got 2 unexpected bit fields: 'f4', 'f5'
            """)

        with pytest.raises(TypeError) as trap:
            MyBits(dict(f1=0, f2=0, f3=0, f4=0, f5=0))

        assert str(trap.value) == expected_message

    def test_bad_kwarg_single(self):
        """Test unknown bit field name as keyword argument."""
        expected_message = Baseline("""
            MyBits() got 1 unexpected bit field: 'f4'
            """)

        with pytest.raises(TypeError) as trap:
            MyBits(f1=0, f2=0, f3=0, f4=0)

        assert str(trap.value) == expected_message

    def test_bad_kwarg_multiple(self):
        """Test unknown bit field names as keyword arguments."""
        expected_message = Baseline("""
            MyBits() got 2 unexpected bit fields: 'f4', 'f5'
            """)

        with pytest.raises(TypeError) as trap:
            MyBits(f1=0, f2=0, f3=0, f4=0, f5=0)

        assert str(trap.value) == expected_message

    def test_bad_dict_and_kwarg(self):
        """Test unknown bit field name in both dict and as keyword argument."""
        expected_message = Baseline("""
            MyBits() got 3 unexpected bit fields: 'f4', 'f5', 'f6'
            """)

        with pytest.raises(TypeError) as trap:
            MyBits(dict(f1=0, f6=0), f2=0, f3=0, f4=0, f5=0)

        assert str(trap.value) == expected_message

    def test_invalid_arg_type(self):
        expected_message = Baseline("""
            [1] object is not an int or bit field dict
            """)

        with pytest.raises(TypeError) as trap:
            MyBits([1])

        assert str(trap.value) == expected_message


class ForCompare(BitFields, nbytes=1, fill=0x0, ignore=0xc0):

    f1: int = bitfield(pos=0, size=4)
    f2: int = bitfield(pos=4, size=2, ignore=True)
    f3: int = bitfield(pos=6, size=2)  # gets ignored from class 'ignore'


class TestEquality:

    def test_int(self):
        """Verify when other is int, nothing ignored"""
        assert ForCompare(f1=1, f2=2, f3=2) == 0xa1

    def test_dict_ignore_field(self):
        """Verify when other is dict, field marked as ignore doesn't matter."""
        assert ForCompare(f1=1, f2=2, f3=2) == dict(f1=1, f2=0, f3=2)
        assert not (ForCompare(f1=0, f2=2, f3=2) == dict(f1=1, f2=2, f3=2))

    def test_dict_ignore_mask(self):
        """Verify when other is dict, subclass ignore mask applies."""
        assert ForCompare(f1=1, f2=2, f3=2) == dict(f1=1, f2=2, f3=3)
        assert not (ForCompare(f1=0, f2=2, f3=2) == dict(f1=1, f2=2, f3=2))

    def test_same_ignore_field(self):
        """Verify when other is same type as self, field marked as ignore doesn't matter."""
        assert ForCompare(f1=1, f2=2, f3=2) == dict(f1=1, f2=0, f3=2)
        assert not (ForCompare(f1=0, f2=2, f3=2) == dict(f1=1, f2=2, f3=2))

    def test_same_ignore_mask(self):
        """Verify when other is same type as self, subclass ignore mask applies."""
        assert ForCompare(f1=1, f2=2, f3=2) == dict(f1=1, f2=2, f3=3)
        assert not (ForCompare(f1=0, f2=2, f3=2) == dict(f1=1, f2=2, f3=2))


class TestCompares:

    """Verify comparison operators.

    Assume all operators implemented with a common normalization
    algorithm. Only spot check each operator and rely on TestEquality
    test cases to validate the common normalization algorithm.

    """

    def test_lt(self):
        """Spot check 'lt' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) < 0xa2
        assert not (ForCompare(f1=1, f2=2, f3=2) < 0xa0)

    def test_le(self):
        """Spot check 'lt' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) <= 0xa1
        assert not (ForCompare(f1=1, f2=2, f3=2) <= 0xa0)

    def test_eq(self):
        """Spot check 'eq' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) == 0xa1
        assert not (ForCompare(f1=1, f2=2, f3=2) == 0xa0)

    def test_ne(self):
        """Spot check 'ne' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) != 0xa0
        assert not (ForCompare(f1=1, f2=2, f3=2) != 0xa1)

    def test_gt(self):
        """Spot check 'gt' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) > 0xa0
        assert not (ForCompare(f1=1, f2=2, f3=2) > 0xa2)

    def test_ge(self):
        """Spot check 'ge' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) >= 0xa1
        assert not (ForCompare(f1=1, f2=2, f3=2) >= 0xa2)


class TestHash:

    def test_hash(self):
        """Verify hash does not include ignored fields."""
        assert hash(ForCompare(f1=1, f2=1, f3=1)) == hash(1)


class TestBool:

    def test_bool(self):
        """Verify bool does not consider ignored fields."""
        assert ForCompare(f1=1, f2=0, f3=0)
        assert not ForCompare(f1=0, f2=1, f3=1)
