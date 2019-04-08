# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""IoC container for data providers."""
from typing import Any, Dict, Optional

from automl.client.core.common.featurization.data.abstract_wordembeddings_provider \
    import AbstractWordEmbeddingsProvider
from automl.client.core.common.featurization.data.automl_wordembeddings_provider import AutoMLEmbeddingsProvider
from automl.client.core.common.featurization.data.word_embeddings_info import EmbeddingInfo


class DataProviders:
    """IoC container for data providers."""

    @classmethod
    def get(cls, embeddings_name: str) -> Any:
        """
        Get data provider based on embedding name.

        :param embeddings_name: Name of the embeddings.
        """
        if embeddings_name in EmbeddingInfo._all_:
            factory_method = getattr(cls, embeddings_name)
            if factory_method:
                return factory_method()

        return None

    @classmethod
    def wiki_news_300d_1M_subword(cls, *args: Any, **kwargs: Any) -> AutoMLEmbeddingsProvider:
        """Create fast text based word embeddings provider."""
        return AutoMLEmbeddingsProvider(*args, **kwargs)
