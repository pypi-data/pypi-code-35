from pytest_mock import mocker

from dtest import Dtest
from dtest.rmqhandler import RabbitMQHandler

connectionConfig = {
    "host": "localhost",
    "username": None,
    "password": None,
    "exchange": "test.dtest",
    "exchange_type": "fanout"
}
metadata = {
    "description": "This is a test suite",
    "topic": "test.dtest",
    "ruleSet": "Testing some random things",
    "dataSet": "random_data_set_123912731.csv"
}


def test_dtest(mocker):
    mocker.patch.object(RabbitMQHandler, 'connect', autospec=True)
    mocker.patch.object(RabbitMQHandler, 'publishResults', autospec=True)
    mocker.patch.object(RabbitMQHandler, 'closeConnection', autospec=True)

    dt = Dtest(connectionConfig, metadata)

    assert dt.assertTrue(
        len([0, 1]) > 1, "len(dsQubert) > 1") == True

    assert dt.assertFalse(
        len([0, 1]) < 1, "len(dsQubert) < 1") == False

    dt.finish()
