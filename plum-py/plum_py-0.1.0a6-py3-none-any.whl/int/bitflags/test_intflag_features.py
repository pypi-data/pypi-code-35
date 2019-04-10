# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test IntFlag features."""

from . import BitFlags


class Sample(BitFlags, nbytes=2, flag=True):

    """Test sample."""

    OPTION1 = 0x01
    OPTION2 = 0x02
    OPTION3 = 0x04


def test_iterable():
    """Test class iteration."""
    assert list(Sample) == [Sample.OPTION1, Sample.OPTION2, Sample.OPTION3]


def test_member_lookup():
    """Test member lookup."""
    assert Sample["OPTION3"] == Sample.OPTION3


def test_value():
    """Test flags value."""
    assert Sample(5).value == 5


def test_name():
    """Test flags name."""
    assert Sample(5).name == "OPTION3|OPTION1"
