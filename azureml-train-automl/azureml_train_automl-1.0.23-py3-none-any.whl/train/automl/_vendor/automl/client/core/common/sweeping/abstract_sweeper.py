# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base class for all sweepers."""
from typing import Any
from abc import ABC, abstractmethod

import logging

from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline

from automl.client.core.common.sampling import AbstractSampler
from automl.client.core.common.scoring import AbstractScorer
from automl.client.core.common.types import TransformerType, DataInputType, DataSingleColumnInputType


class AbstractSweeper(ABC):
    """Base class for all sweepers."""

    def __init__(self, sampler: AbstractSampler, baseline: Pipeline, experiment: Pipeline,
                 estimator: BaseEstimator, scorer: AbstractScorer, epsilon: float,
                 include_baseline_features_in_experiment: bool = True, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the abstract sweeper.

        :param sampler: Sampler to use.
        :param baseline: Baseline set of transformers to run.
        :param experiment: Experiment to compare with.
        :param estimator: Estimator to train.
        :param scorer: Scorer to use.
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._sampler = sampler
        self._baseline = baseline
        self._experiment = experiment
        self._estimator = estimator
        self._scorer = scorer
        self._epsilon = epsilon
        self._include_baseline_features_in_experiment = include_baseline_features_in_experiment
        self._validate()

    @abstractmethod
    def sweep(self, X: DataInputType, y: DataSingleColumnInputType, *args: Any, **kwargs: Any) -> bool:
        """
        Sweep over parameters provided and return if experiment was better than baseline.

        :param X: Input data.
        :param y: Input label.
        :return: Whether experiment was better than baseline.
        """
        raise NotImplementedError()

    def _validate(self) -> bool:
        """
        Validate if the current sweeper has all the needed stuff.

        :return: True if the validation passed. If not, false.
        """
        return self._baseline is not None and self._experiment is not None

    def __str__(self):
        """
        Create and return string representation of the sweeper.

        :return: String representing the sweeper.
        """
        return "Sampler: {sampler}, Estimator: {estimator}, Baseline: {baseline}, Experiment: {experiment}".format(
            sampler=self._sampler,
            estimator=self._estimator,
            baseline=self._baseline,
            experiment=self._experiment
        )
