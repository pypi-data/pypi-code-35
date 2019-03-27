import datetime
import decimal
import uuid

import pytest  # pylint: disable=import-error

from dataclass_structor import structure
from ._fixtures import AnimalEnum, SoundsEnum


def test_structure__bad_str__int():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", int)
    assert "Could not convert Tomato of type <class 'str'> into a <class 'int'>" in str(
        exinfo.value
    )


def test_structure__bad_str__float():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", float)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <class 'float'>"
        in str(exinfo.value)
    )


def test_structure__bad_str__decimal():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", decimal.Decimal)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <class 'decimal.Decimal'>"
        in str(exinfo.value)
    )


def test_structure__bad_str__date():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", datetime.date)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <class 'datetime.date'>"
        in str(exinfo.value)
    )


def test_structure__bad_str__datetime():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", datetime.datetime)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <class 'datetime.datetime'>"
        in str(exinfo.value)
    )


def test_structure__bad_str__uuid():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", uuid.UUID)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <class 'uuid.UUID'>"
        in str(exinfo.value)
    )


def test_structure__bad_str__int_enum():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", AnimalEnum)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <enum 'AnimalEnum'> enum."
        in str(exinfo.value)
    )


def test_structure__bad_str__str_enum():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", SoundsEnum)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <enum 'SoundsEnum'> enum."
        in str(exinfo.value)
    )
