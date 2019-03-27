from uuid import UUID
from typing import Union, Optional
from datetime import datetime, timezone

from dataclass_structor import structure


def test_structure__union__primatives():
    assert structure("Potato", Union[int, str]) == "Potato"
    assert structure(1, Union[int, str]) == 1


def test_structure__union__more_specific_types__none():
    assert structure("Potato", Union[str, None]) == "Potato"
    assert structure(None, Union[str, None]) is None

    assert structure("Potato", Optional[str]) == "Potato"
    assert structure(None, Optional[str]) is None


def test_structure__union__more_specific_types__uuid():
    assert structure("Potato", Union[str, UUID]) == "Potato"
    uuid_str = "a0b8bcd4-9c83-46bd-bc0b-d8d62d8c22d6"
    assert structure(uuid_str, Union[str, UUID]) == UUID(uuid_str)


def test_structure__union__more_specific_types__datetime():
    assert structure("Potato", Union[str, datetime]) == "Potato"
    datetime_obj = datetime(2018, 9, 1, 0, 57, 11, tzinfo=timezone.utc)
    datetime_str = "2018-09-01T00:57:11+00:00"
    assert structure(datetime_str, Union[str, datetime]) == datetime_obj
