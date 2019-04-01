from pytest_mock import mocker

from dtest import Dtest
from dtest.rmqhandler import RabbitMQHandler

connectionConfig = {
    "host": "localhost",
    "exchange": "test.dtest",
    "exchange_type": "fanout"
}
metadata = {
    "description": "This is a test of the assertCondition",
    "topic": "test.dtest",
}


def test_dtest(mocker):
    mocker.patch.object(RabbitMQHandler, 'connect', autospec=True)
    mocker.patch.object(RabbitMQHandler, 'publishResults', autospec=True)
    mocker.patch.object(RabbitMQHandler, 'closeConnection', autospec=True)

    dt = Dtest(connectionConfig, metadata)
    assert dt.assertTrue(len([0, 1]) > 1) == True
