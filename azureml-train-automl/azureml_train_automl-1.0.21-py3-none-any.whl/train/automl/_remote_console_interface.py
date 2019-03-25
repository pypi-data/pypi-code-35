# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Console interface for AutoML experiments logs"""

from collections import defaultdict
from datetime import datetime
import json
import numpy as np
import pytz
import time
from automl.client.core.common import constants, logging_utilities
from automl.client.core.common.metrics import minimize_or_maximize
from automl.client.core.common.console_interface import ConsoleInterface
from ._azureautomlsettings import AzureAutoMLSettings


class RemoteConsoleInterface(ConsoleInterface):
    """
    Class responsible for printing iteration information to console for a remote run
    """

    def __init__(self, logger, file_logger=None):
        """
        RemoteConsoleInterface constructor
        :param logger: Console logger for printing this info
        :param file_logger: Optional file logger for more detailed logs
        """
        self._console_logger = logger
        self.logger = file_logger
        self.metric_map = {}
        self.run_map = {}
        self.properties_map = {}
        self.best_metric = None
        super().__init__("score", self._console_logger)

    def print_scores(self, parent_run, primary_metric):
        """
        Print all history for a given parent run
        :param parent_run: AutoMLRun to print status for
        :param primary_metric: Metric being optimized for this run
        :return:
        """
        try:
            self.print_descriptions()
            self.print_columns()
        except Exception as e:
            logging_utilities.log_traceback(e, self.logger)
            raise

        best_metric = None
        parent_run_properties = parent_run.get_properties()
        automl_settings = AzureAutoMLSettings(
            experiment=None, **json.loads(parent_run_properties['AMLSettingsJsonString']))
        tags = parent_run.get_tags()
        total_children_count = int(tags.get('iterations', "0"))
        if total_children_count == 0:
            total_children_count = automl_settings.iterations
        max_concurrency = automl_settings.max_concurrent_iterations

        i = 0
        child_runs_not_finished = []

        while i < total_children_count:
            child_runs_not_finished.append('{}_{}'.format(parent_run.run_id, i))
            i += 1

        objective = minimize_or_maximize(metric=primary_metric)

        runs_to_query = []

        while True:
            runs_to_query = child_runs_not_finished[:max_concurrency]

            status = parent_run.get_tags().get('_aml_system_automl_status', None)
            if status is None:
                status = parent_run.get_status()
            if status in ('Completed', 'Failed', 'Canceled') and runs_to_query is not None and len(runs_to_query) == 0:
                break
            new_children_dtos = parent_run._client.run.get_runs_by_run_ids(run_ids=runs_to_query)

            runs_finished = []

            for run in new_children_dtos:
                run_id = run.run_id
                status = run.status
                if ((run_id not in self.run_map) and (status in ('Completed', 'Failed'))):
                    runs_finished.append(run_id)
                    self.run_map[run_id] = run

            if runs_finished:
                metrics = parent_run._client.run.get_metrics_by_run_ids(run_ids=runs_finished)
                metrics_dtos_by_run = defaultdict(list)
                for dto in metrics:
                    metrics_dtos_by_run[dto.run_id].append(dto)
                run_metrics_map = {
                    runid: parent_run._client.metrics.dto_to_metrics_dict(
                        metric_dto_list)
                    for runid, metric_dto_list in metrics_dtos_by_run.items()
                }

                for run_id in run_metrics_map:
                    self.metric_map[run_id] = run_metrics_map[run_id]

                for run_id in runs_finished:
                    run = self.run_map[run_id]
                    status = run.status
                    properties = run.properties
                    current_iter = properties['iteration']
                    run_metric = self.metric_map.get(run_id, {})
                    print_line = properties.get('run_preprocessor', "") + " " + properties.get('run_algorithm', "")

                    start_iter_time = run.created_utc.replace(tzinfo=pytz.UTC)

                    end_iter_time = run.end_time_utc.replace(tzinfo=pytz.UTC)

                    iter_duration = str(end_iter_time - start_iter_time).split(".")[0]

                    if primary_metric in run_metric:
                        score = run_metric[primary_metric]
                    else:
                        score = constants.Defaults.DEFAULT_PIPELINE_SCORE

                    if best_metric is None or best_metric == 'nan' or np.isnan(best_metric):
                        best_metric = score
                    elif objective == constants.OptimizerObjectives.MINIMIZE:
                        if score < best_metric:
                            best_metric = score
                    elif objective == constants.OptimizerObjectives.MAXIMIZE:
                        if score > best_metric:
                            best_metric = score
                    else:
                        best_metric = 'Unknown'

                    self.print_start(current_iter)
                    self.print_pipeline(print_line)
                    self.print_end(iter_duration, score, best_metric)

                    errors = properties.get('friendly_errors', None)
                    if errors is not None:
                        error_dict = json.loads(errors)
                        for error in error_dict:
                            self.print_error(error_dict[error])
                    child_runs_not_finished.remove(run_id)

            time.sleep(10)

    @staticmethod
    def _show_output(current_run, logger, file_logger, primary_metric):
        try:
            remote_printer = RemoteConsoleInterface(
                logger, file_logger)
            remote_printer.print_scores(current_run, primary_metric)
        except KeyboardInterrupt:
            logger.write("Received interrupt. Returning now.")
