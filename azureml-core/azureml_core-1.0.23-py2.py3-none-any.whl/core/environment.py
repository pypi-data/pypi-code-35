# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes for managing environment definition."""
import logging
import collections
import json

from azureml._base_sdk_common.abstract_run_config_element import _AbstractRunConfigElement
from azureml._base_sdk_common.field_info import _FieldInfo
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.container_registry import ContainerRegistry
from azureml.core._databricks import DatabricksEnvironment

from azureml._restclient.environment_client import EnvironmentClient
from azureml.core._serialization_utils import _serialize_to_dict, _deserialize_and_add_to_object


module_logger = logging.getLogger(__name__)

DEFAULT_CPU_IMAGE = "mcr.microsoft.com/azureml/base:0.2.4"
DEFAULT_GPU_IMAGE = "mcr.microsoft.com/azureml/base-gpu:0.2.4"


class PythonEnvironment(_AbstractRunConfigElement):
    """A class for managing PythonEnvironment.

    :param user_managed_dependencies: True means that AzureML reuses an existing python environment, False means
        that AzureML will create a python environment based on the Conda dependencies specification.
    :type user_managed_dependencies: bool

    :param interpreter_path: The python interpreter path. This is only used when user_managed_dependencies=True
    :type interpreter_path: str

    :param conda_dependencies_file: Path to the conda dependencies file to use for this run. If a project
        contains multiple programs with different sets of dependencies, it may be convenient to manage
        those environments with separate files.
    :type conda_dependencies_file: str
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("user_managed_dependencies", _FieldInfo(bool, "user_managed_dependencies=True indicates that the environment"
                                                       "will be user managed. False indicates that AzureML will"
                                                       "manage the user environment.")),
        ("interpreter_path", _FieldInfo(str, "The python interpreter path")),
        ("conda_dependencies_file", _FieldInfo(
            str, "Path to the conda dependencies file to use for this run. If a project\n"
                 "contains multiple programs with different sets of dependencies, it may be\n"
                 "convenient to manage those environments with separate files.")),
        ("_base_conda_environment", _FieldInfo(
            str, "The base conda environment used for incremental environment creation.",
            serialized_name="base_conda_environment")),
    ])

    def __init__(self):
        """Class PythonEnvironment constructor."""
        super(PythonEnvironment, self).__init__()

        self.interpreter_path = "python"
        self.user_managed_dependencies = False
        self.conda_dependencies_file = None
        self.conda_dependencies = None
        self._base_conda_environment = None
        self._initialized = True


class DockerEnvironment(_AbstractRunConfigElement):
    """A class for managing DockerEnvironment.

    :param enabled: Set True to perform this run inside a Docker container.
    :type enabled: bool

    :param base_image: Base image used for Docker-based runs. example- ubuntu:latest
    :type base_image: str

    :param shared_volumes: Set False if necessary to work around shared volume bugs on Windows.
    :type shared_volumes: bool

    :param gpu_support: Run with NVidia Docker extension to support GPUs.
    :type gpu_support: bool

    :param arguments: Extra arguments to the Docker run command.
    :type arguments: :class:`list`

    :param base_image_registry: Image registry that contains the base image.
    :type base_image_registry: azureml.core.container_registry.ContainerRegistry
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("enabled", _FieldInfo(
            bool, "Set True to perform this run inside a Docker container.")),
        ("base_image", _FieldInfo(str, "Base image used for Docker-based runs.")),
        ("shared_volumes", _FieldInfo(
            bool, "Set False if necessary to work around shared volume bugs.")),
        ("gpu_support", _FieldInfo(
            bool, "Run with NVidia Docker extension to support GPUs.")),
        ("shm_size", _FieldInfo(
            str, "Shared memory size for Docker container. Default is 1g.")),
        ("arguments", _FieldInfo(
            list, "Extra arguments to the Docker run command.", list_element_type=str)),
        ("base_image_registry", _FieldInfo(ContainerRegistry,
                                           "Image registry that contains the base image.")),
    ])

    def __init__(self):
        """Class DockerEnvironment constructor."""
        super(DockerEnvironment, self).__init__()
        self.enabled = False
        self.gpu_support = False
        self.shm_size = "1g"
        self.shared_volumes = True
        self.arguments = list()
        self.base_image = DEFAULT_CPU_IMAGE
        self.base_image_registry = ContainerRegistry()
        self._initialized = True


class SparkPackage(_AbstractRunConfigElement):
    """A class for managing SparkPackage.

    :param group:
    :type group: str
    :param artifact:
    :type artifact: str
    :param version:
    :type version: str
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("group", _FieldInfo(str, "")),
        ("artifact", _FieldInfo(str, "")),
        ("version", _FieldInfo(str, ""))
    ])

    def __init__(self, group=None, artifact=None, version=None):
        """Class SparkPackage constructor."""
        super(SparkPackage, self).__init__()
        self.group = group
        self.artifact = artifact
        self.version = version
        self._initialized = True


class SparkEnvironment(_AbstractRunConfigElement):
    """A class for managing SparkEnvironment.

    :param repositories: List of spark repositories.
    :type repositories: :class:`list`

    :param packages: The packages to use.
    :type packages: :class:`list`

    :param precache_packages: Whether to preckage the packages.
    :type precache_packages: bool
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("repositories", _FieldInfo(
            list, "List of spark repositories.", list_element_type=str)),
        ("packages", _FieldInfo(list, "The packages to use.",
                                list_element_type=SparkPackage)),
        ("precache_packages", _FieldInfo(bool, "Whether to precache the packages."))
    ])

    def __init__(self):
        """Class SparkEnvironment constructor."""
        super(SparkEnvironment, self).__init__()
        self.repositories = [
            "https://mmlspark.azureedge.net/maven"]
        self.packages = [
            SparkPackage("com.microsoft.ml.spark", "mmlspark_2.11", "0.12")]
        self.precache_packages = True
        self._initialized = True


class _ImageDetails(object):
    """A class for image details.

    :param data: Dictionary response from the request
    :type data: dict
    """

    def __init__(self, data):
        """Class _ImageDetails constructor."""
        self.__dict__ = data

    def __repr__(self):
        """Representation of the object.

        :return: Return the string form of the ImageDetails object
        :rtype: str
        """
        return json.dumps(self.__dict__, indent=4)


class Environment(_AbstractRunConfigElement):
    """Configure the python environment where the experiment is executed.

    :param name: The name of the environment
    :type name: string

    :param environment_variables: A dictionary of environment variables names and values.
        These environment variables are set on the process where user script is being executed.
    :type environment_variables: dict

    :param python: This section specifies which python environment and interpreter to use on the target compute.
    :type python: PythonEnvironment

    :param docker: This section configures if and how Docker containers are used by the run.
    :type docker: DockerEnvironment

    :param spark: The section configures Spark settings. It is only used when framework is set to PySpark.
    :type spark: SparkEnvironment

    :param databricks: The section configures Databricks library dependencies.
    :type databricks: DatabricksEnvironment
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        # In dict, values are assumed to be str
        ("name", _FieldInfo(str, "Environment name")),
        ("environment_variables", _FieldInfo(
            dict, "Environment variables set for the run.", user_keys=True)),
        ("python", _FieldInfo(PythonEnvironment, "Python details")),
        ("docker", _FieldInfo(DockerEnvironment, "Docker details")),
        ("spark", _FieldInfo(SparkEnvironment, "Spark details")),
        ("databricks", _FieldInfo(DatabricksEnvironment, "Databricks details"))
    ])

    def __init__(self, name):
        """Class Environment constructor."""
        super(Environment, self).__init__()

        # Add Name/version validation for env management
        self.name = name
        self.version = None
        self.python = PythonEnvironment()
        self.environment_variables = {"EXAMPLE_ENV_VAR": "EXAMPLE_VALUE"}
        self.docker = DockerEnvironment()
        self.spark = SparkEnvironment()
        self.databricks = DatabricksEnvironment()
        self._initialized = True

    def __repr__(self):
        """Representation of the object.

        :return: Return the string form of the Environment object
        :rtype: str
        """
        environment_dict = Environment._serialize_to_dict(self)
        return json.dumps(environment_dict, indent=4)

    def _register(self, workspace):
        """Register the environment object in your workspace.

        :param workspace: The workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :return: Returns the environment object
        :rtype: azureml.core.environment.Environment
        """
        environment_client = EnvironmentClient(workspace.service_context)
        environment_dict = Environment._serialize_to_dict(self)
        response = environment_client._register_environment_definition(environment_dict)
        self.version = response["version"]

        return self

    @staticmethod
    def _get(workspace, name, version=None):
        """Return the environment object.

        :param workspace: The workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param version:
        :type version: str
        :return: Returns the environment object
        :rtype: azureml.core.environment.Environment
        """
        environment_client = EnvironmentClient(workspace.service_context)
        environment_dict = environment_client._get_environment_definition(name=name, version=version)
        env = Environment._deserialize_and_add_to_object(environment_dict)

        return env

    @staticmethod
    def _from_conda_environment(name, file_path):
        """Create an environment object created from a conda yaml file.

        :param name:
        :type name: str
        :param file_path:
        :type The conda yaml file path.
        :return: Returns the environment object
        :rtype: azureml.core.environment.Environment
        """
        conda_dependencies = CondaDependencies(conda_dependencies_file_path=file_path)
        env = Environment(name=name)
        env.python.conda_dependencies = conda_dependencies

        return env

    @staticmethod
    def _from_pip_requirements(name, file_path):
        """Create an environment object created from a pip requirements file.

        :param name:
        :type name: str
        :param file_path:
        :type The pip requirements file path.
        :return: Returns the environment object
        :rtype: azureml.core.environment.Environment
        """
        requirements_list = []
        with open(file_path) as in_file:
            requirements_list = in_file.read().splitlines()

        conda_dependencies = CondaDependencies.create(pip_packages=requirements_list)
        env = Environment(name=name)
        env.python.conda_dependencies = conda_dependencies

        return env

    def _get_image_details(self, workspace):
        """Return the Image details.

        :param workspace: The workspace
        :type workspace: azureml.core.workspace.Workspace
        :return: Returns the image details object
        :rtype: azureml.core.environment.ImageDetails
        """
        environment_client = EnvironmentClient(workspace.service_context)
        image_details_dict = environment_client._get_image_details(
            name=self.name, version=self.version)

        image_details_object = _ImageDetails(image_details_dict)

        return image_details_object

    @staticmethod
    def _serialize_to_dict(environment):
        environment_dict = _serialize_to_dict(environment)

        # _serialization_utils._serialize_to_dict does not serialize condadependencies correctly.
        # Hence the work around to copy this in to the env object
        if environment.python.conda_dependencies is not None:
            inline = environment.python.conda_dependencies._conda_dependencies
            environment_dict["python"]["condaDependencies"] = inline

        return environment_dict

    @staticmethod
    def _deserialize_and_add_to_object(environment_dict):
        # _serialization_utils._deserialize_and_add_to_object does deserialize condaDependencies correctly.
        # Hence the work around to inject it to env object
        environment_name = environment_dict["name"]
        environment_version = environment_dict["version"]
        inline_conda_dependencies = environment_dict["python"]["condaDependencies"]

        environment_object = Environment(environment_name)
        environment_object.version = environment_version
        env = _deserialize_and_add_to_object(Environment, environment_dict, environment_object)

        if inline_conda_dependencies is not None:
            conda_dependencies = CondaDependencies(_underlying_structure=inline_conda_dependencies)
            env.python.conda_dependencies = conda_dependencies

        return env
