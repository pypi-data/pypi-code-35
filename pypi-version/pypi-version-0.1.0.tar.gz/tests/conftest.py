"""
Provide fixtures and useful functionality for testing.
"""
import pytest


class Response:
    """
    Implements response fixture.
    """

    def __init__(self, status_code=None):
        self._status_code = status_code

    @property
    def status_code(self):
        """
        Get response status code.
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code_):
        """
        Set response status code.
        """
        self._status_code = status_code_


@pytest.fixture
def response():
    """
    Get response object fixture.
    """
    return Response()
