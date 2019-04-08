# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for Text featurizers."""
from typing import Any

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from automl.client.core.common.featurization.data.word_embeddings_info import EmbeddingInfo
from automl.client.core.common.featurization.text.stats_transformer import StatsTransformer
from automl.client.core.common.featurization.text.bagofwords_transformer import BagOfWordsTransformer
from automl.client.core.common.featurization.text.wordembedding_transformer import WordEmbeddingTransformer
from automl.client.core.common.featurization.text.stringcast_transformer import StringCastTransformer
from automl.client.core.common.featurization.generic.modelbased_target_encoder import ModelBasedTargetEncoder
from automl.client.core.common.featurization.data import DataProviders


class TextFeaturizers:
    """Container for Text featurizers."""

    @classmethod
    def bow_transformer(cls, *args: Any, **kwargs: Any) -> BagOfWordsTransformer:
        """Create bag of words transformer."""
        return BagOfWordsTransformer(*args, **kwargs)

    @classmethod
    def count_vectorizer(cls, *args: Any, **kwargs: Any) -> CountVectorizer:
        """Create count vectorizer featurizer."""
        return CountVectorizer(*args, **kwargs)

    @classmethod
    def naive_bayes(cls, *args: Any, **kwargs: Any) -> ModelBasedTargetEncoder:
        """Create naive bayes featurizer."""
        if not kwargs:
            kwargs = {}

        kwargs["model_class"] = MultinomialNB
        return ModelBasedTargetEncoder(*args, **kwargs)

    @classmethod
    def string_cast(cls, *args: Any, **kwargs: Any) -> StringCastTransformer:
        """Create string cast featurizer."""
        return StringCastTransformer(*args, **kwargs)

    @classmethod
    def text_stats_transformer(cls, *args: Any, **kwargs: Any) -> StatsTransformer:
        """Create text stats transformer."""
        return StatsTransformer(*args, **kwargs)

    @classmethod
    def text_target_encoder(cls, *args: Any, **kwargs: Any) -> ModelBasedTargetEncoder:
        """Create text target encoder."""
        return ModelBasedTargetEncoder(*args, **kwargs)

    @classmethod
    def tfidf_vectorizer(cls, *args: Any, **kwargs: Any) -> TfidfVectorizer:
        """Create tfidf featurizer."""
        return TfidfVectorizer(*args, **kwargs)

    @classmethod
    def word_embeddings(cls, embeddings_name: str = EmbeddingInfo.ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300,
                        *args: Any, **kwargs: Any) -> WordEmbeddingTransformer:
        """
        Create word embedding based transformer.

        :param embeddings_name: Name of the embeddings of interest.
        """
        kwargs = {}
        assert embeddings_name is not None and embeddings_name in EmbeddingInfo._all_
        if WordEmbeddingTransformer.EMBEDDING_PROVIDER_KEY not in kwargs:
            kwargs[WordEmbeddingTransformer.EMBEDDING_PROVIDER_KEY] = DataProviders.get(embeddings_name)
        return WordEmbeddingTransformer(*args, **kwargs)

    @classmethod
    def get(cls, sweeper_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Create and return the request sweeper.

        :param sweeper_name: Name of the requested sweeper.
        """
        if hasattr(cls, sweeper_name):
            member = getattr(cls, sweeper_name)
            if hasattr(member, "__call__"):  # Check that the member is a callable
                return member(*args, **kwargs)
        return None
