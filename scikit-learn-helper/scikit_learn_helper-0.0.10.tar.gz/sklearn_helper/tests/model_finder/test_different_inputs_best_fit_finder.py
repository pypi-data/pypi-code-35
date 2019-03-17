import unittest

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression

from sklearn_helper.model.evaluator import Evaluator
from sklearn_helper.tests.util.test_util import TestUtil


class DifferentInputsBestFitFinderTests(unittest.TestCase):

    sample_size = 500

    def test_pandas_dataframe(self):
        df = pd.DataFrame({"a": np.arange(self.sample_size),
                           "b": np.arange(self.sample_size) ** 2,
                           "c": np.arange(self.sample_size) ** 3,
                           "d": np.arange(self.sample_size)})
        X = df[["a", "b", "c"]]
        y = df[["d"]]

        models = TestUtil.generate_model_input(DummyRegressor(), LinearRegression())
        evaluator = Evaluator(models)

        model = evaluator.evaluate(X, y)
        self.assertEqual(LinearRegression, type(model))

    def test_numpy_array(self):
        X = np.array([np.arange(self.sample_size), np.arange(self.sample_size)**2, np.arange(self.sample_size) ** 3]).T
        y = np.arange(self.sample_size)

        models = TestUtil.generate_model_input(DummyRegressor(), LinearRegression())
        evaluator = Evaluator(models)

        model = evaluator.evaluate(X, y)
        self.assertEqual(LinearRegression, type(model))

