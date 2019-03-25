# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods used by automated machine learning."""
from automl.client.core.common import utilities as common_utilities
from automl.client.core.common.exceptions import AutoMLException
from msrest.exceptions import HttpOperationError

from . import _constants_azureml


def friendly_http_exception(exception: HttpOperationError, api_name: str):
    """
    Friendly exceptions for a http exceptions.

    :param exception: Exception.
    :param api_name: string.
    :raise: ServiceException
    """
    try:
        # Raise bug with msrest team that response.status_code is always 500
        status_code = exception.error.response.status_code
        if status_code == 500:
            message = exception.message
            substr = 'Received '
            status_code = message[message.find(
                substr) + len(substr): message.find(substr) + len(substr) + 3]
    except Exception:
        raise exception.with_traceback(exception.__traceback__)

    if status_code in _constants_azureml.HTTP_ERROR_MAP:
        http_error = _constants_azureml.HTTP_ERROR_MAP[status_code]
    else:
        http_error = _constants_azureml.HTTP_ERROR_MAP['default']
    if api_name in http_error:
        error_message = http_error[api_name]
    else:
        error_message = http_error['default']
    raise AutoMLException(
        "{0} error raised. {1}".format(http_error['Name'], error_message), http_error['type']
    ).with_traceback(exception.__traceback__) from exception


def get_primary_metrics(task):
    """
    Get the primary metrics supported for a given task as a list.

    :param task: string "classification" or "regression".
    :return: A list of the primary metrics supported for the task.
    """
    return common_utilities.get_primary_metrics(task)


def _get_package_version():
    """
    Get the package version string.

    :return: The version string.
    """
    from . import __version__
    return __version__
