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
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codepipeline", "0.28.0", __name__, "aws-codepipeline@0.28.0.jsii.tgz")
class Action(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline.Action"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ActionProxy

    def __init__(self, *, artifact_bounds: "ActionArtifactBounds", category: "ActionCategory", provider: str, configuration: typing.Any=None, owner: typing.Optional[str]=None, region: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, version: typing.Optional[str]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: ActionProps = {"artifactBounds": artifact_bounds, "category": category, "provider": provider, "actionName": action_name}

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

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(Action, self, [props])

    @jsii.member(jsii_name="addInputArtifact")
    def _add_input_artifact(self, artifact: "Artifact") -> "Action":
        return jsii.invoke(self, "addInputArtifact", [artifact])

    @jsii.member(jsii_name="addOutputArtifact")
    def _add_output_artifact(self, name: str) -> "Artifact":
        return jsii.invoke(self, "addOutputArtifact", [name])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def _bind(self, *, pipeline: "IPipeline", role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: "IStage") -> None:
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
    @jsii.member(jsii_name="actionInputArtifacts")
    def _action_input_artifacts(self) -> typing.List["Artifact"]:
        return jsii.get(self, "actionInputArtifacts")

    @property
    @jsii.member(jsii_name="actionName")
    def action_name(self) -> str:
        return jsii.get(self, "actionName")

    @property
    @jsii.member(jsii_name="actionOutputArtifacts")
    def _action_output_artifacts(self) -> typing.List["Artifact"]:
        return jsii.get(self, "actionOutputArtifacts")

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
    def _bind(self, *, pipeline: "IPipeline", role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: "IStage") -> None:
        info: ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.ActionArtifactBounds")
class ActionArtifactBounds(jsii.compat.TypedDict):
    maxInputs: jsii.Number
    maxOutputs: jsii.Number
    minInputs: jsii.Number
    minOutputs: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.ActionBind")
class ActionBind(jsii.compat.TypedDict):
    pipeline: "IPipeline"
    role: aws_cdk.aws_iam.IRole
    scope: aws_cdk.cdk.Construct
    stage: "IStage"

@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline.ActionCategory")
class ActionCategory(enum.Enum):
    Source = "Source"
    Build = "Build"
    Test = "Test"
    Approval = "Approval"
    Deploy = "Deploy"
    Invoke = "Invoke"

class Artifact(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.Artifact"):
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


class ArtifactPath(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.ArtifactPath"):
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


class BuildAction(Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline.BuildAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BuildActionProxy

    def __init__(self, *, artifact_bounds: "ActionArtifactBounds", input_artifact: "Artifact", output_artifact_name: str, provider: str, configuration: typing.Any=None, owner: typing.Optional[str]=None, version: typing.Optional[str]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: BuildActionProps = {"artifactBounds": artifact_bounds, "inputArtifact": input_artifact, "outputArtifactName": output_artifact_name, "provider": provider, "actionName": action_name}

        if configuration is not None:
            props["configuration"] = configuration

        if owner is not None:
            props["owner"] = owner

        if version is not None:
            props["version"] = version

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(BuildAction, self, [props])

    @property
    @jsii.member(jsii_name="outputArtifact")
    def output_artifact(self) -> "Artifact":
        return jsii.get(self, "outputArtifact")


class _BuildActionProxy(BuildAction, jsii.proxy_for(Action)):
    pass

class CfnCustomActionType(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, category: str, input_artifact_details: typing.Union[aws_cdk.cdk.Token, "ArtifactDetailsProperty"], output_artifact_details: typing.Union[aws_cdk.cdk.Token, "ArtifactDetailsProperty"], provider: str, configuration_properties: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ConfigurationPropertiesProperty"]]]]=None, settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SettingsProperty"]]=None, version: typing.Optional[str]=None) -> None:
        props: CfnCustomActionTypeProps = {"category": category, "inputArtifactDetails": input_artifact_details, "outputArtifactDetails": output_artifact_details, "provider": provider}

        if configuration_properties is not None:
            props["configurationProperties"] = configuration_properties

        if settings is not None:
            props["settings"] = settings

        if version is not None:
            props["version"] = version

        jsii.create(CfnCustomActionType, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="customActionTypeName")
    def custom_action_type_name(self) -> str:
        return jsii.get(self, "customActionTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCustomActionTypeProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.ArtifactDetailsProperty")
    class ArtifactDetailsProperty(jsii.compat.TypedDict):
        maximumCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minimumCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _ConfigurationPropertiesProperty(jsii.compat.TypedDict, total=False):
        description: str
        queryable: typing.Union[bool, aws_cdk.cdk.Token]
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.ConfigurationPropertiesProperty")
    class ConfigurationPropertiesProperty(_ConfigurationPropertiesProperty):
        key: typing.Union[bool, aws_cdk.cdk.Token]
        name: str
        required: typing.Union[bool, aws_cdk.cdk.Token]
        secret: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.SettingsProperty")
    class SettingsProperty(jsii.compat.TypedDict, total=False):
        entityUrlTemplate: str
        executionUrlTemplate: str
        revisionUrlTemplate: str
        thirdPartyConfigurationUrl: str


class _CfnCustomActionTypeProps(jsii.compat.TypedDict, total=False):
    configurationProperties: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCustomActionType.ConfigurationPropertiesProperty"]]]
    settings: typing.Union[aws_cdk.cdk.Token, "CfnCustomActionType.SettingsProperty"]
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionTypeProps")
class CfnCustomActionTypeProps(_CfnCustomActionTypeProps):
    category: str
    inputArtifactDetails: typing.Union[aws_cdk.cdk.Token, "CfnCustomActionType.ArtifactDetailsProperty"]
    outputArtifactDetails: typing.Union[aws_cdk.cdk.Token, "CfnCustomActionType.ArtifactDetailsProperty"]
    provider: str

class CfnPipeline(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, role_arn: str, stages: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "StageDeclarationProperty"]]], artifact_store: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ArtifactStoreProperty"]]=None, artifact_stores: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ArtifactStoreMapProperty"]]]]=None, disable_inbound_stage_transitions: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "StageTransitionProperty"]]]]=None, name: typing.Optional[str]=None, restart_execution_on_update: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnPipelineProps = {"roleArn": role_arn, "stages": stages}

        if artifact_store is not None:
            props["artifactStore"] = artifact_store

        if artifact_stores is not None:
            props["artifactStores"] = artifact_stores

        if disable_inbound_stage_transitions is not None:
            props["disableInboundStageTransitions"] = disable_inbound_stage_transitions

        if name is not None:
            props["name"] = name

        if restart_execution_on_update is not None:
            props["restartExecutionOnUpdate"] = restart_execution_on_update

        jsii.create(CfnPipeline, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> str:
        return jsii.get(self, "pipelineName")

    @property
    @jsii.member(jsii_name="pipelineVersion")
    def pipeline_version(self) -> str:
        return jsii.get(self, "pipelineVersion")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPipelineProps":
        return jsii.get(self, "propertyOverrides")

    class _ActionDeclarationProperty(jsii.compat.TypedDict, total=False):
        configuration: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        inputArtifacts: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.InputArtifactProperty"]]]
        outputArtifacts: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.OutputArtifactProperty"]]]
        region: str
        roleArn: str
        runOrder: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ActionDeclarationProperty")
    class ActionDeclarationProperty(_ActionDeclarationProperty):
        actionTypeId: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ActionTypeIdProperty"]
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ActionTypeIdProperty")
    class ActionTypeIdProperty(jsii.compat.TypedDict):
        category: str
        owner: str
        provider: str
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ArtifactStoreMapProperty")
    class ArtifactStoreMapProperty(jsii.compat.TypedDict):
        artifactStore: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ArtifactStoreProperty"]
        region: str

    class _ArtifactStoreProperty(jsii.compat.TypedDict, total=False):
        encryptionKey: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.EncryptionKeyProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ArtifactStoreProperty")
    class ArtifactStoreProperty(_ArtifactStoreProperty):
        location: str
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.BlockerDeclarationProperty")
    class BlockerDeclarationProperty(jsii.compat.TypedDict):
        name: str
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.EncryptionKeyProperty")
    class EncryptionKeyProperty(jsii.compat.TypedDict):
        id: str
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.InputArtifactProperty")
    class InputArtifactProperty(jsii.compat.TypedDict):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.OutputArtifactProperty")
    class OutputArtifactProperty(jsii.compat.TypedDict):
        name: str

    class _StageDeclarationProperty(jsii.compat.TypedDict, total=False):
        blockers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.BlockerDeclarationProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.StageDeclarationProperty")
    class StageDeclarationProperty(_StageDeclarationProperty):
        actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ActionDeclarationProperty"]]]
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.StageTransitionProperty")
    class StageTransitionProperty(jsii.compat.TypedDict):
        reason: str
        stageName: str


class _CfnPipelineProps(jsii.compat.TypedDict, total=False):
    artifactStore: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ArtifactStoreProperty"]
    artifactStores: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ArtifactStoreMapProperty"]]]
    disableInboundStageTransitions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.StageTransitionProperty"]]]
    name: str
    restartExecutionOnUpdate: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipelineProps")
class CfnPipelineProps(_CfnPipelineProps):
    roleArn: str
    stages: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.StageDeclarationProperty"]]]

class CfnWebhook(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authentication: str, authentication_configuration: typing.Union[aws_cdk.cdk.Token, "WebhookAuthConfigurationProperty"], filters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "WebhookFilterRuleProperty"]]], target_action: str, target_pipeline: str, target_pipeline_version: typing.Union[jsii.Number, aws_cdk.cdk.Token], name: typing.Optional[str]=None, register_with_third_party: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnWebhookProps = {"authentication": authentication, "authenticationConfiguration": authentication_configuration, "filters": filters, "targetAction": target_action, "targetPipeline": target_pipeline, "targetPipelineVersion": target_pipeline_version}

        if name is not None:
            props["name"] = name

        if register_with_third_party is not None:
            props["registerWithThirdParty"] = register_with_third_party

        jsii.create(CfnWebhook, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnWebhookProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="webhookName")
    def webhook_name(self) -> str:
        return jsii.get(self, "webhookName")

    @property
    @jsii.member(jsii_name="webhookUrl")
    def webhook_url(self) -> str:
        return jsii.get(self, "webhookUrl")

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook.WebhookAuthConfigurationProperty")
    class WebhookAuthConfigurationProperty(jsii.compat.TypedDict, total=False):
        allowedIpRange: str
        secretToken: str

    class _WebhookFilterRuleProperty(jsii.compat.TypedDict, total=False):
        matchEquals: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook.WebhookFilterRuleProperty")
    class WebhookFilterRuleProperty(_WebhookFilterRuleProperty):
        jsonPath: str


class _CfnWebhookProps(jsii.compat.TypedDict, total=False):
    name: str
    registerWithThirdParty: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnWebhookProps")
class CfnWebhookProps(_CfnWebhookProps):
    authentication: str
    authenticationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnWebhook.WebhookAuthConfigurationProperty"]
    filters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnWebhook.WebhookFilterRuleProperty"]]]
    targetAction: str
    targetPipeline: str
    targetPipelineVersion: typing.Union[jsii.Number, aws_cdk.cdk.Token]

class _CommonActionProps(jsii.compat.TypedDict, total=False):
    runOrder: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CommonActionProps")
class CommonActionProps(_CommonActionProps):
    actionName: str

class _ActionProps(CommonActionProps, jsii.compat.TypedDict, total=False):
    configuration: typing.Any
    owner: str
    region: str
    role: aws_cdk.aws_iam.IRole
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.ActionProps")
class ActionProps(_ActionProps):
    artifactBounds: "ActionArtifactBounds"
    category: "ActionCategory"
    provider: str

class _BuildActionProps(CommonActionProps, jsii.compat.TypedDict, total=False):
    configuration: typing.Any
    owner: str
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.BuildActionProps")
class BuildActionProps(_BuildActionProps):
    artifactBounds: "ActionArtifactBounds"
    inputArtifact: "Artifact"
    outputArtifactName: str
    provider: str

class CrossRegionScaffoldStack(aws_cdk.cdk.Stack, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.CrossRegionScaffoldStack"):
    def __init__(self, scope: aws_cdk.cdk.App, *, account: str, region: str) -> None:
        props: CrossRegionScaffoldStackProps = {"account": account, "region": region}

        jsii.create(CrossRegionScaffoldStack, self, [scope, props])

    @property
    @jsii.member(jsii_name="replicationBucketName")
    def replication_bucket_name(self) -> str:
        return jsii.get(self, "replicationBucketName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CrossRegionScaffoldStackProps")
class CrossRegionScaffoldStackProps(jsii.compat.TypedDict):
    account: str
    region: str

class DeployAction(Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline.DeployAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _DeployActionProxy

    def __init__(self, *, artifact_bounds: "ActionArtifactBounds", input_artifact: "Artifact", provider: str, configuration: typing.Any=None, owner: typing.Optional[str]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: DeployActionProps = {"artifactBounds": artifact_bounds, "inputArtifact": input_artifact, "provider": provider, "actionName": action_name}

        if configuration is not None:
            props["configuration"] = configuration

        if owner is not None:
            props["owner"] = owner

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(DeployAction, self, [props])


class _DeployActionProxy(DeployAction, jsii.proxy_for(Action)):
    pass

class _DeployActionProps(CommonActionProps, jsii.compat.TypedDict, total=False):
    configuration: typing.Any
    owner: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.DeployActionProps")
class DeployActionProps(_DeployActionProps):
    artifactBounds: "ActionArtifactBounds"
    inputArtifact: "Artifact"
    provider: str

@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IPipeline")
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

    @jsii.member(jsii_name="grantBucketRead")
    def grant_bucket_read(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantBucketReadWrite")
    def grant_bucket_read_write(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...


class _IPipelineProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_events.IEventRuleTarget)):
    __jsii_type__ = "@aws-cdk/aws-codepipeline.IPipeline"
    @property
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> str:
        return jsii.get(self, "pipelineArn")

    @property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> str:
        return jsii.get(self, "pipelineName")

    @jsii.member(jsii_name="grantBucketRead")
    def grant_bucket_read(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantBucketRead", [identity])

    @jsii.member(jsii_name="grantBucketReadWrite")
    def grant_bucket_read_write(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantBucketReadWrite", [identity])


@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IStage")
class IStage(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IStageProxy

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
    __jsii_type__ = "@aws-cdk/aws-codepipeline.IStage"
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


@jsii.implements(IPipeline)
class Pipeline(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.Pipeline"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, artifact_bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, cross_region_replication_buckets: typing.Optional[typing.Mapping[str,str]]=None, pipeline_name: typing.Optional[str]=None, restart_execution_on_update: typing.Optional[bool]=None, stages: typing.Optional[typing.List["StageProps"]]=None) -> None:
        props: PipelineProps = {}

        if artifact_bucket is not None:
            props["artifactBucket"] = artifact_bucket

        if cross_region_replication_buckets is not None:
            props["crossRegionReplicationBuckets"] = cross_region_replication_buckets

        if pipeline_name is not None:
            props["pipelineName"] = pipeline_name

        if restart_execution_on_update is not None:
            props["restartExecutionOnUpdate"] = restart_execution_on_update

        if stages is not None:
            props["stages"] = stages

        jsii.create(Pipeline, self, [scope, id, props])

    @jsii.member(jsii_name="addStage")
    def add_stage(self, *, placement: typing.Optional["StagePlacement"]=None, name: str, actions: typing.Optional[typing.List["Action"]]=None) -> "IStage":
        props: StageAddToPipelineProps = {"name": name}

        if placement is not None:
            props["placement"] = placement

        if actions is not None:
            props["actions"] = actions

        return jsii.invoke(self, "addStage", [props])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @jsii.member(jsii_name="grantBucketRead")
    def grant_bucket_read(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantBucketRead", [identity])

    @jsii.member(jsii_name="grantBucketReadWrite")
    def grant_bucket_read_write(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantBucketReadWrite", [identity])

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
    @jsii.member(jsii_name="artifactBucket")
    def artifact_bucket(self) -> aws_cdk.aws_s3.IBucket:
        return jsii.get(self, "artifactBucket")

    @property
    @jsii.member(jsii_name="crossRegionScaffoldStacks")
    def cross_region_scaffold_stacks(self) -> typing.Mapping[str,"CrossRegionScaffoldStack"]:
        return jsii.get(self, "crossRegionScaffoldStacks")

    @property
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> str:
        return jsii.get(self, "pipelineArn")

    @property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> str:
        return jsii.get(self, "pipelineName")

    @property
    @jsii.member(jsii_name="pipelineVersion")
    def pipeline_version(self) -> str:
        return jsii.get(self, "pipelineVersion")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "role")

    @property
    @jsii.member(jsii_name="stageCount")
    def stage_count(self) -> jsii.Number:
        return jsii.get(self, "stageCount")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.PipelineProps")
class PipelineProps(jsii.compat.TypedDict, total=False):
    artifactBucket: aws_cdk.aws_s3.IBucket
    crossRegionReplicationBuckets: typing.Mapping[str,str]
    pipelineName: str
    restartExecutionOnUpdate: bool
    stages: typing.List["StageProps"]

class SourceAction(Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline.SourceAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _SourceActionProxy

    def __init__(self, *, output_artifact_name: str, provider: str, configuration: typing.Any=None, owner: typing.Optional[str]=None, version: typing.Optional[str]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: SourceActionProps = {"outputArtifactName": output_artifact_name, "provider": provider, "actionName": action_name}

        if configuration is not None:
            props["configuration"] = configuration

        if owner is not None:
            props["owner"] = owner

        if version is not None:
            props["version"] = version

        if run_order is not None:
            props["runOrder"] = run_order

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

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.SourceActionProps")
class SourceActionProps(_SourceActionProps):
    outputArtifactName: str
    provider: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StagePlacement")
class StagePlacement(jsii.compat.TypedDict, total=False):
    atIndex: jsii.Number
    justAfter: "IStage"
    rightBefore: "IStage"

class _StageProps(jsii.compat.TypedDict, total=False):
    actions: typing.List["Action"]

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StageProps")
class StageProps(_StageProps):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StageAddToPipelineProps")
class StageAddToPipelineProps(StageProps, jsii.compat.TypedDict, total=False):
    placement: "StagePlacement"

class TestAction(Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline.TestAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _TestActionProxy

    def __init__(self, *, artifact_bounds: "ActionArtifactBounds", input_artifact: "Artifact", provider: str, configuration: typing.Any=None, output_artifact_name: typing.Optional[str]=None, owner: typing.Optional[str]=None, version: typing.Optional[str]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: TestActionProps = {"artifactBounds": artifact_bounds, "inputArtifact": input_artifact, "provider": provider, "actionName": action_name}

        if configuration is not None:
            props["configuration"] = configuration

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if owner is not None:
            props["owner"] = owner

        if version is not None:
            props["version"] = version

        if run_order is not None:
            props["runOrder"] = run_order

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

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.TestActionProps")
class TestActionProps(_TestActionProps):
    artifactBounds: "ActionArtifactBounds"
    inputArtifact: "Artifact"
    provider: str

__all__ = ["Action", "ActionArtifactBounds", "ActionBind", "ActionCategory", "ActionProps", "Artifact", "ArtifactPath", "BuildAction", "BuildActionProps", "CfnCustomActionType", "CfnCustomActionTypeProps", "CfnPipeline", "CfnPipelineProps", "CfnWebhook", "CfnWebhookProps", "CommonActionProps", "CrossRegionScaffoldStack", "CrossRegionScaffoldStackProps", "DeployAction", "DeployActionProps", "IPipeline", "IStage", "Pipeline", "PipelineProps", "SourceAction", "SourceActionProps", "StageAddToPipelineProps", "StagePlacement", "StageProps", "TestAction", "TestActionProps", "__jsii_assembly__"]

publication.publish()
