import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codepipeline-api", "0.26.0", __name__, "aws-codepipeline-api@0.26.0.jsii.tgz")
class Action(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-api.Action"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ActionProxy

    def __init__(self, *, artifact_bounds: "ActionArtifactBounds", category: "ActionCategory", provider: str, configuration: typing.Any=None, owner: typing.Optional[str]=None, region: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, version: typing.Optional[str]=None) -> None:
        props: ActionProps = {"artifactBounds": artifact_bounds, "category": category, "provider": provider}

        if configuration is not None:
            props["configuration"] = configuration

        if owner is not None:
            props["owner"] = owner

        if region is not None:
            props["region"] = region

        if role is not None:
            props["role"] = role

        if version is not None:
            props["version"] = version

        jsii.create(Action, self, [props])

    @jsii.member(jsii_name="addInputArtifact")
    def _add_input_artifact(self, artifact: "Artifact") -> "Action":
        return jsii.invoke(self, "addInputArtifact", [artifact])

    @jsii.member(jsii_name="addOutputArtifact")
    def _add_output_artifact(self, name: str) -> "Artifact":
        return jsii.invoke(self, "addOutputArtifact", [name])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def _bind(self, stage: "IStage", scope: aws_cdk.cdk.Construct) -> None:
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="actionName")
    def action_name(self) -> str:
        return jsii.get(self, "actionName")

    @property
    @jsii.member(jsii_name="category")
    def category(self) -> "ActionCategory":
        return jsii.get(self, "category")

    @property
    @jsii.member(jsii_name="owner")
    def owner(self) -> str:
        return jsii.get(self, "owner")

    @property
    @jsii.member(jsii_name="provider")
    def provider(self) -> str:
        return jsii.get(self, "provider")

    @property
    @jsii.member(jsii_name="runOrder")
    def run_order(self) -> jsii.Number:
        return jsii.get(self, "runOrder")

    @property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> aws_cdk.cdk.Construct:
        return jsii.get(self, "scope")

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        return jsii.get(self, "version")

    @property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> typing.Any:
        return jsii.get(self, "configuration")

    @property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[str]:
        return jsii.get(self, "region")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


class _ActionProxy(Action):
    @jsii.member(jsii_name="bind")
    def _bind(self, stage: "IStage", scope: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [stage, scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-api.ActionArtifactBounds")
class ActionArtifactBounds(jsii.compat.TypedDict):
    maxInputs: jsii.Number
    maxOutputs: jsii.Number
    minInputs: jsii.Number
    minOutputs: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline-api.ActionCategory")
class ActionCategory(enum.Enum):
    Source = "Source"
    Build = "Build"
    Test = "Test"
    Approval = "Approval"
    Deploy = "Deploy"
    Invoke = "Invoke"

class Artifact(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-api.Artifact"):
    def __init__(self, artifact_name: str) -> None:
        jsii.create(Artifact, self, [artifact_name])

    @jsii.member(jsii_name="atPath")
    def at_path(self, file_name: str) -> "ArtifactPath":
        return jsii.invoke(self, "atPath", [file_name])

    @jsii.member(jsii_name="getParam")
    def get_param(self, json_file: str, key_name: str) -> str:
        return jsii.invoke(self, "getParam", [json_file, key_name])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="artifactName")
    def artifact_name(self) -> str:
        return jsii.get(self, "artifactName")

    @property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        return jsii.get(self, "bucketName")

    @property
    @jsii.member(jsii_name="objectKey")
    def object_key(self) -> str:
        return jsii.get(self, "objectKey")

    @property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        return jsii.get(self, "url")


class ArtifactPath(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-api.ArtifactPath"):
    def __init__(self, artifact: "Artifact", file_name: str) -> None:
        jsii.create(ArtifactPath, self, [artifact, file_name])

    @property
    @jsii.member(jsii_name="artifact")
    def artifact(self) -> "Artifact":
        return jsii.get(self, "artifact")

    @property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> str:
        return jsii.get(self, "fileName")

    @property
    @jsii.member(jsii_name="location")
    def location(self) -> str:
        return jsii.get(self, "location")


class BuildAction(Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-api.BuildAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BuildActionProxy

    def __init__(self, *, artifact_bounds: "ActionArtifactBounds", input_artifact: "Artifact", output_artifact_name: str, provider: str, configuration: typing.Any=None, owner: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        props: BuildActionProps = {"artifactBounds": artifact_bounds, "inputArtifact": input_artifact, "outputArtifactName": output_artifact_name, "provider": provider}

        if configuration is not None:
            props["configuration"] = configuration

        if owner is not None:
            props["owner"] = owner

        if version is not None:
            props["version"] = version

        jsii.create(BuildAction, self, [props])

    @property
    @jsii.member(jsii_name="outputArtifact")
    def output_artifact(self) -> "Artifact":
        return jsii.get(self, "outputArtifact")


class _BuildActionProxy(BuildAction, jsii.proxy_for(Action)):
    pass

class _CommonActionProps(jsii.compat.TypedDict, total=False):
    runOrder: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-api.CommonActionProps")
class CommonActionProps(_CommonActionProps):
    actionName: str

class _ActionProps(CommonActionProps, jsii.compat.TypedDict, total=False):
    configuration: typing.Any
    owner: str
    region: str
    role: aws_cdk.aws_iam.IRole
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-api.ActionProps")
class ActionProps(_ActionProps):
    artifactBounds: "ActionArtifactBounds"
    category: "ActionCategory"
    provider: str

class _BuildActionProps(CommonActionProps, jsii.compat.TypedDict, total=False):
    configuration: typing.Any
    owner: str
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-api.BuildActionProps")
class BuildActionProps(_BuildActionProps):
    artifactBounds: "ActionArtifactBounds"
    inputArtifact: "Artifact"
    outputArtifactName: str
    provider: str

class DeployAction(Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-api.DeployAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _DeployActionProxy

    def __init__(self, *, artifact_bounds: "ActionArtifactBounds", input_artifact: "Artifact", provider: str, configuration: typing.Any=None, owner: typing.Optional[str]=None) -> None:
        props: DeployActionProps = {"artifactBounds": artifact_bounds, "inputArtifact": input_artifact, "provider": provider}

        if configuration is not None:
            props["configuration"] = configuration

        if owner is not None:
            props["owner"] = owner

        jsii.create(DeployAction, self, [props])


class _DeployActionProxy(DeployAction, jsii.proxy_for(Action)):
    pass

class _DeployActionProps(CommonActionProps, jsii.compat.TypedDict, total=False):
    configuration: typing.Any
    owner: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-api.DeployActionProps")
class DeployActionProps(_DeployActionProps):
    artifactBounds: "ActionArtifactBounds"
    inputArtifact: "Artifact"
    provider: str

@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline-api.IPipeline")
class IPipeline(aws_cdk.cdk.IConstruct, aws_cdk.aws_events.IEventRuleTarget, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPipelineProxy

    @property
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.Role:
        ...

    @jsii.member(jsii_name="grantBucketRead")
    def grant_bucket_read(self, identity: typing.Optional[aws_cdk.aws_iam.IPrincipal]=None) -> None:
        ...

    @jsii.member(jsii_name="grantBucketReadWrite")
    def grant_bucket_read_write(self, identity: typing.Optional[aws_cdk.aws_iam.IPrincipal]=None) -> None:
        ...


class _IPipelineProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_events.IEventRuleTarget)):
    __jsii_type__ = "@aws-cdk/aws-codepipeline-api.IPipeline"
    @property
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> str:
        return jsii.get(self, "pipelineArn")

    @property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> str:
        return jsii.get(self, "pipelineName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "role")

    @jsii.member(jsii_name="grantBucketRead")
    def grant_bucket_read(self, identity: typing.Optional[aws_cdk.aws_iam.IPrincipal]=None) -> None:
        return jsii.invoke(self, "grantBucketRead", [identity])

    @jsii.member(jsii_name="grantBucketReadWrite")
    def grant_bucket_read_write(self, identity: typing.Optional[aws_cdk.aws_iam.IPrincipal]=None) -> None:
        return jsii.invoke(self, "grantBucketReadWrite", [identity])


@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline-api.IStage")
class IStage(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IStageProxy

    @property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> "IPipeline":
        ...

    @property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        ...

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: "Action") -> None:
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...


class _IStageProxy():
    __jsii_type__ = "@aws-cdk/aws-codepipeline-api.IStage"
    @property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> "IPipeline":
        return jsii.get(self, "pipeline")

    @property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        return jsii.get(self, "stageName")

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: "Action") -> None:
        return jsii.invoke(self, "addAction", [action])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onStateChange", [name, target, options])


class SourceAction(Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-api.SourceAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _SourceActionProxy

    def __init__(self, *, output_artifact_name: str, provider: str, configuration: typing.Any=None, owner: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        props: SourceActionProps = {"outputArtifactName": output_artifact_name, "provider": provider}

        if configuration is not None:
            props["configuration"] = configuration

        if owner is not None:
            props["owner"] = owner

        if version is not None:
            props["version"] = version

        jsii.create(SourceAction, self, [props])

    @property
    @jsii.member(jsii_name="outputArtifact")
    def output_artifact(self) -> "Artifact":
        return jsii.get(self, "outputArtifact")


class _SourceActionProxy(SourceAction, jsii.proxy_for(Action)):
    pass

class _SourceActionProps(CommonActionProps, jsii.compat.TypedDict, total=False):
    configuration: typing.Any
    owner: str
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-api.SourceActionProps")
class SourceActionProps(_SourceActionProps):
    outputArtifactName: str
    provider: str

class TestAction(Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-api.TestAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _TestActionProxy

    def __init__(self, *, artifact_bounds: "ActionArtifactBounds", input_artifact: "Artifact", provider: str, configuration: typing.Any=None, output_artifact_name: typing.Optional[str]=None, owner: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        props: TestActionProps = {"artifactBounds": artifact_bounds, "inputArtifact": input_artifact, "provider": provider}

        if configuration is not None:
            props["configuration"] = configuration

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if owner is not None:
            props["owner"] = owner

        if version is not None:
            props["version"] = version

        jsii.create(TestAction, self, [props])

    @property
    @jsii.member(jsii_name="outputArtifact")
    def output_artifact(self) -> typing.Optional["Artifact"]:
        return jsii.get(self, "outputArtifact")


class _TestActionProxy(TestAction, jsii.proxy_for(Action)):
    pass

class _TestActionProps(CommonActionProps, jsii.compat.TypedDict, total=False):
    configuration: typing.Any
    outputArtifactName: str
    owner: str
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-api.TestActionProps")
class TestActionProps(_TestActionProps):
    artifactBounds: "ActionArtifactBounds"
    inputArtifact: "Artifact"
    provider: str

__all__ = ["Action", "ActionArtifactBounds", "ActionCategory", "ActionProps", "Artifact", "ArtifactPath", "BuildAction", "BuildActionProps", "CommonActionProps", "DeployAction", "DeployActionProps", "IPipeline", "IStage", "SourceAction", "SourceActionProps", "TestAction", "TestActionProps", "__jsii_assembly__"]

publication.publish()
