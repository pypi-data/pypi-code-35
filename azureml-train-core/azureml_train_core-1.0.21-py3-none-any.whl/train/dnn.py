# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Estimators typically used in DNN training."""

from azureml.core._experiment_method import experiment_method
from azureml.exceptions import TrainingException

from .estimator import FrameworkBaseEstimator, _estimator_submit_method


class TensorFlow(FrameworkBaseEstimator):
    """A TensorFlow Estimator is used to train a TensorFlow-based model.

    This estimator ensures that the TensorFlow framework is installed and configured correctly.

    :param source_directory: A local directory containing experiment configuration files.
    :type source_directory: str
    :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
            string "local".
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param vm_size: The VM size of the compute target that will be created for the training.
            Supported values: Any Azure VM size. The list of available VM sizes are listed here.
            https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
    :type vm_size: str
    :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, it will be defaulted to 'dedicated'.
            Supported values: 'dedicated' and 'lowpriority'.
            This takes effect only when the vm_size param is specified in the input.
    :type vm_priority: str
    :param entry_script: A string representing the relative path to the file used to start training.
    :type entry_script: str
    :param script_params: A dict containing parameters to the entry_script.
    :type script_params: dict
    :param node_count: Number of nodes in the compute target used for training. Only AmlCompute compute target
        is supported for distributed training (node_count > 1).
    :type node_count: int
    :param process_count_per_node: When using MPI, number of processes per node.
    :type process_count_per_node: int
    :param worker_count: When using Parameter Server, the number of worker nodes.
    :type worker_count: int
    :param parameter_server_count: When using Parameter Server, the number of parameter server nodes.
    :type parameter_server_count: int
    :param distributed_backend: Communication backend for distributed training.
        Supported values: 'mpi' and 'ps'.
        'mpi': MPI/Horovod
        'ps': parameter server
        This parameter is required when any of node_count, process_count_per_node, worker_count, or
        parameter_server_count > 1.
        When node_count == 1 and process_count_per_node == 1, no backend will be used unless the backend
        is explicitly set. Only AmlCompute compute target is supported for distributed training.
    :type distributed_backend: str
    :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
        If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
        image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
        parameter is not set. This setting is used only in docker enabled compute targets.
    :type use_gpu: bool
    :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
    :type use_docker: bool
    :param custom_docker_image: The name of the docker image from which the image to use for training
        will be built. If not set, a default CPU based image will be used as the base image.
    :type custom_docker_image: str
    :param image_registry_details: The details of the docker image registry.
    :type image_registry_details: azureml.core.runconfig.ContainerRegistry
    :param user_managed: True means that AzureML reuses an existing python environment, False means
        that AzureML will create a python environment based on the Conda dependencies specification.
    :type user_managed: bool
    :param conda_packages: List of strings representing conda packages to be added to the Python environment
        for the experiment.
    :type conda_packages: list
    :param pip_packages: List of strings representing pip packages to be added to the Python environment
        for the experiment.
    :type pip_packages: list
    :param pip_requirements_file_path: A string representing the full path to the pip requirements file. This
        can be provided in combination with the pip_packages parameter.
    :type pip_requirements_file_path: str
    :param environment_definition: The EnvironmentDefinition for the experiment. It includes
        PythonEnvironment and DockerEnvironment and environment variables. Any environment option not directly
        exposed through other parameters to the Estimator construction can be set using environment_definition
        parameter. If this parameter is specified, it will take precedence over other environment related
        parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
        reported on these invalid combinations.
    :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
    :param inputs: Data references as input.
    :type inputs: list
    :param source_directory_data_store: Backing datastore for project share.
    :type source_directory_data_store: str
    :param shm_size: The size of the shared memory block. Default is 1g.
    :type shm_size: str
    """

    FRAMEWORK_NAME = "TensorFlow"
    DEFAULT_VERSION = '1.10'

    @experiment_method(submit_function=_estimator_submit_method)
    def __init__(self,
                 source_directory,
                 *,
                 compute_target=None,
                 vm_size=None,
                 vm_priority=None,
                 entry_script=None,
                 script_params=None,
                 node_count=1,
                 process_count_per_node=1,
                 worker_count=1,
                 parameter_server_count=1,
                 distributed_backend=None,
                 use_gpu=False,
                 use_docker=True,
                 custom_docker_image=None,
                 image_registry_details=None,
                 user_managed=False,
                 conda_packages=None,
                 pip_packages=None,
                 pip_requirements_file_path=None,
                 environment_definition=None,
                 inputs=None,
                 source_directory_data_store=None,
                 shm_size=None):
        """Initialize a TensorFlow estimator.

        :param source_directory: A local directory containing experiment configuration files.
        :type source_directory: str
        :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param vm_size: The VM size of the compute target that will be created for the training.
        Supported values: Any Azure VM size. The list of available VM sizes are listed here.
        https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
        :type vm_size: str
        :param vm_priority: The VM priority of the compute target that will be created for the training. If not
        specified, it will be defaulted to 'dedicated'.
         Supported values: 'dedicated' and 'lowpriority'.
         This takes effect only when the vm_size param is specified in the input.
        :type vm_priority: str
        :param entry_script: A string representing the relative path to the file used to start training.
        :type entry_script: str
        :param script_params: A dict containing parameters to the entry_script.
        :type script_params: dict
        :param node_count: Number of nodes in the compute target used for training. Only AmlCompute compute target
            is supported for distributed training (node_count > 1).
        :type node_count: int
        :param process_count_per_node: When using MPI, number of processes per node.
        :type process_count_per_node: int
        :param worker_count: When using Parameter Server, the number of worker nodes.
        :type worker_count: int
        :param parameter_server_count: When using Parameter Server, the number of parameter server nodes.
        :type parameter_server_count: int
        :param distributed_backend: Communication backend for distributed training.
            Supported values: 'mpi' and 'ps'.
            'mpi': MPI/Horovod
            'ps': parameter server
            This parameter is required when any of node_count, process_count_per_node, worker_count, or
            parameter_server_count > 1.
            When node_count == 1 and process_count_per_node == 1, no backend will be used unless the backend
            is explicitly set. Only AmlCompute compute target is supported for distributed training.
        :type distributed_backend: str
        :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
            If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
            image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
            parameter is not set. This setting is used only in docker enabled compute targets.
        :type use_gpu: bool
        :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
        :type use_docker: bool
        :param custom_docker_image: The name of the docker image from which the image to use for training
            will be built. If not set, a default CPU based image will be used as the base image.
        :type custom_docker_image: str
        :param image_registry_details: The details of the docker image registry.
        :type image_registry_details: azureml.core.runconfig.ContainerRegistry
        :param user_managed: True means that AzureML reuses an existing python environment, False means
            that AzureML will create a python environment based on the Conda dependencies specification.
        :type user_managed: bool
        :param conda_packages: List of strings representing conda packages to be added to the Python environment
            for the experiment.
        :type conda_packages: list
        :param pip_packages: List of strings representing pip packages to be added to the Python environment
            for the experiment.
        :type pip_packages: list
        :param pip_requirements_file_path: A string representing the full path to the pip requirements file. This
            can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file_path: str
        :param environment_definition: The EnvironmentDefinition for the experiment. It includes
            PythonEnvironment and DockerEnvironment and environment variables. Any environment option not directly
            exposed through other parameters to the Estimator construction can be set using environment_definition
            parameter. If this parameter is specified, it will take precedence over other environment related
            parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
            reported on these invalid combinations.
        :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
        :param inputs: Data references as input.
        :type inputs: list
        :param source_directory_data_store: Backing datastore for project share.
        :type source_directory_data_store: str
        :param shm_size: The size of the shared memory block. Default is 1g.
        :type shm_size: str
        """
        if distributed_backend and distributed_backend.lower() not in ["mpi", "ps"]:
            raise TrainingException("Unsupported distributed backend value: "
                                    "{}. Supported backends: mpi, ps.".format(distributed_backend))

        super().__init__(source_directory, compute_target=compute_target, vm_size=vm_size,
                         vm_priority=vm_priority, entry_script=entry_script,
                         script_params=script_params, node_count=node_count,
                         process_count_per_node=process_count_per_node,
                         distributed_backend=distributed_backend, use_gpu=use_gpu,
                         use_docker=use_docker, custom_docker_image=custom_docker_image,
                         image_registry_details=image_registry_details,
                         user_managed=user_managed, conda_packages=conda_packages,
                         pip_packages=pip_packages,
                         pip_requirements_file_path=pip_requirements_file_path,
                         environment_definition=environment_definition, inputs=inputs,
                         source_directory_data_store=source_directory_data_store,
                         framework_name=self.FRAMEWORK_NAME,
                         framework_version=self.DEFAULT_VERSION)

        self._estimator_config.tensorflow.worker_count = worker_count
        self._estimator_config.tensorflow.parameter_server_count = parameter_server_count

    def _get_telemetry_values(self, func):
        telemetry_values = super()._get_telemetry_values(func)
        telemetry_values['numOfWorkers'] = self._estimator_config.tensorflow.worker_count
        telemetry_values['numOfPSNodes'] = self._estimator_config.tensorflow.parameter_server_count
        return telemetry_values


class PyTorch(FrameworkBaseEstimator):
    """A PyTorch Estimator is used to train a PyTorch specific experiment.

    :param source_directory: A local directory containing experiment configuration files.
    :type source_directory: str
    :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
            string "local".
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param vm_size: The VM size of the compute target that will be created for the training.
        Supported values: Any Azure VM size. The list of available VM sizes are listed here.
        https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
    :type vm_size: str
    :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, it will be defaulted to 'dedicated'.
            Supported values: 'dedicated' and 'lowpriority'.
            This takes effect only when the vm_size param is specified in the input.
    :type vm_priority: str
    :param entry_script: A string representing the relative path to the file used to start training.
    :type entry_script: str
    :param script_params: A dict containing parameters to the entry_script.
    :type script_params: dict
    :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
         distributed job will be run. Only AmlCompute compute target is supported for distributed jobs.
    :type node_count: int
    :param process_count_per_node: Number of processes per node. If greater than 1, mpi
         distributed job will be run. Only AmlCompute compute target is supported for distributed jobs.
    :type process_count_per_node: int
    :param distributed_backend: Communication backend for distributed training.
        Supported value: 'mpi'.
        'mpi': MPI/Horovod
        This parameter is required when node_count > 1 and/or process_count_per_node > 1.
        When node_count == 1 and process_count_per_node == 1, no backend will be used unless the backend
        is explicitly set. Only AmlCompute compute target is supported for distributed training.
    :type distributed_backend: str
    :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
        If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
        image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
        parameter is not set. This setting is used only in docker enabled compute targets.
    :type use_gpu: bool
    :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
    :type use_docker: bool
    :param custom_docker_image: The name of the docker image from which the image to use for training
        will be built. If not set, a default CPU based image will be used as the base image.
    :type custom_docker_image: str
    :param image_registry_details: The details of the docker image registry.
    :type image_registry_details: azureml.core.runconfig.ContainerRegistry
    :param user_managed: True means that AzureML reuses an existing python environment, False means
        that AzureML will create a python environment based on the Conda dependencies specification.
    :type user_managed: bool
    :param conda_packages: List of strings representing conda packages to be added to the Python environment
        for the experiment.
    :type conda_packages: list
    :param pip_packages: List of strings representing pip packages to be added to the Python environment
        for the experiment.
    :type pip_packages: list
    :param pip_requirements_file_path: A string representing the full path to the pip requirements file. This
        can be provided in combination with the pip_packages parameter.
    :type pip_requirements_file_path: str
    :param environment_definition: The EnvironmentDefinition for the experiment. It includes
        PythonEnvironment and DockerEnvironment and environment variables. Any environment option not directly
        exposed through other parameters to the Estimator construction can be set using environment_definition
        parameter. If this parameter is specified, it will take precedence over other environment related
        parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
        reported on these invalid combinations.
    :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
    :param inputs: Data references as input.
    :type inputs: list
    :param source_directory_data_store: Backing datastore for project share.
    :type source_directory_data_store: str
    :param shm_size: The size of the shared memory block. Default is 1g.
    :type shm_size: str
    """

    FRAMEWORK_NAME = "PyTorch"
    DEFAULT_VERSION = '1.0'

    @experiment_method(submit_function=_estimator_submit_method)
    def __init__(self,
                 source_directory,
                 *,
                 compute_target=None,
                 vm_size=None,
                 vm_priority=None,
                 entry_script=None,
                 script_params=None,
                 node_count=1,
                 process_count_per_node=1,
                 distributed_backend=None,
                 use_gpu=False,
                 use_docker=True,
                 custom_docker_image=None,
                 image_registry_details=None,
                 user_managed=False,
                 conda_packages=None,
                 pip_packages=None,
                 pip_requirements_file_path=None,
                 environment_definition=None,
                 inputs=None,
                 source_directory_data_store=None,
                 shm_size=None):
        """Initialize a PyTorch estimator.

        :param source_directory: A local directory containing experiment configuration files.
        :type source_directory: str
        :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param vm_size: The VM size of the compute target that will be created for the training.
            Supported values: Any Azure VM size. The list of available VM sizes are listed here.
            https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
        :type vm_size: str
        :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, it will be defaulted to 'dedicated'.
            Supported values: 'dedicated' and 'lowpriority'.
            This takes effect only when the vm_size param is specified in the input.
        :type vm_priority: str
        :param entry_script: A string representing the relative path to the file used to start training.
        :type entry_script: str
        :param script_params: A dict containing parameters to the entry_script.
        :type script_params: dict
        :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
            distributed job will be run. Only AmlCompute compute target is supported for distributed jobs.
        :type node_count: int
        :param process_count_per_node: Number of processes per node. If greater than 1, mpi
            distributed job will be run. Only AmlCompute compute target is supported for distributed jobs.
        :type process_count_per_node: int
        :param distributed_backend: Communication backend for distributed training.
            Supported value: 'mpi'.
            'mpi': MPI/Horovod
            This parameter is required when node_count > 1 and/or process_count_per_node > 1.
            When node_count == 1 and process_count_per_node == 1, no backend will be used unless the backend
            is explicitly set. Only AmlCompute compute target is supported for distributed training.
        :type distributed_backend: str
        :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
            If set to true, gpu-based default docker image will be used in the environment. If set to false,
            CPU based image will be used. Default docker images (CPU or GPU) will be used only if
            custom_docker_image parameter is not set. This setting is used only in docker enabled compute targets.
        :type use_gpu: bool
        :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
        :type use_docker: bool
        :param custom_docker_image: The name of the docker image from which the image to use for training
            will be built. If not set, a default CPU based image will be used as the base image.
        :type custom_docker_image: str
        :param image_registry_details: The details of the docker image registry.
        :type image_registry_details: azureml.core.runconfig.ContainerRegistry
        :param user_managed: True means that AzureML reuses an existing python environment, False means
            that AzureML will create a python environment based on the Conda dependencies specification.
        :type user_managed: bool
        :param conda_packages: List of strings representing conda packages to be added to the Python environment
            for the experiment.
        :type conda_packages: list
        :param pip_packages: List of strings representing pip packages to be added to the Python environment
            for the experiment.
        :type pip_packages: list
        :param pip_requirements_file_path: A string representing the full path to the pip requirements file. This
            can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file_path: str
        :param environment_definition: The EnvironmentDefinition for the experiment. It includes
            PythonEnvironment and DockerEnvironment and environment variables. Any environment option not directly
            exposed through other parameters to the Estimator construction can be set using environment_definition
            parameter. If this parameter is specified, it will take precedence over other environment related
            parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
            reported on these invalid combinations.
        :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
        :param inputs: Data references as input.
        :type inputs: list
        :param source_directory_data_store: Backing datastore for project share.
        :type source_directory_data_store: Datastore
        :param shm_size: The size of the shared memory block. Default is 1g.
        :type shm_size: str
        """
        if distributed_backend and distributed_backend.lower() != "mpi":
            raise TrainingException("Unsupported distributed backend value: "
                                    "{}. Supported backends: mpi.".format(distributed_backend))

        super().__init__(source_directory, compute_target=compute_target, vm_size=vm_size,
                         vm_priority=vm_priority, entry_script=entry_script,
                         script_params=script_params, node_count=node_count,
                         process_count_per_node=process_count_per_node,
                         distributed_backend=distributed_backend, use_gpu=use_gpu,
                         use_docker=use_docker, custom_docker_image=custom_docker_image,
                         image_registry_details=image_registry_details,
                         user_managed=user_managed, conda_packages=conda_packages,
                         pip_packages=pip_packages,
                         pip_requirements_file_path=pip_requirements_file_path,
                         environment_definition=environment_definition, inputs=inputs,
                         source_directory_data_store=source_directory_data_store,
                         framework_name=self.FRAMEWORK_NAME,
                         framework_version=self.DEFAULT_VERSION)


class Chainer(FrameworkBaseEstimator):
    """A Chainer Estimator is used to train a Chainer specific experiment.

    :param source_directory: A local directory containing experiment configuration files.
    :type source_directory: str
    :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
            string "local".
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param vm_size: The VM size of the compute target that will be created for the training.
        Supported values: Any Azure VM size. The list of available VM sizes are listed here.
        https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
    :type vm_size: str
    :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, it will be defaulted to 'dedicated'.
            Supported values: 'dedicated' and 'lowpriority'.
            This takes effect only when the vm_size param is specified in the input.
    :type vm_priority: str
    :param entry_script: A string representing the relative path to the file used to start training.
    :type entry_script: str
    :param script_params: A dict containing parameters to the entry_script.
    :type script_params: dict
    :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
         distributed job will be run. Only AmlCompute compute target is supported for distributed jobs.
    :type node_count: int
    :param process_count_per_node: Number of processes per node. If greater than 1, mpi
         distributed job will be run. Only AmlCompute compute target is supported for distributed jobs.
    :type process_count_per_node: int
    :param distributed_backend: Communication backend for distributed training.
        Supported value: 'mpi'.
        'mpi': MPI/Horovod
        This parameter is required when node_count > 1 and/or process_count_per_node > 1.
        When node_count == 1 and process_count_per_node == 1, no backend will be used unless the backend
        is explicitly set. Only AmlCompute compute target is supported for distributed training.
    :type distributed_backend: str
    :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
        If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
        image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
        parameter is not set. This setting is used only in docker enabled compute targets.
    :type use_gpu: bool
    :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
    :type use_docker: bool
    :param custom_docker_image: The name of the docker image from which the image to use for training
        will be built. If not set, a default CPU based image will be used as the base image.
    :type custom_docker_image: str
    :param image_registry_details: The details of the docker image registry.
    :type image_registry_details: azureml.core.runconfig.ContainerRegistry
    :param user_managed: True means that AzureML reuses an existing python environment, False means
        that AzureML will create a python environment based on the Conda dependencies specification.
    :type user_managed: bool
    :param conda_packages: List of strings representing conda packages to be added to the Python environment
        for the experiment.
    :type conda_packages: list
    :param pip_packages: List of strings representing pip packages to be added to the Python environment
        for the experiment.
    :type pip_packages: list
    :param pip_requirements_file_path: A string representing the full path to the pip requirements file. This
        can be provided in combination with the pip_packages parameter.
    :type pip_requirements_file_path: str
    :param environment_definition: The EnvironmentDefinition for the experiment. It includes
        PythonEnvironment and DockerEnvironment and environment variables. Any environment option not directly
        exposed through other parameters to the Estimator construction can be set using environment_definition
        parameter. If this parameter is specified, it will take precedence over other environment related
        parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
        reported on these invalid combinations.
    :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
    :param inputs: Data references as input.
    :type inputs: list
    :param source_directory_data_store: Backing datastore for project share.
    :type source_directory_data_store: str
    """

    FRAMEWORK_NAME = "Chainer"
    DEFAULT_VERSION = '5.1.0'

    @experiment_method(submit_function=_estimator_submit_method)
    def __init__(self,
                 source_directory,
                 *,
                 compute_target=None,
                 vm_size=None,
                 vm_priority=None,
                 entry_script=None,
                 script_params=None,
                 node_count=1,
                 process_count_per_node=1,
                 distributed_backend=None,
                 use_gpu=False,
                 use_docker=True,
                 custom_docker_image=None,
                 image_registry_details=None,
                 user_managed=False,
                 conda_packages=None,
                 pip_packages=None,
                 pip_requirements_file_path=None,
                 environment_definition=None,
                 inputs=None,
                 source_directory_data_store=None):
        """Initialize a Chainer estimator.

        :param source_directory: A local directory containing experiment configuration files.
        :type source_directory: str
        :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param vm_size: The VM size of the compute target that will be created for the training.
        Supported values: Any Azure VM size. The list of available VM sizes are listed here.
        https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
        :type vm_size: str
        :param vm_priority: The VM priority of the compute target that will be created for the training. If not
        specified, it will be defaulted to 'dedicated'.
         Supported values: 'dedicated' and 'lowpriority'.
         This takes effect only when the vm_size param is specified in the input.
        :type vm_priority: str
        :param entry_script: A string representing the relative path to the file used to start training.
        :type entry_script: str
        :param script_params: A dict containing parameters to the entry_script.
        :type script_params: dict
        :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
             distributed job will be run. Only AmlCompute compute target is supported for distributed jobs.
        :type node_count: int
        :param process_count_per_node: Number of processes per node. If greater than 1, mpi
             distributed job will be run. Only AmlCompute compute target is supported for distributed jobs.
        :type process_count_per_node: int
        :param distributed_backend: Communication backend for distributed training.
            Supported value: 'mpi'.
            'mpi': MPI/Horovod
            This parameter is required when node_count > 1 and/or process_count_per_node > 1.
            When node_count == 1 and process_count_per_node == 1, no backend will be used unless the backend
            is explicitly set. Only AmlCompute compute target is supported for distributed training.
        :type distributed_backend: str
        :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
            If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
            image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
            parameter is not set. This setting is used only in docker enabled compute targets.
        :type use_gpu: bool
        :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
        :type use_docker: bool
        :param custom_docker_image: The name of the docker image from which the image to use for training
            will be built. If not set, a default CPU based image will be used as the base image.
        :type custom_docker_image: str
        :param image_registry_details: The details of the docker image registry.
        :type image_registry_details: azureml.core.runconfig.ContainerRegistry
        :param user_managed: True means that AzureML reuses an existing python environment, False means
            that AzureML will create a python environment based on the Conda dependencies specification.
        :type user_managed: bool
        :param conda_packages: List of strings representing conda packages to be added to the Python environment
            for the experiment.
        :type conda_packages: list
        :param pip_packages: List of strings representing pip packages to be added to the Python environment
            for the experiment.
        :type pip_packages: list
        :param pip_requirements_file_path: A string representing the full path to the pip requirements file. This
            can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file_path: str
        :param environment_definition: The EnvironmentDefinition for the experiment. It includes
            PythonEnvironment and DockerEnvironment and environment variables. Any environment option not directly
            exposed through other parameters to the Estimator construction can be set using environment_definition
            parameter. If this parameter is specified, it will take precedence over other environment related
            parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
            reported on these invalid combinations.
        :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
        :param inputs: Data references as input.
        :type inputs: list
        :param source_directory_data_store: Backing datastore for project share.
        :type source_directory_data_store: Datastore
        """
        if distributed_backend and distributed_backend.lower() != "mpi":
            raise TrainingException("Unsupported distributed backend value: "
                                    "{}. Supported backends: mpi.".
                                    format(distributed_backend))

        super().__init__(source_directory, compute_target=compute_target, vm_size=vm_size,
                         vm_priority=vm_priority, entry_script=entry_script,
                         script_params=script_params, node_count=node_count,
                         process_count_per_node=process_count_per_node,
                         distributed_backend=distributed_backend, use_gpu=use_gpu,
                         use_docker=use_docker, custom_docker_image=custom_docker_image,
                         image_registry_details=image_registry_details,
                         user_managed=user_managed, conda_packages=conda_packages,
                         pip_packages=pip_packages,
                         pip_requirements_file_path=pip_requirements_file_path,
                         environment_definition=environment_definition, inputs=inputs,
                         source_directory_data_store=source_directory_data_store,
                         framework_name=self.FRAMEWORK_NAME,
                         framework_version=self.DEFAULT_VERSION)

        if self._estimator_config.communicator == "IntelMpi":
            self._update_environment_variables(self._estimator_config,
                                               ['NCCL_SOCKET_IFNAME', 'NCCL_IB_DISABLE'],
                                               ['eth0', '1'])
