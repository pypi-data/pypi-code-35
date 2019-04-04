import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-amazonmq", "0.28.0", __name__, "aws-amazonmq@0.28.0.jsii.tgz")
class CfnBroker(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-amazonmq.CfnBroker"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_minor_version_upgrade: typing.Union[bool, aws_cdk.cdk.Token], broker_name: str, deployment_mode: str, engine_type: str, engine_version: str, host_instance_type: str, publicly_accessible: typing.Union[bool, aws_cdk.cdk.Token], users: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "UserProperty"]]], configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ConfigurationIdProperty"]]=None, logs: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LogListProperty"]]=None, maintenance_window_start_time: typing.Optional[typing.Union[aws_cdk.cdk.Token, "MaintenanceWindowProperty"]]=None, security_groups: typing.Optional[typing.List[str]]=None, subnet_ids: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        props: CfnBrokerProps = {"autoMinorVersionUpgrade": auto_minor_version_upgrade, "brokerName": broker_name, "deploymentMode": deployment_mode, "engineType": engine_type, "engineVersion": engine_version, "hostInstanceType": host_instance_type, "publiclyAccessible": publicly_accessible, "users": users}

        if configuration is not None:
            props["configuration"] = configuration

        if logs is not None:
            props["logs"] = logs

        if maintenance_window_start_time is not None:
            props["maintenanceWindowStartTime"] = maintenance_window_start_time

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if subnet_ids is not None:
            props["subnetIds"] = subnet_ids

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnBroker, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="brokerAmqpEndpoints")
    def broker_amqp_endpoints(self) -> typing.List[str]:
        return jsii.get(self, "brokerAmqpEndpoints")

    @property
    @jsii.member(jsii_name="brokerArn")
    def broker_arn(self) -> str:
        return jsii.get(self, "brokerArn")

    @property
    @jsii.member(jsii_name="brokerConfigurationId")
    def broker_configuration_id(self) -> str:
        return jsii.get(self, "brokerConfigurationId")

    @property
    @jsii.member(jsii_name="brokerConfigurationRevision")
    def broker_configuration_revision(self) -> aws_cdk.cdk.Token:
        return jsii.get(self, "brokerConfigurationRevision")

    @property
    @jsii.member(jsii_name="brokerId")
    def broker_id(self) -> str:
        return jsii.get(self, "brokerId")

    @property
    @jsii.member(jsii_name="brokerIpAddresses")
    def broker_ip_addresses(self) -> typing.List[str]:
        return jsii.get(self, "brokerIpAddresses")

    @property
    @jsii.member(jsii_name="brokerMqttEndpoints")
    def broker_mqtt_endpoints(self) -> typing.List[str]:
        return jsii.get(self, "brokerMqttEndpoints")

    @property
    @jsii.member(jsii_name="brokerOpenWireEndpoints")
    def broker_open_wire_endpoints(self) -> typing.List[str]:
        return jsii.get(self, "brokerOpenWireEndpoints")

    @property
    @jsii.member(jsii_name="brokerStompEndpoints")
    def broker_stomp_endpoints(self) -> typing.List[str]:
        return jsii.get(self, "brokerStompEndpoints")

    @property
    @jsii.member(jsii_name="brokerWssEndpoints")
    def broker_wss_endpoints(self) -> typing.List[str]:
        return jsii.get(self, "brokerWssEndpoints")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBrokerProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.ConfigurationIdProperty")
    class ConfigurationIdProperty(jsii.compat.TypedDict):
        id: str
        revision: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.LogListProperty")
    class LogListProperty(jsii.compat.TypedDict, total=False):
        audit: typing.Union[bool, aws_cdk.cdk.Token]
        general: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.MaintenanceWindowProperty")
    class MaintenanceWindowProperty(jsii.compat.TypedDict):
        dayOfWeek: str
        timeOfDay: str
        timeZone: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.TagsEntryProperty")
    class TagsEntryProperty(jsii.compat.TypedDict):
        key: str
        value: str

    class _UserProperty(jsii.compat.TypedDict, total=False):
        consoleAccess: typing.Union[bool, aws_cdk.cdk.Token]
        groups: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.UserProperty")
    class UserProperty(_UserProperty):
        password: str
        username: str


class _CfnBrokerProps(jsii.compat.TypedDict, total=False):
    configuration: typing.Union[aws_cdk.cdk.Token, "CfnBroker.ConfigurationIdProperty"]
    logs: typing.Union[aws_cdk.cdk.Token, "CfnBroker.LogListProperty"]
    maintenanceWindowStartTime: typing.Union[aws_cdk.cdk.Token, "CfnBroker.MaintenanceWindowProperty"]
    securityGroups: typing.List[str]
    subnetIds: typing.List[str]
    tags: typing.List["CfnBroker.TagsEntryProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBrokerProps")
class CfnBrokerProps(_CfnBrokerProps):
    autoMinorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    brokerName: str
    deploymentMode: str
    engineType: str
    engineVersion: str
    hostInstanceType: str
    publiclyAccessible: typing.Union[bool, aws_cdk.cdk.Token]
    users: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBroker.UserProperty"]]]

class CfnConfiguration(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-amazonmq.CfnConfiguration"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, data: str, engine_type: str, engine_version: str, name: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        props: CfnConfigurationProps = {"data": data, "engineType": engine_type, "engineVersion": engine_version, "name": name}

        if description is not None:
            props["description"] = description

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="configurationArn")
    def configuration_arn(self) -> str:
        return jsii.get(self, "configurationArn")

    @property
    @jsii.member(jsii_name="configurationId")
    def configuration_id(self) -> str:
        return jsii.get(self, "configurationId")

    @property
    @jsii.member(jsii_name="configurationRevision")
    def configuration_revision(self) -> aws_cdk.cdk.Token:
        return jsii.get(self, "configurationRevision")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnConfiguration.TagsEntryProperty")
    class TagsEntryProperty(jsii.compat.TypedDict):
        key: str
        value: str


class CfnConfigurationAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, broker: str, configuration: typing.Union[aws_cdk.cdk.Token, "ConfigurationIdProperty"]) -> None:
        props: CfnConfigurationAssociationProps = {"broker": broker, "configuration": configuration}

        jsii.create(CfnConfigurationAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="configurationAssociationId")
    def configuration_association_id(self) -> str:
        return jsii.get(self, "configurationAssociationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociation.ConfigurationIdProperty")
    class ConfigurationIdProperty(jsii.compat.TypedDict):
        id: str
        revision: typing.Union[jsii.Number, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociationProps")
class CfnConfigurationAssociationProps(jsii.compat.TypedDict):
    broker: str
    configuration: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationAssociation.ConfigurationIdProperty"]

class _CfnConfigurationProps(jsii.compat.TypedDict, total=False):
    description: str
    tags: typing.List["CfnConfiguration.TagsEntryProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationProps")
class CfnConfigurationProps(_CfnConfigurationProps):
    data: str
    engineType: str
    engineVersion: str
    name: str

__all__ = ["CfnBroker", "CfnBrokerProps", "CfnConfiguration", "CfnConfigurationAssociation", "CfnConfigurationAssociationProps", "CfnConfigurationProps", "__jsii_assembly__"]

publication.publish()
