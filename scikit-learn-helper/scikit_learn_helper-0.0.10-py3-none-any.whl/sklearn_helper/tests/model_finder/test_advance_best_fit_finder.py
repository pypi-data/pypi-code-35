import unittest

import numpy as np
from sklearn import datasets, metrics
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.linear_model import Ridge, LogisticRegressionCV
from sklearn.model_selection import StratifiedKFold
from sklearn_helper.model.evaluator import Evaluator
from sklearn_helper.tests.util.model_input_builder import ModelInputBuilder
from sklearn_helper.tests.util.test_util import TestUtil


class BasicBestFitFinderTests(unittest.TestCase):

    def test_tune_model(self):
        alpha = np.linspace(0, 0.1, num=10)
        max_iter = range(10**4, 10**6, 10**4)

        models = ModelInputBuilder()\
            .add_model(DummyRegressor())\
            .add_model(Ridge(), {"alpha": alpha, "max_iter": max_iter})\
            .build()

        evaluator = Evaluator(models)

        dataset = datasets.load_boston()
        X, y = dataset.data, dataset.target
        model = evaluator.evaluate(X, y)

        self.assertEqual(Ridge, type(model))
        self.assertTrue(model.alpha in alpha)
        self.assertTrue(model.max_iter in max_iter)

    def test_custom_data_splitter(self):
        models = TestUtil.generate_model_input(DummyClassifier(), LogisticRegressionCV())

        evaluator = Evaluator(models,
                              data_splitter=StratifiedKFold(10),
                              main_metric=metrics.roc_auc_score,
                              maximize_metric=True,
                              additional_metrics=[metrics.f1_score, metrics.accuracy_score])

        breast_cancer = datasets.load_breast_cancer()
        X, y = breast_cancer.data, breast_cancer.target
        model = evaluator.evaluate(X, y)

        self.assertEqual(LogisticRegressionCV, type(model))
