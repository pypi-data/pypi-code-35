from dataclass_structor import structure, unstructure
from ._fixtures import SlottedGuest


def test_unstructure__guest_with_first_name():
    expected = {"first_name": "Bobby Jim"}
    assert unstructure(SlottedGuest(first_name="Bobby Jim")) == expected


def test_structure__guest_with_first_name():
    expected = SlottedGuest(first_name="Bobby Jim")
    assert structure({"first_name": "Bobby Jim"}, SlottedGuest) == expected


def test_unstructure__guest_without_first_name():
    expected = {"first_name": None}
    assert unstructure(SlottedGuest(first_name=None)) == expected


def test_structure__guest_without_first_name():
    expected = SlottedGuest(first_name=None)
    assert structure({"first_name": None}, SlottedGuest) == expected
