# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Auto ML common logging module."""
import logging

from automl.client.core.common import logging_utilities as log_utils
from automl.client.core.common.activity_logger import TelemetryActivityLogger
from azureml.telemetry import AML_INTERNAL_LOGGER_NAMESPACE, get_telemetry_log_handler

TELEMETRY_AUTOML_COMPONENT_KEY = 'automl'


def get_logger(
    log_file_name=None,
    verbosity=logging.DEBUG,
    automl_settings=None
):
    """
    Create the logger with telemetry hook.

    :param log_file_name: log file name
    :param verbosity: logging verbosity
    :return logger if log file name is provided otherwise null logger
    :rtype
    """
    telemetry_handler = get_telemetry_log_handler(component_name=TELEMETRY_AUTOML_COMPONENT_KEY)
    try:
        from automl.client.core.common import __version__ as common_core_version
        from azureml.train.automl import __version__ as sdk_version
    except Exception:
        common_core_version = None
        sdk_version = None
    custom_dimensions = {
        "automl_client": "azureml",
        "common_core_version": common_core_version,
        "automl_sdk_version": sdk_version
    }
    if automl_settings is not None:
        if automl_settings.is_timeseries:
            task_type = "forecasting"
        else:
            task_type = automl_settings.task_type
        custom_dimensions.update(
            {
                "experiment_id": automl_settings.name,
                "task_type": task_type,
                "compute_target": automl_settings.compute_target,
                "subscription_id": automl_settings.subscription_id,
                "region": automl_settings.region
            }
        )
    logger = TelemetryActivityLogger(
        namespace=AML_INTERNAL_LOGGER_NAMESPACE,
        filename=log_file_name,
        verbosity=verbosity,
        extra_handlers=[telemetry_handler],
        custom_dimensions=custom_dimensions)
    return logger
