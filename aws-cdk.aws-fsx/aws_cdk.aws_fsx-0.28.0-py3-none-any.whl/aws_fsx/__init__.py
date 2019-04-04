import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-fsx", "0.28.0", __name__, "aws-fsx@0.28.0.jsii.tgz")
class CfnFileSystem(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-fsx.CfnFileSystem"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, backup_id: typing.Optional[str]=None, file_system_type: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, lustre_configuration: typing.Optional[typing.Union["LustreConfigurationProperty", aws_cdk.cdk.Token]]=None, security_group_ids: typing.Optional[typing.List[str]]=None, storage_capacity: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, subnet_ids: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List["TagEntryProperty"]]=None, windows_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "WindowsConfigurationProperty"]]=None) -> None:
        props: CfnFileSystemProps = {}

        if backup_id is not None:
            props["backupId"] = backup_id

        if file_system_type is not None:
            props["fileSystemType"] = file_system_type

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if lustre_configuration is not None:
            props["lustreConfiguration"] = lustre_configuration

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if storage_capacity is not None:
            props["storageCapacity"] = storage_capacity

        if subnet_ids is not None:
            props["subnetIds"] = subnet_ids

        if tags is not None:
            props["tags"] = tags

        if windows_configuration is not None:
            props["windowsConfiguration"] = windows_configuration

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

    @jsii.data_type(jsii_type="@aws-cdk/aws-fsx.CfnFileSystem.LustreConfigurationProperty")
    class LustreConfigurationProperty(jsii.compat.TypedDict, total=False):
        exportPath: str
        importedFileChunkSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        importPath: str
        weeklyMaintenanceStartTime: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-fsx.CfnFileSystem.TagEntryProperty")
    class TagEntryProperty(jsii.compat.TypedDict):
        key: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-fsx.CfnFileSystem.WindowsConfigurationProperty")
    class WindowsConfigurationProperty(jsii.compat.TypedDict, total=False):
        activeDirectoryId: str
        automaticBackupRetentionDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        copyTagsToBackups: typing.Union[bool, aws_cdk.cdk.Token]
        dailyAutomaticBackupStartTime: str
        throughputCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        weeklyMaintenanceStartTime: str


@jsii.data_type(jsii_type="@aws-cdk/aws-fsx.CfnFileSystemProps")
class CfnFileSystemProps(jsii.compat.TypedDict, total=False):
    backupId: str
    fileSystemType: str
    kmsKeyId: str
    lustreConfiguration: typing.Union["CfnFileSystem.LustreConfigurationProperty", aws_cdk.cdk.Token]
    securityGroupIds: typing.List[str]
    storageCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    subnetIds: typing.List[str]
    tags: typing.List["CfnFileSystem.TagEntryProperty"]
    windowsConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnFileSystem.WindowsConfigurationProperty"]

__all__ = ["CfnFileSystem", "CfnFileSystemProps", "__jsii_assembly__"]

publication.publish()
