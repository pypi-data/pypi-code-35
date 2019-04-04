import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-dax", "0.28.0", __name__, "aws-dax@0.28.0.jsii.tgz")
class CfnCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dax.CfnCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, iam_role_arn: str, node_type: str, replication_factor: typing.Union[jsii.Number, aws_cdk.cdk.Token], availability_zones: typing.Optional[typing.List[str]]=None, cluster_name: typing.Optional[str]=None, description: typing.Optional[str]=None, notification_topic_arn: typing.Optional[str]=None, parameter_group_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, sse_specification: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SSESpecificationProperty"]]=None, subnet_group_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[typing.Any, typing.Any]]=None) -> None:
        props: CfnClusterProps = {"iamRoleArn": iam_role_arn, "nodeType": node_type, "replicationFactor": replication_factor}

        if availability_zones is not None:
            props["availabilityZones"] = availability_zones

        if cluster_name is not None:
            props["clusterName"] = cluster_name

        if description is not None:
            props["description"] = description

        if notification_topic_arn is not None:
            props["notificationTopicArn"] = notification_topic_arn

        if parameter_group_name is not None:
            props["parameterGroupName"] = parameter_group_name

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if sse_specification is not None:
            props["sseSpecification"] = sse_specification

        if subnet_group_name is not None:
            props["subnetGroupName"] = subnet_group_name

        if tags is not None:
            props["tags"] = tags

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
    @jsii.member(jsii_name="clusterDiscoveryEndpoint")
    def cluster_discovery_endpoint(self) -> str:
        return jsii.get(self, "clusterDiscoveryEndpoint")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-dax.CfnCluster.SSESpecificationProperty")
    class SSESpecificationProperty(jsii.compat.TypedDict, total=False):
        sseEnabled: typing.Union[bool, aws_cdk.cdk.Token]


class _CfnClusterProps(jsii.compat.TypedDict, total=False):
    availabilityZones: typing.List[str]
    clusterName: str
    description: str
    notificationTopicArn: str
    parameterGroupName: str
    preferredMaintenanceWindow: str
    securityGroupIds: typing.List[str]
    sseSpecification: typing.Union[aws_cdk.cdk.Token, "CfnCluster.SSESpecificationProperty"]
    subnetGroupName: str
    tags: typing.Mapping[typing.Any, typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/aws-dax.CfnClusterProps")
class CfnClusterProps(_CfnClusterProps):
    iamRoleArn: str
    nodeType: str
    replicationFactor: typing.Union[jsii.Number, aws_cdk.cdk.Token]

class CfnParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dax.CfnParameterGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, parameter_group_name: typing.Optional[str]=None, parameter_name_values: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None) -> None:
        props: CfnParameterGroupProps = {}

        if description is not None:
            props["description"] = description

        if parameter_group_name is not None:
            props["parameterGroupName"] = parameter_group_name

        if parameter_name_values is not None:
            props["parameterNameValues"] = parameter_name_values

        jsii.create(CfnParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="parameterGroupArn")
    def parameter_group_arn(self) -> str:
        return jsii.get(self, "parameterGroupArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnParameterGroupProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-dax.CfnParameterGroupProps")
class CfnParameterGroupProps(jsii.compat.TypedDict, total=False):
    description: str
    parameterGroupName: str
    parameterNameValues: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnSubnetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dax.CfnSubnetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, subnet_ids: typing.List[str], description: typing.Optional[str]=None, subnet_group_name: typing.Optional[str]=None) -> None:
        props: CfnSubnetGroupProps = {"subnetIds": subnet_ids}

        if description is not None:
            props["description"] = description

        if subnet_group_name is not None:
            props["subnetGroupName"] = subnet_group_name

        jsii.create(CfnSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubnetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetGroupArn")
    def subnet_group_arn(self) -> str:
        return jsii.get(self, "subnetGroupArn")


class _CfnSubnetGroupProps(jsii.compat.TypedDict, total=False):
    description: str
    subnetGroupName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-dax.CfnSubnetGroupProps")
class CfnSubnetGroupProps(_CfnSubnetGroupProps):
    subnetIds: typing.List[str]

__all__ = ["CfnCluster", "CfnClusterProps", "CfnParameterGroup", "CfnParameterGroupProps", "CfnSubnetGroup", "CfnSubnetGroupProps", "__jsii_assembly__"]

publication.publish()
