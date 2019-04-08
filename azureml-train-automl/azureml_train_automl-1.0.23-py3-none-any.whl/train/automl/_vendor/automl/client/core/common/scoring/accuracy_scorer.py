# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Scorer for Accuracy."""
from typing import Any, cast, Dict

import logging

import numpy as np
from sklearn.metrics import accuracy_score

from .abstract_scorer import AbstractScorer


class AccuracyScorer(AbstractScorer):
    """Scorer for Accuracy."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the object."""
        self._logger = logging.getLogger(self.__class__.__name__)

    def score(self, y_actual: np.ndarray, y_predict: np.ndarray) -> float:
        """
        Override this to provide score given the prediction and actual values.

        :param y_actual: Actual values of y.
        :param y_predict: Predicted values of y by the trained model.
        :return: Score value.
        """
        return cast(float, accuracy_score(y_actual, y_predict))

    def is_experiment_better_than_baseline(self, baseline_score: float, experiment_score: float,
                                           epsilon: float) -> bool:
        """
        Override this to provide comparison between two experiment outputs.

        :param baseline_score: The baseline score.
        :param experiment_score: Experiment score.
        :param epsilon: Minimum delta considered gain/loss.
        :return: Whether or not the experiment score is better than baseline.
        """
        return experiment_score > baseline_score * (1 + epsilon)
