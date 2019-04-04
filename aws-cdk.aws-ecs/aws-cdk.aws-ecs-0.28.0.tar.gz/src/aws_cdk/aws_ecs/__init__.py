import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.assets_docker
import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_autoscaling
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudformation
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_route53
import aws_cdk.aws_secretsmanager
import aws_cdk.aws_servicediscovery
import aws_cdk.aws_sns
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecs", "0.28.0", __name__, "aws-ecs@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AddAutoScalingGroupCapacityOptions")
class AddAutoScalingGroupCapacityOptions(jsii.compat.TypedDict, total=False):
    containersAccessInstanceRole: bool
    taskDrainTimeSeconds: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AddCapacityOptions")
class AddCapacityOptions(AddAutoScalingGroupCapacityOptions, aws_cdk.aws_autoscaling.CommonAutoScalingGroupProps, jsii.compat.TypedDict):
    instanceType: aws_cdk.aws_ec2.InstanceType

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AssetImageProps")
class AssetImageProps(jsii.compat.TypedDict):
    directory: str

class _AwsLogDriverProps(jsii.compat.TypedDict, total=False):
    datetimeFormat: str
    logGroup: aws_cdk.aws_logs.ILogGroup
    multilinePattern: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AwsLogDriverProps")
class AwsLogDriverProps(_AwsLogDriverProps):
    streamPrefix: str

@jsii.implements(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget)
class BaseService(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.BaseService"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseServiceProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, props: "BaseServiceProps", additional_props: typing.Any, cluster_name: str, task_definition: "TaskDefinition") -> None:
        jsii.create(BaseService, self, [scope, id, props, additional_props, cluster_name, task_definition])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @jsii.member(jsii_name="autoScaleTaskCount")
    def auto_scale_task_count(self, *, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> "ScalableTaskCount":
        props: aws_cdk.aws_applicationautoscaling.EnableScalingProps = {"maxCapacity": max_capacity}

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        return jsii.invoke(self, "autoScaleTaskCount", [props])

    @jsii.member(jsii_name="configureAwsVpcNetworking")
    def _configure_aws_vpc_networking(self, vpc: aws_cdk.aws_ec2.IVpcNetwork, assign_public_ip: typing.Optional[bool]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None) -> None:
        return jsii.invoke(self, "configureAwsVpcNetworking", [vpc, assign_public_ip, vpc_subnets, security_group])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        return jsii.get(self, "serviceName")

    @property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> "TaskDefinition":
        return jsii.get(self, "taskDefinition")

    @property
    @jsii.member(jsii_name="cluster")
    def _cluster(self) -> "ICluster":
        return jsii.get(self, "cluster")

    @_cluster.setter
    def _cluster(self, value: "ICluster"):
        return jsii.set(self, "cluster", value)

    @property
    @jsii.member(jsii_name="loadBalancers")
    def _load_balancers(self) -> typing.List["CfnService.LoadBalancerProperty"]:
        return jsii.get(self, "loadBalancers")

    @_load_balancers.setter
    def _load_balancers(self, value: typing.List["CfnService.LoadBalancerProperty"]):
        return jsii.set(self, "loadBalancers", value)

    @property
    @jsii.member(jsii_name="serviceRegistries")
    def _service_registries(self) -> typing.List["CfnService.ServiceRegistryProperty"]:
        return jsii.get(self, "serviceRegistries")

    @_service_registries.setter
    def _service_registries(self, value: typing.List["CfnService.ServiceRegistryProperty"]):
        return jsii.set(self, "serviceRegistries", value)

    @property
    @jsii.member(jsii_name="cloudmapService")
    def _cloudmap_service(self) -> typing.Optional[aws_cdk.aws_servicediscovery.Service]:
        return jsii.get(self, "cloudmapService")

    @_cloudmap_service.setter
    def _cloudmap_service(self, value: typing.Optional[aws_cdk.aws_servicediscovery.Service]):
        return jsii.set(self, "cloudmapService", value)

    @property
    @jsii.member(jsii_name="networkConfiguration")
    def _network_configuration(self) -> typing.Optional["CfnService.NetworkConfigurationProperty"]:
        return jsii.get(self, "networkConfiguration")

    @_network_configuration.setter
    def _network_configuration(self, value: typing.Optional["CfnService.NetworkConfigurationProperty"]):
        return jsii.set(self, "networkConfiguration", value)


class _BaseServiceProxy(BaseService):
    pass

class _BaseServiceProps(jsii.compat.TypedDict, total=False):
    desiredCount: jsii.Number
    healthCheckGracePeriodSeconds: jsii.Number
    maximumPercent: jsii.Number
    minimumHealthyPercent: jsii.Number
    serviceDiscoveryOptions: "ServiceDiscoveryOptions"
    serviceName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.BaseServiceProps")
class BaseServiceProps(_BaseServiceProps):
    cluster: "ICluster"

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.BinPackResource")
class BinPackResource(enum.Enum):
    Cpu = "Cpu"
    Memory = "Memory"

class BuiltInAttributes(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.BuiltInAttributes"):
    def __init__(self) -> None:
        jsii.create(BuiltInAttributes, self, [])

    @classproperty
    @jsii.member(jsii_name="AmiId")
    def AMI_ID(cls) -> str:
        return jsii.sget(cls, "AmiId")

    @classproperty
    @jsii.member(jsii_name="AvailabilityZone")
    def AVAILABILITY_ZONE(cls) -> str:
        return jsii.sget(cls, "AvailabilityZone")

    @classproperty
    @jsii.member(jsii_name="InstanceId")
    def INSTANCE_ID(cls) -> str:
        return jsii.sget(cls, "InstanceId")

    @classproperty
    @jsii.member(jsii_name="InstanceType")
    def INSTANCE_TYPE(cls) -> str:
        return jsii.sget(cls, "InstanceType")

    @classproperty
    @jsii.member(jsii_name="OsType")
    def OS_TYPE(cls) -> str:
        return jsii.sget(cls, "OsType")


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Capability")
class Capability(enum.Enum):
    All = "All"
    AuditControl = "AuditControl"
    AuditWrite = "AuditWrite"
    BlockSuspend = "BlockSuspend"
    Chown = "Chown"
    DacOverride = "DacOverride"
    DacReadSearch = "DacReadSearch"
    Fowner = "Fowner"
    Fsetid = "Fsetid"
    IpcLock = "IpcLock"
    IpcOwner = "IpcOwner"
    Kill = "Kill"
    Lease = "Lease"
    LinuxImmutable = "LinuxImmutable"
    MacAdmin = "MacAdmin"
    MacOverride = "MacOverride"
    Mknod = "Mknod"
    NetAdmin = "NetAdmin"
    NetBindService = "NetBindService"
    NetBroadcast = "NetBroadcast"
    NetRaw = "NetRaw"
    Setfcap = "Setfcap"
    Setgid = "Setgid"
    Setpcap = "Setpcap"
    Setuid = "Setuid"
    SysAdmin = "SysAdmin"
    SysBoot = "SysBoot"
    SysChroot = "SysChroot"
    SysModule = "SysModule"
    SysNice = "SysNice"
    SysPacct = "SysPacct"
    SysPtrace = "SysPtrace"
    SysRawio = "SysRawio"
    SysResource = "SysResource"
    SysTime = "SysTime"
    SysTtyConfig = "SysTtyConfig"
    Syslog = "Syslog"
    WakeAlarm = "WakeAlarm"

class CfnCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster_name: typing.Optional[str]=None) -> None:
        props: CfnClusterProps = {}

        if cluster_name is not None:
            props["clusterName"] = cluster_name

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnClusterProps")
class CfnClusterProps(jsii.compat.TypedDict, total=False):
    clusterName: str

class CfnService(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnService"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, task_definition: str, cluster: typing.Optional[str]=None, deployment_configuration: typing.Optional[typing.Union["DeploymentConfigurationProperty", aws_cdk.cdk.Token]]=None, desired_count: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, health_check_grace_period_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, launch_type: typing.Optional[str]=None, load_balancers: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["LoadBalancerProperty", aws_cdk.cdk.Token]]]]=None, network_configuration: typing.Optional[typing.Union["NetworkConfigurationProperty", aws_cdk.cdk.Token]]=None, placement_constraints: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PlacementConstraintProperty"]]]]=None, placement_strategies: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PlacementStrategyProperty"]]]]=None, platform_version: typing.Optional[str]=None, role: typing.Optional[str]=None, scheduling_strategy: typing.Optional[str]=None, service_name: typing.Optional[str]=None, service_registries: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ServiceRegistryProperty", aws_cdk.cdk.Token]]]]=None) -> None:
        props: CfnServiceProps = {"taskDefinition": task_definition}

        if cluster is not None:
            props["cluster"] = cluster

        if deployment_configuration is not None:
            props["deploymentConfiguration"] = deployment_configuration

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if health_check_grace_period_seconds is not None:
            props["healthCheckGracePeriodSeconds"] = health_check_grace_period_seconds

        if launch_type is not None:
            props["launchType"] = launch_type

        if load_balancers is not None:
            props["loadBalancers"] = load_balancers

        if network_configuration is not None:
            props["networkConfiguration"] = network_configuration

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if placement_strategies is not None:
            props["placementStrategies"] = placement_strategies

        if platform_version is not None:
            props["platformVersion"] = platform_version

        if role is not None:
            props["role"] = role

        if scheduling_strategy is not None:
            props["schedulingStrategy"] = scheduling_strategy

        if service_name is not None:
            props["serviceName"] = service_name

        if service_registries is not None:
            props["serviceRegistries"] = service_registries

        jsii.create(CfnService, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnServiceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        return jsii.get(self, "serviceName")

    class _AwsVpcConfigurationProperty(jsii.compat.TypedDict, total=False):
        assignPublicIp: str
        securityGroups: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.AwsVpcConfigurationProperty")
    class AwsVpcConfigurationProperty(_AwsVpcConfigurationProperty):
        subnets: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.DeploymentConfigurationProperty")
    class DeploymentConfigurationProperty(jsii.compat.TypedDict, total=False):
        maximumPercent: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minimumHealthyPercent: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _LoadBalancerProperty(jsii.compat.TypedDict, total=False):
        containerName: str
        loadBalancerName: str
        targetGroupArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.LoadBalancerProperty")
    class LoadBalancerProperty(_LoadBalancerProperty):
        containerPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.NetworkConfigurationProperty")
    class NetworkConfigurationProperty(jsii.compat.TypedDict, total=False):
        awsvpcConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnService.AwsVpcConfigurationProperty"]

    class _PlacementConstraintProperty(jsii.compat.TypedDict, total=False):
        expression: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.PlacementConstraintProperty")
    class PlacementConstraintProperty(_PlacementConstraintProperty):
        type: str

    class _PlacementStrategyProperty(jsii.compat.TypedDict, total=False):
        field: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.PlacementStrategyProperty")
    class PlacementStrategyProperty(_PlacementStrategyProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.ServiceRegistryProperty")
    class ServiceRegistryProperty(jsii.compat.TypedDict, total=False):
        containerName: str
        containerPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        registryArn: str


class _CfnServiceProps(jsii.compat.TypedDict, total=False):
    cluster: str
    deploymentConfiguration: typing.Union["CfnService.DeploymentConfigurationProperty", aws_cdk.cdk.Token]
    desiredCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    healthCheckGracePeriodSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    launchType: str
    loadBalancers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnService.LoadBalancerProperty", aws_cdk.cdk.Token]]]
    networkConfiguration: typing.Union["CfnService.NetworkConfigurationProperty", aws_cdk.cdk.Token]
    placementConstraints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnService.PlacementConstraintProperty"]]]
    placementStrategies: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnService.PlacementStrategyProperty"]]]
    platformVersion: str
    role: str
    schedulingStrategy: str
    serviceName: str
    serviceRegistries: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnService.ServiceRegistryProperty", aws_cdk.cdk.Token]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnServiceProps")
class CfnServiceProps(_CfnServiceProps):
    taskDefinition: str

class CfnTaskDefinition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, container_definitions: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ContainerDefinitionProperty", aws_cdk.cdk.Token]]]]=None, cpu: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, family: typing.Optional[str]=None, memory: typing.Optional[str]=None, network_mode: typing.Optional[str]=None, placement_constraints: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TaskDefinitionPlacementConstraintProperty"]]]]=None, requires_compatibilities: typing.Optional[typing.List[str]]=None, task_role_arn: typing.Optional[str]=None, volumes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "VolumeProperty"]]]]=None) -> None:
        props: CfnTaskDefinitionProps = {}

        if container_definitions is not None:
            props["containerDefinitions"] = container_definitions

        if cpu is not None:
            props["cpu"] = cpu

        if execution_role_arn is not None:
            props["executionRoleArn"] = execution_role_arn

        if family is not None:
            props["family"] = family

        if memory is not None:
            props["memory"] = memory

        if network_mode is not None:
            props["networkMode"] = network_mode

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if requires_compatibilities is not None:
            props["requiresCompatibilities"] = requires_compatibilities

        if task_role_arn is not None:
            props["taskRoleArn"] = task_role_arn

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(CfnTaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTaskDefinitionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        return jsii.get(self, "taskDefinitionArn")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ContainerDefinitionProperty")
    class ContainerDefinitionProperty(jsii.compat.TypedDict, total=False):
        command: typing.List[str]
        cpu: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        disableNetworking: typing.Union[bool, aws_cdk.cdk.Token]
        dnsSearchDomains: typing.List[str]
        dnsServers: typing.List[str]
        dockerLabels: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        dockerSecurityOptions: typing.List[str]
        entryPoint: typing.List[str]
        environment: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.KeyValuePairProperty"]]]
        essential: typing.Union[bool, aws_cdk.cdk.Token]
        extraHosts: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.HostEntryProperty"]]]
        healthCheck: typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.HealthCheckProperty"]
        hostname: str
        image: str
        links: typing.List[str]
        linuxParameters: typing.Union["CfnTaskDefinition.LinuxParametersProperty", aws_cdk.cdk.Token]
        logConfiguration: typing.Union["CfnTaskDefinition.LogConfigurationProperty", aws_cdk.cdk.Token]
        memory: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        memoryReservation: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        mountPoints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.MountPointProperty"]]]
        name: str
        portMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.PortMappingProperty"]]]
        privileged: typing.Union[bool, aws_cdk.cdk.Token]
        readonlyRootFilesystem: typing.Union[bool, aws_cdk.cdk.Token]
        repositoryCredentials: typing.Union["CfnTaskDefinition.RepositoryCredentialsProperty", aws_cdk.cdk.Token]
        ulimits: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.UlimitProperty"]]]
        user: str
        volumesFrom: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.VolumeFromProperty"]]]
        workingDirectory: str

    class _DeviceProperty(jsii.compat.TypedDict, total=False):
        containerPath: str
        permissions: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.DeviceProperty")
    class DeviceProperty(_DeviceProperty):
        hostPath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.DockerVolumeConfigurationProperty")
    class DockerVolumeConfigurationProperty(jsii.compat.TypedDict, total=False):
        autoprovision: typing.Union[bool, aws_cdk.cdk.Token]
        driver: str
        driverOpts: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        labels: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        scope: str

    class _HealthCheckProperty(jsii.compat.TypedDict, total=False):
        interval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        retries: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        startPeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        timeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HealthCheckProperty")
    class HealthCheckProperty(_HealthCheckProperty):
        command: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HostEntryProperty")
    class HostEntryProperty(jsii.compat.TypedDict):
        hostname: str
        ipAddress: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HostVolumePropertiesProperty")
    class HostVolumePropertiesProperty(jsii.compat.TypedDict, total=False):
        sourcePath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.KernelCapabilitiesProperty")
    class KernelCapabilitiesProperty(jsii.compat.TypedDict, total=False):
        add: typing.List[str]
        drop: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.KeyValuePairProperty")
    class KeyValuePairProperty(jsii.compat.TypedDict, total=False):
        name: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.LinuxParametersProperty")
    class LinuxParametersProperty(jsii.compat.TypedDict, total=False):
        capabilities: typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.KernelCapabilitiesProperty"]
        devices: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.DeviceProperty"]]]
        initProcessEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        sharedMemorySize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        tmpfs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.TmpfsProperty"]]]

    class _LogConfigurationProperty(jsii.compat.TypedDict, total=False):
        options: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.LogConfigurationProperty")
    class LogConfigurationProperty(_LogConfigurationProperty):
        logDriver: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.MountPointProperty")
    class MountPointProperty(jsii.compat.TypedDict, total=False):
        containerPath: str
        readOnly: typing.Union[bool, aws_cdk.cdk.Token]
        sourceVolume: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.PortMappingProperty")
    class PortMappingProperty(jsii.compat.TypedDict, total=False):
        containerPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        hostPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        protocol: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.RepositoryCredentialsProperty")
    class RepositoryCredentialsProperty(jsii.compat.TypedDict, total=False):
        credentialsParameter: str

    class _TaskDefinitionPlacementConstraintProperty(jsii.compat.TypedDict, total=False):
        expression: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty")
    class TaskDefinitionPlacementConstraintProperty(_TaskDefinitionPlacementConstraintProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.TmpfsProperty")
    class TmpfsProperty(jsii.compat.TypedDict, total=False):
        containerPath: str
        mountOptions: typing.List[str]
        size: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.UlimitProperty")
    class UlimitProperty(jsii.compat.TypedDict):
        hardLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        name: str
        softLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.VolumeFromProperty")
    class VolumeFromProperty(jsii.compat.TypedDict, total=False):
        readOnly: typing.Union[bool, aws_cdk.cdk.Token]
        sourceContainer: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.VolumeProperty")
    class VolumeProperty(jsii.compat.TypedDict, total=False):
        dockerVolumeConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.DockerVolumeConfigurationProperty"]
        host: typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.HostVolumePropertiesProperty"]
        name: str


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinitionProps")
class CfnTaskDefinitionProps(jsii.compat.TypedDict, total=False):
    containerDefinitions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnTaskDefinition.ContainerDefinitionProperty", aws_cdk.cdk.Token]]]
    cpu: str
    executionRoleArn: str
    family: str
    memory: str
    networkMode: str
    placementConstraints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty"]]]
    requiresCompatibilities: typing.List[str]
    taskRoleArn: str
    volumes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTaskDefinition.VolumeProperty"]]]

class _ClusterImportProps(jsii.compat.TypedDict, total=False):
    clusterArn: str
    defaultNamespace: aws_cdk.aws_servicediscovery.NamespaceImportProps
    hasEc2Capacity: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ClusterImportProps")
class ClusterImportProps(_ClusterImportProps):
    clusterName: str
    securityGroups: typing.List[aws_cdk.aws_ec2.SecurityGroupImportProps]
    vpc: aws_cdk.aws_ec2.VpcNetworkImportProps

class _ClusterProps(jsii.compat.TypedDict, total=False):
    clusterName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ClusterProps")
class ClusterProps(_ClusterProps):
    vpc: aws_cdk.aws_ec2.IVpcNetwork

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CommonTaskDefinitionProps")
class CommonTaskDefinitionProps(jsii.compat.TypedDict, total=False):
    executionRole: aws_cdk.aws_iam.IRole
    family: str
    taskRole: aws_cdk.aws_iam.IRole
    volumes: typing.List["Volume"]

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Compatibility")
class Compatibility(enum.Enum):
    Ec2 = "Ec2"
    Fargate = "Fargate"
    Ec2AndFargate = "Ec2AndFargate"

class ContainerDefinition(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.ContainerDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, task_definition: "TaskDefinition", image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str,str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str,str]]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> None:
        props: ContainerDefinitionProps = {"taskDefinition": task_definition, "image": image}

        if command is not None:
            props["command"] = command

        if cpu is not None:
            props["cpu"] = cpu

        if disable_networking is not None:
            props["disableNetworking"] = disable_networking

        if dns_search_domains is not None:
            props["dnsSearchDomains"] = dns_search_domains

        if dns_servers is not None:
            props["dnsServers"] = dns_servers

        if docker_labels is not None:
            props["dockerLabels"] = docker_labels

        if docker_security_options is not None:
            props["dockerSecurityOptions"] = docker_security_options

        if entry_point is not None:
            props["entryPoint"] = entry_point

        if environment is not None:
            props["environment"] = environment

        if essential is not None:
            props["essential"] = essential

        if extra_hosts is not None:
            props["extraHosts"] = extra_hosts

        if health_check is not None:
            props["healthCheck"] = health_check

        if hostname is not None:
            props["hostname"] = hostname

        if logging is not None:
            props["logging"] = logging

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        if privileged is not None:
            props["privileged"] = privileged

        if readonly_root_filesystem is not None:
            props["readonlyRootFilesystem"] = readonly_root_filesystem

        if user is not None:
            props["user"] = user

        if working_directory is not None:
            props["workingDirectory"] = working_directory

        jsii.create(ContainerDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="addLink")
    def add_link(self, container: "ContainerDefinition", alias: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "addLink", [container, alias])

    @jsii.member(jsii_name="addMountPoints")
    def add_mount_points(self, *, container_path: str, read_only: bool, source_volume: str) -> None:
        mount_points: MountPoint = {"containerPath": container_path, "readOnly": read_only, "sourceVolume": source_volume}

        return jsii.invoke(self, "addMountPoints", [mount_points])

    @jsii.member(jsii_name="addPortMappings")
    def add_port_mappings(self, *, container_port: jsii.Number, host_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None) -> None:
        port_mappings: PortMapping = {"containerPort": container_port}

        if host_port is not None:
            port_mappings["hostPort"] = host_port

        if protocol is not None:
            port_mappings["protocol"] = protocol

        return jsii.invoke(self, "addPortMappings", [port_mappings])

    @jsii.member(jsii_name="addScratch")
    def add_scratch(self, *, container_path: str, name: str, read_only: bool, source_path: str) -> None:
        scratch: ScratchSpace = {"containerPath": container_path, "name": name, "readOnly": read_only, "sourcePath": source_path}

        return jsii.invoke(self, "addScratch", [scratch])

    @jsii.member(jsii_name="addToExecutionPolicy")
    def add_to_execution_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToExecutionPolicy", [statement])

    @jsii.member(jsii_name="addUlimits")
    def add_ulimits(self, *, hard_limit: jsii.Number, name: "UlimitName", soft_limit: jsii.Number) -> None:
        ulimits: Ulimit = {"hardLimit": hard_limit, "name": name, "softLimit": soft_limit}

        return jsii.invoke(self, "addUlimits", [ulimits])

    @jsii.member(jsii_name="addVolumesFrom")
    def add_volumes_from(self, *, read_only: bool, source_container: str) -> None:
        volumes_from: VolumeFrom = {"readOnly": read_only, "sourceContainer": source_container}

        return jsii.invoke(self, "addVolumesFrom", [volumes_from])

    @jsii.member(jsii_name="renderContainerDefinition")
    def render_container_definition(self) -> "CfnTaskDefinition.ContainerDefinitionProperty":
        return jsii.invoke(self, "renderContainerDefinition", [])

    @property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        return jsii.get(self, "containerPort")

    @property
    @jsii.member(jsii_name="essential")
    def essential(self) -> bool:
        return jsii.get(self, "essential")

    @property
    @jsii.member(jsii_name="ingressPort")
    def ingress_port(self) -> jsii.Number:
        return jsii.get(self, "ingressPort")

    @property
    @jsii.member(jsii_name="linuxParameters")
    def linux_parameters(self) -> "LinuxParameters":
        return jsii.get(self, "linuxParameters")

    @property
    @jsii.member(jsii_name="memoryLimitSpecified")
    def memory_limit_specified(self) -> bool:
        return jsii.get(self, "memoryLimitSpecified")

    @property
    @jsii.member(jsii_name="mountPoints")
    def mount_points(self) -> typing.List["MountPoint"]:
        return jsii.get(self, "mountPoints")

    @property
    @jsii.member(jsii_name="portMappings")
    def port_mappings(self) -> typing.List["PortMapping"]:
        return jsii.get(self, "portMappings")

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ContainerDefinitionProps":
        return jsii.get(self, "props")

    @property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> "TaskDefinition":
        return jsii.get(self, "taskDefinition")

    @property
    @jsii.member(jsii_name="ulimits")
    def ulimits(self) -> typing.List["Ulimit"]:
        return jsii.get(self, "ulimits")

    @property
    @jsii.member(jsii_name="volumesFrom")
    def volumes_from(self) -> typing.List["VolumeFrom"]:
        return jsii.get(self, "volumesFrom")


class _ContainerDefinitionOptions(jsii.compat.TypedDict, total=False):
    command: typing.List[str]
    cpu: jsii.Number
    disableNetworking: bool
    dnsSearchDomains: typing.List[str]
    dnsServers: typing.List[str]
    dockerLabels: typing.Mapping[str,str]
    dockerSecurityOptions: typing.List[str]
    entryPoint: typing.List[str]
    environment: typing.Mapping[str,str]
    essential: bool
    extraHosts: typing.Mapping[str,str]
    healthCheck: "HealthCheck"
    hostname: str
    logging: "LogDriver"
    memoryLimitMiB: jsii.Number
    memoryReservationMiB: jsii.Number
    privileged: bool
    readonlyRootFilesystem: bool
    user: str
    workingDirectory: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerDefinitionOptions")
class ContainerDefinitionOptions(_ContainerDefinitionOptions):
    image: "ContainerImage"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerDefinitionProps")
class ContainerDefinitionProps(ContainerDefinitionOptions, jsii.compat.TypedDict):
    taskDefinition: "TaskDefinition"

class ContainerImage(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.ContainerImage"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ContainerImageProxy

    def __init__(self) -> None:
        jsii.create(ContainerImage, self, [])

    @jsii.member(jsii_name="fromAsset")
    @classmethod
    def from_asset(cls, scope: aws_cdk.cdk.Construct, id: str, *, directory: str) -> "AssetImage":
        props: AssetImageProps = {"directory": directory}

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromEcrRepository")
    @classmethod
    def from_ecr_repository(cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str]=None) -> "EcrImage":
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="fromRegistry")
    @classmethod
    def from_registry(cls, name: str, *, credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None) -> "RepositoryImage":
        props: RepositoryImageProps = {}

        if credentials is not None:
            props["credentials"] = credentials

        return jsii.sinvoke(cls, "fromRegistry", [name, props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, container_definition: "ContainerDefinition") -> None:
        ...

    @jsii.member(jsii_name="toRepositoryCredentialsJson")
    @abc.abstractmethod
    def to_repository_credentials_json(self) -> typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]:
        ...

    @property
    @jsii.member(jsii_name="imageName")
    @abc.abstractmethod
    def image_name(self) -> str:
        ...


class _ContainerImageProxy(ContainerImage):
    @jsii.member(jsii_name="bind")
    def bind(self, container_definition: "ContainerDefinition") -> None:
        return jsii.invoke(self, "bind", [container_definition])

    @jsii.member(jsii_name="toRepositoryCredentialsJson")
    def to_repository_credentials_json(self) -> typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]:
        return jsii.invoke(self, "toRepositoryCredentialsJson", [])

    @property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> str:
        return jsii.get(self, "imageName")


class AssetImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.AssetImage"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, directory: str) -> None:
        props: AssetImageProps = {"directory": directory}

        jsii.create(AssetImage, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(self, container_definition: "ContainerDefinition") -> None:
        return jsii.invoke(self, "bind", [container_definition])

    @jsii.member(jsii_name="toRepositoryCredentialsJson")
    def to_repository_credentials_json(self) -> typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]:
        return jsii.invoke(self, "toRepositoryCredentialsJson", [])

    @property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> str:
        return jsii.get(self, "imageName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CpuUtilizationScalingProps")
class CpuUtilizationScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    targetUtilizationPercent: jsii.Number

class _Device(jsii.compat.TypedDict, total=False):
    containerPath: str
    permissions: typing.List["DevicePermission"]

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Device")
class Device(_Device):
    hostPath: str

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.DevicePermission")
class DevicePermission(enum.Enum):
    Read = "Read"
    Write = "Write"
    Mknod = "Mknod"

class _DockerVolumeConfiguration(jsii.compat.TypedDict, total=False):
    autoprovision: bool
    driverOpts: typing.List[str]
    labels: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.DockerVolumeConfiguration")
class DockerVolumeConfiguration(_DockerVolumeConfiguration):
    driver: str
    scope: "Scope"

@jsii.implements(aws_cdk.aws_events.IEventRuleTarget)
class Ec2EventRuleTarget(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Ec2EventRuleTarget"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster: "ICluster", task_definition: "TaskDefinition", task_count: typing.Optional[jsii.Number]=None) -> None:
        props: Ec2EventRuleTargetProps = {"cluster": cluster, "taskDefinition": task_definition}

        if task_count is not None:
            props["taskCount"] = task_count

        jsii.create(Ec2EventRuleTarget, self, [scope, id, props])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_unique_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_unique_id])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        return jsii.invoke(self, "prepare", [])

    @property
    @jsii.member(jsii_name="eventsRole")
    def events_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "eventsRole")


class _Ec2EventRuleTargetProps(jsii.compat.TypedDict, total=False):
    taskCount: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ec2EventRuleTargetProps")
class Ec2EventRuleTargetProps(_Ec2EventRuleTargetProps):
    cluster: "ICluster"
    taskDefinition: "TaskDefinition"

@jsii.implements(aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget)
class Ec2Service(BaseService, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Ec2Service"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, task_definition: "TaskDefinition", daemon: typing.Optional[bool]=None, place_on_distinct_instances: typing.Optional[bool]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cluster: "ICluster", desired_count: typing.Optional[jsii.Number]=None, health_check_grace_period_seconds: typing.Optional[jsii.Number]=None, maximum_percent: typing.Optional[jsii.Number]=None, minimum_healthy_percent: typing.Optional[jsii.Number]=None, service_discovery_options: typing.Optional["ServiceDiscoveryOptions"]=None, service_name: typing.Optional[str]=None) -> None:
        props: Ec2ServiceProps = {"taskDefinition": task_definition, "cluster": cluster}

        if daemon is not None:
            props["daemon"] = daemon

        if place_on_distinct_instances is not None:
            props["placeOnDistinctInstances"] = place_on_distinct_instances

        if security_group is not None:
            props["securityGroup"] = security_group

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if health_check_grace_period_seconds is not None:
            props["healthCheckGracePeriodSeconds"] = health_check_grace_period_seconds

        if maximum_percent is not None:
            props["maximumPercent"] = maximum_percent

        if minimum_healthy_percent is not None:
            props["minimumHealthyPercent"] = minimum_healthy_percent

        if service_discovery_options is not None:
            props["serviceDiscoveryOptions"] = service_discovery_options

        if service_name is not None:
            props["serviceName"] = service_name

        jsii.create(Ec2Service, self, [scope, id, props])

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer) -> None:
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCpuUtilization")
    def metric_cpu_utilization(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricCpuUtilization", [props])

    @jsii.member(jsii_name="metricMemoryUtilization")
    def metric_memory_utilization(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricMemoryUtilization", [props])

    @jsii.member(jsii_name="placeOnMemberOf")
    def place_on_member_of(self, *expressions: str) -> None:
        return jsii.invoke(self, "placeOnMemberOf", [expressions])

    @jsii.member(jsii_name="placePackedBy")
    def place_packed_by(self, resource: "BinPackResource") -> None:
        return jsii.invoke(self, "placePackedBy", [resource])

    @jsii.member(jsii_name="placeRandomly")
    def place_randomly(self) -> None:
        return jsii.invoke(self, "placeRandomly", [])

    @jsii.member(jsii_name="placeSpreadAcross")
    def place_spread_across(self, *fields: str) -> None:
        return jsii.invoke(self, "placeSpreadAcross", [fields])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")


class _Ec2ServiceProps(BaseServiceProps, jsii.compat.TypedDict, total=False):
    daemon: bool
    placeOnDistinctInstances: bool
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ec2ServiceProps")
class Ec2ServiceProps(_Ec2ServiceProps):
    taskDefinition: "TaskDefinition"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ec2TaskDefinitionProps")
class Ec2TaskDefinitionProps(CommonTaskDefinitionProps, jsii.compat.TypedDict, total=False):
    networkMode: "NetworkMode"
    placementConstraints: typing.List["PlacementConstraint"]

class EcrImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.EcrImage"):
    def __init__(self, repository: aws_cdk.aws_ecr.IRepository, tag: str) -> None:
        jsii.create(EcrImage, self, [repository, tag])

    @jsii.member(jsii_name="bind")
    def bind(self, container_definition: "ContainerDefinition") -> None:
        return jsii.invoke(self, "bind", [container_definition])

    @jsii.member(jsii_name="toRepositoryCredentialsJson")
    def to_repository_credentials_json(self) -> typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]:
        return jsii.invoke(self, "toRepositoryCredentialsJson", [])

    @property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> str:
        return jsii.get(self, "imageName")


@jsii.implements(aws_cdk.aws_ec2.IMachineImageSource)
class EcsOptimizedAmi(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.EcsOptimizedAmi"):
    def __init__(self, *, generation: typing.Optional[aws_cdk.aws_ec2.AmazonLinuxGeneration]=None) -> None:
        props: EcsOptimizedAmiProps = {}

        if generation is not None:
            props["generation"] = generation

        jsii.create(EcsOptimizedAmi, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> aws_cdk.aws_ec2.MachineImage:
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.EcsOptimizedAmiProps")
class EcsOptimizedAmiProps(jsii.compat.TypedDict, total=False):
    generation: aws_cdk.aws_ec2.AmazonLinuxGeneration

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.FargatePlatformVersion")
class FargatePlatformVersion(enum.Enum):
    Latest = "Latest"
    Version1_3 = "Version1_3"
    Version1_2 = "Version1_2"
    Version1_1 = "Version1_1"
    Version1_0 = "Version1_0"

class FargateService(BaseService, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.FargateService"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, platform_version: typing.Optional["FargatePlatformVersion"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cluster: "ICluster", desired_count: typing.Optional[jsii.Number]=None, health_check_grace_period_seconds: typing.Optional[jsii.Number]=None, maximum_percent: typing.Optional[jsii.Number]=None, minimum_healthy_percent: typing.Optional[jsii.Number]=None, service_discovery_options: typing.Optional["ServiceDiscoveryOptions"]=None, service_name: typing.Optional[str]=None) -> None:
        props: FargateServiceProps = {"taskDefinition": task_definition, "cluster": cluster}

        if assign_public_ip is not None:
            props["assignPublicIp"] = assign_public_ip

        if platform_version is not None:
            props["platformVersion"] = platform_version

        if security_group is not None:
            props["securityGroup"] = security_group

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if health_check_grace_period_seconds is not None:
            props["healthCheckGracePeriodSeconds"] = health_check_grace_period_seconds

        if maximum_percent is not None:
            props["maximumPercent"] = maximum_percent

        if minimum_healthy_percent is not None:
            props["minimumHealthyPercent"] = minimum_healthy_percent

        if service_discovery_options is not None:
            props["serviceDiscoveryOptions"] = service_discovery_options

        if service_name is not None:
            props["serviceName"] = service_name

        jsii.create(FargateService, self, [scope, id, props])


class _FargateServiceProps(BaseServiceProps, jsii.compat.TypedDict, total=False):
    assignPublicIp: bool
    platformVersion: "FargatePlatformVersion"
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.FargateServiceProps")
class FargateServiceProps(_FargateServiceProps):
    taskDefinition: "TaskDefinition"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.FargateTaskDefinitionProps")
class FargateTaskDefinitionProps(CommonTaskDefinitionProps, jsii.compat.TypedDict, total=False):
    cpu: str
    memoryMiB: str

class _HealthCheck(jsii.compat.TypedDict, total=False):
    intervalSeconds: jsii.Number
    retries: jsii.Number
    startPeriod: jsii.Number
    timeout: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.HealthCheck")
class HealthCheck(_HealthCheck):
    command: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Host")
class Host(jsii.compat.TypedDict, total=False):
    sourcePath: str

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.ICluster")
class ICluster(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        ...

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        ...

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpcNetwork:
        ...

    @property
    @jsii.member(jsii_name="defaultNamespace")
    def default_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterImportProps":
        ...


class _IClusterProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ecs.ICluster"
    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        return jsii.get(self, "hasEc2Capacity")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpcNetwork:
        return jsii.get(self, "vpc")

    @property
    @jsii.member(jsii_name="defaultNamespace")
    def default_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        return jsii.get(self, "defaultNamespace")

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterImportProps":
        return jsii.invoke(self, "export", [])


@jsii.implements(ICluster)
class Cluster(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Cluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpcNetwork, cluster_name: typing.Optional[str]=None) -> None:
        props: ClusterProps = {"vpc": vpc}

        if cluster_name is not None:
            props["clusterName"] = cluster_name

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, cluster_name: str, security_groups: typing.List[aws_cdk.aws_ec2.SecurityGroupImportProps], vpc: aws_cdk.aws_ec2.VpcNetworkImportProps, cluster_arn: typing.Optional[str]=None, default_namespace: typing.Optional[aws_cdk.aws_servicediscovery.NamespaceImportProps]=None, has_ec2_capacity: typing.Optional[bool]=None) -> "ICluster":
        props: ClusterImportProps = {"clusterName": cluster_name, "securityGroups": security_groups, "vpc": vpc}

        if cluster_arn is not None:
            props["clusterArn"] = cluster_arn

        if default_namespace is not None:
            props["defaultNamespace"] = default_namespace

        if has_ec2_capacity is not None:
            props["hasEc2Capacity"] = has_ec2_capacity

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, auto_scaling_group: aws_cdk.aws_autoscaling.AutoScalingGroup, *, containers_access_instance_role: typing.Optional[bool]=None, task_drain_time_seconds: typing.Optional[jsii.Number]=None) -> None:
        options: AddAutoScalingGroupCapacityOptions = {}

        if containers_access_instance_role is not None:
            options["containersAccessInstanceRole"] = containers_access_instance_role

        if task_drain_time_seconds is not None:
            options["taskDrainTimeSeconds"] = task_drain_time_seconds

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(self, id: str, *, instance_type: aws_cdk.aws_ec2.InstanceType, containers_access_instance_role: typing.Optional[bool]=None, task_drain_time_seconds: typing.Optional[jsii.Number]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, desired_capacity: typing.Optional[jsii.Number]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout_sec: typing.Optional[jsii.Number]=None, rolling_update_configuration: typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]=None, update_type: typing.Optional[aws_cdk.aws_autoscaling.UpdateType]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        options: AddCapacityOptions = {"instanceType": instance_type}

        if containers_access_instance_role is not None:
            options["containersAccessInstanceRole"] = containers_access_instance_role

        if task_drain_time_seconds is not None:
            options["taskDrainTimeSeconds"] = task_drain_time_seconds

        if allow_all_outbound is not None:
            options["allowAllOutbound"] = allow_all_outbound

        if associate_public_ip_address is not None:
            options["associatePublicIpAddress"] = associate_public_ip_address

        if cooldown_seconds is not None:
            options["cooldownSeconds"] = cooldown_seconds

        if desired_capacity is not None:
            options["desiredCapacity"] = desired_capacity

        if ignore_unmodified_size_properties is not None:
            options["ignoreUnmodifiedSizeProperties"] = ignore_unmodified_size_properties

        if key_name is not None:
            options["keyName"] = key_name

        if max_capacity is not None:
            options["maxCapacity"] = max_capacity

        if min_capacity is not None:
            options["minCapacity"] = min_capacity

        if notifications_topic is not None:
            options["notificationsTopic"] = notifications_topic

        if replacing_update_min_successful_instances_percent is not None:
            options["replacingUpdateMinSuccessfulInstancesPercent"] = replacing_update_min_successful_instances_percent

        if resource_signal_count is not None:
            options["resourceSignalCount"] = resource_signal_count

        if resource_signal_timeout_sec is not None:
            options["resourceSignalTimeoutSec"] = resource_signal_timeout_sec

        if rolling_update_configuration is not None:
            options["rollingUpdateConfiguration"] = rolling_update_configuration

        if update_type is not None:
            options["updateType"] = update_type

        if vpc_subnets is not None:
            options["vpcSubnets"] = vpc_subnets

        return jsii.invoke(self, "addCapacity", [id, options])

    @jsii.member(jsii_name="addDefaultCloudMapNamespace")
    def add_default_cloud_map_namespace(self, *, name: str, type: typing.Optional["NamespaceType"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]=None) -> aws_cdk.aws_servicediscovery.INamespace:
        options: NamespaceOptions = {"name": name}

        if type is not None:
            options["type"] = type

        if vpc is not None:
            options["vpc"] = vpc

        return jsii.invoke(self, "addDefaultCloudMapNamespace", [options])

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCpuReservation")
    def metric_cpu_reservation(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricCpuReservation", [props])

    @jsii.member(jsii_name="metricMemoryReservation")
    def metric_memory_reservation(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricMemoryReservation", [props])

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        return jsii.get(self, "hasEc2Capacity")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpcNetwork:
        return jsii.get(self, "vpc")

    @property
    @jsii.member(jsii_name="defaultNamespace")
    def default_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        return jsii.get(self, "defaultNamespace")


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.ITaskDefinitionExtension")
class ITaskDefinitionExtension(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ITaskDefinitionExtensionProxy

    @jsii.member(jsii_name="extend")
    def extend(self, task_definition: "TaskDefinition") -> None:
        ...


class _ITaskDefinitionExtensionProxy():
    __jsii_type__ = "@aws-cdk/aws-ecs.ITaskDefinitionExtension"
    @jsii.member(jsii_name="extend")
    def extend(self, task_definition: "TaskDefinition") -> None:
        return jsii.invoke(self, "extend", [task_definition])


class LinuxParameters(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.LinuxParameters"):
    def __init__(self) -> None:
        jsii.create(LinuxParameters, self, [])

    @jsii.member(jsii_name="addCapabilities")
    def add_capabilities(self, *cap: "Capability") -> None:
        return jsii.invoke(self, "addCapabilities", [cap])

    @jsii.member(jsii_name="addDevices")
    def add_devices(self, *, host_path: str, container_path: typing.Optional[str]=None, permissions: typing.Optional[typing.List["DevicePermission"]]=None) -> None:
        device: Device = {"hostPath": host_path}

        if container_path is not None:
            device["containerPath"] = container_path

        if permissions is not None:
            device["permissions"] = permissions

        return jsii.invoke(self, "addDevices", [device])

    @jsii.member(jsii_name="addTmpfs")
    def add_tmpfs(self, *, container_path: str, size: jsii.Number, mount_options: typing.Optional[typing.List["TmpfsMountOption"]]=None) -> None:
        tmpfs: Tmpfs = {"containerPath": container_path, "size": size}

        if mount_options is not None:
            tmpfs["mountOptions"] = mount_options

        return jsii.invoke(self, "addTmpfs", [tmpfs])

    @jsii.member(jsii_name="dropCapabilities")
    def drop_capabilities(self, *cap: "Capability") -> None:
        return jsii.invoke(self, "dropCapabilities", [cap])

    @jsii.member(jsii_name="renderLinuxParameters")
    def render_linux_parameters(self) -> "CfnTaskDefinition.LinuxParametersProperty":
        return jsii.invoke(self, "renderLinuxParameters", [])

    @property
    @jsii.member(jsii_name="initProcessEnabled")
    def init_process_enabled(self) -> typing.Optional[bool]:
        return jsii.get(self, "initProcessEnabled")

    @init_process_enabled.setter
    def init_process_enabled(self, value: typing.Optional[bool]):
        return jsii.set(self, "initProcessEnabled", value)

    @property
    @jsii.member(jsii_name="sharedMemorySize")
    def shared_memory_size(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "sharedMemorySize")

    @shared_memory_size.setter
    def shared_memory_size(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "sharedMemorySize", value)


class LoadBalancedFargateServiceApplet(aws_cdk.cdk.Stack, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.LoadBalancedFargateServiceApplet"):
    def __init__(self, scope: aws_cdk.cdk.App, id: str, *, image: str, certificate: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, cpu: typing.Optional[str]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, memory_mi_b: typing.Optional[str]=None, public_load_balancer: typing.Optional[bool]=None, public_tasks: typing.Optional[bool]=None, auto_deploy: typing.Optional[bool]=None, env: typing.Optional[aws_cdk.cdk.Environment]=None, naming_scheme: typing.Optional[aws_cdk.cdk.IAddressingScheme]=None, stack_name: typing.Optional[str]=None) -> None:
        props: LoadBalancedFargateServiceAppletProps = {"image": image}

        if certificate is not None:
            props["certificate"] = certificate

        if container_port is not None:
            props["containerPort"] = container_port

        if cpu is not None:
            props["cpu"] = cpu

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if domain_name is not None:
            props["domainName"] = domain_name

        if domain_zone is not None:
            props["domainZone"] = domain_zone

        if environment is not None:
            props["environment"] = environment

        if memory_mi_b is not None:
            props["memoryMiB"] = memory_mi_b

        if public_load_balancer is not None:
            props["publicLoadBalancer"] = public_load_balancer

        if public_tasks is not None:
            props["publicTasks"] = public_tasks

        if auto_deploy is not None:
            props["autoDeploy"] = auto_deploy

        if env is not None:
            props["env"] = env

        if naming_scheme is not None:
            props["namingScheme"] = naming_scheme

        if stack_name is not None:
            props["stackName"] = stack_name

        jsii.create(LoadBalancedFargateServiceApplet, self, [scope, id, props])


class _LoadBalancedFargateServiceAppletProps(aws_cdk.cdk.StackProps, jsii.compat.TypedDict, total=False):
    certificate: str
    containerPort: jsii.Number
    cpu: str
    desiredCount: jsii.Number
    domainName: str
    domainZone: str
    environment: typing.Mapping[str,str]
    memoryMiB: str
    publicLoadBalancer: bool
    publicTasks: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LoadBalancedFargateServiceAppletProps")
class LoadBalancedFargateServiceAppletProps(_LoadBalancedFargateServiceAppletProps):
    image: str

class LoadBalancedServiceBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.LoadBalancedServiceBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _LoadBalancedServiceBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster: "ICluster", image: "ContainerImage", certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None) -> None:
        props: LoadBalancedServiceBaseProps = {"cluster": cluster, "image": image}

        if certificate is not None:
            props["certificate"] = certificate

        if container_port is not None:
            props["containerPort"] = container_port

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if environment is not None:
            props["environment"] = environment

        if load_balancer_type is not None:
            props["loadBalancerType"] = load_balancer_type

        if public_load_balancer is not None:
            props["publicLoadBalancer"] = public_load_balancer

        jsii.create(LoadBalancedServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(self, service: "BaseService") -> None:
        return jsii.invoke(self, "addServiceAsTarget", [service])

    @property
    @jsii.member(jsii_name="listener")
    def listener(self) -> typing.Union[aws_cdk.aws_elasticloadbalancingv2.ApplicationListener, aws_cdk.aws_elasticloadbalancingv2.NetworkListener]:
        return jsii.get(self, "listener")

    @property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> aws_cdk.aws_elasticloadbalancingv2.BaseLoadBalancer:
        return jsii.get(self, "loadBalancer")

    @property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> "LoadBalancerType":
        return jsii.get(self, "loadBalancerType")

    @property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> typing.Union[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup, aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup]:
        return jsii.get(self, "targetGroup")


class _LoadBalancedServiceBaseProxy(LoadBalancedServiceBase):
    pass

class LoadBalancedEc2Service(LoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.LoadBalancedEc2Service"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None, cluster: "ICluster", image: "ContainerImage", certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None) -> None:
        props: LoadBalancedEc2ServiceProps = {"cluster": cluster, "image": image}

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        if certificate is not None:
            props["certificate"] = certificate

        if container_port is not None:
            props["containerPort"] = container_port

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if environment is not None:
            props["environment"] = environment

        if load_balancer_type is not None:
            props["loadBalancerType"] = load_balancer_type

        if public_load_balancer is not None:
            props["publicLoadBalancer"] = public_load_balancer

        jsii.create(LoadBalancedEc2Service, self, [scope, id, props])


class LoadBalancedFargateService(LoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.LoadBalancedFargateService"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cpu: typing.Optional[str]=None, create_logs: typing.Optional[bool]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, memory_mi_b: typing.Optional[str]=None, public_tasks: typing.Optional[bool]=None, cluster: "ICluster", image: "ContainerImage", certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None) -> None:
        props: LoadBalancedFargateServiceProps = {"cluster": cluster, "image": image}

        if cpu is not None:
            props["cpu"] = cpu

        if create_logs is not None:
            props["createLogs"] = create_logs

        if domain_name is not None:
            props["domainName"] = domain_name

        if domain_zone is not None:
            props["domainZone"] = domain_zone

        if memory_mi_b is not None:
            props["memoryMiB"] = memory_mi_b

        if public_tasks is not None:
            props["publicTasks"] = public_tasks

        if certificate is not None:
            props["certificate"] = certificate

        if container_port is not None:
            props["containerPort"] = container_port

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if environment is not None:
            props["environment"] = environment

        if load_balancer_type is not None:
            props["loadBalancerType"] = load_balancer_type

        if public_load_balancer is not None:
            props["publicLoadBalancer"] = public_load_balancer

        jsii.create(LoadBalancedFargateService, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "FargateService":
        return jsii.get(self, "service")


class _LoadBalancedServiceBaseProps(jsii.compat.TypedDict, total=False):
    certificate: aws_cdk.aws_certificatemanager.ICertificate
    containerPort: jsii.Number
    desiredCount: jsii.Number
    environment: typing.Mapping[str,str]
    loadBalancerType: "LoadBalancerType"
    publicLoadBalancer: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LoadBalancedServiceBaseProps")
class LoadBalancedServiceBaseProps(_LoadBalancedServiceBaseProps):
    cluster: "ICluster"
    image: "ContainerImage"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LoadBalancedEc2ServiceProps")
class LoadBalancedEc2ServiceProps(LoadBalancedServiceBaseProps, jsii.compat.TypedDict, total=False):
    memoryLimitMiB: jsii.Number
    memoryReservationMiB: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LoadBalancedFargateServiceProps")
class LoadBalancedFargateServiceProps(LoadBalancedServiceBaseProps, jsii.compat.TypedDict, total=False):
    cpu: str
    createLogs: bool
    domainName: str
    domainZone: aws_cdk.aws_route53.IHostedZone
    memoryMiB: str
    publicTasks: bool

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.LoadBalancerType")
class LoadBalancerType(enum.Enum):
    Application = "Application"
    Network = "Network"

class LogDriver(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.LogDriver"):
    @staticmethod
    def __jsii_proxy_class__():
        return _LogDriverProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(LogDriver, self, [scope, id])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, container_definition: "ContainerDefinition") -> None:
        ...

    @jsii.member(jsii_name="renderLogDriver")
    @abc.abstractmethod
    def render_log_driver(self) -> "CfnTaskDefinition.LogConfigurationProperty":
        ...


class _LogDriverProxy(LogDriver):
    @jsii.member(jsii_name="bind")
    def bind(self, container_definition: "ContainerDefinition") -> None:
        return jsii.invoke(self, "bind", [container_definition])

    @jsii.member(jsii_name="renderLogDriver")
    def render_log_driver(self) -> "CfnTaskDefinition.LogConfigurationProperty":
        return jsii.invoke(self, "renderLogDriver", [])


class AwsLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.AwsLogDriver"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup]=None, multiline_pattern: typing.Optional[str]=None) -> None:
        props: AwsLogDriverProps = {"streamPrefix": stream_prefix}

        if datetime_format is not None:
            props["datetimeFormat"] = datetime_format

        if log_group is not None:
            props["logGroup"] = log_group

        if multiline_pattern is not None:
            props["multilinePattern"] = multiline_pattern

        jsii.create(AwsLogDriver, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(self, container_definition: "ContainerDefinition") -> None:
        return jsii.invoke(self, "bind", [container_definition])

    @jsii.member(jsii_name="renderLogDriver")
    def render_log_driver(self) -> "CfnTaskDefinition.LogConfigurationProperty":
        return jsii.invoke(self, "renderLogDriver", [])

    @property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> aws_cdk.aws_logs.ILogGroup:
        return jsii.get(self, "logGroup")

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "AwsLogDriverProps":
        return jsii.get(self, "props")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.MemoryUtilizationScalingProps")
class MemoryUtilizationScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    targetUtilizationPercent: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.MountPoint")
class MountPoint(jsii.compat.TypedDict):
    containerPath: str
    readOnly: bool
    sourceVolume: str

class _NamespaceOptions(jsii.compat.TypedDict, total=False):
    type: "NamespaceType"
    vpc: aws_cdk.aws_ec2.IVpcNetwork

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.NamespaceOptions")
class NamespaceOptions(_NamespaceOptions):
    name: str

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.NamespaceType")
class NamespaceType(enum.Enum):
    PrivateDns = "PrivateDns"
    PublicDns = "PublicDns"

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.NetworkMode")
class NetworkMode(enum.Enum):
    None_ = "None"
    Bridge = "Bridge"
    AwsVpc = "AwsVpc"
    Host = "Host"

class _PlacementConstraint(jsii.compat.TypedDict, total=False):
    expression: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.PlacementConstraint")
class PlacementConstraint(_PlacementConstraint):
    type: "PlacementConstraintType"

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.PlacementConstraintType")
class PlacementConstraintType(enum.Enum):
    DistinctInstance = "DistinctInstance"
    MemberOf = "MemberOf"

class _PortMapping(jsii.compat.TypedDict, total=False):
    hostPort: jsii.Number
    protocol: "Protocol"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.PortMapping")
class PortMapping(_PortMapping):
    containerPort: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Protocol")
class Protocol(enum.Enum):
    Tcp = "Tcp"
    Udp = "Udp"

class RepositoryImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.RepositoryImage"):
    def __init__(self, image_name: str, *, credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None) -> None:
        props: RepositoryImageProps = {}

        if credentials is not None:
            props["credentials"] = credentials

        jsii.create(RepositoryImage, self, [image_name, props])

    @jsii.member(jsii_name="bind")
    def bind(self, container_definition: "ContainerDefinition") -> None:
        return jsii.invoke(self, "bind", [container_definition])

    @jsii.member(jsii_name="toRepositoryCredentialsJson")
    def to_repository_credentials_json(self) -> typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]:
        return jsii.invoke(self, "toRepositoryCredentialsJson", [])

    @property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> str:
        return jsii.get(self, "imageName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.RepositoryImageProps")
class RepositoryImageProps(jsii.compat.TypedDict, total=False):
    credentials: aws_cdk.aws_secretsmanager.ISecret

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.RequestCountScalingProps")
class RequestCountScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    requestsPerTarget: jsii.Number
    targetGroup: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup

class ScalableTaskCount(aws_cdk.aws_applicationautoscaling.BaseScalableAttribute, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.ScalableTaskCount"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dimension: str, resource_id: str, role: aws_cdk.aws_iam.IRole, service_namespace: aws_cdk.aws_applicationautoscaling.ServiceNamespace, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> None:
        props: aws_cdk.aws_applicationautoscaling.BaseScalableAttributeProps = {"dimension": dimension, "resourceId": resource_id, "role": role, "serviceNamespace": service_namespace, "maxCapacity": max_capacity}

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        jsii.create(ScalableTaskCount, self, [scope, id, props])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        props: CpuUtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnMemoryUtilization")
    def scale_on_memory_utilization(self, id: str, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        props: MemoryUtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "scaleOnMemoryUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval], adjustment_type: typing.Optional[aws_cdk.aws_applicationautoscaling.AdjustmentType]=None, cooldown_sec: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        props: aws_cdk.aws_applicationautoscaling.BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnRequestCount")
    def scale_on_request_count(self, id: str, *, requests_per_target: jsii.Number, target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        props: RequestCountScalingProps = {"requestsPerTarget": requests_per_target, "targetGroup": target_group}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "scaleOnRequestCount", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        props: aws_cdk.aws_applicationautoscaling.ScalingSchedule = {"schedule": schedule}

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackCustomMetric")
    def scale_to_track_custom_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, target_value: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        props: TrackCustomMetricProps = {"metric": metric, "targetValue": target_value}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "scaleToTrackCustomMetric", [id, props])


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Scope")
class Scope(enum.Enum):
    Task = "Task"
    Shared = "Shared"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ScratchSpace")
class ScratchSpace(jsii.compat.TypedDict):
    containerPath: str
    name: str
    readOnly: bool
    sourcePath: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ServiceDiscoveryOptions")
class ServiceDiscoveryOptions(jsii.compat.TypedDict, total=False):
    dnsRecordType: aws_cdk.aws_servicediscovery.DnsRecordType
    dnsTtlSec: jsii.Number
    failureThreshold: jsii.Number
    name: str

class _ServiceRegistry(jsii.compat.TypedDict, total=False):
    containerName: str
    containerPort: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ServiceRegistry")
class ServiceRegistry(_ServiceRegistry):
    arn: str

class TaskDefinition(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.TaskDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, compatibility: "Compatibility", cpu: typing.Optional[str]=None, memory_mi_b: typing.Optional[str]=None, network_mode: typing.Optional["NetworkMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        props: TaskDefinitionProps = {"compatibility": compatibility}

        if cpu is not None:
            props["cpu"] = cpu

        if memory_mi_b is not None:
            props["memoryMiB"] = memory_mi_b

        if network_mode is not None:
            props["networkMode"] = network_mode

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if execution_role is not None:
            props["executionRole"] = execution_role

        if family is not None:
            props["family"] = family

        if task_role is not None:
            props["taskRole"] = task_role

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(TaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="addContainer")
    def add_container(self, id: str, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str,str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str,str]]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> "ContainerDefinition":
        props: ContainerDefinitionOptions = {"image": image}

        if command is not None:
            props["command"] = command

        if cpu is not None:
            props["cpu"] = cpu

        if disable_networking is not None:
            props["disableNetworking"] = disable_networking

        if dns_search_domains is not None:
            props["dnsSearchDomains"] = dns_search_domains

        if dns_servers is not None:
            props["dnsServers"] = dns_servers

        if docker_labels is not None:
            props["dockerLabels"] = docker_labels

        if docker_security_options is not None:
            props["dockerSecurityOptions"] = docker_security_options

        if entry_point is not None:
            props["entryPoint"] = entry_point

        if environment is not None:
            props["environment"] = environment

        if essential is not None:
            props["essential"] = essential

        if extra_hosts is not None:
            props["extraHosts"] = extra_hosts

        if health_check is not None:
            props["healthCheck"] = health_check

        if hostname is not None:
            props["hostname"] = hostname

        if logging is not None:
            props["logging"] = logging

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        if privileged is not None:
            props["privileged"] = privileged

        if readonly_root_filesystem is not None:
            props["readonlyRootFilesystem"] = readonly_root_filesystem

        if user is not None:
            props["user"] = user

        if working_directory is not None:
            props["workingDirectory"] = working_directory

        return jsii.invoke(self, "addContainer", [id, props])

    @jsii.member(jsii_name="addExtension")
    def add_extension(self, extension: "ITaskDefinitionExtension") -> None:
        return jsii.invoke(self, "addExtension", [extension])

    @jsii.member(jsii_name="addPlacementConstraint")
    def add_placement_constraint(self, *, type: "PlacementConstraintType", expression: typing.Optional[str]=None) -> None:
        constraint: PlacementConstraint = {"type": type}

        if expression is not None:
            constraint["expression"] = expression

        return jsii.invoke(self, "addPlacementConstraint", [constraint])

    @jsii.member(jsii_name="addToExecutionRolePolicy")
    def add_to_execution_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToExecutionRolePolicy", [statement])

    @jsii.member(jsii_name="addToTaskRolePolicy")
    def add_to_task_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToTaskRolePolicy", [statement])

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, *, name: str, docker_volume_configuration: typing.Optional["DockerVolumeConfiguration"]=None, host: typing.Optional["Host"]=None) -> None:
        volume: Volume = {"name": name}

        if docker_volume_configuration is not None:
            volume["dockerVolumeConfiguration"] = docker_volume_configuration

        if host is not None:
            volume["host"] = host

        return jsii.invoke(self, "addVolume", [volume])

    @jsii.member(jsii_name="obtainExecutionRole")
    def obtain_execution_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.invoke(self, "obtainExecutionRole", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="containers")
    def _containers(self) -> typing.List["ContainerDefinition"]:
        return jsii.get(self, "containers")

    @property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        return jsii.get(self, "family")

    @property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> "NetworkMode":
        return jsii.get(self, "networkMode")

    @property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        return jsii.get(self, "taskDefinitionArn")

    @property
    @jsii.member(jsii_name="taskRole")
    def task_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "taskRole")

    @property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        return jsii.get(self, "compatibility")

    @compatibility.setter
    def compatibility(self, value: "Compatibility"):
        return jsii.set(self, "compatibility", value)

    @property
    @jsii.member(jsii_name="defaultContainer")
    def default_container(self) -> typing.Optional["ContainerDefinition"]:
        return jsii.get(self, "defaultContainer")

    @default_container.setter
    def default_container(self, value: typing.Optional["ContainerDefinition"]):
        return jsii.set(self, "defaultContainer", value)

    @property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "executionRole")

    @execution_role.setter
    def execution_role(self, value: typing.Optional[aws_cdk.aws_iam.IRole]):
        return jsii.set(self, "executionRole", value)


class Ec2TaskDefinition(TaskDefinition, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Ec2TaskDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, network_mode: typing.Optional["NetworkMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        props: Ec2TaskDefinitionProps = {}

        if network_mode is not None:
            props["networkMode"] = network_mode

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if execution_role is not None:
            props["executionRole"] = execution_role

        if family is not None:
            props["family"] = family

        if task_role is not None:
            props["taskRole"] = task_role

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(Ec2TaskDefinition, self, [scope, id, props])


class FargateTaskDefinition(TaskDefinition, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.FargateTaskDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cpu: typing.Optional[str]=None, memory_mi_b: typing.Optional[str]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        props: FargateTaskDefinitionProps = {}

        if cpu is not None:
            props["cpu"] = cpu

        if memory_mi_b is not None:
            props["memoryMiB"] = memory_mi_b

        if execution_role is not None:
            props["executionRole"] = execution_role

        if family is not None:
            props["family"] = family

        if task_role is not None:
            props["taskRole"] = task_role

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(FargateTaskDefinition, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> "NetworkMode":
        return jsii.get(self, "networkMode")


class _TaskDefinitionProps(CommonTaskDefinitionProps, jsii.compat.TypedDict, total=False):
    cpu: str
    memoryMiB: str
    networkMode: "NetworkMode"
    placementConstraints: typing.List["PlacementConstraint"]

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.TaskDefinitionProps")
class TaskDefinitionProps(_TaskDefinitionProps):
    compatibility: "Compatibility"

class _Tmpfs(jsii.compat.TypedDict, total=False):
    mountOptions: typing.List["TmpfsMountOption"]

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Tmpfs")
class Tmpfs(_Tmpfs):
    containerPath: str
    size: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.TmpfsMountOption")
class TmpfsMountOption(enum.Enum):
    Defaults = "Defaults"
    Ro = "Ro"
    Rw = "Rw"
    Suid = "Suid"
    Nosuid = "Nosuid"
    Dev = "Dev"
    Nodev = "Nodev"
    Exec = "Exec"
    Noexec = "Noexec"
    Sync = "Sync"
    Async = "Async"
    Dirsync = "Dirsync"
    Remount = "Remount"
    Mand = "Mand"
    Nomand = "Nomand"
    Atime = "Atime"
    Noatime = "Noatime"
    Diratime = "Diratime"
    Nodiratime = "Nodiratime"
    Bind = "Bind"
    Rbind = "Rbind"
    Unbindable = "Unbindable"
    Runbindable = "Runbindable"
    Private = "Private"
    Rprivate = "Rprivate"
    Shared = "Shared"
    Rshared = "Rshared"
    Slave = "Slave"
    Rslave = "Rslave"
    Relatime = "Relatime"
    Norelatime = "Norelatime"
    Strictatime = "Strictatime"
    Nostrictatime = "Nostrictatime"
    Mode = "Mode"
    Uid = "Uid"
    Gid = "Gid"
    NrInodes = "NrInodes"
    NrBlocks = "NrBlocks"
    Mpol = "Mpol"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.TrackCustomMetricProps")
class TrackCustomMetricProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    metric: aws_cdk.aws_cloudwatch.Metric
    targetValue: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ulimit")
class Ulimit(jsii.compat.TypedDict):
    hardLimit: jsii.Number
    name: "UlimitName"
    softLimit: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.UlimitName")
class UlimitName(enum.Enum):
    Core = "Core"
    Cpu = "Cpu"
    Data = "Data"
    Fsize = "Fsize"
    Locks = "Locks"
    Memlock = "Memlock"
    Msgqueue = "Msgqueue"
    Nice = "Nice"
    Nofile = "Nofile"
    Nproc = "Nproc"
    Rss = "Rss"
    Rtprio = "Rtprio"
    Rttime = "Rttime"
    Sigpending = "Sigpending"
    Stack = "Stack"

class _Volume(jsii.compat.TypedDict, total=False):
    dockerVolumeConfiguration: "DockerVolumeConfiguration"
    host: "Host"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Volume")
class Volume(_Volume):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.VolumeFrom")
class VolumeFrom(jsii.compat.TypedDict):
    readOnly: bool
    sourceContainer: str

__all__ = ["AddAutoScalingGroupCapacityOptions", "AddCapacityOptions", "AssetImage", "AssetImageProps", "AwsLogDriver", "AwsLogDriverProps", "BaseService", "BaseServiceProps", "BinPackResource", "BuiltInAttributes", "Capability", "CfnCluster", "CfnClusterProps", "CfnService", "CfnServiceProps", "CfnTaskDefinition", "CfnTaskDefinitionProps", "Cluster", "ClusterImportProps", "ClusterProps", "CommonTaskDefinitionProps", "Compatibility", "ContainerDefinition", "ContainerDefinitionOptions", "ContainerDefinitionProps", "ContainerImage", "CpuUtilizationScalingProps", "Device", "DevicePermission", "DockerVolumeConfiguration", "Ec2EventRuleTarget", "Ec2EventRuleTargetProps", "Ec2Service", "Ec2ServiceProps", "Ec2TaskDefinition", "Ec2TaskDefinitionProps", "EcrImage", "EcsOptimizedAmi", "EcsOptimizedAmiProps", "FargatePlatformVersion", "FargateService", "FargateServiceProps", "FargateTaskDefinition", "FargateTaskDefinitionProps", "HealthCheck", "Host", "ICluster", "ITaskDefinitionExtension", "LinuxParameters", "LoadBalancedEc2Service", "LoadBalancedEc2ServiceProps", "LoadBalancedFargateService", "LoadBalancedFargateServiceApplet", "LoadBalancedFargateServiceAppletProps", "LoadBalancedFargateServiceProps", "LoadBalancedServiceBase", "LoadBalancedServiceBaseProps", "LoadBalancerType", "LogDriver", "MemoryUtilizationScalingProps", "MountPoint", "NamespaceOptions", "NamespaceType", "NetworkMode", "PlacementConstraint", "PlacementConstraintType", "PortMapping", "Protocol", "RepositoryImage", "RepositoryImageProps", "RequestCountScalingProps", "ScalableTaskCount", "Scope", "ScratchSpace", "ServiceDiscoveryOptions", "ServiceRegistry", "TaskDefinition", "TaskDefinitionProps", "Tmpfs", "TmpfsMountOption", "TrackCustomMetricProps", "Ulimit", "UlimitName", "Volume", "VolumeFrom", "__jsii_assembly__"]

publication.publish()
