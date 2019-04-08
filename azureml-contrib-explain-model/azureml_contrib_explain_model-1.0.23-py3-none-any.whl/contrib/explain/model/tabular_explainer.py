# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the tabular explainer meta-api for returning the best explanation result based on the given model."""

from azureml.explain.model import tabular_explainer
from azureml.explain.model.tabular_explainer import _tabular_explainer_decorator
from azureml.explain.model.dataset.decorator import tabular_decorator
from azureml.explain.model._internal.constants import ExplainParams
from .shap.tree_explainer import TreeExplainer
from .shap.deep_explainer import DeepExplainer
from .shap.kernel_explainer import KernelExplainer


class TabularExplainer(tabular_explainer.TabularExplainer):
    """Defines the tabular explainer meta-api for returning the best explanation result based on the given model."""

    @tabular_decorator
    @_tabular_explainer_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None, create_scoring_model=False):
        """Globally explains the black box model or function.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :param create_scoring_model: Creates a model that can be used for scoring to approximate the feature
            importance values of data faster than LimeTabularExplainer.
        :type create_scoring_model: bool
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation. If SHAP is used for the
            explanation, it will also have the properties of a LocalExplanation and the ExpectedValuesMixin. If the
            model does classification, it will have the properties of the PerClassMixin. If create_scoring_model is
            set to True, it will have the properties of the HasScoringModel mixin.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = {ExplainParams.SAMPLING_POLICY: sampling_policy,
                  ExplainParams.CREATE_SCORING_MODEL: create_scoring_model}
        return self.explainer.explain_global(evaluation_examples, **kwargs)

    def _get_uninitialized_explainers(self):
        """Return the uninitialized explainers used by the tabular explainer.

        :return: A list of the uninitialized explainers.
        :rtype: list
        """
        return [TreeExplainer, DeepExplainer, KernelExplainer]
