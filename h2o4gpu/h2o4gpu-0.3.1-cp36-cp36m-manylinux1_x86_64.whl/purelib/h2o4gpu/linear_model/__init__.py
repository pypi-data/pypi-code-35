"""
The :mod:`h2o4gpu.linear_model` module implements generalized linear models. It
includes RidgeSklearn regression, Bayesian Regression, LassoSklearn and Elastic Net
estimators computed with Least Angle Regression and coordinate descent. It also
implements Stochastic Gradient Descent related algorithms.
"""

# See http://h2o4gpu.sourceforge.net/modules/sgd.html and
# http://h2o4gpu.sourceforge.net/modules/linear_model.html for
# complete documentation.

from .base import LinearRegressionSklearn

from .bayes import BayesianRidgeSklearn, ARDRegression
from .least_angle import (Lars, LassoSklearnLars, lars_path, LarsCV, LassoSklearnLarsCV,
                          LassoSklearnLarsIC)
from .coordinate_descent import (LassoSklearn, ElasticNetSklearn, LassoSklearnCV, ElasticNetSklearnCV,
                                 lasso_path, enet_path, MultiTaskLassoSklearn,
                                 MultiTaskElasticNetSklearn, MultiTaskElasticNetSklearnCV,
                                 MultiTaskLassoSklearnCV)
from .huber import HuberRegressor
from .sgd_fast import Hinge, Log, ModifiedHuber, SquaredLoss, Huber
from .stochastic_gradient import SGDClassifier, SGDRegressor
from .ridge import (RidgeSklearn, RidgeSklearnCV, RidgeSklearnClassifier, RidgeSklearnClassifierCV,
                    ridge_regression)
from .logistic import (LogisticRegressionSklearn, LogisticRegressionSklearnCV,
                       logistic_regression_path)
from .omp import (orthogonal_mp, orthogonal_mp_gram, OrthogonalMatchingPursuit,
                  OrthogonalMatchingPursuitCV)
from .passive_aggressive import PassiveAggressiveClassifier
from .passive_aggressive import PassiveAggressiveRegressor
from .perceptron import Perceptron

from .randomized_l1 import (RandomizedLassoSklearn, RandomizedLogisticRegressionSklearn,
                            lasso_stability_path)

from .ransac import RANSACRegressor
from .theil_sen import TheilSenRegressor

__all__ = ['ARDRegression',
           'BayesianRidgeSklearn',
           'ElasticNetSklearn',
           'ElasticNetSklearnCV',
           'Hinge',
           'Huber',
           'HuberRegressor',
           'Lars',
           'LarsCV',
           'LassoSklearn',
           'LassoSklearnCV',
           'LassoSklearnLars',
           'LassoSklearnLarsCV',
           'LassoSklearnLarsIC',
           'LinearRegressionSklearn',
           'Log',
           'LogisticRegressionSklearn',
           'LogisticRegressionSklearnCV',
           'ModifiedHuber',
           'MultiTaskElasticNetSklearn',
           'MultiTaskElasticNetSklearnCV',
           'MultiTaskLassoSklearn',
           'MultiTaskLassoSklearnCV',
           'OrthogonalMatchingPursuit',
           'OrthogonalMatchingPursuitCV',
           'PassiveAggressiveClassifier',
           'PassiveAggressiveRegressor',
           'Perceptron',
           'RandomizedLassoSklearn',
           'RandomizedLogisticRegressionSklearn',
           'RidgeSklearn',
           'RidgeSklearnCV',
           'RidgeSklearnClassifier',
           'RidgeSklearnClassifierCV',
           'SGDClassifier',
           'SGDRegressor',
           'SquaredLoss',
           'TheilSenRegressor',
           'enet_path',
           'lars_path',
           'lasso_path',
           'lasso_stability_path',
           'logistic_regression_path',
           'orthogonal_mp',
           'orthogonal_mp_gram',
           'ridge_regression',
           'RANSACRegressor']
import h2o4gpu.solvers.ridge
import h2o4gpu.solvers.lasso
import h2o4gpu.solvers.logistic
import h2o4gpu.solvers.linear_regression
import h2o4gpu.solvers.elastic_net
