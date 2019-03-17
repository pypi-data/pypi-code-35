import pytest


@pytest.fixture(scope="session")
def mypy_structured_data():
    import mypy_structured_data as _mypy_structured_data

    return _mypy_structured_data
