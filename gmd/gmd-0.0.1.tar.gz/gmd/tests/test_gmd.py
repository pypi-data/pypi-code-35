import pytest
import numpy as np

from sklearn.datasets import load_iris
from sklearn.utils.testing import assert_dict_equal

from gmd import GMD


@pytest.fixture
def data():
    return load_iris(return_X_y=True)

def test_gmd_estimator(data):
    est = GMD(random_state=1234)
    assert est.alpha == 0.1
    assert est.runs == 100

    est.fit(*data)
    assert hasattr(est, 'is_fitted_')

    assert_dict_equal(est.subspaces_, {0: [0, 2, 1], 1: [1, 2, 0], 2: [2, 3], 3: [3, 2]})