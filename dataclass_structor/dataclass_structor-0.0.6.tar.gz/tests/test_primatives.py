import datetime
import decimal
import uuid

from dataclass_structor import structure, unstructure


def test_unstructure__str():
    assert unstructure("Potato") == "Potato"


def test_structure__str():
    assert structure("Tomato", str) == "Tomato"


def test_unstructure__int():
    assert unstructure(1) == 1


def test_structure__int():
    assert structure(1, int) == 1


def test_unstructure__float():
    assert unstructure(1.0) == 1.0


def test_structure__float():
    assert structure(1.0, float) == 1.0
    assert structure(1, float) == 1.0
    assert structure("1.0", float) == 1.0


def test_unstructure__decimal():
    assert unstructure(decimal.Decimal("1.0")) == "1.0"


def test_structure__decimal():
    assert structure(1.0, decimal.Decimal) == decimal.Decimal(1.0)
    assert structure(1, decimal.Decimal) == decimal.Decimal(1.0)
    assert structure("1.0", decimal.Decimal) == decimal.Decimal(1.0)


def test_unstructure__date():
    assert unstructure(datetime.date(2018, 8, 28)) == "2018-08-28"


def test_structure__date():
    assert structure("2018-08-28", datetime.date) == datetime.date(2018, 8, 28)


def test_unstructure__datetime():
    result = unstructure(
        datetime.datetime(2018, 2, 1, 2, 2, 2, tzinfo=datetime.timezone.utc)
    )
    assert result == "2018-02-01T02:02:02+00:00"

    result = unstructure(datetime.datetime(2018, 2, 1, 2, 2, 2))
    assert result == "2018-02-01T02:02:02"


def test_structure__datetime():
    input_datetime = "2018-02-01T02:02:02+00:00"
    expected = datetime.datetime(2018, 2, 1, 2, 2, 2, tzinfo=datetime.timezone.utc)
    assert structure(input_datetime, datetime.datetime) == expected


def test_unstructure__bool():
    assert unstructure(True) is True
    assert unstructure(False) is False


def test_structure__bool():
    assert structure(True, bool) is True
    assert structure(False, bool) is False


def test_unstructure__uuid():
    expected = "d1337d56-4e6a-4cf7-8f7a-730bf4ea3fac"
    assert unstructure(uuid.UUID(expected)) == expected


def test_structure__uuid():
    uuid_str = "d1337d56-4e6a-4cf7-8f7a-730bf4ea3fac"
    expected = uuid.UUID(uuid_str)
    assert structure(uuid_str, uuid.UUID) == expected
