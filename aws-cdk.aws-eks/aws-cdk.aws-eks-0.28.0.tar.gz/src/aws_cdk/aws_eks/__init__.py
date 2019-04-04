import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-eks", "0.28.0", __name__, "aws-eks@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-eks.AddAutoScalingGroupOptions")
class AddAutoScalingGroupOptions(jsii.compat.TypedDict):
    maxPods: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-eks.AddWorkerNodesOptions")
class AddWorkerNodesOptions(aws_cdk.aws_autoscaling.CommonAutoScalingGroupProps, jsii.compat.TypedDict):
    instanceType: aws_cdk.aws_ec2.InstanceType

class CfnCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.CfnCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resources_vpc_config: typing.Union["ResourcesVpcConfigProperty", aws_cdk.cdk.Token], role_arn: str, name: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        props: CfnClusterProps = {"resourcesVpcConfig": resources_vpc_config, "roleArn": role_arn}

        if name is not None:
            props["name"] = name

        if version is not None:
            props["version"] = version

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
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        return jsii.get(self, "clusterCertificateAuthorityData")

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterProps":
        return jsii.get(self, "propertyOverrides")

    class _ResourcesVpcConfigProperty(jsii.compat.TypedDict, total=False):
        securityGroupIds: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnCluster.ResourcesVpcConfigProperty")
    class ResourcesVpcConfigProperty(_ResourcesVpcConfigProperty):
        subnetIds: typing.List[str]


class _CfnClusterProps(jsii.compat.TypedDict, total=False):
    name: str
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnClusterProps")
class CfnClusterProps(_CfnClusterProps):
    resourcesVpcConfig: typing.Union["CfnCluster.ResourcesVpcConfigProperty", aws_cdk.cdk.Token]
    roleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-eks.ClusterImportProps")
class ClusterImportProps(jsii.compat.TypedDict):
    clusterArn: str
    clusterCertificateAuthorityData: str
    clusterEndpoint: str
    clusterName: str
    securityGroups: typing.List[aws_cdk.aws_ec2.SecurityGroupImportProps]
    vpc: aws_cdk.aws_ec2.VpcNetworkImportProps

class _ClusterProps(jsii.compat.TypedDict, total=False):
    clusterName: str
    role: aws_cdk.aws_iam.IRole
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    version: str
    vpcSubnets: typing.List[aws_cdk.aws_ec2.SubnetSelection]

@jsii.data_type(jsii_type="@aws-cdk/aws-eks.ClusterProps")
class ClusterProps(_ClusterProps):
    vpc: aws_cdk.aws_ec2.IVpcNetwork

@jsii.implements(aws_cdk.aws_ec2.IMachineImageSource)
class EksOptimizedAmi(aws_cdk.aws_ec2.GenericLinuxImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.EksOptimizedAmi"):
    def __init__(self, *, kubernetes_version: typing.Optional[str]=None, node_type: typing.Optional["NodeType"]=None) -> None:
        props: EksOptimizedAmiProps = {}

        if kubernetes_version is not None:
            props["kubernetesVersion"] = kubernetes_version

        if node_type is not None:
            props["nodeType"] = node_type

        jsii.create(EksOptimizedAmi, self, [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.EksOptimizedAmiProps")
class EksOptimizedAmiProps(jsii.compat.TypedDict, total=False):
    kubernetesVersion: str
    nodeType: "NodeType"

@jsii.interface(jsii_type="@aws-cdk/aws-eks.ICluster")
class ICluster(aws_cdk.cdk.IConstruct, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpcNetwork:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterImportProps":
        ...


class _IClusterProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    __jsii_type__ = "@aws-cdk/aws-eks.ICluster"
    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        return jsii.get(self, "clusterCertificateAuthorityData")

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpcNetwork:
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterImportProps":
        return jsii.invoke(self, "export", [])


@jsii.implements(ICluster)
class ClusterBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-eks.ClusterBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ClusterBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(ClusterBase, self, [scope, id])

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="clusterArn")
    @abc.abstractmethod
    def cluster_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    @abc.abstractmethod
    def cluster_certificate_authority_data(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    @abc.abstractmethod
    def cluster_endpoint(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="clusterName")
    @abc.abstractmethod
    def cluster_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="connections")
    @abc.abstractmethod
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        ...

    @property
    @jsii.member(jsii_name="vpc")
    @abc.abstractmethod
    def vpc(self) -> aws_cdk.aws_ec2.IVpcNetwork:
        ...


class _ClusterBaseProxy(ClusterBase):
    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        return jsii.get(self, "clusterCertificateAuthorityData")

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpcNetwork:
        return jsii.get(self, "vpc")


class Cluster(ClusterBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.Cluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpcNetwork, cluster_name: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, version: typing.Optional[str]=None, vpc_subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]=None) -> None:
        props: ClusterProps = {"vpc": vpc}

        if cluster_name is not None:
            props["clusterName"] = cluster_name

        if role is not None:
            props["role"] = role

        if security_group is not None:
            props["securityGroup"] = security_group

        if version is not None:
            props["version"] = version

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, cluster_arn: str, cluster_certificate_authority_data: str, cluster_endpoint: str, cluster_name: str, security_groups: typing.List[aws_cdk.aws_ec2.SecurityGroupImportProps], vpc: aws_cdk.aws_ec2.VpcNetworkImportProps) -> "ICluster":
        props: ClusterImportProps = {"clusterArn": cluster_arn, "clusterCertificateAuthorityData": cluster_certificate_authority_data, "clusterEndpoint": cluster_endpoint, "clusterName": cluster_name, "securityGroups": security_groups, "vpc": vpc}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, auto_scaling_group: aws_cdk.aws_autoscaling.AutoScalingGroup, *, max_pods: jsii.Number) -> None:
        options: AddAutoScalingGroupOptions = {"maxPods": max_pods}

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(self, id: str, *, instance_type: aws_cdk.aws_ec2.InstanceType, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, desired_capacity: typing.Optional[jsii.Number]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout_sec: typing.Optional[jsii.Number]=None, rolling_update_configuration: typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]=None, update_type: typing.Optional[aws_cdk.aws_autoscaling.UpdateType]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        options: AddWorkerNodesOptions = {"instanceType": instance_type}

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

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        return jsii.get(self, "clusterCertificateAuthorityData")

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "role")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpcNetwork:
        return jsii.get(self, "vpc")


@jsii.enum(jsii_type="@aws-cdk/aws-eks.NodeType")
class NodeType(enum.Enum):
    Normal = "Normal"
    GPU = "GPU"

__all__ = ["AddAutoScalingGroupOptions", "AddWorkerNodesOptions", "CfnCluster", "CfnClusterProps", "Cluster", "ClusterBase", "ClusterImportProps", "ClusterProps", "EksOptimizedAmi", "EksOptimizedAmiProps", "ICluster", "NodeType", "__jsii_assembly__"]

publication.publish()
