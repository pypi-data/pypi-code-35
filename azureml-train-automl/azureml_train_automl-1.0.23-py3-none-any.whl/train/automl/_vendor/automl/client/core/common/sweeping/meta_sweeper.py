# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Runs all enabled features sweepers."""
from typing import Any, Dict, List, Optional

import logging

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.pipeline import make_pipeline

from automl.client.core.common.configuration import FeatureConfig, SweeperConfig, ConfigKeys
from automl.client.core.common.estimation import Estimators
from automl.client.core.common.exceptions import ConfigException
from automl.client.core.common.featurization import Featurizers
from automl.client.core.common.sampling import Samplers, AbstractSampler
from automl.client.core.common.scoring import Scorers, AbstractScorer
from automl.client.core.common.sweeping.abstract_sweeper import AbstractSweeper
from automl.client.core.common.sweeping.sweepers import Sweepers
from automl.client.core.common.types import DataInputType, DataSingleColumnInputType


class MetaSweeper:
    """Runs all enabled features sweepers."""

    _cfg = {}  # type: Dict[str, Any]
    _enabled = False
    _sweepers = []  # type: List[AbstractSweeper]

    def __init__(self) -> None:
        """Load configuration and create sweeper configurations."""
        self._logger = logging.getLogger(MetaSweeper.__class__.__name__)
        MetaSweeper._cfg = MetaSweeper.setup()
        MetaSweeper._enabled = MetaSweeper._cfg.get(ConfigKeys.SWEEPING_ENABLED, False)
        if MetaSweeper._enabled:
            sweeper_configs = [{}] if MetaSweeper._cfg is None \
                else MetaSweeper._cfg.get(ConfigKeys.ENABLED_SWEEPERS, [])  # type: List[Dict[str, Any]]
            self._enabled_sweeper_configs = []  # type: List[SweeperConfig]
            for sweeper_config in sweeper_configs:
                self._enabled_sweeper_configs.append(SweeperConfig.from_dict(sweeper_config))

            self._sweepers = self._build_sweepers(sweeper_configs=self._enabled_sweeper_configs)

    def sweep(self, X, y, stats_and_column_purposes):
        """Sweep through all the sweepers in the configurations."""
        if MetaSweeper._enabled is False:
            self._logger.debug("Feature sweeping disabled.")
            return []

        column_groups = {}  # type: Dict[str, List[str]]
        if self._validate(X, y):
            for stats, column_purpose, column in stats_and_column_purposes:
                column_groups.setdefault(column_purpose.lower(), []).append(column)

            return_transforms = []
            for sweeper_idx, sweeper in enumerate(self._sweepers):
                relevant_columns = []
                for purpose in self._enabled_sweeper_configs[sweeper_idx]._column_purposes:
                    relevant_columns.extend(column_groups.get(purpose, []))

                for column in relevant_columns:
                    X_column = X[column]
                    if sweeper.sweep(X_column.values, y):
                        self._logger.info("Sweep returned true for: {sweeper} on column: {col}".
                                          format(sweeper=sweeper, col=column))
                        return_transforms.append((column, sweeper._experiment))
                    else:
                        self._logger.info(
                            "Sweep returned false for: {sweeper} on column: {col}".format(sweeper=sweeper, col=column))
            return return_transforms

    def _build_sweepers(self, sweeper_configs: Optional[List[SweeperConfig]] = None) -> List[AbstractSweeper]:
        """Sweep over all enabled sweepers."""
        if not sweeper_configs:
            return []

        sweepers = []
        for enabled_sweeper_config in sweeper_configs:
            sampler = Samplers.get(enabled_sweeper_config._sampler)  # type: Optional[AbstractSampler]
            estimator = Estimators.get(enabled_sweeper_config._estimator)  # type: Optional[BaseEstimator]
            scorer = Scorers.get(enabled_sweeper_config._scorer)  # type: Optional[AbstractScorer]
            baseline_featurizer = self._build_featurizers(enabled_sweeper_config._baseline)  # type: FeatureConfig
            experiment_featurizer = self._build_featurizers(enabled_sweeper_config._experiment)  # type: FeatureConfig

            include_baseline_features = True
            if enabled_sweeper_config._experiment:
                include_baseline_features = enabled_sweeper_config._experiment.\
                    get(ConfigKeys.INCLUDE_BASELINE_FEATURES)

            kwargs = {"sampler": sampler, "estimator": estimator, "scorer": scorer, "baseline": baseline_featurizer,
                      "experiment": experiment_featurizer, "epsilon": enabled_sweeper_config._epsilon,
                      "include_baseline_features_in_experiment": include_baseline_features}  # type: Dict[str, Any]

            sweeper = Sweepers.get(enabled_sweeper_config._type, **kwargs)  # type: Optional[AbstractSweeper]
            if sweeper:
                sweepers.append(sweeper)

        return sweepers

    @classmethod
    def _validate(cls, X: DataInputType, y: DataSingleColumnInputType) -> bool:
        if X is None or y is None:
            return False

        if len(X) != len(y):
            return False

        if len(np.unique(y)) == 1:
            return False

        return True

    @classmethod
    def _build_featurizers(cls, feature_config):
        feature_steps = feature_config.get(ConfigKeys.FEATURIZERS)
        if not isinstance(feature_steps, list):
            raise ConfigException("Incorrect configuration. {Key} missing in featurization.".format(
                Key=ConfigKeys.FEATURIZERS))
        steps = []

        for c in feature_steps:
            f_config = FeatureConfig.from_dict(c)
            steps.append(Featurizers.get(f_config))

        return make_pipeline(*steps)

    @staticmethod
    def setup() -> Dict[str, Any]:
        """Read config and setup the list of enabled sweepers."""
        logger = logging.getLogger()
        try:
            return SweeperConfig().get_config()
        except (IOError, FileNotFoundError) as e:
            logger.info("Error trying to read configuration file: {e}".format(e=e))
            return {}
