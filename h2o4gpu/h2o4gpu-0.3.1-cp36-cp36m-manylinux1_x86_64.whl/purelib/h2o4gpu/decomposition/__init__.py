"""
The :mod:`h2o4gpu.decomposition` module includes matrix decomposition
algorithms, including among others PCASklearn, NMF or ICA. Most of the algorithms of
this module can be regarded as dimensionality reduction techniques.
"""

from .nmf import NMF, non_negative_factorization
from .pca import PCASklearn
from .incremental_pca import IncrementalPCASklearn
from .kernel_pca import KernelPCASklearn
from .sparse_pca import SparsePCASklearn, MiniBatchSparsePCASklearn
from .truncated_svd import TruncatedSVDSklearn
from .fastica_ import FastICA, fastica
from .dict_learning import (dict_learning, dict_learning_online, sparse_encode,
                            DictionaryLearning, MiniBatchDictionaryLearning,
                            SparseCoder)
from .factor_analysis import FactorAnalysis
from ..utils.extmath import randomized_svd
from .online_lda import LatentDirichletAllocation

__all__ = ['DictionaryLearning',
           'FastICA',
           'IncrementalPCASklearn',
           'KernelPCASklearn',
           'MiniBatchDictionaryLearning',
           'MiniBatchSparsePCASklearn',
           'NMF',
           'PCASklearn',
           'SparseCoder',
           'SparsePCASklearn',
           'dict_learning',
           'dict_learning_online',
           'fastica',
           'non_negative_factorization',
           'randomized_svd',
           'sparse_encode',
           'FactorAnalysis',
           'TruncatedSVDSklearn',
           'LatentDirichletAllocation']
