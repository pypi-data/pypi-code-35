# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Sweeper that sweeps and returns whether or not to include the featurizer(s) provide any lift."""
from typing import Any, Optional, Union

import copy
import logging

import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, make_pipeline, make_union
from sklearn.model_selection import train_test_split

from automl.client.core.common.estimation import Estimators
from automl.client.core.common.sampling import AbstractSampler, Samplers
from automl.client.core.common.scoring import AbstractScorer, Scorers
from automl.client.core.common.sweeping.abstract_sweeper import AbstractSweeper
from automl.client.core.common.types import DataSingleColumnInputType, DataInputType


class BinarySweeper(AbstractSweeper):
    """Sweeper that sweeps and returns whether or not to include the featurizer(s) provide any lift."""

    def sweep(self, X: DataInputType, y: DataSingleColumnInputType, *args: Any, **kwargs: Any) -> bool:
        """Sweeper method."""
        # Sample
        X_train_sample, X_valid_sample, y_train_sample, y_valid_sample = self._sampler.sample(X, y)

        # Featurizer
        baseline_featurizer = self._baseline
        experiment_featurizer = self._experiment
        if self._include_baseline_features_in_experiment:
            experiment_featurizer = make_union(self._baseline, self._experiment)

        baseline_features = baseline_featurizer.fit_transform(X_train_sample, y_train_sample)
        experiment_features = experiment_featurizer.fit_transform(X_train_sample, y_train_sample)

        # Train
        baseline_estimator = copy.deepcopy(self._estimator)
        experiment_estimator = self._estimator

        baseline_estimator.fit(baseline_features, y_train_sample)
        experiment_estimator.fit(experiment_features, y_train_sample)

        baseline_valid_features = baseline_featurizer.transform(X_valid_sample)
        experiment_valid_features = experiment_featurizer.transform(X_valid_sample)

        baseline_valid_scores = baseline_estimator.predict(baseline_valid_features)
        experiment_valid_scores = experiment_estimator.predict(experiment_valid_features)

        # Validate
        baseline_score = self._scorer.score(
            y_valid_sample,
            baseline_valid_scores
        )

        experiment_score = self._scorer.score(
            y_valid_sample,
            experiment_valid_scores
        )

        is_experiment_better = self._scorer.is_experiment_better_than_baseline(baseline_score=baseline_score,
                                                                               experiment_score=experiment_score,
                                                                               epsilon=self._epsilon)
        self._logger.info("Sweeper: {sweeper}, Baseline score: {bscore}, Experiment score: {escore}, "
                          "IsExperimentBetter: {is_experiment_better}".format(sweeper=self, bscore=baseline_score,
                                                                              escore=experiment_score,
                                                                              is_experiment_better=is_experiment_better
                                                                              ))

        return is_experiment_better
