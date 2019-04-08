# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the TreeExplainer for returning explanations for tree-based models."""

from azureml.explain.model.shap import tree_explainer
from azureml.explain.model.dataset.decorator import tabular_decorator
from azureml.explain.model._internal.constants import ExplainParams
from ..scoring.scoring_model import KNNScoringModel
from ..explanation.explanation import _create_local_explanation
from .kwargs_utils import _get_explain_global_kwargs
from ..common.aggregate import contrib_aggregator


@contrib_aggregator
class TreeExplainer(tree_explainer.TreeExplainer):
    """Defines the TreeExplainer for returning explanations for tree-based models."""

    @tabular_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None, create_scoring_model=False):
        """Explain the model globally by aggregating local explanations to global.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :param create_scoring_model: Creates a model that can be used for scoring to approximate the feature
            importance values.
        :type create_scoring_model: bool
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation which also has the properties
            of LocalExplanation and ExpectedValuesMixin. If the model is a classifier, it will have the properties of
            PerClassMixin. If create_scoring_model is set to True, it will have the properties of HasScoringModel.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = _get_explain_global_kwargs(sampling_policy, create_scoring_model)
        return self._explain_global(evaluation_examples, **kwargs)

    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Explain the model by using shap's tree explainer.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: DatasetWrapper
        :return: A model explanation object. It is guaranteed to be a LocalExplanation which also has the properties
            of ExpectedValuesMixin. If the model is a classfier, it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        kwargs = super(TreeExplainer, self)._get_explain_local_kwargs(evaluation_examples)
        scoring_model = None
        if self._create_scoring_model:
            scoring_model = KNNScoringModel(evaluation_examples.dataset, kwargs[ExplainParams.LOCAL_IMPORTANCE_VALUES])
        kwargs[ExplainParams.SCORING_MODEL] = scoring_model
        return _create_local_explanation(**kwargs)
