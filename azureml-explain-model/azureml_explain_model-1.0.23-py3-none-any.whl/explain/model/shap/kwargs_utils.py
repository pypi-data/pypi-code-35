# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines utilities for handling kwargs on SHAP-based explainers."""

from azureml.explain.model._internal.constants import ExplainParams, ExplainType


def _get_explain_global_kwargs(sampling_policy):
    """Get the kwargs for explain_global.

    :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
        SamplingPolicy for more information.
    :type sampling_policy: SamplingPolicy
    :return: Args for explain_global.
    :rtype: dict
    """
    kwargs = {ExplainParams.METHOD: ExplainType.SHAP,
              ExplainParams.SAMPLING_POLICY: sampling_policy}
    return kwargs
