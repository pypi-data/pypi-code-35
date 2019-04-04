import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-iot1click", "0.28.0", __name__, "aws-iot1click@0.28.0.jsii.tgz")
class CfnDevice(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot1click.CfnDevice"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, device_id: str, enabled: typing.Union[bool, aws_cdk.cdk.Token]) -> None:
        props: CfnDeviceProps = {"deviceId": device_id, "enabled": enabled}

        jsii.create(CfnDevice, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deviceArn")
    def device_arn(self) -> str:
        return jsii.get(self, "deviceArn")

    @property
    @jsii.member(jsii_name="deviceEnabled")
    def device_enabled(self) -> aws_cdk.cdk.Token:
        return jsii.get(self, "deviceEnabled")

    @property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> str:
        return jsii.get(self, "deviceId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeviceProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-iot1click.CfnDeviceProps")
class CfnDeviceProps(jsii.compat.TypedDict):
    deviceId: str
    enabled: typing.Union[bool, aws_cdk.cdk.Token]

class CfnPlacement(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot1click.CfnPlacement"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, project_name: str, associated_devices: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, attributes: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, placement_name: typing.Optional[str]=None) -> None:
        props: CfnPlacementProps = {"projectName": project_name}

        if associated_devices is not None:
            props["associatedDevices"] = associated_devices

        if attributes is not None:
            props["attributes"] = attributes

        if placement_name is not None:
            props["placementName"] = placement_name

        jsii.create(CfnPlacement, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="placementName")
    def placement_name(self) -> str:
        return jsii.get(self, "placementName")

    @property
    @jsii.member(jsii_name="placementPath")
    def placement_path(self) -> str:
        return jsii.get(self, "placementPath")

    @property
    @jsii.member(jsii_name="placementProjectName")
    def placement_project_name(self) -> str:
        return jsii.get(self, "placementProjectName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPlacementProps":
        return jsii.get(self, "propertyOverrides")


class _CfnPlacementProps(jsii.compat.TypedDict, total=False):
    associatedDevices: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    attributes: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    placementName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iot1click.CfnPlacementProps")
class CfnPlacementProps(_CfnPlacementProps):
    projectName: str

class CfnProject(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot1click.CfnProject"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, placement_template: typing.Union[aws_cdk.cdk.Token, "PlacementTemplateProperty"], description: typing.Optional[str]=None, project_name: typing.Optional[str]=None) -> None:
        props: CfnProjectProps = {"placementTemplate": placement_template}

        if description is not None:
            props["description"] = description

        if project_name is not None:
            props["projectName"] = project_name

        jsii.create(CfnProject, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        return jsii.get(self, "projectArn")

    @property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        return jsii.get(self, "projectName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnProjectProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot1click.CfnProject.DeviceTemplateProperty")
    class DeviceTemplateProperty(jsii.compat.TypedDict, total=False):
        callbackOverrides: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        deviceType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot1click.CfnProject.PlacementTemplateProperty")
    class PlacementTemplateProperty(jsii.compat.TypedDict, total=False):
        defaultAttributes: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        deviceTemplates: typing.Union[aws_cdk.cdk.Token, "CfnProject.DeviceTemplateProperty"]


class _CfnProjectProps(jsii.compat.TypedDict, total=False):
    description: str
    projectName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iot1click.CfnProjectProps")
class CfnProjectProps(_CfnProjectProps):
    placementTemplate: typing.Union[aws_cdk.cdk.Token, "CfnProject.PlacementTemplateProperty"]

__all__ = ["CfnDevice", "CfnDeviceProps", "CfnPlacement", "CfnPlacementProps", "CfnProject", "CfnProjectProps", "__jsii_assembly__"]

publication.publish()
