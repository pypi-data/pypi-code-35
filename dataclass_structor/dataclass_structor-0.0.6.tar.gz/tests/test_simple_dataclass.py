from dataclass_structor import structure, unstructure

from ._fixtures import DataClassGuest as Guest


def test_unstructure__guest_with_first_name():
    expected = {"first_name": "Bobby Jim"}
    assert unstructure(Guest(first_name="Bobby Jim")) == expected


def test_structure__guest_with_first_name():
    expected = Guest(first_name="Bobby Jim")
    assert structure({"first_name": "Bobby Jim"}, Guest) == expected


def test_unstructure__guest_without_first_name():
    expected = {"first_name": None}
    assert unstructure(Guest(first_name=None)) == expected


def test_structure__guest_without_first_name():
    expected = Guest(first_name=None)
    assert structure({"first_name": None}, Guest) == expected
