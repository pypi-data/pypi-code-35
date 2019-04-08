# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility functions for memory related operations."""
import sys

import numpy as np
import scipy
import pandas as pd


def get_data_memory_size(data):
    """
    Return the total memory size of this object.

    This utility function currently supports approximate sizes of numpy ndarray,
    sparse matrix and pandas DataFrame.

    :param data: data object primarily for training
    :type data: numpy.ndarray or scipy.sparse or pandas.DataFrame or some python object
    :return: estimated memory size of the python object in bytes.
    """
    if scipy.sparse.issparse(data):
        return data.data.nbytes + data.indptr.nbytes + data.indices.nbytes
    elif isinstance(data, pd.DataFrame):
        return data.memory_usage(index=True, deep=True).sum()
    elif isinstance(data, np.ndarray):
        if sys.getsizeof(data) > data.nbytes:
            return sys.getsizeof(data)
        else:
            return data.nbytes

    # For ndarrays and other object types, return memory size by sys.getsizeof()
    return sys.getsizeof(data)
