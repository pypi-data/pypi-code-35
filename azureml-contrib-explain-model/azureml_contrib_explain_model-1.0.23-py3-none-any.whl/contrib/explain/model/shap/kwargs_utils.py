# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines utilities for handling kwargs on SHAP-based explainers."""

from azureml.explain.model._internal.constants import ExplainParams
from azureml.explain.model.shap import kwargs_utils


def _get_explain_global_kwargs(sampling_policy, create_scoring_model):
    """Get the kwargs for explain_global.

    :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
        SamplingPolicy for more information.
    :type sampling_policy: SamplingPolicy
    :param create_scoring_model: If true, creates a model that can be used for scoring to approximate the feature
        importance values.
    :type create_scoring_model: bool
    :return: Args for explain_global.
    :rtype: dict
    """
    kwargs = kwargs_utils._get_explain_global_kwargs(sampling_policy)
    kwargs[ExplainParams.CREATE_SCORING_MODEL] = create_scoring_model
    return kwargs
