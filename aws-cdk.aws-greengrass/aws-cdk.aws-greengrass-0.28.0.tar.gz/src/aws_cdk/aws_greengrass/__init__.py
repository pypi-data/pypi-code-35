import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-greengrass", "0.28.0", __name__, "aws-greengrass@0.28.0.jsii.tgz")
class CfnConnectorDefinition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, initial_version: typing.Optional[typing.Union["ConnectorDefinitionVersionProperty", aws_cdk.cdk.Token]]=None) -> None:
        props: CfnConnectorDefinitionProps = {"name": name}

        if initial_version is not None:
            props["initialVersion"] = initial_version

        jsii.create(CfnConnectorDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="connectorDefinitionArn")
    def connector_definition_arn(self) -> str:
        return jsii.get(self, "connectorDefinitionArn")

    @property
    @jsii.member(jsii_name="connectorDefinitionId")
    def connector_definition_id(self) -> str:
        return jsii.get(self, "connectorDefinitionId")

    @property
    @jsii.member(jsii_name="connectorDefinitionLatestVersionArn")
    def connector_definition_latest_version_arn(self) -> str:
        return jsii.get(self, "connectorDefinitionLatestVersionArn")

    @property
    @jsii.member(jsii_name="connectorDefinitionName")
    def connector_definition_name(self) -> str:
        return jsii.get(self, "connectorDefinitionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConnectorDefinitionProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinition.ConnectorDefinitionVersionProperty")
    class ConnectorDefinitionVersionProperty(jsii.compat.TypedDict):
        connectors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConnectorDefinition.ConnectorProperty"]]]

    class _ConnectorProperty(jsii.compat.TypedDict, total=False):
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinition.ConnectorProperty")
    class ConnectorProperty(_ConnectorProperty):
        connectorArn: str
        id: str


class _CfnConnectorDefinitionProps(jsii.compat.TypedDict, total=False):
    initialVersion: typing.Union["CfnConnectorDefinition.ConnectorDefinitionVersionProperty", aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinitionProps")
class CfnConnectorDefinitionProps(_CfnConnectorDefinitionProps):
    name: str

class CfnConnectorDefinitionVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinitionVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, connector_definition_id: str, connectors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ConnectorProperty"]]]) -> None:
        props: CfnConnectorDefinitionVersionProps = {"connectorDefinitionId": connector_definition_id, "connectors": connectors}

        jsii.create(CfnConnectorDefinitionVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="connectorDefinitionVersionArn")
    def connector_definition_version_arn(self) -> str:
        return jsii.get(self, "connectorDefinitionVersionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConnectorDefinitionVersionProps":
        return jsii.get(self, "propertyOverrides")

    class _ConnectorProperty(jsii.compat.TypedDict, total=False):
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinitionVersion.ConnectorProperty")
    class ConnectorProperty(_ConnectorProperty):
        connectorArn: str
        id: str


@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinitionVersionProps")
class CfnConnectorDefinitionVersionProps(jsii.compat.TypedDict):
    connectorDefinitionId: str
    connectors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConnectorDefinitionVersion.ConnectorProperty"]]]

class CfnCoreDefinition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, initial_version: typing.Optional[typing.Union[aws_cdk.cdk.Token, "CoreDefinitionVersionProperty"]]=None) -> None:
        props: CfnCoreDefinitionProps = {"name": name}

        if initial_version is not None:
            props["initialVersion"] = initial_version

        jsii.create(CfnCoreDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="coreDefinitionArn")
    def core_definition_arn(self) -> str:
        return jsii.get(self, "coreDefinitionArn")

    @property
    @jsii.member(jsii_name="coreDefinitionId")
    def core_definition_id(self) -> str:
        return jsii.get(self, "coreDefinitionId")

    @property
    @jsii.member(jsii_name="coreDefinitionLatestVersionArn")
    def core_definition_latest_version_arn(self) -> str:
        return jsii.get(self, "coreDefinitionLatestVersionArn")

    @property
    @jsii.member(jsii_name="coreDefinitionName")
    def core_definition_name(self) -> str:
        return jsii.get(self, "coreDefinitionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCoreDefinitionProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinition.CoreDefinitionVersionProperty")
    class CoreDefinitionVersionProperty(jsii.compat.TypedDict):
        cores: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCoreDefinition.CoreProperty"]]]

    class _CoreProperty(jsii.compat.TypedDict, total=False):
        syncShadow: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinition.CoreProperty")
    class CoreProperty(_CoreProperty):
        certificateArn: str
        id: str
        thingArn: str


class _CfnCoreDefinitionProps(jsii.compat.TypedDict, total=False):
    initialVersion: typing.Union[aws_cdk.cdk.Token, "CfnCoreDefinition.CoreDefinitionVersionProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinitionProps")
class CfnCoreDefinitionProps(_CfnCoreDefinitionProps):
    name: str

class CfnCoreDefinitionVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinitionVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, core_definition_id: str, cores: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CoreProperty"]]]) -> None:
        props: CfnCoreDefinitionVersionProps = {"coreDefinitionId": core_definition_id, "cores": cores}

        jsii.create(CfnCoreDefinitionVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="coreDefinitionVersionArn")
    def core_definition_version_arn(self) -> str:
        return jsii.get(self, "coreDefinitionVersionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCoreDefinitionVersionProps":
        return jsii.get(self, "propertyOverrides")

    class _CoreProperty(jsii.compat.TypedDict, total=False):
        syncShadow: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinitionVersion.CoreProperty")
    class CoreProperty(_CoreProperty):
        certificateArn: str
        id: str
        thingArn: str


@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinitionVersionProps")
class CfnCoreDefinitionVersionProps(jsii.compat.TypedDict):
    coreDefinitionId: str
    cores: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCoreDefinitionVersion.CoreProperty"]]]

class CfnDeviceDefinition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, initial_version: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DeviceDefinitionVersionProperty"]]=None) -> None:
        props: CfnDeviceDefinitionProps = {"name": name}

        if initial_version is not None:
            props["initialVersion"] = initial_version

        jsii.create(CfnDeviceDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deviceDefinitionArn")
    def device_definition_arn(self) -> str:
        return jsii.get(self, "deviceDefinitionArn")

    @property
    @jsii.member(jsii_name="deviceDefinitionId")
    def device_definition_id(self) -> str:
        return jsii.get(self, "deviceDefinitionId")

    @property
    @jsii.member(jsii_name="deviceDefinitionLatestVersionArn")
    def device_definition_latest_version_arn(self) -> str:
        return jsii.get(self, "deviceDefinitionLatestVersionArn")

    @property
    @jsii.member(jsii_name="deviceDefinitionName")
    def device_definition_name(self) -> str:
        return jsii.get(self, "deviceDefinitionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeviceDefinitionProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinition.DeviceDefinitionVersionProperty")
    class DeviceDefinitionVersionProperty(jsii.compat.TypedDict):
        devices: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeviceDefinition.DeviceProperty"]]]

    class _DeviceProperty(jsii.compat.TypedDict, total=False):
        syncShadow: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinition.DeviceProperty")
    class DeviceProperty(_DeviceProperty):
        certificateArn: str
        id: str
        thingArn: str


class _CfnDeviceDefinitionProps(jsii.compat.TypedDict, total=False):
    initialVersion: typing.Union[aws_cdk.cdk.Token, "CfnDeviceDefinition.DeviceDefinitionVersionProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinitionProps")
class CfnDeviceDefinitionProps(_CfnDeviceDefinitionProps):
    name: str

class CfnDeviceDefinitionVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinitionVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, device_definition_id: str, devices: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "DeviceProperty"]]]) -> None:
        props: CfnDeviceDefinitionVersionProps = {"deviceDefinitionId": device_definition_id, "devices": devices}

        jsii.create(CfnDeviceDefinitionVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deviceDefinitionVersionArn")
    def device_definition_version_arn(self) -> str:
        return jsii.get(self, "deviceDefinitionVersionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeviceDefinitionVersionProps":
        return jsii.get(self, "propertyOverrides")

    class _DeviceProperty(jsii.compat.TypedDict, total=False):
        syncShadow: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinitionVersion.DeviceProperty")
    class DeviceProperty(_DeviceProperty):
        certificateArn: str
        id: str
        thingArn: str


@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinitionVersionProps")
class CfnDeviceDefinitionVersionProps(jsii.compat.TypedDict):
    deviceDefinitionId: str
    devices: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeviceDefinitionVersion.DeviceProperty"]]]

class CfnFunctionDefinition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, initial_version: typing.Optional[typing.Union[aws_cdk.cdk.Token, "FunctionDefinitionVersionProperty"]]=None) -> None:
        props: CfnFunctionDefinitionProps = {"name": name}

        if initial_version is not None:
            props["initialVersion"] = initial_version

        jsii.create(CfnFunctionDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="functionDefinitionArn")
    def function_definition_arn(self) -> str:
        return jsii.get(self, "functionDefinitionArn")

    @property
    @jsii.member(jsii_name="functionDefinitionId")
    def function_definition_id(self) -> str:
        return jsii.get(self, "functionDefinitionId")

    @property
    @jsii.member(jsii_name="functionDefinitionLatestVersionArn")
    def function_definition_latest_version_arn(self) -> str:
        return jsii.get(self, "functionDefinitionLatestVersionArn")

    @property
    @jsii.member(jsii_name="functionDefinitionName")
    def function_definition_name(self) -> str:
        return jsii.get(self, "functionDefinitionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFunctionDefinitionProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.DefaultConfigProperty")
    class DefaultConfigProperty(jsii.compat.TypedDict):
        execution: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.ExecutionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.EnvironmentProperty")
    class EnvironmentProperty(jsii.compat.TypedDict, total=False):
        accessSysfs: typing.Union[bool, aws_cdk.cdk.Token]
        execution: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.ExecutionProperty"]
        resourceAccessPolicies: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.ResourceAccessPolicyProperty"]]]
        variables: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.ExecutionProperty")
    class ExecutionProperty(jsii.compat.TypedDict, total=False):
        isolationMode: str
        runAs: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.RunAsProperty"]

    class _FunctionConfigurationProperty(jsii.compat.TypedDict, total=False):
        encodingType: str
        environment: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.EnvironmentProperty"]
        execArgs: str
        executable: str
        pinned: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.FunctionConfigurationProperty")
    class FunctionConfigurationProperty(_FunctionConfigurationProperty):
        memorySize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        timeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _FunctionDefinitionVersionProperty(jsii.compat.TypedDict, total=False):
        defaultConfig: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.DefaultConfigProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.FunctionDefinitionVersionProperty")
    class FunctionDefinitionVersionProperty(_FunctionDefinitionVersionProperty):
        functions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.FunctionProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.FunctionProperty")
    class FunctionProperty(jsii.compat.TypedDict):
        functionArn: str
        functionConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.FunctionConfigurationProperty"]
        id: str

    class _ResourceAccessPolicyProperty(jsii.compat.TypedDict, total=False):
        permission: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty")
    class ResourceAccessPolicyProperty(_ResourceAccessPolicyProperty):
        resourceId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.RunAsProperty")
    class RunAsProperty(jsii.compat.TypedDict, total=False):
        gid: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        uid: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnFunctionDefinitionProps(jsii.compat.TypedDict, total=False):
    initialVersion: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinition.FunctionDefinitionVersionProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionProps")
class CfnFunctionDefinitionProps(_CfnFunctionDefinitionProps):
    name: str

class CfnFunctionDefinitionVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, function_definition_id: str, functions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "FunctionProperty"]]], default_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DefaultConfigProperty"]]=None) -> None:
        props: CfnFunctionDefinitionVersionProps = {"functionDefinitionId": function_definition_id, "functions": functions}

        if default_config is not None:
            props["defaultConfig"] = default_config

        jsii.create(CfnFunctionDefinitionVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="functionDefinitionVersionArn")
    def function_definition_version_arn(self) -> str:
        return jsii.get(self, "functionDefinitionVersionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFunctionDefinitionVersionProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.DefaultConfigProperty")
    class DefaultConfigProperty(jsii.compat.TypedDict):
        execution: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinitionVersion.ExecutionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.EnvironmentProperty")
    class EnvironmentProperty(jsii.compat.TypedDict, total=False):
        accessSysfs: typing.Union[bool, aws_cdk.cdk.Token]
        execution: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinitionVersion.ExecutionProperty"]
        resourceAccessPolicies: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty"]]]
        variables: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.ExecutionProperty")
    class ExecutionProperty(jsii.compat.TypedDict, total=False):
        isolationMode: str
        runAs: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinitionVersion.RunAsProperty"]

    class _FunctionConfigurationProperty(jsii.compat.TypedDict, total=False):
        encodingType: str
        environment: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinitionVersion.EnvironmentProperty"]
        execArgs: str
        executable: str
        pinned: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.FunctionConfigurationProperty")
    class FunctionConfigurationProperty(_FunctionConfigurationProperty):
        memorySize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        timeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.FunctionProperty")
    class FunctionProperty(jsii.compat.TypedDict):
        functionArn: str
        functionConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinitionVersion.FunctionConfigurationProperty"]
        id: str

    class _ResourceAccessPolicyProperty(jsii.compat.TypedDict, total=False):
        permission: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty")
    class ResourceAccessPolicyProperty(_ResourceAccessPolicyProperty):
        resourceId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.RunAsProperty")
    class RunAsProperty(jsii.compat.TypedDict, total=False):
        gid: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        uid: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnFunctionDefinitionVersionProps(jsii.compat.TypedDict, total=False):
    defaultConfig: typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinitionVersion.DefaultConfigProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersionProps")
class CfnFunctionDefinitionVersionProps(_CfnFunctionDefinitionVersionProps):
    functionDefinitionId: str
    functions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnFunctionDefinitionVersion.FunctionProperty"]]]

class CfnGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, initial_version: typing.Optional[typing.Union[aws_cdk.cdk.Token, "GroupVersionProperty"]]=None, role_arn: typing.Optional[str]=None) -> None:
        props: CfnGroupProps = {"name": name}

        if initial_version is not None:
            props["initialVersion"] = initial_version

        if role_arn is not None:
            props["roleArn"] = role_arn

        jsii.create(CfnGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> str:
        return jsii.get(self, "groupArn")

    @property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> str:
        return jsii.get(self, "groupId")

    @property
    @jsii.member(jsii_name="groupLatestVersionArn")
    def group_latest_version_arn(self) -> str:
        return jsii.get(self, "groupLatestVersionArn")

    @property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        return jsii.get(self, "groupName")

    @property
    @jsii.member(jsii_name="groupRoleArn")
    def group_role_arn(self) -> str:
        return jsii.get(self, "groupRoleArn")

    @property
    @jsii.member(jsii_name="groupRoleAttachedAt")
    def group_role_attached_at(self) -> str:
        return jsii.get(self, "groupRoleAttachedAt")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnGroupProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnGroup.GroupVersionProperty")
    class GroupVersionProperty(jsii.compat.TypedDict, total=False):
        connectorDefinitionVersionArn: str
        coreDefinitionVersionArn: str
        deviceDefinitionVersionArn: str
        functionDefinitionVersionArn: str
        loggerDefinitionVersionArn: str
        resourceDefinitionVersionArn: str
        subscriptionDefinitionVersionArn: str


class _CfnGroupProps(jsii.compat.TypedDict, total=False):
    initialVersion: typing.Union[aws_cdk.cdk.Token, "CfnGroup.GroupVersionProperty"]
    roleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnGroupProps")
class CfnGroupProps(_CfnGroupProps):
    name: str

class CfnGroupVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnGroupVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_id: str, connector_definition_version_arn: typing.Optional[str]=None, core_definition_version_arn: typing.Optional[str]=None, device_definition_version_arn: typing.Optional[str]=None, function_definition_version_arn: typing.Optional[str]=None, logger_definition_version_arn: typing.Optional[str]=None, resource_definition_version_arn: typing.Optional[str]=None, subscription_definition_version_arn: typing.Optional[str]=None) -> None:
        props: CfnGroupVersionProps = {"groupId": group_id}

        if connector_definition_version_arn is not None:
            props["connectorDefinitionVersionArn"] = connector_definition_version_arn

        if core_definition_version_arn is not None:
            props["coreDefinitionVersionArn"] = core_definition_version_arn

        if device_definition_version_arn is not None:
            props["deviceDefinitionVersionArn"] = device_definition_version_arn

        if function_definition_version_arn is not None:
            props["functionDefinitionVersionArn"] = function_definition_version_arn

        if logger_definition_version_arn is not None:
            props["loggerDefinitionVersionArn"] = logger_definition_version_arn

        if resource_definition_version_arn is not None:
            props["resourceDefinitionVersionArn"] = resource_definition_version_arn

        if subscription_definition_version_arn is not None:
            props["subscriptionDefinitionVersionArn"] = subscription_definition_version_arn

        jsii.create(CfnGroupVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="groupVersionArn")
    def group_version_arn(self) -> str:
        return jsii.get(self, "groupVersionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnGroupVersionProps":
        return jsii.get(self, "propertyOverrides")


class _CfnGroupVersionProps(jsii.compat.TypedDict, total=False):
    connectorDefinitionVersionArn: str
    coreDefinitionVersionArn: str
    deviceDefinitionVersionArn: str
    functionDefinitionVersionArn: str
    loggerDefinitionVersionArn: str
    resourceDefinitionVersionArn: str
    subscriptionDefinitionVersionArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnGroupVersionProps")
class CfnGroupVersionProps(_CfnGroupVersionProps):
    groupId: str

class CfnLoggerDefinition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, initial_version: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LoggerDefinitionVersionProperty"]]=None) -> None:
        props: CfnLoggerDefinitionProps = {"name": name}

        if initial_version is not None:
            props["initialVersion"] = initial_version

        jsii.create(CfnLoggerDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="loggerDefinitionArn")
    def logger_definition_arn(self) -> str:
        return jsii.get(self, "loggerDefinitionArn")

    @property
    @jsii.member(jsii_name="loggerDefinitionId")
    def logger_definition_id(self) -> str:
        return jsii.get(self, "loggerDefinitionId")

    @property
    @jsii.member(jsii_name="loggerDefinitionLatestVersionArn")
    def logger_definition_latest_version_arn(self) -> str:
        return jsii.get(self, "loggerDefinitionLatestVersionArn")

    @property
    @jsii.member(jsii_name="loggerDefinitionName")
    def logger_definition_name(self) -> str:
        return jsii.get(self, "loggerDefinitionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLoggerDefinitionProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinition.LoggerDefinitionVersionProperty")
    class LoggerDefinitionVersionProperty(jsii.compat.TypedDict):
        loggers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoggerDefinition.LoggerProperty"]]]

    class _LoggerProperty(jsii.compat.TypedDict, total=False):
        space: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinition.LoggerProperty")
    class LoggerProperty(_LoggerProperty):
        component: str
        id: str
        level: str
        type: str


class _CfnLoggerDefinitionProps(jsii.compat.TypedDict, total=False):
    initialVersion: typing.Union[aws_cdk.cdk.Token, "CfnLoggerDefinition.LoggerDefinitionVersionProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinitionProps")
class CfnLoggerDefinitionProps(_CfnLoggerDefinitionProps):
    name: str

class CfnLoggerDefinitionVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinitionVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, logger_definition_id: str, loggers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "LoggerProperty"]]]) -> None:
        props: CfnLoggerDefinitionVersionProps = {"loggerDefinitionId": logger_definition_id, "loggers": loggers}

        jsii.create(CfnLoggerDefinitionVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="loggerDefinitionVersionArn")
    def logger_definition_version_arn(self) -> str:
        return jsii.get(self, "loggerDefinitionVersionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLoggerDefinitionVersionProps":
        return jsii.get(self, "propertyOverrides")

    class _LoggerProperty(jsii.compat.TypedDict, total=False):
        space: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinitionVersion.LoggerProperty")
    class LoggerProperty(_LoggerProperty):
        component: str
        id: str
        level: str
        type: str


@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinitionVersionProps")
class CfnLoggerDefinitionVersionProps(jsii.compat.TypedDict):
    loggerDefinitionId: str
    loggers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoggerDefinitionVersion.LoggerProperty"]]]

class CfnResourceDefinitionVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_definition_id: str, resources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ResourceInstanceProperty"]]]) -> None:
        props: CfnResourceDefinitionVersionProps = {"resourceDefinitionId": resource_definition_id, "resources": resources}

        jsii.create(CfnResourceDefinitionVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResourceDefinitionVersionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resourceDefinitionVersionArn")
    def resource_definition_version_arn(self) -> str:
        return jsii.get(self, "resourceDefinitionVersionArn")

    class _GroupOwnerSettingProperty(jsii.compat.TypedDict, total=False):
        groupOwner: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty")
    class GroupOwnerSettingProperty(_GroupOwnerSettingProperty):
        autoAddGroupOwner: typing.Union[bool, aws_cdk.cdk.Token]

    class _LocalDeviceResourceDataProperty(jsii.compat.TypedDict, total=False):
        groupOwnerSetting: typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.GroupOwnerSettingProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty")
    class LocalDeviceResourceDataProperty(_LocalDeviceResourceDataProperty):
        sourcePath: str

    class _LocalVolumeResourceDataProperty(jsii.compat.TypedDict, total=False):
        groupOwnerSetting: typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.GroupOwnerSettingProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty")
    class LocalVolumeResourceDataProperty(_LocalVolumeResourceDataProperty):
        destinationPath: str
        sourcePath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.ResourceDataContainerProperty")
    class ResourceDataContainerProperty(jsii.compat.TypedDict, total=False):
        localDeviceResourceData: typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty"]
        localVolumeResourceData: typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty"]
        s3MachineLearningModelResourceData: typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty"]
        sageMakerMachineLearningModelResourceData: typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty"]
        secretsManagerSecretResourceData: typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.ResourceInstanceProperty")
    class ResourceInstanceProperty(jsii.compat.TypedDict):
        id: str
        name: str
        resourceDataContainer: typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.ResourceDataContainerProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty")
    class S3MachineLearningModelResourceDataProperty(jsii.compat.TypedDict):
        destinationPath: str
        s3Uri: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty")
    class SageMakerMachineLearningModelResourceDataProperty(jsii.compat.TypedDict):
        destinationPath: str
        sageMakerJobArn: str

    class _SecretsManagerSecretResourceDataProperty(jsii.compat.TypedDict, total=False):
        additionalStagingLabelsToDownload: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty")
    class SecretsManagerSecretResourceDataProperty(_SecretsManagerSecretResourceDataProperty):
        arn: str


@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersionProps")
class CfnResourceDefinitionVersionProps(jsii.compat.TypedDict):
    resourceDefinitionId: str
    resources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnResourceDefinitionVersion.ResourceInstanceProperty"]]]

class CfnSubscriptionDefinition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, initial_version: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SubscriptionDefinitionVersionProperty"]]=None) -> None:
        props: CfnSubscriptionDefinitionProps = {"name": name}

        if initial_version is not None:
            props["initialVersion"] = initial_version

        jsii.create(CfnSubscriptionDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubscriptionDefinitionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subscriptionDefinitionArn")
    def subscription_definition_arn(self) -> str:
        return jsii.get(self, "subscriptionDefinitionArn")

    @property
    @jsii.member(jsii_name="subscriptionDefinitionId")
    def subscription_definition_id(self) -> str:
        return jsii.get(self, "subscriptionDefinitionId")

    @property
    @jsii.member(jsii_name="subscriptionDefinitionLatestVersionArn")
    def subscription_definition_latest_version_arn(self) -> str:
        return jsii.get(self, "subscriptionDefinitionLatestVersionArn")

    @property
    @jsii.member(jsii_name="subscriptionDefinitionName")
    def subscription_definition_name(self) -> str:
        return jsii.get(self, "subscriptionDefinitionName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty")
    class SubscriptionDefinitionVersionProperty(jsii.compat.TypedDict):
        subscriptions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSubscriptionDefinition.SubscriptionProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinition.SubscriptionProperty")
    class SubscriptionProperty(jsii.compat.TypedDict):
        id: str
        source: str
        subject: str
        target: str


class _CfnSubscriptionDefinitionProps(jsii.compat.TypedDict, total=False):
    initialVersion: typing.Union[aws_cdk.cdk.Token, "CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinitionProps")
class CfnSubscriptionDefinitionProps(_CfnSubscriptionDefinitionProps):
    name: str

class CfnSubscriptionDefinitionVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinitionVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, subscription_definition_id: str, subscriptions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SubscriptionProperty"]]]) -> None:
        props: CfnSubscriptionDefinitionVersionProps = {"subscriptionDefinitionId": subscription_definition_id, "subscriptions": subscriptions}

        jsii.create(CfnSubscriptionDefinitionVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubscriptionDefinitionVersionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subscriptionDefinitionVersionArn")
    def subscription_definition_version_arn(self) -> str:
        return jsii.get(self, "subscriptionDefinitionVersionArn")

    @jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinitionVersion.SubscriptionProperty")
    class SubscriptionProperty(jsii.compat.TypedDict):
        id: str
        source: str
        subject: str
        target: str


@jsii.data_type(jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinitionVersionProps")
class CfnSubscriptionDefinitionVersionProps(jsii.compat.TypedDict):
    subscriptionDefinitionId: str
    subscriptions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSubscriptionDefinitionVersion.SubscriptionProperty"]]]

__all__ = ["CfnConnectorDefinition", "CfnConnectorDefinitionProps", "CfnConnectorDefinitionVersion", "CfnConnectorDefinitionVersionProps", "CfnCoreDefinition", "CfnCoreDefinitionProps", "CfnCoreDefinitionVersion", "CfnCoreDefinitionVersionProps", "CfnDeviceDefinition", "CfnDeviceDefinitionProps", "CfnDeviceDefinitionVersion", "CfnDeviceDefinitionVersionProps", "CfnFunctionDefinition", "CfnFunctionDefinitionProps", "CfnFunctionDefinitionVersion", "CfnFunctionDefinitionVersionProps", "CfnGroup", "CfnGroupProps", "CfnGroupVersion", "CfnGroupVersionProps", "CfnLoggerDefinition", "CfnLoggerDefinitionProps", "CfnLoggerDefinitionVersion", "CfnLoggerDefinitionVersionProps", "CfnResourceDefinitionVersion", "CfnResourceDefinitionVersionProps", "CfnSubscriptionDefinition", "CfnSubscriptionDefinitionProps", "CfnSubscriptionDefinitionVersion", "CfnSubscriptionDefinitionVersionProps", "__jsii_assembly__"]

publication.publish()
