import dataclasses
import typing

from dataclass_structor import structure, unstructure

from ._fixtures import DataClassGuest as Guest


@dataclasses.dataclass
class Invite:
    email: str
    guests: typing.List["Guest"]


def test_unstructure__invite_with_no_guests():
    value_type = Invite(email="billy@joel.example.com", guests=[])
    expected = {"email": "billy@joel.example.com", "guests": []}
    assert unstructure(value_type) == expected


def test_unstructure__invite_with_a_guest():
    value_type = Invite(
        email="billy@joel.example.com", guests=[Guest(first_name="Bobby Jim")]
    )
    expected = {
        "email": "billy@joel.example.com",
        "guests": [{"first_name": "Bobby Jim"}],
    }
    assert unstructure(value_type) == expected


def test_structure__invite_with_no_guests():
    expected = Invite(email="billy@joel.example.com", guests=[])
    value_to_structure = {"email": "billy@joel.example.com", "guests": []}
    assert structure(value_to_structure, Invite) == expected


def test_structure__invite_with_a_guest():
    expected = Invite(
        email="billy@joel.example.com", guests=[Guest(first_name="Bobby Jim")]
    )
    value_to_structure = {
        "email": "billy@joel.example.com",
        "guests": [{"first_name": "Bobby Jim"}],
    }
    assert structure(value_to_structure, Invite) == expected
