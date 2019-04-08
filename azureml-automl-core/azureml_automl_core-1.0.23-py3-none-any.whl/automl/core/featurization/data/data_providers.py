# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""IoC container for data providers."""
from typing import Any
from .automl_wordembeddings_provider import AutoMLEmbeddingsProvider


class DataProviders:
    """IoC container for data providers."""

    @classmethod
    def fasttext_wordembeddings_provider(cls, *args: Any, **kwargs: Any) -> AutoMLEmbeddingsProvider:
        """Create fast text word embeddings provider."""
        return AutoMLEmbeddingsProvider()
