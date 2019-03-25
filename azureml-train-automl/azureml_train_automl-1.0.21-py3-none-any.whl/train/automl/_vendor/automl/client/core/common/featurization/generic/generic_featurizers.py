# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for generic featurizers."""

from sklearn.preprocessing import Imputer

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
