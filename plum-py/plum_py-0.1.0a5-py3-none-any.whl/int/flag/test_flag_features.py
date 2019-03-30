# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test flag features."""

from plum.int.flag import Flag


class Sample(Flag, nbytes=2):

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
    # pylint: disable=comparison-with-callable
    assert Sample(5).value == 5


def test_name():
    """Test flags name."""
    # pylint: disable=comparison-with-callable
    assert Sample(4).name == "OPTION3"


def test_attribute_access():
    """Test bit access."""
    assert Sample(5).option1 is True
    assert Sample(5).option2 is False
    assert Sample(5).option3 is True
