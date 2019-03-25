# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the Mimic Explainer for computing explanations on black box models or functions.

The mimic explainer trains an explainable model to reproduce the output of the given black box model.
The explainable model is called a surrogate model and the black box model is called a teacher model.
Once trained to reproduce the output of the teacher model, the surrogate model's explanation can
be used to explain the teacher model.
"""

import numpy as np

from azureml.explain.model._internal.common import _order_imp

from ..common.blackbox_explainer import BlackBoxExplainer
from ..common.explanation_utils import _convert_to_list, _generate_augmented_data

from .model_distill import model_distill
from ..explanation.explanation import _create_local_explanation, _create_global_explanation, \
    _aggregate_global_from_local_explanation
from ..dataset.decorator import tabular_decorator, init_tabular_decorator
from ..dataset.dataset_wrapper import DatasetWrapper
from azureml.explain.model._internal.constants import ExplainParams, ExplainType

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    from shap.common import DenseData


class MimicExplainer(BlackBoxExplainer):
    """Defines the Mimic Explainer for explaining black box models or functions."""

    @init_tabular_decorator
    def __init__(self, model, initialization_examples, explainable_model, explainable_model_args={},
                 is_function=False, augment_data=True, max_num_of_augmentations=1000, explain_subset=None,
                 features=None, classes=None, **kwargs):
        """Initialize the MimicExplainer.

        :param model: The black box model or function (if is_function is True) to be explained.  Also known
            as the teacher model.
        :type model: model that implements predict or predict_proba or function that accepts a 2d ndarray
        :param initialization_examples: A matrix of feature vector examples (# examples x # features) for
            initializing the explainer.
        :type initialization_examples: numpy.array or pandas.DataFrame or iml.datatypes.DenseData or
            scipy.sparse.csr_matrix
        :param explainable_model: The uninitialized surrogate model used to explain the black box model.
            Also known as the student model.
        :type explainable_model: BaseExplainableModel
        :param explainable_model_args: An optional map of arguments to pass to the explainable model
            for initialization.
        :type explainable_model_args: dict
        :param is_function: Default set to false, set to True if passing function instead of model.
        :type is_function: bool
        :param augment_data: If true, oversamples the initialization examples to improve surrogate
            model accuracy to fit teacher model.  Useful for high-dimensional data where
            the number of rows is less than the number of columns.
        :type augment_data: bool
        :param max_num_of_augmentations: max number of times we can increase the input data size.
        :type max_num_of_augmentations: int
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation. Note for mimic explainer this will
            not affect the execution time of getting the global explanation.
        :type explain_subset: list[int]
        :param features: A list of feature names.
        :type features: list[str]
        :param classes: Class names as a list of strings. The order of the class names should match
            that of the model output.  Only required if explaining classifier.
        :type classes: list[str]
        """
        super(MimicExplainer, self).__init__(model, is_function=is_function, **kwargs)
        self._logger.debug('Initializing MimicExplainer')
        self.initialization_examples = initialization_examples
        self.features = features
        self.classes = classes
        self.explain_subset = explain_subset
        # Train the mimic model on the given model
        training_data = self.initialization_examples.dataset
        if isinstance(training_data, DenseData):
            training_data = training_data.data

        # augment the data if necessary
        if augment_data:
            training_data = _generate_augmented_data(training_data,
                                                     max_num_of_augmentations=max_num_of_augmentations)
        self.surrogate_model = model_distill(self.function, explainable_model, training_data,
                                             explainable_model_args)

    def explain_global(self, evaluation_examples=None):
        """Globally explains the blackbox model using the surrogate model.

        If evaluation_examples are unspecified, retrieves global feature importances from explainable
        surrogate model.  Note this will not include per class feature importances.  If evaluation_examples
        are specified, aggregates local explanations to global from the given evaluation_examples - which
        computes both global and per class feature importances.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which to
            explain the model's output.  If specified, computes feature importances through aggregation.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation. If evaluation_examples are
            passed in, it will also have the properties of a LocalExplanation. If the model is a classifier (has
            predict_proba), it will have the properties of ClassesMixin, and if evaluation_examples were passed in it
            will also have the properties of PerClassMixin.
        :rtype: DynamicGlobalExplanation
        """
        is_classification = self.predict_proba_flag
        kwargs = {ExplainParams.METHOD: ExplainType.MIMIC}
        if is_classification:
            kwargs[ExplainParams.CLASSES] = self.classes
        if evaluation_examples is not None:
            if not isinstance(evaluation_examples, DatasetWrapper):
                self._logger.debug('Eval examples not wrapped, wrapping')
                evaluation_examples = DatasetWrapper(evaluation_examples)
            # first get local explanation
            local_explanation = self.explain_local(evaluation_examples)
            # Aggregate local explanation to global
            return _aggregate_global_from_local_explanation(local_explanation=local_explanation,
                                                            **kwargs)
        global_importance_values = self.surrogate_model.explain_global()
        order = _order_imp(global_importance_values)
        return _create_global_explanation(expected_values=None, classification=is_classification,
                                          global_importance_values=global_importance_values,
                                          global_importance_rank=order, features=self.features,
                                          **kwargs)

    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Locally explains the blackbox model using the surrogate model.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: A model explanation object. It is guaranteed to be a LocalExplanation. If the model is a classifier,
            it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        local_importance_values = self.surrogate_model.explain_local(evaluation_examples.dataset)
        is_classification = self.predict_proba_flag
        is_binary = isinstance(local_importance_values, np.ndarray)
        # If binary case, we need to reformat the data to have importances per class
        if is_classification and is_binary:
            local_importance_values = [-local_importance_values, local_importance_values]
        kwargs = {ExplainParams.METHOD: ExplainType.MIMIC}
        kwargs[ExplainParams.FEATURES] = self.features
        if is_classification:
            kwargs[ExplainParams.CLASSES] = self.classes
        # Reformat local_importance_values result if explain_subset specified
        if self.explain_subset:
            self._logger.debug('Getting subset of local_importance_values')
            if is_classification:
                for i in range(len(local_importance_values)):
                    local_importance_values[i] = local_importance_values[i][:, self.explain_subset]
            else:
                local_importance_values = local_importance_values[:, self.explain_subset]
        local_importance_values = _convert_to_list(local_importance_values)
        return _create_local_explanation(local_importance_values=np.array(local_importance_values),
                                         expected_values=None,
                                         classification=is_classification,
                                         **kwargs)
