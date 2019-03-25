# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Package containing modules used in automated machine learning.

Included classes provide resources for configuring, managing pipelines, and examining run output
for automated machine learning experiments.

For more information on automated machine learning, please see 
https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-automated-ml
"""
import os
import sys

vendor_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "_vendor"))
sys.path.append(vendor_folder)

from automl.client.core.common.utilities import extract_user_data, get_sdk_dependencies

from .automl import fit_pipeline
from .automlconfig import AutoMLConfig
from .automl_step import AutoMLStep

__all__ = [
    'AutoMLConfig',
    'AutoMLStep',
    'fit_pipeline',
    'extract_user_data',
    'get_sdk_dependencies']

try:
    from ._version import ver as VERSION
    __version__ = VERSION
except ImportError:
    VERSION = '0.0.0+dev'
    __version__ = VERSION
