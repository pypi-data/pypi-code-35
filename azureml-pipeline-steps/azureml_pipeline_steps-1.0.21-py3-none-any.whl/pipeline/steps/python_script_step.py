# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""To add a step to run a Python script."""
from azureml.pipeline.core._python_script_step_base import _PythonScriptStepBase


class PythonScriptStep(_PythonScriptStepBase):
    r"""Add a step to run a Python script in a Pipeline.

    :param script_name: name of a python script (relative to source_directory)
    :type script_name: str
    :param name: Name of the step.  If unspecified, script_name will be used
    :type name: str
    :param arguments: List of command-line arguments
    :type arguments: list
    :param compute_target: Compute target to use.  This may be a compute target object or the string name
        of a compute target on the workspace.  Optionally if the compute target is not available at pipeline
        creation time, you may specify a tuple of ('compute target name', 'compute target type') to avoid fetching
        the compute target object (AmlCompute type is 'AmlCompute' and RemoteTarget type is 'VirtualMachine')
    :type compute_target: DsvmCompute, AmlCompute, RemoteTarget, HDIClusterTarget, str, tuple
    :param runconfig: Runconfig to use
    :type runconfig: azureml.core.runconfig.RunConfiguration
    :param runconfig_pipeline_params: Override runconfig properties at runtime using key-value pairs each with
                                    name of the runconfig property and PipelineParameter for that property
    :type runconfig_pipeline_params: {str: PipelineParameter}
    :param inputs: List of input port bindings
    :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
        azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
    :param outputs: List of output port bindings
    :type outputs: list[azureml.pipeline.core.builder.PipelineData, azureml.pipeline.core.graph.OutputPortBinding]
    :param params: Dictionary of name-value pairs. Registered as environment variables with "AML_PARAMETER\_"
    :type params: dict
    :param source_directory: folder that contains the script, conda env etc.
    :type source_directory: str
    :param allow_reuse: Whether the step should reuse previous results when run with the same settings/inputs.
        If this is false, a new run will always be generated for this step during pipeline execution.
    :type allow_reuse: bool
    :param version: Optional version tag to denote a change in functionality for the step
    :type version: str
    :param hash_paths: list of paths to hash to detect a change (script file is always hashed)
    :type hash_paths: list
    """

    def __init__(self, script_name, name=None, arguments=None, compute_target=None, runconfig=None,
                 runconfig_pipeline_params=None, inputs=None, outputs=None, params=None, source_directory=None,
                 allow_reuse=True, version=None, hash_paths=None):
        """
        Add a step to run a Python script in a Pipeline.

        :param script_name: Name of a python script (relative to source_directory)
        :type script_name: str
        :param name: Name of the step.  If unspecified, script_name will be used
        :type name: str
        :param arguments: List of command-line arguments to pass to the python script
        :type arguments: [str]
        :param compute_target: Compute target to use.  This may be a compute target object or the string name
            of a compute target on the workspace.  Optionally, if the compute target is not available at pipeline
            creation time, you may specify a tuple of ('compute target name', 'compute target type') to avoid fetching
            the compute target object (AmlCompute type is 'AmlCompute' and RemoteTarget type is 'VirtualMachine')
        :type compute_target: DsvmCompute, AmlCompute, RemoteTarget, HDIClusterTarget, str, tuple
        :param runconfig: Runconfig to use.  If unspecified, a default runconfig will be created
        :type runconfig: RunConfiguration
        :param runconfig_pipeline_params: Override runconfig properties at runtime using key-value pairs each with
                                        name of the runconfig property and PipelineParameter for that property
        :type runconfig_pipeline_params: {str: PipelineParameter}
        :param inputs: List of input port bindings
        :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
                     azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
        :param outputs: List of output port bindings
        :type outputs: list[azureml.pipeline.core.builder.PipelineData, azureml.pipeline.core.graph.OutputPortBinding]
        :param params: Dictionary of name-value pairs. Registered as environment variables with "AML_PARAMETER_"
        :type params: {str: str}
        :param source_directory: folder that contains the script, conda env etc.
        :type source_directory: str
        :param allow_reuse: Whether the step should reuse previous results when run with the same settings/inputs
        :type allow_reuse: bool
        :param version: Optional version tag to denote a change in functionality for the step
        :type version: str
        :param hash_paths: list of paths to hash to detect a change (script file is always hashed)
        :type hash_paths: [str]
        """
        super(PythonScriptStep, self).__init__(
            script_name=script_name, name=name, arguments=arguments, compute_target=compute_target,
            runconfig=runconfig, runconfig_pipeline_params=runconfig_pipeline_params, inputs=inputs, outputs=outputs,
            params=params, source_directory=source_directory, allow_reuse=allow_reuse, version=version,
            hash_paths=hash_paths)

    def create_node(self, graph, default_datastore, context):
        """
        Create a node for python script step.

        :param graph: graph object
        :type graph: azureml.pipeline.core.graph.Graph
        :param default_datastore: default datastore
        :type default_datastore: azureml.core.AbstractAzureStorageDatastore, azureml.core.AzureDataLakeDatastore
        :param context: context
        :type context: _GraphContext

        :return: The created node
        :rtype: azureml.pipeline.core.graph.Node
        """
        return super(PythonScriptStep, self).create_node(
            graph=graph, default_datastore=default_datastore, context=context)

    def set_amlcompute_params(self, native_shared_directory=None):
        """
        Set AmlCompute native shared directory param.

        :param native_shared_directory: native shared directory
        :type native_shared_directory: str
        """
        super(PythonScriptStep, self).set_amlcompute_params(native_shared_directory=native_shared_directory)
