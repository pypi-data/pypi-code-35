
import datetime

from h2o4gpu.utils.bench import total_seconds
from h2o4gpu.utils.testing import assert_equal


def test_total_seconds():
    delta = (datetime.datetime(2012, 1, 1, 5, 5, 1)
             - datetime.datetime(2012, 1, 1, 5, 5, 4))
    assert_equal(86397, total_seconds(delta))
