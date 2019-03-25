# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Class for handling notebook run configuration."""
import os
import shutil
import json
from azureml.core.script_run_config import ScriptRunConfig


class NotebookExecutionHandler:
    """Base class for handling notebook execution handler."""

    # Convention how to transform dict notebooks parameters into a command line for the handler script
    # Can be overwritten for individual handlers and/or extended by the handler configurable parameters.
    # Default is to flatten
    @staticmethod
    def _flatten_parameters(parameters=None):
        if parameters is None:
            return []
        return [item for sub in [[i, v] for i, v in parameters.items()] for item in sub]

    def argument_handling_contract(self, notebook, output_notebook, parameters=None):
        """Transform arguments.

        Flatten dictionary of named parameters to a list (key1, value1) into key1 value1

        :param notebook: Input notebook
        :type path: str
        :param output_notebook: Output notebook
        :type path: str
        :param parameters: Dictionary of parameters
        :type path: dict

        :return: List of parameters.
        :rtype: list
        """
        return ["-i", notebook,
                "-o", output_notebook if output_notebook else _insert_suffix(notebook),
                "-p", json.dumps(parameters)]

    def __init__(self, handler_script, dependencies=None):
        """Construct NotebookExecutionHandler object.

        :param handler_script: Python script name to execute a notebook.
        :type handler_script: str
        :param dependencies: List of pip dependencies.
        :type dependencies: list
        """
        self._script_source = handler_script
        self.script = os.path.basename(handler_script)
        # Dependencies for the handler only. Notebook dependencies must be added into a run config
        self.dependencies = dependencies if dependencies else []


class PapermillExecutionHandler(NotebookExecutionHandler):
    """Papermill-based notebook execution handler."""

    known_options = ["engine_name",
                     "prepare_only",
                     "kernel_name",
                     "progress_bar",
                     "log_output",
                     "start_timeout",
                     "report_mode",
                     "cwd"]

    def __init__(self, history=True, **kwargs):
        """Construct PapermillExecutionHandler object.

        Takes named parameters for papermill.execute_notebook()

        :param kwargs: Dictionary of papermill parameters
        :type path: dict
        """
        super().__init__(os.path.join(os.path.dirname(__file__),
                                      "handlers",
                                      "papermill_notebook_run_handler.py"))

        for key, val in kwargs.items():
            if key not in self.known_options:
                raise Exception("Unknown option {}".format(key))

        self.papermill_args = kwargs
        self.execution_args = {"history": history}
        self.dependencies.append("papermill")
        self.dependencies.append("ipykernel")

    def argument_handling_contract(self, notebook, output_notebook, parameters=None):
        """Papermill argument handler.

        Flatten dictionary of named parameters to a list (key1, value1) into key1 value1

        :param notebook: Input notebook
        :type path: str
        :param output_notebook: Output notebook
        :type path: str
        :param parameters: Dictionary of parameters
        :type path: dict

        :return: List of parameters.
        :rtype: list
        """
        if not output_notebook:
            output_notebook = _insert_suffix(notebook)

        return ["-i", notebook,
                "-o", output_notebook,
                "-e", json.dumps(self.execution_args),
                "-p", json.dumps(self.papermill_args),
                "-n", json.dumps(parameters)]


def _insert_suffix(filename, suffix="output"):
    base = os.path.splitext(filename)
    return base[0] + ".output" + base[1]


def _copy_handler(handler, destination):
    handler_filename = os.path.basename(handler)
    destination_path = os.path.join(destination, handler_filename)

    if os.path.normpath(handler) == os.path.normpath(destination_path):
        return

    if os.path.exists(destination_path):
        os.remove(destination_path)
    shutil.copyfile(handler, destination_path)


class NotebookRunConfig(ScriptRunConfig):
    """A class for setting up configurations for notebooks runs.

    Type: ChainedIdentity.
    """

    def __init__(self,
                 source_directory,
                 notebook,
                 output_notebook=None,
                 parameters=None,
                 handler=None,
                 run_config=None,
                 _telemetry_values=None):
        """Class NotebookRunConfig constructor.

        :param source_directory: Source directory
        :type source_directory: str
        :param notebook: Notebook file name
        :type notebook: str
        :param output_notebook: Output notebook file name
        :type output_notebook: str
        :param parameters: Dictionary of notebook parameters
        :type parameters: dict
        :param handler: Instance of the NotebookExecutionHandler
        :type handler: NotebookExecutionHandler
        :param run_config:
        :type run_config: azureml.core.runconfig.RunConfiguration
        :param _telemetry_values:
        :type _telemetry_values: dict
        """
        super().__init__(source_directory, run_config=run_config, _telemetry_values=_telemetry_values)

        # Default handler for now is papermill
        if handler is None:
            handler = PapermillExecutionHandler()

        _copy_handler(handler._script_source, source_directory)

        self.arguments = handler.argument_handling_contract(notebook, output_notebook, parameters)

        self.script = handler.script

        for dep in handler.dependencies:
            self.run_config.environment.python.conda_dependencies.add_pip_package(dep)
