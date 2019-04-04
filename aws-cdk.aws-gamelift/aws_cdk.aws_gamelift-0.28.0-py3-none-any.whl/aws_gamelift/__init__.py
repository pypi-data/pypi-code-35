import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-gamelift", "0.28.0", __name__, "aws-gamelift@0.28.0.jsii.tgz")
class CfnAlias(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-gamelift.CfnAlias"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, routing_strategy: typing.Union["RoutingStrategyProperty", aws_cdk.cdk.Token], description: typing.Optional[str]=None) -> None:
        props: CfnAliasProps = {"name": name, "routingStrategy": routing_strategy}

        if description is not None:
            props["description"] = description

        jsii.create(CfnAlias, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> str:
        return jsii.get(self, "aliasId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAliasProps":
        return jsii.get(self, "propertyOverrides")

    class _RoutingStrategyProperty(jsii.compat.TypedDict, total=False):
        fleetId: str
        message: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnAlias.RoutingStrategyProperty")
    class RoutingStrategyProperty(_RoutingStrategyProperty):
        type: str


class _CfnAliasProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnAliasProps")
class CfnAliasProps(_CfnAliasProps):
    name: str
    routingStrategy: typing.Union["CfnAlias.RoutingStrategyProperty", aws_cdk.cdk.Token]

class CfnBuild(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-gamelift.CfnBuild"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: typing.Optional[str]=None, storage_location: typing.Optional[typing.Union[aws_cdk.cdk.Token, "S3LocationProperty"]]=None, version: typing.Optional[str]=None) -> None:
        props: CfnBuildProps = {}

        if name is not None:
            props["name"] = name

        if storage_location is not None:
            props["storageLocation"] = storage_location

        if version is not None:
            props["version"] = version

        jsii.create(CfnBuild, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="buildId")
    def build_id(self) -> str:
        return jsii.get(self, "buildId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBuildProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnBuild.S3LocationProperty")
    class S3LocationProperty(jsii.compat.TypedDict):
        bucket: str
        key: str
        roleArn: str


@jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnBuildProps")
class CfnBuildProps(jsii.compat.TypedDict, total=False):
    name: str
    storageLocation: typing.Union[aws_cdk.cdk.Token, "CfnBuild.S3LocationProperty"]
    version: str

class CfnFleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-gamelift.CfnFleet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, build_id: str, desired_ec2_instances: typing.Union[jsii.Number, aws_cdk.cdk.Token], ec2_instance_type: str, name: str, server_launch_path: str, description: typing.Optional[str]=None, ec2_inbound_permissions: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "IpPermissionProperty"]]]]=None, log_paths: typing.Optional[typing.List[str]]=None, max_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, min_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, server_launch_parameters: typing.Optional[str]=None) -> None:
        props: CfnFleetProps = {"buildId": build_id, "desiredEc2Instances": desired_ec2_instances, "ec2InstanceType": ec2_instance_type, "name": name, "serverLaunchPath": server_launch_path}

        if description is not None:
            props["description"] = description

        if ec2_inbound_permissions is not None:
            props["ec2InboundPermissions"] = ec2_inbound_permissions

        if log_paths is not None:
            props["logPaths"] = log_paths

        if max_size is not None:
            props["maxSize"] = max_size

        if min_size is not None:
            props["minSize"] = min_size

        if server_launch_parameters is not None:
            props["serverLaunchParameters"] = server_launch_parameters

        jsii.create(CfnFleet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="fleetId")
    def fleet_id(self) -> str:
        return jsii.get(self, "fleetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFleetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnFleet.IpPermissionProperty")
    class IpPermissionProperty(jsii.compat.TypedDict):
        fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        ipRange: str
        protocol: str
        toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnFleetProps(jsii.compat.TypedDict, total=False):
    description: str
    ec2InboundPermissions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnFleet.IpPermissionProperty"]]]
    logPaths: typing.List[str]
    maxSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    minSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    serverLaunchParameters: str

@jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnFleetProps")
class CfnFleetProps(_CfnFleetProps):
    buildId: str
    desiredEc2Instances: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    ec2InstanceType: str
    name: str
    serverLaunchPath: str

__all__ = ["CfnAlias", "CfnAliasProps", "CfnBuild", "CfnBuildProps", "CfnFleet", "CfnFleetProps", "__jsii_assembly__"]

publication.publish()
