# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines scoring models for approximating feature importance values."""

import scipy as sp
import numpy as np
import logging
from abc import ABCMeta, abstractmethod

try:
    from azureml._logging import ChainedIdentity
except ImportError:
    from ..common.chained_identity import ChainedIdentity

from azureml.explain.model._internal.constants import SKLearn

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    import shap

LOGGER = '_logger'
AZUREML = 'azureml'


class ScoringModel(ChainedIdentity):
    """Defines a scoring model."""

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """Initialize the ScoringModel."""
        super(ScoringModel, self).__init__(**kwargs)
        self._logger.debug('Initializing ScoringModel')

    @abstractmethod
    def explain(self, evaluation_examples):
        """Use the model for scoring to approximate the feature importance values of data."""
        pass


class TreeScoringModel(ScoringModel):
    """Defines a scoring model based on TreeExplainer."""

    def __init__(self, tree_model, **kwargs):
        """Initialize the TreeScoringModel.

        :param tree_model: The tree model to build the TreeExplainer from for local explanations.
        :type tree_model: tree-based model
        """
        super(TreeScoringModel, self).__init__(**kwargs)
        self._logger.debug('Initializing TreeScoringModel')
        self.tree_explainer = shap.TreeExplainer(tree_model)

    def explain(self, evaluation_examples):
        """Use the TreeExplainer and tree model for scoring to get the feature importance values of data.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on
            which to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return local_importance_values: For a model with a single output such as regression,
            this returns a matrix of feature importance values. For models with vector outputs
            this function returns a list of such matrices, one for each output. The dimension
            of this matrix is (# examples x # features).
        :rtype local_importance_values: list
        """
        return self.tree_explainer.shap_values(evaluation_examples)

    def __getstate__(self):
        """Influence how TreeScoringModel is pickled.

        Removes logger which is not serializable.

        :return state: The state to be pickled, with logger removed.
        :rtype state: dict
        """
        odict = self.__dict__.copy()
        del odict[LOGGER]
        return odict

    def __setstate__(self, dict):
        """Influence how TreeScoringModel is unpickled.

        Re-adds logger which is not serializable.

        :param dict: A dictionary of deserialized state.
        :type dict: dict
        """
        self.__dict__.update(dict)
        parent = logging.getLogger(AZUREML)
        self._logger = parent.getChild(self._identity)


class KNNScoringModel(ScoringModel):
    """Defines a scoring model based on 1-Nearest Neighbor."""

    def __init__(self, evaluation_examples, local_importance_values, **kwargs):
        """Initialize the KNNScoringModel.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param local_importance_values: The feature importance values.
        :type local_importance_values: list
        """
        super(KNNScoringModel, self).__init__(**kwargs)
        self._logger.debug('Initializing KNNScoringModel')
        # normalize features prior to using knn
        from sklearn.preprocessing import StandardScaler
        if sp.sparse.issparse(evaluation_examples):
            self._logger.debug('In KNNScoringModel for sparse data using StandardScaler without mean')
            self.scaler = StandardScaler(with_mean=False).fit(evaluation_examples)
        else:
            self._logger.debug('In KNNScoringModel for dense data using StandardScaler with mean')
            self.scaler = StandardScaler().fit(evaluation_examples)
        # compute nearest neighbors, can be used in scoring path
        from sklearn.neighbors import NearestNeighbors
        scaled_data = self.scaler.transform(evaluation_examples)
        self.neighbors = NearestNeighbors(n_neighbors=1, algorithm=SKLearn.BALL_TREE).fit(scaled_data)
        self.nn_feature_importance = np.array(local_importance_values)
        self.classification = len(self.nn_feature_importance.shape) == 3

    def explain(self, evaluation_examples):
        """Use the KNN model for scoring to approximate the feature importance values of data.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on
            which to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return local_importance_values: For a model with a single output such as regression,
            this returns a matrix of feature importance values. For models with vector outputs
            this function returns a list of such matrices, one for each output. The dimension
            of this matrix is (# examples x # features).
        :rtype local_importance_values: list
        """
        _, indices = self.neighbors.kneighbors(self.scaler.transform(evaluation_examples))
        # flatten indices for 1-NN
        indices = [index for row in indices for index in row]
        if self.classification:
            shap_values = []
            for i in range(self.nn_feature_importance.shape[0]):
                shap_values.append(self.nn_feature_importance[i][indices].tolist())
            return shap_values
        else:
            return self.nn_feature_importance[indices].tolist()

    def __getstate__(self):
        """Influence how KNNScoringModel is pickled.

        Removes logger which is not serializable.

        :return state: The state to be pickled, with logger removed.
        :rtype state: dict
        """
        odict = self.__dict__.copy()
        del odict[LOGGER]
        return odict

    def __setstate__(self, dict):
        """Influence how KNNScoringModel is unpickled.

        Re-adds logger which is not serializable.

        :param dict: A dictionary of deserialized state.
        :type dict: dict
        """
        self.__dict__.update(dict)
        parent = logging.getLogger(AZUREML)
        self._logger = parent.getChild(self._identity)


class LinearScoringModel(ScoringModel):
    """Defines a scoring model based on LinearExplainer."""

    def __init__(self, linear_model, initialization_examples, **kwargs):
        """Initialize the LinearScoringModel.

        :param linear_model: The linear model to build the LinearExplainer from for local explanations.
        :type linear_model: linear model
        """
        super(LinearScoringModel, self).__init__(**kwargs)
        self._logger.debug('Initializing TreeScoringModel')
        self.linear_explainer = shap.LinearExplainer(linear_model, initialization_examples)

    def explain(self, evaluation_examples):
        """Use the LinearExplainer for scoring to get the feature importance values of data.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on
            which to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return local_importance_values: For a model with a single output such as regression,
            this returns a matrix of feature importance values. For models with vector outputs
            this function returns a list of such matrices, one for each output. The dimension
            of this matrix is (# examples x # features).
        :rtype local_importance_values: list
        """
        return self.linear_explainer.shap_values(evaluation_examples)

    def __getstate__(self):
        """Influence how LinearScoringModel is pickled.

        Removes logger which is not serializable.

        :return state: The state to be pickled, with logger removed.
        :rtype state: dict
        """
        odict = self.__dict__.copy()
        del odict[LOGGER]
        return odict

    def __setstate__(self, dict):
        """Influence how LinearScoringModel is unpickled.

        Re-adds logger which is not serializable.

        :param dict: A dictionary of deserialized state.
        :type dict: dict
        """
        self.__dict__.update(dict)
        parent = logging.getLogger(AZUREML)
        self._logger = parent.getChild(self._identity)
