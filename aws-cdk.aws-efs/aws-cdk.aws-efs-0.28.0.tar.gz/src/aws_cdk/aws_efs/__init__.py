import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-efs", "0.28.0", __name__, "aws-efs@0.28.0.jsii.tgz")
class CfnFileSystem(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-efs.CfnFileSystem"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, encrypted: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, file_system_tags: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ElasticFileSystemTagProperty"]]]]=None, kms_key_id: typing.Optional[str]=None, performance_mode: typing.Optional[str]=None, provisioned_throughput_in_mibps: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, throughput_mode: typing.Optional[str]=None) -> None:
        props: CfnFileSystemProps = {}

        if encrypted is not None:
            props["encrypted"] = encrypted

        if file_system_tags is not None:
            props["fileSystemTags"] = file_system_tags

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if performance_mode is not None:
            props["performanceMode"] = performance_mode

        if provisioned_throughput_in_mibps is not None:
            props["provisionedThroughputInMibps"] = provisioned_throughput_in_mibps

        if throughput_mode is not None:
            props["throughputMode"] = throughput_mode

        jsii.create(CfnFileSystem, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        return jsii.get(self, "fileSystemId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFileSystemProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnFileSystem.ElasticFileSystemTagProperty")
    class ElasticFileSystemTagProperty(jsii.compat.TypedDict):
        key: str
        value: str


@jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnFileSystemProps")
class CfnFileSystemProps(jsii.compat.TypedDict, total=False):
    encrypted: typing.Union[bool, aws_cdk.cdk.Token]
    fileSystemTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnFileSystem.ElasticFileSystemTagProperty"]]]
    kmsKeyId: str
    performanceMode: str
    provisionedThroughputInMibps: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    throughputMode: str

class CfnMountTarget(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-efs.CfnMountTarget"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, file_system_id: str, security_groups: typing.List[str], subnet_id: str, ip_address: typing.Optional[str]=None) -> None:
        props: CfnMountTargetProps = {"fileSystemId": file_system_id, "securityGroups": security_groups, "subnetId": subnet_id}

        if ip_address is not None:
            props["ipAddress"] = ip_address

        jsii.create(CfnMountTarget, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="mountTargetId")
    def mount_target_id(self) -> str:
        return jsii.get(self, "mountTargetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMountTargetProps":
        return jsii.get(self, "propertyOverrides")


class _CfnMountTargetProps(jsii.compat.TypedDict, total=False):
    ipAddress: str

@jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnMountTargetProps")
class CfnMountTargetProps(_CfnMountTargetProps):
    fileSystemId: str
    securityGroups: typing.List[str]
    subnetId: str

__all__ = ["CfnFileSystem", "CfnFileSystemProps", "CfnMountTarget", "CfnMountTargetProps", "__jsii_assembly__"]

publication.publish()
