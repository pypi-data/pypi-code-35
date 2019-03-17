import unittest

from sklearn import metrics, datasets
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import StratifiedKFold
from sklearn_helper.model.evaluator import Evaluator
from sklearn_helper.tests.util.test_util import TestUtil


class BasicBestFitFinderTests(unittest.TestCase):

    def setUp(self):
        dataset = datasets.load_boston()
        self.X, self.y = dataset.data, dataset.target

    def test_basic_regression(self):
        models = TestUtil.generate_model_input(DummyRegressor())
        evaluator = Evaluator(models)

        model = evaluator.evaluate(self.X, self.y)
        self.assertEqual(DummyRegressor, type(model))

    def test_multiple_models(self):
        models = TestUtil.generate_model_input(DummyRegressor(), LinearRegression())
        evaluator = Evaluator(models)

        model = evaluator.evaluate(self.X, self.y)
        self.assertEqual(LinearRegression, type(model))

    def test_multiple_models_with_custom_metric_and_maximize(self):
        models = TestUtil.generate_model_input(DummyRegressor(), LinearRegression())
        evaluator = Evaluator(models,
                                 main_metric=metrics.r2_score,
                                 maximize_metric=True)

        model = evaluator.evaluate(self.X, self.y)
        self.assertEqual(LinearRegression, type(model))

    def test_multiple_models_with_additional_metrics(self):
        models = TestUtil.generate_model_input(DummyRegressor(), LinearRegression())
        evaluator = Evaluator(models,
                                 main_metric=metrics.r2_score,
                                 maximize_metric=True,
                                 additional_metrics=[metrics.mean_squared_error])

        model = evaluator.evaluate(self.X, self.y)
        self.assertEqual(LinearRegression, type(model))

    def test_models_with_custom_number_of_jobs(self):
        models = TestUtil.generate_model_input(DummyRegressor(), LinearRegression())
        evaluator = Evaluator(models,
                                 n_jobs=1)

        model = evaluator.evaluate(self.X, self.y)
        self.assertEqual(LinearRegression, type(model))

    def test_models_with_jobs_as_minus_1(self):
        models = TestUtil.generate_model_input(DummyRegressor(), LinearRegression())
        evaluator = Evaluator(models,
                                 n_jobs=-1)

        model = evaluator.evaluate(self.X, self.y)
        self.assertEqual(LinearRegression, type(model))

    def test_models_with_custom_data_splitter(self):
        models = TestUtil.generate_model_input(DummyRegressor(), LinearRegression())
        evaluator = Evaluator(models, data_splitter=StratifiedKFold(10))

        breast_cancer = datasets.load_breast_cancer()
        X, y = breast_cancer.data, breast_cancer.target
        model = evaluator.evaluate(X, y)
        self.assertEqual(LinearRegression, type(model))


