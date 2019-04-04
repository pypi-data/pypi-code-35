import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-batch", "0.28.0", __name__, "aws-batch@0.28.0.jsii.tgz")
class CfnComputeEnvironment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service_role: str, type: str, compute_environment_name: typing.Optional[str]=None, compute_resources: typing.Optional[typing.Union["ComputeResourcesProperty", aws_cdk.cdk.Token]]=None, state: typing.Optional[str]=None) -> None:
        props: CfnComputeEnvironmentProps = {"serviceRole": service_role, "type": type}

        if compute_environment_name is not None:
            props["computeEnvironmentName"] = compute_environment_name

        if compute_resources is not None:
            props["computeResources"] = compute_resources

        if state is not None:
            props["state"] = state

        jsii.create(CfnComputeEnvironment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> str:
        return jsii.get(self, "computeEnvironmentArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnComputeEnvironmentProps":
        return jsii.get(self, "propertyOverrides")

    class _ComputeResourcesProperty(jsii.compat.TypedDict, total=False):
        bidPercentage: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        desiredvCpus: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        ec2KeyPair: str
        imageId: str
        launchTemplate: typing.Union[aws_cdk.cdk.Token, "CfnComputeEnvironment.LaunchTemplateSpecificationProperty"]
        placementGroup: str
        spotIamFleetRole: str
        tags: typing.Mapping[typing.Any, typing.Any]

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.ComputeResourcesProperty")
    class ComputeResourcesProperty(_ComputeResourcesProperty):
        instanceRole: str
        instanceTypes: typing.List[str]
        maxvCpus: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minvCpus: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        securityGroupIds: typing.List[str]
        subnets: typing.List[str]
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty")
    class LaunchTemplateSpecificationProperty(jsii.compat.TypedDict, total=False):
        launchTemplateId: str
        launchTemplateName: str
        version: str


class _CfnComputeEnvironmentProps(jsii.compat.TypedDict, total=False):
    computeEnvironmentName: str
    computeResources: typing.Union["CfnComputeEnvironment.ComputeResourcesProperty", aws_cdk.cdk.Token]
    state: str

@jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironmentProps")
class CfnComputeEnvironmentProps(_CfnComputeEnvironmentProps):
    serviceRole: str
    type: str

class CfnJobDefinition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.CfnJobDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, type: str, container_properties: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ContainerPropertiesProperty"]]=None, job_definition_name: typing.Optional[str]=None, node_properties: typing.Optional[typing.Union[aws_cdk.cdk.Token, "NodePropertiesProperty"]]=None, parameters: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, retry_strategy: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RetryStrategyProperty"]]=None, timeout: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TimeoutProperty"]]=None) -> None:
        props: CfnJobDefinitionProps = {"type": type}

        if container_properties is not None:
            props["containerProperties"] = container_properties

        if job_definition_name is not None:
            props["jobDefinitionName"] = job_definition_name

        if node_properties is not None:
            props["nodeProperties"] = node_properties

        if parameters is not None:
            props["parameters"] = parameters

        if retry_strategy is not None:
            props["retryStrategy"] = retry_strategy

        if timeout is not None:
            props["timeout"] = timeout

        jsii.create(CfnJobDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> str:
        return jsii.get(self, "jobDefinitionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnJobDefinitionProps":
        return jsii.get(self, "propertyOverrides")

    class _ContainerPropertiesProperty(jsii.compat.TypedDict, total=False):
        command: typing.List[str]
        environment: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.EnvironmentProperty"]]]
        instanceType: str
        jobRoleArn: str
        mountPoints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.MountPointsProperty"]]]
        privileged: typing.Union[bool, aws_cdk.cdk.Token]
        readonlyRootFilesystem: typing.Union[bool, aws_cdk.cdk.Token]
        ulimits: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.UlimitProperty"]]]
        user: str
        volumes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.VolumesProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.ContainerPropertiesProperty")
    class ContainerPropertiesProperty(_ContainerPropertiesProperty):
        image: str
        memory: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        vcpus: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EnvironmentProperty")
    class EnvironmentProperty(jsii.compat.TypedDict, total=False):
        name: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.MountPointsProperty")
    class MountPointsProperty(jsii.compat.TypedDict, total=False):
        containerPath: str
        readOnly: typing.Union[bool, aws_cdk.cdk.Token]
        sourceVolume: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NodePropertiesProperty")
    class NodePropertiesProperty(jsii.compat.TypedDict):
        mainNode: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        nodeRangeProperties: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.NodeRangePropertyProperty"]]]
        numNodes: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _NodeRangePropertyProperty(jsii.compat.TypedDict, total=False):
        container: typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.ContainerPropertiesProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NodeRangePropertyProperty")
    class NodeRangePropertyProperty(_NodeRangePropertyProperty):
        targetNodes: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.RetryStrategyProperty")
    class RetryStrategyProperty(jsii.compat.TypedDict, total=False):
        attempts: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.TimeoutProperty")
    class TimeoutProperty(jsii.compat.TypedDict, total=False):
        attemptDurationSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.UlimitProperty")
    class UlimitProperty(jsii.compat.TypedDict):
        hardLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        name: str
        softLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.VolumesHostProperty")
    class VolumesHostProperty(jsii.compat.TypedDict, total=False):
        sourcePath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.VolumesProperty")
    class VolumesProperty(jsii.compat.TypedDict, total=False):
        host: typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.VolumesHostProperty"]
        name: str


class _CfnJobDefinitionProps(jsii.compat.TypedDict, total=False):
    containerProperties: typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.ContainerPropertiesProperty"]
    jobDefinitionName: str
    nodeProperties: typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.NodePropertiesProperty"]
    parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    retryStrategy: typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.RetryStrategyProperty"]
    timeout: typing.Union[aws_cdk.cdk.Token, "CfnJobDefinition.TimeoutProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobDefinitionProps")
class CfnJobDefinitionProps(_CfnJobDefinitionProps):
    type: str

class CfnJobQueue(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch.CfnJobQueue"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, compute_environment_order: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ComputeEnvironmentOrderProperty"]]], priority: typing.Union[jsii.Number, aws_cdk.cdk.Token], job_queue_name: typing.Optional[str]=None, state: typing.Optional[str]=None) -> None:
        props: CfnJobQueueProps = {"computeEnvironmentOrder": compute_environment_order, "priority": priority}

        if job_queue_name is not None:
            props["jobQueueName"] = job_queue_name

        if state is not None:
            props["state"] = state

        jsii.create(CfnJobQueue, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> str:
        return jsii.get(self, "jobQueueArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnJobQueueProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobQueue.ComputeEnvironmentOrderProperty")
    class ComputeEnvironmentOrderProperty(jsii.compat.TypedDict):
        computeEnvironment: str
        order: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnJobQueueProps(jsii.compat.TypedDict, total=False):
    jobQueueName: str
    state: str

@jsii.data_type(jsii_type="@aws-cdk/aws-batch.CfnJobQueueProps")
class CfnJobQueueProps(_CfnJobQueueProps):
    computeEnvironmentOrder: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnJobQueue.ComputeEnvironmentOrderProperty"]]]
    priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]

__all__ = ["CfnComputeEnvironment", "CfnComputeEnvironmentProps", "CfnJobDefinition", "CfnJobDefinitionProps", "CfnJobQueue", "CfnJobQueueProps", "__jsii_assembly__"]

publication.publish()
