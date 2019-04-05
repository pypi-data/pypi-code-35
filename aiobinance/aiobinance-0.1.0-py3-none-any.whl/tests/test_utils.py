import pytest

from aiobinance.types import OrderType
from aiobinance.utils import check_limit_max, check_mandatory_params, check_limit_values


def test_check_limit_max():
    assert check_limit_max(0) == 0
    assert check_limit_max(None) == None
    assert check_limit_max(limit=500, limit_max=1000) == 500
    assert check_limit_max(limit=1000, limit_max=1000) == 1000
    with pytest.raises(ValueError):
        assert check_limit_max(limit=2000, limit_max=1000)


def test_check_mandatory_params():
    with pytest.raises(KeyError):
        check_mandatory_params(**{})

    with pytest.raises(ValueError):
        check_mandatory_params(**{'order_type': 'wrong'})

    with pytest.raises(ValueError):
        check_mandatory_params(**{'order_type': OrderType.MARKET})

    with pytest.raises(ValueError):
        check_mandatory_params(**{'order_type': 'MARKET'})

    with pytest.raises(ValueError):
        check_mandatory_params(**{'order_type': 'MARKET', 'quantity': None})

    assert check_mandatory_params(**{'order_type': 'MARKET', 'quantity': '123'}) is None


def test_check_limit_values():
    assert check_limit_values(limit=5, valid_limits=(5, 10)) == 5
    with pytest.raises(ValueError):
        assert check_limit_values(3, (5, 10))
