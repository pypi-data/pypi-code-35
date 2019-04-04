import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-opsworkscm", "0.28.0", __name__, "aws-opsworkscm@0.28.0.jsii.tgz")
class CfnServer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworkscm.CfnServer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_profile_arn: str, instance_type: str, service_role_arn: str, associate_public_ip_address: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, backup_id: typing.Optional[str]=None, backup_retention_count: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, disable_automated_backup: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, engine: typing.Optional[str]=None, engine_attributes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "EngineAttributeProperty"]]]]=None, engine_model: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, key_pair: typing.Optional[str]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, server_name: typing.Optional[str]=None, subnet_ids: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnServerProps = {"instanceProfileArn": instance_profile_arn, "instanceType": instance_type, "serviceRoleArn": service_role_arn}

        if associate_public_ip_address is not None:
            props["associatePublicIpAddress"] = associate_public_ip_address

        if backup_id is not None:
            props["backupId"] = backup_id

        if backup_retention_count is not None:
            props["backupRetentionCount"] = backup_retention_count

        if disable_automated_backup is not None:
            props["disableAutomatedBackup"] = disable_automated_backup

        if engine is not None:
            props["engine"] = engine

        if engine_attributes is not None:
            props["engineAttributes"] = engine_attributes

        if engine_model is not None:
            props["engineModel"] = engine_model

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if key_pair is not None:
            props["keyPair"] = key_pair

        if preferred_backup_window is not None:
            props["preferredBackupWindow"] = preferred_backup_window

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if server_name is not None:
            props["serverName"] = server_name

        if subnet_ids is not None:
            props["subnetIds"] = subnet_ids

        jsii.create(CfnServer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnServerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="serverArn")
    def server_arn(self) -> str:
        return jsii.get(self, "serverArn")

    @property
    @jsii.member(jsii_name="serverEndpoint")
    def server_endpoint(self) -> str:
        return jsii.get(self, "serverEndpoint")

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworkscm.CfnServer.EngineAttributeProperty")
    class EngineAttributeProperty(jsii.compat.TypedDict, total=False):
        name: str
        value: str


class _CfnServerProps(jsii.compat.TypedDict, total=False):
    associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
    backupId: str
    backupRetentionCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    disableAutomatedBackup: typing.Union[bool, aws_cdk.cdk.Token]
    engine: str
    engineAttributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnServer.EngineAttributeProperty"]]]
    engineModel: str
    engineVersion: str
    keyPair: str
    preferredBackupWindow: str
    preferredMaintenanceWindow: str
    securityGroupIds: typing.List[str]
    serverName: str
    subnetIds: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworkscm.CfnServerProps")
class CfnServerProps(_CfnServerProps):
    instanceProfileArn: str
    instanceType: str
    serviceRoleArn: str

__all__ = ["CfnServer", "CfnServerProps", "__jsii_assembly__"]

publication.publish()
