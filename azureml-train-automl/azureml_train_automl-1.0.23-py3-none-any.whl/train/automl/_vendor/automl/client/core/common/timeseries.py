# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Includes classes for storing timeseries preprocessing related functions."""

import warnings
import pandas as pd
# Classes have been moved to Featurization module. Referring are retained here for backward compatibility.
from automl.client.core.common.featurization import TimeSeriesTransformer, NumericalizeTransformer, \
    MissingDummiesTransformer


# Prevent warnings when using Jupyter
warnings.simplefilter("ignore")
pd.options.mode.chained_assignment = None
