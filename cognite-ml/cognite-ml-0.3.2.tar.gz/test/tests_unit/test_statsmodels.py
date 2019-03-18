import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_almost_equal as assert_close

import statsmodels.api as sm

from cognite_ml.models import SMRegressor


@pytest.fixture(scope="session")
def train():
    # True relationship: 3 * x
    x = np.arange(1, 51)
    noise = np.random.normal(0, 0.25, 50)
    y = 3 * x + noise
    return pd.DataFrame({"x": x, "y": y})


@pytest.fixture(scope="session")
def estimator(train):
    return SMRegressor(sm.OLS, fit_intercept=True).fit(train[["x"]], train["y"])


@pytest.fixture(scope="session")
def estimator_noconst(train):
    return SMRegressor(sm.OLS, fit_intercept=False).fit(train[["x"]], train["y"])


class TestClassSMRegressor:
    def test_predict(self, train, estimator, estimator_noconst):
        assert_close(pd.Series([15]), estimator.predict(pd.DataFrame({"x": [5]})), decimal=1)
        assert_close(pd.Series([15]), estimator_noconst.predict(pd.DataFrame({"x": [5]})), decimal=1)

    def test_summary(self, estimator):
        assert estimator.summary() is not None

    def test_importance(self, estimator, estimator_noconst):
        assert_close(1 / estimator.feature_importances_, [0], decimal=2)
        assert_close(1 / estimator_noconst.feature_importances_, [0], decimal=2)

    def test_coef(self, estimator, estimator_noconst):
        assert_close(estimator.coef_, [3], decimal=2)
        assert_close(estimator_noconst.coef_, [3], decimal=2)
