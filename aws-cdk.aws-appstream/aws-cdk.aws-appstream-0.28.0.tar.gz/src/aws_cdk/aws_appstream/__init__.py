import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-appstream", "0.28.0", __name__, "aws-appstream@0.28.0.jsii.tgz")
class CfnDirectoryConfig(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, directory_name: str, organizational_unit_distinguished_names: typing.List[str], service_account_credentials: typing.Union["ServiceAccountCredentialsProperty", aws_cdk.cdk.Token]) -> None:
        props: CfnDirectoryConfigProps = {"directoryName": directory_name, "organizationalUnitDistinguishedNames": organizational_unit_distinguished_names, "serviceAccountCredentials": service_account_credentials}

        jsii.create(CfnDirectoryConfig, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDirectoryConfigProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty")
    class ServiceAccountCredentialsProperty(jsii.compat.TypedDict):
        accountName: str
        accountPassword: str


@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfigProps")
class CfnDirectoryConfigProps(jsii.compat.TypedDict):
    directoryName: str
    organizationalUnitDistinguishedNames: typing.List[str]
    serviceAccountCredentials: typing.Union["CfnDirectoryConfig.ServiceAccountCredentialsProperty", aws_cdk.cdk.Token]

class CfnFleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnFleet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, compute_capacity: typing.Union[aws_cdk.cdk.Token, "ComputeCapacityProperty"], instance_type: str, description: typing.Optional[str]=None, disconnect_timeout_in_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, display_name: typing.Optional[str]=None, domain_join_info: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DomainJoinInfoProperty"]]=None, enable_default_internet_access: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, fleet_type: typing.Optional[str]=None, image_arn: typing.Optional[str]=None, image_name: typing.Optional[str]=None, max_user_duration_in_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "VpcConfigProperty"]]=None) -> None:
        props: CfnFleetProps = {"computeCapacity": compute_capacity, "instanceType": instance_type}

        if description is not None:
            props["description"] = description

        if disconnect_timeout_in_seconds is not None:
            props["disconnectTimeoutInSeconds"] = disconnect_timeout_in_seconds

        if display_name is not None:
            props["displayName"] = display_name

        if domain_join_info is not None:
            props["domainJoinInfo"] = domain_join_info

        if enable_default_internet_access is not None:
            props["enableDefaultInternetAccess"] = enable_default_internet_access

        if fleet_type is not None:
            props["fleetType"] = fleet_type

        if image_arn is not None:
            props["imageArn"] = image_arn

        if image_name is not None:
            props["imageName"] = image_name

        if max_user_duration_in_seconds is not None:
            props["maxUserDurationInSeconds"] = max_user_duration_in_seconds

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        if vpc_config is not None:
            props["vpcConfig"] = vpc_config

        jsii.create(CfnFleet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFleetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnFleet.ComputeCapacityProperty")
    class ComputeCapacityProperty(jsii.compat.TypedDict):
        desiredInstances: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnFleet.DomainJoinInfoProperty")
    class DomainJoinInfoProperty(jsii.compat.TypedDict, total=False):
        directoryName: str
        organizationalUnitDistinguishedName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnFleet.VpcConfigProperty")
    class VpcConfigProperty(jsii.compat.TypedDict, total=False):
        securityGroupIds: typing.List[str]
        subnetIds: typing.List[str]


class _CfnFleetProps(jsii.compat.TypedDict, total=False):
    description: str
    disconnectTimeoutInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    displayName: str
    domainJoinInfo: typing.Union[aws_cdk.cdk.Token, "CfnFleet.DomainJoinInfoProperty"]
    enableDefaultInternetAccess: typing.Union[bool, aws_cdk.cdk.Token]
    fleetType: str
    imageArn: str
    imageName: str
    maxUserDurationInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    name: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcConfig: typing.Union[aws_cdk.cdk.Token, "CfnFleet.VpcConfigProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnFleetProps")
class CfnFleetProps(_CfnFleetProps):
    computeCapacity: typing.Union[aws_cdk.cdk.Token, "CfnFleet.ComputeCapacityProperty"]
    instanceType: str

class CfnImageBuilder(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_type: str, appstream_agent_version: typing.Optional[str]=None, description: typing.Optional[str]=None, display_name: typing.Optional[str]=None, domain_join_info: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DomainJoinInfoProperty"]]=None, enable_default_internet_access: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, image_arn: typing.Optional[str]=None, image_name: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "VpcConfigProperty"]]=None) -> None:
        props: CfnImageBuilderProps = {"instanceType": instance_type}

        if appstream_agent_version is not None:
            props["appstreamAgentVersion"] = appstream_agent_version

        if description is not None:
            props["description"] = description

        if display_name is not None:
            props["displayName"] = display_name

        if domain_join_info is not None:
            props["domainJoinInfo"] = domain_join_info

        if enable_default_internet_access is not None:
            props["enableDefaultInternetAccess"] = enable_default_internet_access

        if image_arn is not None:
            props["imageArn"] = image_arn

        if image_name is not None:
            props["imageName"] = image_name

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        if vpc_config is not None:
            props["vpcConfig"] = vpc_config

        jsii.create(CfnImageBuilder, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="imageBuilderStreamingUrl")
    def image_builder_streaming_url(self) -> str:
        return jsii.get(self, "imageBuilderStreamingUrl")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnImageBuilderProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.DomainJoinInfoProperty")
    class DomainJoinInfoProperty(jsii.compat.TypedDict, total=False):
        directoryName: str
        organizationalUnitDistinguishedName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.VpcConfigProperty")
    class VpcConfigProperty(jsii.compat.TypedDict, total=False):
        securityGroupIds: typing.List[str]
        subnetIds: typing.List[str]


class _CfnImageBuilderProps(jsii.compat.TypedDict, total=False):
    appstreamAgentVersion: str
    description: str
    displayName: str
    domainJoinInfo: typing.Union[aws_cdk.cdk.Token, "CfnImageBuilder.DomainJoinInfoProperty"]
    enableDefaultInternetAccess: typing.Union[bool, aws_cdk.cdk.Token]
    imageArn: str
    imageName: str
    name: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcConfig: typing.Union[aws_cdk.cdk.Token, "CfnImageBuilder.VpcConfigProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnImageBuilderProps")
class CfnImageBuilderProps(_CfnImageBuilderProps):
    instanceType: str

class CfnStack(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnStack"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ApplicationSettingsProperty"]]=None, attributes_to_delete: typing.Optional[typing.List[str]]=None, delete_storage_connectors: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, description: typing.Optional[str]=None, display_name: typing.Optional[str]=None, feedback_url: typing.Optional[str]=None, name: typing.Optional[str]=None, redirect_url: typing.Optional[str]=None, storage_connectors: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "StorageConnectorProperty"]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, user_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "UserSettingProperty"]]]]=None) -> None:
        props: CfnStackProps = {}

        if application_settings is not None:
            props["applicationSettings"] = application_settings

        if attributes_to_delete is not None:
            props["attributesToDelete"] = attributes_to_delete

        if delete_storage_connectors is not None:
            props["deleteStorageConnectors"] = delete_storage_connectors

        if description is not None:
            props["description"] = description

        if display_name is not None:
            props["displayName"] = display_name

        if feedback_url is not None:
            props["feedbackUrl"] = feedback_url

        if name is not None:
            props["name"] = name

        if redirect_url is not None:
            props["redirectUrl"] = redirect_url

        if storage_connectors is not None:
            props["storageConnectors"] = storage_connectors

        if tags is not None:
            props["tags"] = tags

        if user_settings is not None:
            props["userSettings"] = user_settings

        jsii.create(CfnStack, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStackProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _ApplicationSettingsProperty(jsii.compat.TypedDict, total=False):
        settingsGroup: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStack.ApplicationSettingsProperty")
    class ApplicationSettingsProperty(_ApplicationSettingsProperty):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    class _StorageConnectorProperty(jsii.compat.TypedDict, total=False):
        domains: typing.List[str]
        resourceIdentifier: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStack.StorageConnectorProperty")
    class StorageConnectorProperty(_StorageConnectorProperty):
        connectorType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStack.UserSettingProperty")
    class UserSettingProperty(jsii.compat.TypedDict):
        action: str
        permission: str


class CfnStackFleetAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnStackFleetAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, fleet_name: str, stack_name: str) -> None:
        props: CfnStackFleetAssociationProps = {"fleetName": fleet_name, "stackName": stack_name}

        jsii.create(CfnStackFleetAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStackFleetAssociationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStackFleetAssociationProps")
class CfnStackFleetAssociationProps(jsii.compat.TypedDict):
    fleetName: str
    stackName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStackProps")
class CfnStackProps(jsii.compat.TypedDict, total=False):
    applicationSettings: typing.Union[aws_cdk.cdk.Token, "CfnStack.ApplicationSettingsProperty"]
    attributesToDelete: typing.List[str]
    deleteStorageConnectors: typing.Union[bool, aws_cdk.cdk.Token]
    description: str
    displayName: str
    feedbackUrl: str
    name: str
    redirectUrl: str
    storageConnectors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStack.StorageConnectorProperty"]]]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    userSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStack.UserSettingProperty"]]]

class CfnStackUserAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnStackUserAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authentication_type: str, stack_name: str, user_name: str, send_email_notification: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnStackUserAssociationProps = {"authenticationType": authentication_type, "stackName": stack_name, "userName": user_name}

        if send_email_notification is not None:
            props["sendEmailNotification"] = send_email_notification

        jsii.create(CfnStackUserAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStackUserAssociationProps":
        return jsii.get(self, "propertyOverrides")


class _CfnStackUserAssociationProps(jsii.compat.TypedDict, total=False):
    sendEmailNotification: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStackUserAssociationProps")
class CfnStackUserAssociationProps(_CfnStackUserAssociationProps):
    authenticationType: str
    stackName: str
    userName: str

class CfnUser(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnUser"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authentication_type: str, user_name: str, first_name: typing.Optional[str]=None, last_name: typing.Optional[str]=None, message_action: typing.Optional[str]=None) -> None:
        props: CfnUserProps = {"authenticationType": authentication_type, "userName": user_name}

        if first_name is not None:
            props["firstName"] = first_name

        if last_name is not None:
            props["lastName"] = last_name

        if message_action is not None:
            props["messageAction"] = message_action

        jsii.create(CfnUser, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserProps":
        return jsii.get(self, "propertyOverrides")


class _CfnUserProps(jsii.compat.TypedDict, total=False):
    firstName: str
    lastName: str
    messageAction: str

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnUserProps")
class CfnUserProps(_CfnUserProps):
    authenticationType: str
    userName: str

__all__ = ["CfnDirectoryConfig", "CfnDirectoryConfigProps", "CfnFleet", "CfnFleetProps", "CfnImageBuilder", "CfnImageBuilderProps", "CfnStack", "CfnStackFleetAssociation", "CfnStackFleetAssociationProps", "CfnStackProps", "CfnStackUserAssociation", "CfnStackUserAssociationProps", "CfnUser", "CfnUserProps", "__jsii_assembly__"]

publication.publish()
