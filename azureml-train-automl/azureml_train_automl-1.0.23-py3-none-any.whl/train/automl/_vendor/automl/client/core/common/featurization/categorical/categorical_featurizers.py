# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for Categorical featurizers."""
from typing import Any

from automl.client.core.common.featurization.generic.countbased_target_encoder import CountBasedTargetEncoder

from .cat_imputer import CatImputer
from .hashonehotvectorizer_transformer import HashOneHotVectorizerTransformer
from .labelencoder_transformer import LabelEncoderTransformer


class CategoricalFeaturizers:
    """Container for Categorical featurizers."""

    @classmethod
    def cat_imputer(cls, *args: Any, **kwargs: Any) -> CatImputer:
        """Create categorical imputer."""
        return CatImputer(*args, **kwargs)

    @classmethod
    def hashonehot_vectorizer(cls, *args: Any, **kwargs: Any) -> HashOneHotVectorizerTransformer:
        """Create hash one hot vectorizer."""
        return HashOneHotVectorizerTransformer(*args, **kwargs)

    @classmethod
    def labelencoder(cls, *args: Any, **kwargs: Any) -> LabelEncoderTransformer:
        """Create label encoder."""
        return LabelEncoderTransformer(*args, **kwargs)

    @classmethod
    def cat_targetencoder(cls, *args: Any, **kwargs: Any) -> CountBasedTargetEncoder:
        """Create categorical target encoder featurizer."""
        if not kwargs:
            kwargs = {}

        return CountBasedTargetEncoder(*args, **kwargs)
