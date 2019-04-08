# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for generic featurizers."""

from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import Imputer, MaxAbsScaler

from .imputation_marker import ImputationMarker
from .lambda_transformer import LambdaTransformer


class GenericFeaturizers:
    """Container for generic featurizers."""

    @classmethod
    def imputation_marker(cls, *args, **kwargs):
        """Create imputation marker."""
        return ImputationMarker(*args, **kwargs)

    @classmethod
    def lambda_featurizer(cls, *args, **kwargs):
        """Create lambda featurizer."""
        return LambdaTransformer(*args, **kwargs)

    @classmethod
    def imputer(cls, *args, **kwargs):
        """Create Imputer."""
        return Imputer(*args, **kwargs)

    @classmethod
    def minibatchkmeans_featurizer(cls, *args, **kwargs):
        """Create mini batch k means featurizer."""
        return MiniBatchKMeans(*args, **kwargs)

    @classmethod
    def maxabsscaler(cls, *args, **kwargs):
        """Create maxabsscaler featurizer."""
        return MaxAbsScaler(*args, **kwargs)
