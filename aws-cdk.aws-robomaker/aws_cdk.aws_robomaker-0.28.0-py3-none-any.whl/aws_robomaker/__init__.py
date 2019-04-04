import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-robomaker", "0.28.0", __name__, "aws-robomaker@0.28.0.jsii.tgz")
class CfnFleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-robomaker.CfnFleet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[typing.Any, typing.Any]]=None) -> None:
        props: CfnFleetProps = {}

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnFleet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="fleetArn")
    def fleet_arn(self) -> str:
        return jsii.get(self, "fleetArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFleetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


@jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnFleetProps")
class CfnFleetProps(jsii.compat.TypedDict, total=False):
    name: str
    tags: typing.Mapping[typing.Any, typing.Any]

class CfnRobot(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-robomaker.CfnRobot"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, architecture: str, greengrass_group_id: str, fleet: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[typing.Any, typing.Any]]=None) -> None:
        props: CfnRobotProps = {"architecture": architecture, "greengrassGroupId": greengrass_group_id}

        if fleet is not None:
            props["fleet"] = fleet

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnRobot, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRobotProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="robotArn")
    def robot_arn(self) -> str:
        return jsii.get(self, "robotArn")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnRobotApplication(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplication"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, robot_software_suite: typing.Union["RobotSoftwareSuiteProperty", aws_cdk.cdk.Token], sources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SourceConfigProperty"]]], current_revision_id: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[typing.Any, typing.Any]]=None) -> None:
        props: CfnRobotApplicationProps = {"robotSoftwareSuite": robot_software_suite, "sources": sources}

        if current_revision_id is not None:
            props["currentRevisionId"] = current_revision_id

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnRobotApplication, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRobotApplicationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="robotApplicationArn")
    def robot_application_arn(self) -> str:
        return jsii.get(self, "robotApplicationArn")

    @property
    @jsii.member(jsii_name="robotApplicationCurrentRevisionId")
    def robot_application_current_revision_id(self) -> str:
        return jsii.get(self, "robotApplicationCurrentRevisionId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty")
    class RobotSoftwareSuiteProperty(jsii.compat.TypedDict):
        name: str
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplication.SourceConfigProperty")
    class SourceConfigProperty(jsii.compat.TypedDict):
        architecture: str
        s3Bucket: str
        s3Key: str


class _CfnRobotApplicationProps(jsii.compat.TypedDict, total=False):
    currentRevisionId: str
    name: str
    tags: typing.Mapping[typing.Any, typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplicationProps")
class CfnRobotApplicationProps(_CfnRobotApplicationProps):
    robotSoftwareSuite: typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", aws_cdk.cdk.Token]
    sources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRobotApplication.SourceConfigProperty"]]]

class CfnRobotApplicationVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplicationVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application: str, current_revision_id: typing.Optional[str]=None) -> None:
        props: CfnRobotApplicationVersionProps = {"application": application}

        if current_revision_id is not None:
            props["currentRevisionId"] = current_revision_id

        jsii.create(CfnRobotApplicationVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRobotApplicationVersionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="robotApplicationVersionArn")
    def robot_application_version_arn(self) -> str:
        return jsii.get(self, "robotApplicationVersionArn")


class _CfnRobotApplicationVersionProps(jsii.compat.TypedDict, total=False):
    currentRevisionId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplicationVersionProps")
class CfnRobotApplicationVersionProps(_CfnRobotApplicationVersionProps):
    application: str

class _CfnRobotProps(jsii.compat.TypedDict, total=False):
    fleet: str
    name: str
    tags: typing.Mapping[typing.Any, typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnRobotProps")
class CfnRobotProps(_CfnRobotProps):
    architecture: str
    greengrassGroupId: str

class CfnSimulationApplication(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rendering_engine: typing.Union[aws_cdk.cdk.Token, "RenderingEngineProperty"], robot_software_suite: typing.Union[aws_cdk.cdk.Token, "RobotSoftwareSuiteProperty"], simulation_software_suite: typing.Union[aws_cdk.cdk.Token, "SimulationSoftwareSuiteProperty"], sources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SourceConfigProperty"]]], current_revision_id: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[typing.Any, typing.Any]]=None) -> None:
        props: CfnSimulationApplicationProps = {"renderingEngine": rendering_engine, "robotSoftwareSuite": robot_software_suite, "simulationSoftwareSuite": simulation_software_suite, "sources": sources}

        if current_revision_id is not None:
            props["currentRevisionId"] = current_revision_id

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnSimulationApplication, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSimulationApplicationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="simulationApplicationArn")
    def simulation_application_arn(self) -> str:
        return jsii.get(self, "simulationApplicationArn")

    @property
    @jsii.member(jsii_name="simulationApplicationCurrentRevisionId")
    def simulation_application_current_revision_id(self) -> str:
        return jsii.get(self, "simulationApplicationCurrentRevisionId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication.RenderingEngineProperty")
    class RenderingEngineProperty(jsii.compat.TypedDict):
        name: str
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty")
    class RobotSoftwareSuiteProperty(jsii.compat.TypedDict):
        name: str
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty")
    class SimulationSoftwareSuiteProperty(jsii.compat.TypedDict):
        name: str
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication.SourceConfigProperty")
    class SourceConfigProperty(jsii.compat.TypedDict):
        architecture: str
        s3Bucket: str
        s3Key: str


class _CfnSimulationApplicationProps(jsii.compat.TypedDict, total=False):
    currentRevisionId: str
    name: str
    tags: typing.Mapping[typing.Any, typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplicationProps")
class CfnSimulationApplicationProps(_CfnSimulationApplicationProps):
    renderingEngine: typing.Union[aws_cdk.cdk.Token, "CfnSimulationApplication.RenderingEngineProperty"]
    robotSoftwareSuite: typing.Union[aws_cdk.cdk.Token, "CfnSimulationApplication.RobotSoftwareSuiteProperty"]
    simulationSoftwareSuite: typing.Union[aws_cdk.cdk.Token, "CfnSimulationApplication.SimulationSoftwareSuiteProperty"]
    sources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSimulationApplication.SourceConfigProperty"]]]

class CfnSimulationApplicationVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplicationVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application: str, current_revision_id: typing.Optional[str]=None) -> None:
        props: CfnSimulationApplicationVersionProps = {"application": application}

        if current_revision_id is not None:
            props["currentRevisionId"] = current_revision_id

        jsii.create(CfnSimulationApplicationVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSimulationApplicationVersionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="simulationApplicationVersionArn")
    def simulation_application_version_arn(self) -> str:
        return jsii.get(self, "simulationApplicationVersionArn")


class _CfnSimulationApplicationVersionProps(jsii.compat.TypedDict, total=False):
    currentRevisionId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplicationVersionProps")
class CfnSimulationApplicationVersionProps(_CfnSimulationApplicationVersionProps):
    application: str

__all__ = ["CfnFleet", "CfnFleetProps", "CfnRobot", "CfnRobotApplication", "CfnRobotApplicationProps", "CfnRobotApplicationVersion", "CfnRobotApplicationVersionProps", "CfnRobotProps", "CfnSimulationApplication", "CfnSimulationApplicationProps", "CfnSimulationApplicationVersion", "CfnSimulationApplicationVersionProps", "__jsii_assembly__"]

publication.publish()
