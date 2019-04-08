# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Generic target encoder."""
import logging
from typing import Any, Dict, Optional, List, Tuple

import numpy as np
import pandas as pd
from automl.client.core.common.featurization.automltransformer import AutoMLTransformer
from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.types import DataSingleColumnInputType

from sklearn.model_selection import KFold, StratifiedKFold


class CountBasedTargetEncoder(AutoMLTransformer):
    """Generic count based target encoder."""

    def __init__(self,
                 blending_param: float = 20,
                 smoothing_param: float = 10,
                 logger: Optional[logging.Logger] = None,
                 num_folds: int = 5) -> None:
        """Construct the target encoder.

        :param blending_param: Value for num of samples where smoothening applies
        :param smoothing_param: Parameter to control smoothening, higher value will lead to more regularization.
        :param logger: The logger.
        :param num_folds: Number of folds to use in Cross Validation strategy.
        """
        super().__init__()
        self._init_logger(logger)
        # TODO support different flavours of Count Based TE using diff parameters
        self._blending_param = blending_param
        self._smoothing_param = smoothing_param
        self._mean = 0.0
        self._mean_folds = []  # type: List[float]
        self._categorical_mappings = {}  # type: Dict[str, Any]
        self._categorical_mappings_folds = []  # type: List[Dict[str, Any]]
        self._folds = []  # type: np.ndarray
        self._num_folds = num_folds

    def __getstate__(self):
        """
        Overridden to remove _num_folds and _folds while pickling.

        :return: this object's state as a dictionary
        """
        state = super(CountBasedTargetEncoder, self).__getstate__()
        newstate = {**state, **self.__dict__}

        # _folds and _num_folds if set tell us that code is in train flow.
        # We want to lose that information on pickling.
        # In case model is unpickled, it will be used on inferencing or refitted.
        # In case it is refitted after unpickling, _folds and _num_folds are again populated.

        newstate['_folds'] = []
        newstate['_num_folds'] = 0
        return newstate

    @function_debug_log_wrapped
    def fit(self, X: DataSingleColumnInputType, y: DataSingleColumnInputType) -> "CountBasedTargetEncoder":
        """
        Instantiate and train on the input data.

        :param X: The data to transform.
        :param y: Target values.
        :return: The instance object: self.
        """
        if not isinstance(X, pd.Series):
            X = pd.Series(X)
        if not isinstance(y, pd.Series):
            y = pd.Series(y)

        self._generate_fold_indices(X)
        self._compute_categorical_mappings(X, y)
        return self

    def _generate_fold_indices(self, X: pd.Series) -> None:
        """
        Generate indices for folds.

        :param X: Data for transform.
        """
        if self._num_folds > 1:
            try:
                skf = StratifiedKFold(n_splits=self._num_folds, shuffle=True, random_state=42)
                for train_index, test_index in skf.split(X, X):
                    self._folds.append(test_index)
            except Exception as ex:
                if self.logger:
                    self.logger.log(logging.DEBUG, 'Error trying to perform StratifiedKFold split.'
                                                   ' Falling back to KFold. Exception: {}', ex)

                self._folds = []
                kf = KFold(n_splits=self._num_folds, shuffle=True, random_state=42)
                for train_index, test_index in kf.split(X):
                    self._folds.append(test_index)

    @function_debug_log_wrapped
    def transform(self, X: DataSingleColumnInputType) -> np.ndarray:
        """
        Return target encoded data for current input data.

        :param X: The data to transform.
        :return: Target encoded values from current X column.
        """
        if not isinstance(X, pd.Series):
            X = pd.Series(X)

        # _folds are precomputed while we fit the data. If folds are still present, we know that we have not
        # transformed data as yet. Folds will be cleaned up post transform

        if len(self._folds) > 1:
            # KFold TE with holdout
            transformed_data = self._cv_transform(X)
        else:
            # TE without holdout
            transformed_data = self._apply_transform(X, self._categorical_mappings)

        self._num_folds = 0
        self._folds = []
        return transformed_data

    def _cv_transform(self, X: pd.Series) -> np.ndarray:
        """
        Transform using cross validation.

        :param X: Data to transform.
        :return: Transformed data
        """
        num_folds = len(self._folds)

        transformed_data = np.empty(X.shape)  # type: np.ndarray
        for in_fold in range(0, num_folds):
            in_fold_data = X[self._folds[in_fold]]

            # Outfold map was created with != fold datavalues
            out_fold_categorical_map = self._categorical_mappings_folds[in_fold]

            # Put data in same order as in X
            transformed_data[self._folds[in_fold]] = \
                self._apply_transform(in_fold_data, out_fold_categorical_map)

        return transformed_data

    def _apply_transform(self, X: pd.Series, mapping: Dict[str, Dict[str, float]]) -> np.ndarray:
        """
        Apply transform on X data using mappings passed.

        :param X: Data to be transformed.
        :param mapping: Mappings to use for transforming the data.
        :return: Transformed data.
        """
        return X.apply(lambda x: mapping.get(x, {'smoothing': self._mean})['smoothing'])

    def _compute_categorical_mappings(self, X: pd.Series, y: pd.Series) -> None:
        """
        Compute categorical mappings for passed Data and target.

        :param X: Data to be transformed.
        :param y: Target data to use for categorical mappings.
        """
        # If foldColumnName was provided, means we are in train case, hence do a KFoldCV and get out of fold maps
        # These out of fold maps will be used to generate Features for InFold data, when we do a transform
        if len(self._folds) > 1:

            # We need to ensure that folds start with index 0
            for curr_fold_indices in self._folds:
                out_fold_indices = ~y.index.isin(curr_fold_indices)

                y_out_fold = y[out_fold_indices]
                X_out_fold = X[out_fold_indices]

                curr_fold_target_agg, prior = self._get_map_for_data(X_out_fold, y_out_fold)

                self._mean_folds.append(prior)
                self._categorical_mappings_folds.append(curr_fold_target_agg)

        # generate a full categorical map as well
        self._categorical_mappings, self._mean = self._get_map_for_data(X, y)

    def _get_map_for_data(self, X: pd.Series, y: pd.Series) -> \
            Tuple[Dict[str, Dict[str, float]], float]:
        """
        Get map for data.

        :param X: Data to be transformed.
        :param y: Target data.
        :return: Computed categorical map using y as target.
        """
        # TODO Support multi-class
        # Mean works fine with binary class as well, but will need change with multi-class
        prior = y.mean()

        # TODO Add more aggregation depending on type of TE
        target_agg = y.groupby(X).agg(['sum', 'count'])

        # Trying to remove novel categories, they can be represented by single value/bin
        # TODO make count for novels a configurable parameter
        target_agg = target_agg[target_agg['count'] > 1]

        target_agg['mean'] = target_agg['sum'] / target_agg['count']
        exponent = (target_agg["count"] - self._blending_param) / self._smoothing_param

        # computing a sigmoid for smoothing
        sigmoid = 1 / (1 + np.exp(-1 * exponent))
        custom_smoothing = prior * (1 - sigmoid) + target_agg['mean'] * sigmoid

        target_agg['smoothing'] = custom_smoothing

        return target_agg.to_dict(orient='index'), prior
