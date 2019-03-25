# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for Text featurizers."""
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from .naive_bayes import NaiveBayes
from .stringcast_transformer import StringCastTransformer


class TextFeaturizers:
    """Container for Text featurizers."""

    @classmethod
    def string_cast(cls, *args, **kwargs):
        """Create string cast featurizer."""
        return StringCastTransformer(*args, **kwargs)

    @classmethod
    def naive_bayes(cls, *args, **kwargs):
        """Create naive bayes featurizer."""
        return NaiveBayes(*args, **kwargs)

    @classmethod
    def count_vectorizer(cls, *args, **kwargs):
        """Create count vectorizer featurizer."""
        return CountVectorizer(*args, **kwargs)

    @classmethod
    def tfidf_vectorizer(cls, *args, **kwargs):
        """Create tfidf featurizer."""
        return TfidfVectorizer(*args, **kwargs)
