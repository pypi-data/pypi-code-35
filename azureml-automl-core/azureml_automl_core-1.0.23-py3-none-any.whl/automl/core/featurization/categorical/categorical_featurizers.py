# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for Categorical featurizers."""
from .cat_imputer import CatImputer
from .hashonehotvectorizer_transformer import HashOneHotVectorizerTransformer
from .labelencoder_transformer import LabelEncoderTransformer


class CategoricalFeaturizers:
    """Container for Categorical featurizers."""

    @classmethod
    def cat_imputer(cls, *args, **kwargs):
        """Create categorical imputer."""
        return CatImputer(*args, **kwargs)

    @classmethod
    def hashonehot_vectorizer(cls, *args, **kwargs):
        """Create hash one hot vectorizer."""
        return HashOneHotVectorizerTransformer(*args, **kwargs)

    @classmethod
    def labelencoder(cls, *args, **kwargs):
        """Create label encoder."""
        return LabelEncoderTransformer(*args, **kwargs)
