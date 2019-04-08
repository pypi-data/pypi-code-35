# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Init file for azureml-contrib-explain-model/azureml/contrib/explain/model/mimic/models."""
from .linear_model import SGDExplainableModel, LinearExplainableModel

__all__ = ["SGDExplainableModel", "LinearExplainableModel"]
