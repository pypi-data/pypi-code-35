# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for Text featurizers."""
from typing import Any

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from .wordembedding_transformer import WordEmbeddingTransformer
from .stringcast_transformer import StringCastTransformer
from ..generic.modelbased_target_encoder import ModelBasedTargetEncoder
from ..data import DataProviders


class TextFeaturizers:
    """Container for Text featurizers."""

    @classmethod
    def string_cast(cls, *args: Any, **kwargs: Any) -> StringCastTransformer:
        """Create string cast featurizer."""
        return StringCastTransformer(*args, **kwargs)

    @classmethod
    def naive_bayes(cls, *args: Any, **kwargs: Any) -> ModelBasedTargetEncoder:
        """Create naive bayes featurizer."""
        if not kwargs:
            kwargs = {}

        kwargs["model_class"] = MultinomialNB
        return ModelBasedTargetEncoder(*args, **kwargs)

    @classmethod
    def count_vectorizer(cls, *args: Any, **kwargs: Any) -> CountVectorizer:
        """Create count vectorizer featurizer."""
        return CountVectorizer(*args, **kwargs)

    @classmethod
    def tfidf_vectorizer(cls, *args: Any, **kwargs: Any) -> TfidfVectorizer:
        """Create tfidf featurizer."""
        return TfidfVectorizer(*args, **kwargs)

    @classmethod
    def text_target_encoder(cls, *args: Any, **kwargs: Any) -> ModelBasedTargetEncoder:
        """Create text target encoder."""
        return ModelBasedTargetEncoder(*args, **kwargs)

    @classmethod
    def word_embeddings(cls, *args: Any, **kwargs: Any) -> WordEmbeddingTransformer:
        """Create word embedding based transformer."""
        if not kwargs:
            kwargs = {}

        if WordEmbeddingTransformer.EMBEDDING_PROVIDER_KEY not in kwargs:
            kwargs[WordEmbeddingTransformer.EMBEDDING_PROVIDER_KEY] = DataProviders.fasttext_wordembeddings_provider()
        return WordEmbeddingTransformer(*args, **kwargs)
