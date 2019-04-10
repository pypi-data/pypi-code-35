# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from baseline import Baseline

from plum import getdump

from plum.int.bitfields import BitFields, bitfield


class Inner(BitFields, fill=0x4):

    i0: int = bitfield(pos=0, size=1, ignore=True)
    i1: int = bitfield(pos=1, size=1, default=1)
    # empty bitfield(pos=2, size=1)
    i2: int = bitfield(pos=3, size=2)


class Middle(BitFields, fill=0xc, ignore=0x4):

    m0: int = bitfield(pos=0, size=1, ignore=True)
    m1: int = bitfield(pos=1, size=1, default=1)
    # empty bitfield(pos=2, size=2)
    m2: Inner = bitfield(pos=4, size=5)


class Outer(BitFields, nbytes=2, fill=0x70, ignore=0x10):

    o0: int = bitfield(pos=0, size=2, ignore=True)
    o1: int = bitfield(pos=2, size=2, default=1)
    # empty bitfield(pos=4, size=3)
    o2: Middle = bitfield(pos=7, size=9)


class TestNested:

    """Verify bit fields may be nested within bitfields arbitrarily.

    Following aspects covered without need for dedicated test cases:

        - dump
        - instantiating with class instances

    """

    expected_dump = Baseline("""
        +----------+-----------+-------+--------+--------+
        | Offset   | Access    | Value | Memory | Type   |
        +----------+-----------+-------+--------+--------+
        | 0        | x         | 46964 | 74 b7  | Outer  |
        |  [0:1]   |   .o0     | 0     |        | int    |
        |  [2:3]   |   .o1     | 1     |        | int    |
        |          |   .o2     |       |        | Middle |
        |  [7]     |     .m0   | 0     |        | int    |
        |  [8]     |     .m1   | 1     |        | int    |
        |          |     .m2   |       |        | Inner  |
        |  [11]    |       .i0 | 0     |        | int    |
        |  [12]    |       .i1 | 1     |        | int    |
        |  [14:15] |       .i2 | 2     |        | int    |
        +----------+-----------+-------+--------+--------+
        """)

    def test_get(self):
        """Verify read access."""
        instance = Outer(o0=0, o1=1, o2=Middle(
            m0=0, m1=1, m2=Inner(i0=0, i1=1, i2=2)))

        assert instance == 0xb774

        assert instance.o0 == 0
        assert instance.o1 == 1
        assert instance.o2 == 0x16e

        assert instance.o2.m0 == 0
        assert instance.o2.m1 == 1
        assert instance.o2.m2 == 0x16

        assert instance.o2.m2.i0 == 0
        assert instance.o2.m2.i1 == 1
        assert instance.o2.m2.i2 == 2

        assert getdump(instance) == self.expected_dump

    def test_set(self):
        """Verify write access."""
        # initialize all fields to zero (except initialize to 1 all fields that
        # should be 0)
        instance = Outer(o0=1, o1=0, o2=Middle(
            m0=1, m1=0, m2=Inner(i0=1, i1=0, i2=0)))

        # fill in each field with expected value
        instance.o0 = 0
        instance.o1 = 1
        instance.o2.m0 = 0
        instance.o2.m1 = 1
        instance.o2.m2.i0 = 0
        instance.o2.m2.i1 = 1
        instance.o2.m2.i2 = 2

        assert getdump(instance) == self.expected_dump

    def test_init_with_dict(self):
        """Verify initialization with dicts."""
        dict_value = dict(o0=0, o1=1, o2=dict(
            m0=0, m1=1, m2=dict(i0=0, i1=1, i2=2)))
        assert getdump(Outer(dict_value)) == self.expected_dump

    def test_ignore_fields(self):
        """Verify ignored fields at lower level don't cause mis-compare.

        Verify bitfield(..., ignore=True) has impact from nested levels.

        """
        item1 = Outer(o0=0, o1=1, o2=Middle(
            m0=0, m1=1, m2=Inner(i0=0, i1=1, i2=2)))
        item2 = Outer(o0=3, o1=1, o2=Middle(
            m0=1, m1=1, m2=Inner(i0=1, i1=1, i2=2)))
        assert item1 == item2

    def test_ignore_background(self):
        """Verify ignored background bits at lower level don't cause mis-compare.

        Verify Middle(..., ignore=0x4) has impact.

        """
        assert Outer(0x210) == Outer(0)

    def test_fill(self):
        """Verify fill patterns for each class are meshed properly."""

        expected_dump = Baseline("""
            +----------+-----------+-------+--------+--------+
            | Offset   | Access    | Value | Memory | Type   |
            +----------+-----------+-------+--------+--------+
            | 0        | x         | 9840  | 70 26  | Outer  |
            |  [0:1]   |   .o0     | 0     |        | int    |
            |  [2:3]   |   .o1     | 0     |        | int    |
            |          |   .o2     |       |        | Middle |
            |  [7]     |     .m0   | 0     |        | int    |
            |  [8]     |     .m1   | 0     |        | int    |
            |          |     .m2   |       |        | Inner  |
            |  [11]    |       .i0 | 0     |        | int    |
            |  [12]    |       .i1 | 0     |        | int    |
            |  [14:15] |       .i2 | 0     |        | int    |
            +----------+-----------+-------+--------+--------+
            """)

        instance = Outer(o0=0, o1=0, o2=Middle(
            m0=0, m1=0, m2=Inner(i0=0, i1=0, i2=0)))

        assert getdump(instance) == expected_dump
