# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base class for all scorers."""
from abc import ABC, abstractmethod

import logging

import numpy as np


class AbstractScorer(ABC):
    """Base class for all scorers."""

    def __init__(self) -> None:
        """Initialize logger to be used by the base class."""
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def score(self, y_actual: np.ndarray, y_predict: np.ndarray) -> float:
        """
        Override this to provide score given the prediction and actual values.

        :param y_actual: Actual values of y.
        :param y_predict: Predicted values of y by the trained model.
        :return: Score value.
        """
        raise NotImplementedError()

    @abstractmethod
    def is_experiment_better_than_baseline(self, baseline_score: float, experiment_score: float,
                                           epsilon: float) -> bool:
        """
        Override this to provide comparison between two experiment outputs.

        :param baseline_score: The baseline score.
        :param experiment_score: Experiment score.
        :param epsilon: Minimum delta considered gain/loss.
        :return: Whether or not the experiment score is better than baseline.
        """
        raise NotImplementedError()
