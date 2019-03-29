# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Creates word embeddings from pre-trained models."""
from typing import Callable, Dict, List, Optional, Union

import re
from logging import Logger

import numpy as np
from automl.client.core.common.types import DataSingleColumnInputType
from automl.client.core.common.featurization.automltransformer import AutoMLTransformer
from automl.client.core.common.featurization.data import AbstractWordEmbeddingsProvider


class WordEmbeddingTransformer(AutoMLTransformer):
    """Creates word embeddings from pre-trained models."""

    def __init__(self,
                 embeddings_provider: AbstractWordEmbeddingsProvider,
                 logger: Optional[Logger] = None,
                 token_pattern: str = r"(?u)\b\w+\b") -> None:          # TODO Inject tokenizer
        """
        Create word embeddings from pre-trained models.

        :param: embeddings_provider: Embeddings provider for the model.
        :param logger: Logger.
        :param token_pattern: Token pattern for splitting the sentence into words.

        """
        self._init_logger(logger)
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        # len(word2vec.itervalues().next())
        self.model = None                                               # type: Optional[Dict[str, np.ndarray]]
        self.dim = 0
        self._is_lower = False
        self.token_pattern = token_pattern
        self.tokenizer = re.compile(self.token_pattern)
        self._provider = embeddings_provider

    def fit(self, X, y=None):
        """
        Fit method.

        :param X: Input data.
        :param y: Labels.
        :return: self.
        """
        self.model = self._provider.model
        if self.model is None:
            # raise DataException("Could not load word embeddings.")
            self.model = {}
            self.dim = 0
        else:
            self.dim = self._provider.vector_size
            self._is_lower = self._provider.is_lower

        return self

    def transform(self, X: DataSingleColumnInputType, y: DataSingleColumnInputType = None) -> np.ndarray:
        """
        Transform method.

        :param X: Input data.
        :param y: Labels.
        :return: Transformed data.
        """
        return self._agg_transformer(X, np.mean) if self.model else np.array([])

    def __getstate__(self):
        """
        Overriden to remove model object when pickling.

        :return: this object's state as a dictionary
        """
        state = super(WordEmbeddingTransformer, self).__getstate__()
        newstate = {**state, **self.__dict__}
        newstate['model'] = None
        newstate['provider'] = None
        return newstate

    def _analyzer(self, doc: str) -> List[str]:
        """Tokenize and provide a list of tokens.

        :param doc: Document to tokenize.
        :return: List of tokens identified.
        """
        return self.tokenizer.findall(doc)

    def _agg_transformer(self, X: DataSingleColumnInputType, agg_func: Callable[..., np.ndarray]) \
            -> np.ndarray:
        """
        Create word embeddings for the given input. Use agg_func for aggregation to create sentence vectors.

        :param X: Input.
        :param agg_func: Aggregation function to use for creating sentence vectors.
        :return: Embedding vectors for each of the sentences.
        """
        target = []                                                     # type: List[np.ndarray]
        if isinstance(X, np.ndarray):
            X = X.reshape(-1)
        for doc in X:
            # TODO Creation abstraction for aggregation function.
            embeddings = agg_func([self._get_embedding(w) for w in self._analyzer(doc)], axis=0)
            target.append(embeddings)
            del embeddings

        t = np.array(target)
        del target
        return t

    def _get_embedding(self, x: str) -> np.ndarray:
        """
        Return embeddings found for the input string in training data. Else return zeros.

        :param x: Input string.
        :return: Embeddings of this string or zeros if the string is not found in the training data.
        """
        if self._is_lower:
            x = x.lower()

        if self.model and x in self.model:
            return self.model[x]
        else:
            return np.zeros(self.dim)
