# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the tabular explainer meta-api for returning the best explanation result based on the given model."""

from .common.base_explainer import BaseExplainer
from .common.structured_model_explainer import PureStructuredModelExplainer
from .dataset.dataset_wrapper import DatasetWrapper
from .dataset.decorator import tabular_decorator
from azureml.explain.model._internal.constants import ExplainParams
from .shap.tree_explainer import TreeExplainer
from .shap.deep_explainer import DeepExplainer
from .shap.kernel_explainer import KernelExplainer
from functools import wraps

InvalidExplainerErr = 'Could not find valid explainer to explain model'


def _tabular_explainer_decorator(explain_func):
    """Decorate an explanation function to validate the model prior to calling the function.

    :param explain_func: An explanation function where the first argument is a dataset.
    :type explain_func: explanation function
    """
    @wraps(explain_func)
    def explain_func_wrapper(self, evaluation_examples, **kwargs):
        self._logger.debug('Explaining tabular data')
        return explain_func(self, evaluation_examples, **kwargs)
    return explain_func_wrapper


class TabularExplainer(BaseExplainer):
    """Defines the tabular explainer meta-api for returning the best explanation result based on the given model."""

    def __init__(self, model, initialization_examples, explain_subset=None, features=None, classes=None, **kwargs):
        """Initialize the TabularExplainer.

        :param model: The model or pipeline to explain.
        :type model: model that implements predict or predict_proba or pipeline function that accepts a 2d ndarray
        :param initialization_examples: A matrix of feature vector examples (# examples x # features) for
            initializing the explainer.
        :type initialization_examples: numpy.array or pandas.DataFrame or iml.datatypes.DenseData or
            scipy.sparse.csr_matrix
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation, which will speed up the explanation
            process when number of features is large and the user already knows the set of interested
            features. The subset can be the top-k features from the model summary.
        :type explain_subset: list[int]
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        """
        super(TabularExplainer, self).__init__(**kwargs)
        self._logger.debug('Initializing TabularExplainer')
        self.model = model
        self.features = features
        self.classes = classes
        self.explain_subset = explain_subset
        kwargs[ExplainParams.EXPLAIN_SUBSET] = explain_subset
        kwargs[ExplainParams.FEATURES] = features
        kwargs[ExplainParams.CLASSES] = classes
        if not isinstance(initialization_examples, DatasetWrapper):
            self._logger.debug('Wrapping init examples with DatasetWrapper')
            self.initialization_examples = DatasetWrapper(initialization_examples)
        else:
            self.initialization_examples = initialization_examples
        uninitialized_explainers = [TreeExplainer, DeepExplainer, KernelExplainer]
        is_valid = False
        for uninitialized_explainer in uninitialized_explainers:
            try:
                if issubclass(uninitialized_explainer, PureStructuredModelExplainer):
                    self.explainer = uninitialized_explainer(self.model, **kwargs)
                else:
                    self.explainer = uninitialized_explainer(self.model, self.initialization_examples, **kwargs)
                self._logger.info('Initialized valid explainer {} with args {}'.format(self.explainer, kwargs))
                is_valid = True
                break
            except Exception as ex:
                self._logger.info('Failed to initialize explainer {} due to error: {}'
                                  .format(uninitialized_explainer, ex))
        if not is_valid:
            self._logger.info(InvalidExplainerErr)
            raise ValueError(InvalidExplainerErr)

    @tabular_decorator
    @_tabular_explainer_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None):
        """Globally explains the black box model or function.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation. If SHAP is used for the
            explanation, it will also have the properties of a LocalExplanation and the ExpectedValuesMixin. If the
            model does classification, it will have the properties of the PerClassMixin.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = {ExplainParams.SAMPLING_POLICY: sampling_policy}
        return self.explainer.explain_global(evaluation_examples, **kwargs)

    @tabular_decorator
    @_tabular_explainer_decorator
    def explain_local(self, evaluation_examples):
        """Locally explains the black box model or function.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: A model explanation object. It is guaranteed to be a LocalExplanation. If SHAP is used for the
            explanation, it will also have the properties of the ExpectedValuesMixin. If the model does
            classification, it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        return self.explainer.explain_local(evaluation_examples)
