# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
The automated machine learning model explainer.

Included classes allow understanding of feature importance during model training. Classification and regression
models allow for different feature importance output.
"""

from automl.client.core.common.exceptions import ClientException
from automl.client.core.common.model_explanation import _convert_explanation
from . import constants
from .ensemble import Ensemble
from ._logging import get_logger


def retrieve_model_explanation(child_run):
    """
    Retrieve the model explanation from the Runhistory.

    Returns a tuple of the following values
    - shap_values = For regression model, this returns a matrix of feature importance values.
    For classification model, the dimension of this matrix is (# examples x # features).
    - expected_values = The expected value of the model applied to the set of initialization examples.
    - overall_summary = The model level feature importance values sorted in descending order.
    - overall_imp = The feature names sorted in the same order as in overall_summary or the indexes
    that would sort overall_summary.
    - per_class_summary = The class level feature importance values sorted in descending order when
    classification model is evaluated. Only available for the classification case.
    - per_class_imp = The feature names sorted in the same order as in per_class_summary or the indexes
    that would sort per_class_summary. Only available for the classification case.

    :param child_run: The run object corresponding to best pipeline.
    :type child_run: azureml.core.run.Run
    :return: tuple(shap_values, expected_values, overall_summary, overall_imp, per_class_summary and per_class_imp)
    :rtype: (Union[list, list[list]], list, list, list, list, list)
    """
    try:
        from azureml.explain.model._internal.explanation_client import ExplanationClient

        client = ExplanationClient.from_run(child_run)
        explanation = client.download_model_explanation()

        return _convert_explanation(explanation)
    except ImportError:
        raise


def explain_model(fitted_model, X_train, X_test, best_run=None, features=None, **kwargs):
    """
    Explain the model with provided X_train and X_test data.

    Returns a tuple of shap_values, expected_values, overall_summary, overall_imp, per_class_summary and
    per_class_imp
    where
    - shap_values = For regression model, this returns a matrix of feature importance values.
    For classification model, the dimension of this matrix is (# examples x # features).
    - expected_values = None.
    - overall_summary = The model level feature importance values sorted in descending order.
    - overall_imp = The feature names sorted in the same order as in overall_summary or the indexes
    that would sort overall_summary.
    - per_class_summary = The class level feature importance values sorted in descending order when
    classification model is evaluated. Only available for the classification case.
    - per_class_imp = The feature names sorted in the same order as in per_class_summary or the indexes
    that would sort per_class_summary. Only available for the classification case.

    :param fitted_model: The fitted AutoML model.
    :type fitted_model: sklearn.pipeline
    :param X_train: A matrix of feature vector examples for initializing the explainer.
    :type X_train: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
    :param X_test: A matrix of feature vector examples on which to explain the model's output.
    :type X_test: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
    :param best_run: The run object corresponding to best pipeline.
    :type best_run: azureml.core.run.Run
    :param features: A list of feature names.
    :type features: list[str]
    :param kwargs:
    :type kwargs: dict
    :return: The model's explanation
    :rtype: (Union[list, list[list]], list, list, list, list, list)
    """
    logger = get_logger()
    run_id = ""
    try:
        from azureml.explain.model.mimic.mimic_explainer import MimicExplainer
        from azureml.explain.model.mimic.models.lightgbm_model import LGBMExplainableModel
        from azureml.explain.model._internal.explanation_client import ExplanationClient

        if best_run is not None:
            run_id = best_run.id

        logger.info("[RunId:{}]Start explain model function.".format(run_id))
        # Transform the dataset for datatransformer and laggingtransformer only
        # Ensembling pipeline may group the miro pipelines into one step
        for name, transformer in fitted_model.steps[:-1]:
            if (transformer is not None) and \
                    (name == "datatransformer" or name == "laggingtransformer" or name == "timeseriestransformer"):
                X_train = transformer.transform(X_train)
                X_test = transformer.transform(X_test)
                features = transformer.get_engineered_feature_names()

        # To explain the pipeline which should exclude datatransformer and laggingtransformer
        fitted_model = Ensemble._transform_single_fitted_pipeline(fitted_model)

        class_labels = kwargs.get('classes', None)
        explainer = MimicExplainer(
            fitted_model, X_train, LGBMExplainableModel, features=features, classes=class_labels
        )

        # Explain the model and save the explanation information to artifact
        explanation = explainer.explain_global(X_test)

        if best_run is not None:
            client = ExplanationClient.from_run(best_run)
            topk = kwargs.get('top_k', 100)
            client.upload_model_explanation(explanation, top_k=topk)
            best_run.tag(constants.MODEL_EXPLANATION_TAG, 'True')

        logger.info("[RunId:{}]End explain model function.".format(run_id))

        return _convert_explanation(explanation)
    except ImportError as import_error:
        logger.warning(
            "[RunId:{}]Explain model function meets import error. Error message:{}".format(run_id, import_error)
        )
        raise
    except Exception as e:
        logger.warning("[RunId:{}]Explain model function meets error. Error message:{}".format(run_id, e))
        raise
