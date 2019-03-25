# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with azureml.dataprep."""
# TODO: Remove this file once remote runs have fully migrated to use SDK's remote script.
from automl.client.core.common.dataprep_utilities import DATAPREP_INSTALLED
from automl.client.core.common.dataprep_utilities import try_retrieve_pandas_dataframe, try_retrieve_numpy_array, \
    try_resolve_cv_splits_indices, get_dataprep_json, save_dataflows_to_json, load_dataflows_from_json, is_dataflow, \
    try_retrieve_pandas_dataframe_adb
