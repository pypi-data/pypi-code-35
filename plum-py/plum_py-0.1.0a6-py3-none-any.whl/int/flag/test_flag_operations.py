# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test flag operations."""

from . import Flag


class Sample(Flag, nbytes=2):

    """Test sample."""

    OPTION1 = 0x01
    OPTION2 = 0x02
    OPTION3 = 0x04


def test_or():
    """Test logical or."""
    new_value = Sample.OPTION2 | Sample.OPTION3
    assert new_value == 6
    assert isinstance(new_value, Sample)


def test_and():
    """Test logical and."""
    new_value = Sample.OPTION2 & Sample.OPTION3
    assert new_value == 0
    assert isinstance(new_value, Sample)


def test_invert():
    """Test logical inversion."""
    new_value = ~Sample.OPTION2
    assert new_value == 65533
    assert isinstance(new_value, Sample)


def test_membership():
    """Test membership."""
    # pylint: disable=unsupported-membership-test
    assert Sample.OPTION2 in Sample.OPTION2
    assert Sample.OPTION1 not in Sample.OPTION2
