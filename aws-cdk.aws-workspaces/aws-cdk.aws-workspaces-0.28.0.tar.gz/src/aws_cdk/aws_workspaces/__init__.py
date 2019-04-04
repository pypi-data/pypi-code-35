import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-workspaces", "0.28.0", __name__, "aws-workspaces@0.28.0.jsii.tgz")
class CfnWorkspace(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-workspaces.CfnWorkspace"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, bundle_id: str, directory_id: str, user_name: str, root_volume_encryption_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, user_volume_encryption_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, volume_encryption_key: typing.Optional[str]=None, workspace_properties: typing.Optional[typing.Union[aws_cdk.cdk.Token, "WorkspacePropertiesProperty"]]=None) -> None:
        props: CfnWorkspaceProps = {"bundleId": bundle_id, "directoryId": directory_id, "userName": user_name}

        if root_volume_encryption_enabled is not None:
            props["rootVolumeEncryptionEnabled"] = root_volume_encryption_enabled

        if tags is not None:
            props["tags"] = tags

        if user_volume_encryption_enabled is not None:
            props["userVolumeEncryptionEnabled"] = user_volume_encryption_enabled

        if volume_encryption_key is not None:
            props["volumeEncryptionKey"] = volume_encryption_key

        if workspace_properties is not None:
            props["workspaceProperties"] = workspace_properties

        jsii.create(CfnWorkspace, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnWorkspaceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="workspaceName")
    def workspace_name(self) -> str:
        return jsii.get(self, "workspaceName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-workspaces.CfnWorkspace.WorkspacePropertiesProperty")
    class WorkspacePropertiesProperty(jsii.compat.TypedDict, total=False):
        computeTypeName: str
        rootVolumeSizeGib: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        runningMode: str
        runningModeAutoStopTimeoutInMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        userVolumeSizeGib: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnWorkspaceProps(jsii.compat.TypedDict, total=False):
    rootVolumeEncryptionEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    userVolumeEncryptionEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    volumeEncryptionKey: str
    workspaceProperties: typing.Union[aws_cdk.cdk.Token, "CfnWorkspace.WorkspacePropertiesProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-workspaces.CfnWorkspaceProps")
class CfnWorkspaceProps(_CfnWorkspaceProps):
    bundleId: str
    directoryId: str
    userName: str

__all__ = ["CfnWorkspace", "CfnWorkspaceProps", "__jsii_assembly__"]

publication.publish()
