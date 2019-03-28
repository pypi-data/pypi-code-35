import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_codepipeline_api
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codepipeline", "0.26.0", __name__, "aws-codepipeline@0.26.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.BasicJenkinsActionProps")
class BasicJenkinsActionProps(aws_cdk.aws_codepipeline_api.CommonActionProps, jsii.compat.TypedDict):
    inputArtifact: aws_cdk.aws_codepipeline_api.Artifact
    projectName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.BasicJenkinsBuildActionProps")
class BasicJenkinsBuildActionProps(BasicJenkinsActionProps, jsii.compat.TypedDict, total=False):
    outputArtifactName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.BasicJenkinsTestActionProps")
class BasicJenkinsTestActionProps(BasicJenkinsActionProps, jsii.compat.TypedDict, total=False):
    outputArtifactName: str

class CfnCustomActionType(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, category: str, input_artifact_details: typing.Union["ArtifactDetailsProperty", aws_cdk.cdk.Token], output_artifact_details: typing.Union["ArtifactDetailsProperty", aws_cdk.cdk.Token], provider: str, configuration_properties: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ConfigurationPropertiesProperty"]]]]=None, settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SettingsProperty"]]=None, version: typing.Optional[str]=None) -> None:
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
    inputArtifactDetails: typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.cdk.Token]
    outputArtifactDetails: typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.cdk.Token]
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

class GitHubSourceAction(aws_cdk.aws_codepipeline_api.SourceAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.GitHubSourceAction"):
    def __init__(self, *, oauth_token: aws_cdk.cdk.Secret, output_artifact_name: str, owner: str, repo: str, branch: typing.Optional[str]=None, poll_for_source_changes: typing.Optional[bool]=None) -> None:
        props: GitHubSourceActionProps = {"oauthToken": oauth_token, "outputArtifactName": output_artifact_name, "owner": owner, "repo": repo}

        if branch is not None:
            props["branch"] = branch

        if poll_for_source_changes is not None:
            props["pollForSourceChanges"] = poll_for_source_changes

        jsii.create(GitHubSourceAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, stage: aws_cdk.aws_codepipeline_api.IStage, scope: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [stage, scope])


class _GitHubSourceActionProps(aws_cdk.aws_codepipeline_api.CommonActionProps, jsii.compat.TypedDict, total=False):
    branch: str
    pollForSourceChanges: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.GitHubSourceActionProps")
class GitHubSourceActionProps(_GitHubSourceActionProps):
    oauthToken: aws_cdk.cdk.Secret
    outputArtifactName: str
    owner: str
    repo: str

@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IJenkinsProvider")
class IJenkinsProvider(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IJenkinsProviderProxy

    @property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        ...

    @jsii.member(jsii_name="toCodePipelineBuildAction")
    def to_code_pipeline_build_action(self, *, output_artifact_name: typing.Optional[str]=None) -> "JenkinsBuildAction":
        ...

    @jsii.member(jsii_name="toCodePipelineTestAction")
    def to_code_pipeline_test_action(self, *, output_artifact_name: typing.Optional[str]=None) -> "JenkinsTestAction":
        ...


class _IJenkinsProviderProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-codepipeline.IJenkinsProvider"
    @property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        return jsii.get(self, "providerName")

    @property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        return jsii.get(self, "serverUrl")

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        return jsii.get(self, "version")

    @jsii.member(jsii_name="toCodePipelineBuildAction")
    def to_code_pipeline_build_action(self, *, output_artifact_name: typing.Optional[str]=None) -> "JenkinsBuildAction":
        props: BasicJenkinsBuildActionProps = {}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        return jsii.invoke(self, "toCodePipelineBuildAction", [props])

    @jsii.member(jsii_name="toCodePipelineTestAction")
    def to_code_pipeline_test_action(self, *, output_artifact_name: typing.Optional[str]=None) -> "JenkinsTestAction":
        props: BasicJenkinsTestActionProps = {}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        return jsii.invoke(self, "toCodePipelineTestAction", [props])


@jsii.implements(IJenkinsProvider)
class BaseJenkinsProvider(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline.BaseJenkinsProvider"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseJenkinsProviderProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, version: typing.Optional[str]=None) -> None:
        jsii.create(BaseJenkinsProvider, self, [scope, id, version])

    @jsii.member(jsii_name="export")
    def export(self) -> "JenkinsProviderImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="toCodePipelineBuildAction")
    def to_code_pipeline_build_action(self, *, output_artifact_name: typing.Optional[str]=None) -> "JenkinsBuildAction":
        props: BasicJenkinsBuildActionProps = {}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        return jsii.invoke(self, "toCodePipelineBuildAction", [props])

    @jsii.member(jsii_name="toCodePipelineTestAction")
    def to_code_pipeline_test_action(self, *, output_artifact_name: typing.Optional[str]=None) -> "JenkinsTestAction":
        props: BasicJenkinsTestActionProps = {}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        return jsii.invoke(self, "toCodePipelineTestAction", [props])

    @property
    @jsii.member(jsii_name="providerName")
    @abc.abstractmethod
    def provider_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="serverUrl")
    @abc.abstractmethod
    def server_url(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        return jsii.get(self, "version")


class _BaseJenkinsProviderProxy(BaseJenkinsProvider):
    @property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        return jsii.get(self, "providerName")

    @property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        return jsii.get(self, "serverUrl")


class JenkinsBuildAction(aws_cdk.aws_codepipeline_api.BuildAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.JenkinsBuildAction"):
    def __init__(self, *, jenkins_provider: "IJenkinsProvider") -> None:
        props: JenkinsBuildActionProps = {"jenkinsProvider": jenkins_provider}

        jsii.create(JenkinsBuildAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, _stage: aws_cdk.aws_codepipeline_api.IStage, _scope: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [_stage, _scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.JenkinsBuildActionProps")
class JenkinsBuildActionProps(BasicJenkinsBuildActionProps, jsii.compat.TypedDict):
    jenkinsProvider: "IJenkinsProvider"

class JenkinsProvider(BaseJenkinsProvider, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.JenkinsProvider"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, provider_name: str, server_url: str, for_build: typing.Optional[bool]=None, for_test: typing.Optional[bool]=None, version: typing.Optional[str]=None) -> None:
        props: JenkinsProviderProps = {"providerName": provider_name, "serverUrl": server_url}

        if for_build is not None:
            props["forBuild"] = for_build

        if for_test is not None:
            props["forTest"] = for_test

        if version is not None:
            props["version"] = version

        jsii.create(JenkinsProvider, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, provider_name: str, server_url: str, version: typing.Optional[str]=None) -> "IJenkinsProvider":
        props: JenkinsProviderImportProps = {"providerName": provider_name, "serverUrl": server_url}

        if version is not None:
            props["version"] = version

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        return jsii.get(self, "providerName")

    @property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        return jsii.get(self, "serverUrl")


class _JenkinsProviderImportProps(jsii.compat.TypedDict, total=False):
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.JenkinsProviderImportProps")
class JenkinsProviderImportProps(_JenkinsProviderImportProps):
    providerName: str
    serverUrl: str

class _JenkinsProviderProps(jsii.compat.TypedDict, total=False):
    forBuild: bool
    forTest: bool
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.JenkinsProviderProps")
class JenkinsProviderProps(_JenkinsProviderProps):
    providerName: str
    serverUrl: str

class JenkinsTestAction(aws_cdk.aws_codepipeline_api.TestAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.JenkinsTestAction"):
    def __init__(self, *, jenkins_provider: "IJenkinsProvider") -> None:
        props: JenkinsTestActionProps = {"jenkinsProvider": jenkins_provider}

        jsii.create(JenkinsTestAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, _stage: aws_cdk.aws_codepipeline_api.IStage, _scope: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [_stage, _scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.JenkinsTestActionProps")
class JenkinsTestActionProps(BasicJenkinsTestActionProps, jsii.compat.TypedDict):
    jenkinsProvider: "IJenkinsProvider"

class ManualApprovalAction(aws_cdk.aws_codepipeline_api.Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.ManualApprovalAction"):
    def __init__(self, *, additional_information: typing.Optional[str]=None, notification_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, notify_emails: typing.Optional[typing.List[str]]=None) -> None:
        props: ManualApprovalActionProps = {}

        if additional_information is not None:
            props["additionalInformation"] = additional_information

        if notification_topic is not None:
            props["notificationTopic"] = notification_topic

        if notify_emails is not None:
            props["notifyEmails"] = notify_emails

        jsii.create(ManualApprovalAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, stage: aws_cdk.aws_codepipeline_api.IStage, scope: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [stage, scope])

    @property
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        return jsii.get(self, "notificationTopic")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.ManualApprovalActionProps")
class ManualApprovalActionProps(aws_cdk.aws_codepipeline_api.CommonActionProps, jsii.compat.TypedDict, total=False):
    additionalInformation: str
    notificationTopic: aws_cdk.aws_sns.ITopic
    notifyEmails: typing.List[str]

@jsii.implements(aws_cdk.aws_codepipeline_api.IPipeline)
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
    def add_stage(self, *, placement: typing.Optional["StagePlacement"]=None) -> aws_cdk.aws_codepipeline_api.IStage:
        props: StageAddToPipelineProps = {}

        if placement is not None:
            props["placement"] = placement

        return jsii.invoke(self, "addStage", [props])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @jsii.member(jsii_name="grantBucketRead")
    def grant_bucket_read(self, identity: typing.Optional[aws_cdk.aws_iam.IPrincipal]=None) -> None:
        return jsii.invoke(self, "grantBucketRead", [identity])

    @jsii.member(jsii_name="grantBucketReadWrite")
    def grant_bucket_read_write(self, identity: typing.Optional[aws_cdk.aws_iam.IPrincipal]=None) -> None:
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

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StagePlacement")
class StagePlacement(jsii.compat.TypedDict, total=False):
    atIndex: jsii.Number
    justAfter: aws_cdk.aws_codepipeline_api.IStage
    rightBefore: aws_cdk.aws_codepipeline_api.IStage

class _StageProps(jsii.compat.TypedDict, total=False):
    actions: typing.List[aws_cdk.aws_codepipeline_api.Action]

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StageProps")
class StageProps(_StageProps):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StageAddToPipelineProps")
class StageAddToPipelineProps(StageProps, jsii.compat.TypedDict, total=False):
    placement: "StagePlacement"

__all__ = ["BaseJenkinsProvider", "BasicJenkinsActionProps", "BasicJenkinsBuildActionProps", "BasicJenkinsTestActionProps", "CfnCustomActionType", "CfnCustomActionTypeProps", "CfnPipeline", "CfnPipelineProps", "CfnWebhook", "CfnWebhookProps", "CrossRegionScaffoldStack", "CrossRegionScaffoldStackProps", "GitHubSourceAction", "GitHubSourceActionProps", "IJenkinsProvider", "JenkinsBuildAction", "JenkinsBuildActionProps", "JenkinsProvider", "JenkinsProviderImportProps", "JenkinsProviderProps", "JenkinsTestAction", "JenkinsTestActionProps", "ManualApprovalAction", "ManualApprovalActionProps", "Pipeline", "PipelineProps", "StageAddToPipelineProps", "StagePlacement", "StageProps", "__jsii_assembly__"]

publication.publish()
