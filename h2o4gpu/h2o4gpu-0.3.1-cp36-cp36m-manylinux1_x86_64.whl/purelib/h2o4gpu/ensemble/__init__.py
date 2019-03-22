"""
The :mod:`h2o4gpu.ensemble` module includes ensemble-based methods for
classification, regression and anomaly detection.
"""

from .base import BaseEnsemble
from .forest import RandomForestClassifierSklearn
from .forest import RandomForestRegressorSklearn
from .forest import RandomTreesEmbedding
from .forest import ExtraTreesClassifier
from .forest import ExtraTreesRegressor
from .bagging import BaggingClassifier
from .bagging import BaggingRegressor
from .iforest import IsolationForest
from .weight_boosting import AdaBoostClassifier
from .weight_boosting import AdaBoostRegressor
from .gradient_boosting import GradientBoostingClassifierSklearn
from .gradient_boosting import GradientBoostingRegressorSklearn
from .voting_classifier import VotingClassifier

from . import bagging
from . import forest
from . import weight_boosting
from . import gradient_boosting
from . import partial_dependence

__all__ = ["BaseEnsemble",
           "RandomForestClassifierSklearn", "RandomForestRegressorSklearn",
           "RandomTreesEmbedding", "ExtraTreesClassifier",
           "ExtraTreesRegressor", "BaggingClassifier",
           "BaggingRegressor", "IsolationForest", "GradientBoostingClassifierSklearn",
           "GradientBoostingRegressorSklearn", "AdaBoostClassifier",
           "AdaBoostRegressor", "VotingClassifier",
           "bagging", "forest", "gradient_boosting",
           "partial_dependence", "weight_boosting"]
