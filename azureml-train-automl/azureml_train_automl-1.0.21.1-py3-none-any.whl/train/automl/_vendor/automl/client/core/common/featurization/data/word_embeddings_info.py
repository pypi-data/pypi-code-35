# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holder for embedding information."""
from typing import cast, Dict, Optional, Tuple


class EmbeddingInfo:
    """Class to hold information of embeddings."""

    ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300 = "fasttext-wiki-news-subwords-300"

    def __init__(self, user_friendly_name: str, embedding_name: str, download_url: str, file_name: str, extension: str,
                 lower_case: bool, license: str, credits: str):
        """
        Create embedding info object.

        :param embedding_name: Name of the embedding.
        :param download_url: Url to download from.
        :param file_name: Name of the file in the url or if it's an archive being downloaded.
        :param extension: Extension of the downloaded file.
        :param lower_case: True if the training happened on strings after lower casing.
        """
        self._user_friendly_name = user_friendly_name
        self._embedding_name = embedding_name
        self._download_url = download_url
        self._file_name = file_name
        self._extension = extension
        self._lower_case = lower_case
        self._license = license
        self._credits = credits


# TODO Make this a full fledged class and move to config
class WordEmbeddingsInfo:
    """Word embeddings information holder."""

    embeddings = {EmbeddingInfo.ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300: EmbeddingInfo(
        user_friendly_name="English word embeddings trained on wikipedia and web",
        embedding_name=EmbeddingInfo.ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300,
        download_url="https://aka.ms/automl-resources/WordVectors/wiki-news-300d-1M-subword.vec.zip",
        file_name="wiki-news-300d-1M-subword.vec",
        extension="zip",
        lower_case=False,
        license="Creative Commons Attribution-Share-Alike License (3.0). More information can be found at: "
                "https://creativecommons.org/licenses/by-sa/3.0/",
        credits="Advances in Pre-Training Distributed Word Representations by P. Bojanowski, E. Grave, A. Joulin, "
                "T. Mikolov, Proceedings of the International Conference on Language Resources and Evaluation "
                "(LREC 2018). More information can be found at: https://fasttext.cc and "
                "http://https://arxiv.org/abs/1712.09405")}   # type: Dict[str, EmbeddingInfo]

    @classmethod
    def get(cls, embeddings_name: str) -> Optional[EmbeddingInfo]:
        """
        Get embedding information given the name.

        :param embeddings_name: Name of the requested embeddings.
        :return: Information on the embeddings.
        """
        return cls.embeddings[embeddings_name] if embeddings_name in cls.embeddings else None
