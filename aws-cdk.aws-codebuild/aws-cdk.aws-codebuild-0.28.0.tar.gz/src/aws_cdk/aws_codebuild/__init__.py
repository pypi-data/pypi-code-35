import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.assets
import aws_cdk.assets_docker
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_codecommit
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codebuild", "0.28.0", __name__, "aws-codebuild@0.28.0.jsii.tgz")
class BuildArtifacts(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.BuildArtifacts"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BuildArtifactsProxy

    def __init__(self, *, identifier: typing.Optional[str]=None) -> None:
        props: BuildArtifactsProps = {}

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(BuildArtifacts, self, [props])

    @jsii.member(jsii_name="toArtifactsJSON")
    def to_artifacts_json(self) -> "CfnProject.ArtifactsProperty":
        return jsii.invoke(self, "toArtifactsJSON", [])

    @jsii.member(jsii_name="toArtifactsProperty")
    def _to_artifacts_property(self) -> typing.Any:
        return jsii.invoke(self, "toArtifactsProperty", [])

    @property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def _type(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        return jsii.get(self, "identifier")


class _BuildArtifactsProxy(BuildArtifacts):
    @property
    @jsii.member(jsii_name="type")
    def _type(self) -> str:
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BuildArtifactsProps")
class BuildArtifactsProps(jsii.compat.TypedDict, total=False):
    identifier: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BuildEnvironment")
class BuildEnvironment(jsii.compat.TypedDict, total=False):
    buildImage: "IBuildImage"
    computeType: "ComputeType"
    environmentVariables: typing.Mapping[str,"BuildEnvironmentVariable"]
    privileged: bool

class _BuildEnvironmentVariable(jsii.compat.TypedDict, total=False):
    type: "BuildEnvironmentVariableType"

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BuildEnvironmentVariable")
class BuildEnvironmentVariable(_BuildEnvironmentVariable):
    value: typing.Any

@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.BuildEnvironmentVariableType")
class BuildEnvironmentVariableType(enum.Enum):
    PlainText = "PlainText"
    ParameterStore = "ParameterStore"

class BuildSource(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.BuildSource"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BuildSourceProxy

    def __init__(self, *, identifier: typing.Optional[str]=None) -> None:
        props: BuildSourceProps = {}

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(BuildSource, self, [props])

    @jsii.member(jsii_name="buildTriggers")
    def build_triggers(self) -> typing.Optional["CfnProject.ProjectTriggersProperty"]:
        return jsii.invoke(self, "buildTriggers", [])

    @jsii.member(jsii_name="toSourceJSON")
    def to_source_json(self) -> "CfnProject.SourceProperty":
        return jsii.invoke(self, "toSourceJSON", [])

    @jsii.member(jsii_name="toSourceProperty")
    def _to_source_property(self) -> typing.Any:
        return jsii.invoke(self, "toSourceProperty", [])

    @property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> "SourceType":
        ...

    @property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        return jsii.get(self, "identifier")


class _BuildSourceProxy(BuildSource):
    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceType":
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BuildSourceProps")
class BuildSourceProps(jsii.compat.TypedDict, total=False):
    identifier: str

class CfnProject(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.CfnProject"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, artifacts: typing.Union["ArtifactsProperty", aws_cdk.cdk.Token], environment: typing.Union[aws_cdk.cdk.Token, "EnvironmentProperty"], service_role: str, source: typing.Union["SourceProperty", aws_cdk.cdk.Token], badge_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, cache: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ProjectCacheProperty"]]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[str]=None, logs_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LogsConfigProperty"]]=None, name: typing.Optional[str]=None, queued_timeout_in_minutes: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, secondary_artifacts: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ArtifactsProperty", aws_cdk.cdk.Token]]]]=None, secondary_sources: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["SourceProperty", aws_cdk.cdk.Token]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, timeout_in_minutes: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, triggers: typing.Optional[typing.Union["ProjectTriggersProperty", aws_cdk.cdk.Token]]=None, vpc_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "VpcConfigProperty"]]=None) -> None:
        props: CfnProjectProps = {"artifacts": artifacts, "environment": environment, "serviceRole": service_role, "source": source}

        if badge_enabled is not None:
            props["badgeEnabled"] = badge_enabled

        if cache is not None:
            props["cache"] = cache

        if description is not None:
            props["description"] = description

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if logs_config is not None:
            props["logsConfig"] = logs_config

        if name is not None:
            props["name"] = name

        if queued_timeout_in_minutes is not None:
            props["queuedTimeoutInMinutes"] = queued_timeout_in_minutes

        if secondary_artifacts is not None:
            props["secondaryArtifacts"] = secondary_artifacts

        if secondary_sources is not None:
            props["secondarySources"] = secondary_sources

        if tags is not None:
            props["tags"] = tags

        if timeout_in_minutes is not None:
            props["timeoutInMinutes"] = timeout_in_minutes

        if triggers is not None:
            props["triggers"] = triggers

        if vpc_config is not None:
            props["vpcConfig"] = vpc_config

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

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _ArtifactsProperty(jsii.compat.TypedDict, total=False):
        artifactIdentifier: str
        encryptionDisabled: typing.Union[bool, aws_cdk.cdk.Token]
        location: str
        name: str
        namespaceType: str
        overrideArtifactName: typing.Union[bool, aws_cdk.cdk.Token]
        packaging: str
        path: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.ArtifactsProperty")
    class ArtifactsProperty(_ArtifactsProperty):
        type: str

    class _CloudWatchLogsConfigProperty(jsii.compat.TypedDict, total=False):
        groupName: str
        streamName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.CloudWatchLogsConfigProperty")
    class CloudWatchLogsConfigProperty(_CloudWatchLogsConfigProperty):
        status: str

    class _EnvironmentProperty(jsii.compat.TypedDict, total=False):
        certificate: str
        environmentVariables: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnProject.EnvironmentVariableProperty"]]]
        imagePullCredentialsType: str
        privilegedMode: typing.Union[bool, aws_cdk.cdk.Token]
        registryCredential: typing.Union[aws_cdk.cdk.Token, "CfnProject.RegistryCredentialProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.EnvironmentProperty")
    class EnvironmentProperty(_EnvironmentProperty):
        computeType: str
        image: str
        type: str

    class _EnvironmentVariableProperty(jsii.compat.TypedDict, total=False):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.EnvironmentVariableProperty")
    class EnvironmentVariableProperty(_EnvironmentVariableProperty):
        name: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.GitSubmodulesConfigProperty")
    class GitSubmodulesConfigProperty(jsii.compat.TypedDict):
        fetchSubmodules: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.LogsConfigProperty")
    class LogsConfigProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLogs: typing.Union[aws_cdk.cdk.Token, "CfnProject.CloudWatchLogsConfigProperty"]
        s3Logs: typing.Union[aws_cdk.cdk.Token, "CfnProject.S3LogsConfigProperty"]

    class _ProjectCacheProperty(jsii.compat.TypedDict, total=False):
        location: str
        modes: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectCacheProperty")
    class ProjectCacheProperty(_ProjectCacheProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectTriggersProperty")
    class ProjectTriggersProperty(jsii.compat.TypedDict, total=False):
        filterGroups: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnProject.WebhookFilterProperty"]]]]]
        webhook: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.RegistryCredentialProperty")
    class RegistryCredentialProperty(jsii.compat.TypedDict):
        credential: str
        credentialProvider: str

    class _S3LogsConfigProperty(jsii.compat.TypedDict, total=False):
        encryptionDisabled: typing.Union[bool, aws_cdk.cdk.Token]
        location: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.S3LogsConfigProperty")
    class S3LogsConfigProperty(_S3LogsConfigProperty):
        status: str

    class _SourceAuthProperty(jsii.compat.TypedDict, total=False):
        resource: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.SourceAuthProperty")
    class SourceAuthProperty(_SourceAuthProperty):
        type: str

    class _SourceProperty(jsii.compat.TypedDict, total=False):
        auth: typing.Union[aws_cdk.cdk.Token, "CfnProject.SourceAuthProperty"]
        buildSpec: str
        gitCloneDepth: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        gitSubmodulesConfig: typing.Union[aws_cdk.cdk.Token, "CfnProject.GitSubmodulesConfigProperty"]
        insecureSsl: typing.Union[bool, aws_cdk.cdk.Token]
        location: str
        reportBuildStatus: typing.Union[bool, aws_cdk.cdk.Token]
        sourceIdentifier: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.SourceProperty")
    class SourceProperty(_SourceProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.VpcConfigProperty")
    class VpcConfigProperty(jsii.compat.TypedDict, total=False):
        securityGroupIds: typing.List[str]
        subnets: typing.List[str]
        vpcId: str

    class _WebhookFilterProperty(jsii.compat.TypedDict, total=False):
        excludeMatchedPattern: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.WebhookFilterProperty")
    class WebhookFilterProperty(_WebhookFilterProperty):
        pattern: str
        type: str


class _CfnProjectProps(jsii.compat.TypedDict, total=False):
    badgeEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    cache: typing.Union[aws_cdk.cdk.Token, "CfnProject.ProjectCacheProperty"]
    description: str
    encryptionKey: str
    logsConfig: typing.Union[aws_cdk.cdk.Token, "CfnProject.LogsConfigProperty"]
    name: str
    queuedTimeoutInMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    secondaryArtifacts: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnProject.ArtifactsProperty", aws_cdk.cdk.Token]]]
    secondarySources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnProject.SourceProperty", aws_cdk.cdk.Token]]]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    timeoutInMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    triggers: typing.Union["CfnProject.ProjectTriggersProperty", aws_cdk.cdk.Token]
    vpcConfig: typing.Union[aws_cdk.cdk.Token, "CfnProject.VpcConfigProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProjectProps")
class CfnProjectProps(_CfnProjectProps):
    artifacts: typing.Union["CfnProject.ArtifactsProperty", aws_cdk.cdk.Token]
    environment: typing.Union[aws_cdk.cdk.Token, "CfnProject.EnvironmentProperty"]
    serviceRole: str
    source: typing.Union["CfnProject.SourceProperty", aws_cdk.cdk.Token]

class CodePipelineBuildArtifacts(BuildArtifacts, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.CodePipelineBuildArtifacts"):
    def __init__(self) -> None:
        jsii.create(CodePipelineBuildArtifacts, self, [])

    @property
    @jsii.member(jsii_name="type")
    def _type(self) -> str:
        return jsii.get(self, "type")


class CodePipelineSource(BuildSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.CodePipelineSource"):
    def __init__(self) -> None:
        jsii.create(CodePipelineSource, self, [])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceType":
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CommonProjectProps")
class CommonProjectProps(jsii.compat.TypedDict, total=False):
    allowAllOutbound: bool
    badge: bool
    buildScriptAsset: aws_cdk.assets.Asset
    buildScriptAssetEntrypoint: str
    buildSpec: typing.Any
    cacheBucket: aws_cdk.aws_s3.IBucket
    cacheDir: str
    description: str
    encryptionKey: aws_cdk.aws_kms.IEncryptionKey
    environment: "BuildEnvironment"
    environmentVariables: typing.Mapping[str,"BuildEnvironmentVariable"]
    projectName: str
    role: aws_cdk.aws_iam.IRole
    securityGroups: typing.List[aws_cdk.aws_ec2.ISecurityGroup]
    subnetSelection: aws_cdk.aws_ec2.SubnetSelection
    timeout: jsii.Number
    vpc: aws_cdk.aws_ec2.IVpcNetwork

@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.ComputeType")
class ComputeType(enum.Enum):
    Small = "Small"
    Medium = "Medium"
    Large = "Large"

class GitBuildSource(BuildSource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.GitBuildSource"):
    @staticmethod
    def __jsii_proxy_class__():
        return _GitBuildSourceProxy

    def __init__(self, *, clone_depth: typing.Optional[jsii.Number]=None, identifier: typing.Optional[str]=None) -> None:
        props: GitBuildSourceProps = {}

        if clone_depth is not None:
            props["cloneDepth"] = clone_depth

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(GitBuildSource, self, [props])

    @jsii.member(jsii_name="toSourceJSON")
    def to_source_json(self) -> "CfnProject.SourceProperty":
        return jsii.invoke(self, "toSourceJSON", [])


class _GitBuildSourceProxy(GitBuildSource, jsii.proxy_for(BuildSource)):
    pass

class BitBucketSource(GitBuildSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.BitBucketSource"):
    def __init__(self, *, owner: str, repo: str, clone_depth: typing.Optional[jsii.Number]=None, identifier: typing.Optional[str]=None) -> None:
        props: BitBucketSourceProps = {"owner": owner, "repo": repo}

        if clone_depth is not None:
            props["cloneDepth"] = clone_depth

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(BitBucketSource, self, [props])

    @jsii.member(jsii_name="toSourceProperty")
    def _to_source_property(self) -> typing.Any:
        return jsii.invoke(self, "toSourceProperty", [])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceType":
        return jsii.get(self, "type")


class CodeCommitSource(GitBuildSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.CodeCommitSource"):
    def __init__(self, *, repository: aws_cdk.aws_codecommit.IRepository, clone_depth: typing.Optional[jsii.Number]=None, identifier: typing.Optional[str]=None) -> None:
        props: CodeCommitSourceProps = {"repository": repository}

        if clone_depth is not None:
            props["cloneDepth"] = clone_depth

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(CodeCommitSource, self, [props])

    @jsii.member(jsii_name="toSourceProperty")
    def _to_source_property(self) -> typing.Any:
        return jsii.invoke(self, "toSourceProperty", [])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceType":
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.GitBuildSourceProps")
class GitBuildSourceProps(BuildSourceProps, jsii.compat.TypedDict, total=False):
    cloneDepth: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BitBucketSourceProps")
class BitBucketSourceProps(GitBuildSourceProps, jsii.compat.TypedDict):
    owner: str
    repo: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CodeCommitSourceProps")
class CodeCommitSourceProps(GitBuildSourceProps, jsii.compat.TypedDict):
    repository: aws_cdk.aws_codecommit.IRepository

class GitHubEnterpriseSource(GitBuildSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.GitHubEnterpriseSource"):
    def __init__(self, *, https_clone_url: str, oauth_token: aws_cdk.cdk.SecretValue, ignore_ssl_errors: typing.Optional[bool]=None, clone_depth: typing.Optional[jsii.Number]=None, identifier: typing.Optional[str]=None) -> None:
        props: GitHubEnterpriseSourceProps = {"httpsCloneUrl": https_clone_url, "oauthToken": oauth_token}

        if ignore_ssl_errors is not None:
            props["ignoreSslErrors"] = ignore_ssl_errors

        if clone_depth is not None:
            props["cloneDepth"] = clone_depth

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(GitHubEnterpriseSource, self, [props])

    @jsii.member(jsii_name="toSourceProperty")
    def _to_source_property(self) -> typing.Any:
        return jsii.invoke(self, "toSourceProperty", [])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceType":
        return jsii.get(self, "type")


class _GitHubEnterpriseSourceProps(GitBuildSourceProps, jsii.compat.TypedDict, total=False):
    ignoreSslErrors: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.GitHubEnterpriseSourceProps")
class GitHubEnterpriseSourceProps(_GitHubEnterpriseSourceProps):
    httpsCloneUrl: str
    oauthToken: aws_cdk.cdk.SecretValue

class GitHubSource(GitBuildSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.GitHubSource"):
    def __init__(self, *, oauth_token: aws_cdk.cdk.SecretValue, owner: str, repo: str, report_build_status: typing.Optional[bool]=None, webhook: typing.Optional[bool]=None, clone_depth: typing.Optional[jsii.Number]=None, identifier: typing.Optional[str]=None) -> None:
        props: GitHubSourceProps = {"oauthToken": oauth_token, "owner": owner, "repo": repo}

        if report_build_status is not None:
            props["reportBuildStatus"] = report_build_status

        if webhook is not None:
            props["webhook"] = webhook

        if clone_depth is not None:
            props["cloneDepth"] = clone_depth

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(GitHubSource, self, [props])

    @jsii.member(jsii_name="buildTriggers")
    def build_triggers(self) -> typing.Optional["CfnProject.ProjectTriggersProperty"]:
        return jsii.invoke(self, "buildTriggers", [])

    @jsii.member(jsii_name="toSourceProperty")
    def _to_source_property(self) -> typing.Any:
        return jsii.invoke(self, "toSourceProperty", [])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceType":
        return jsii.get(self, "type")


class _GitHubSourceProps(GitBuildSourceProps, jsii.compat.TypedDict, total=False):
    reportBuildStatus: bool
    webhook: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.GitHubSourceProps")
class GitHubSourceProps(_GitHubSourceProps):
    oauthToken: aws_cdk.cdk.SecretValue
    owner: str
    repo: str

@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IBuildImage")
class IBuildImage(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IBuildImageProxy

    @property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        ...

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        ...

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> typing.Any:
        ...

    @jsii.member(jsii_name="validate")
    def validate(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None) -> typing.List[str]:
        ...


class _IBuildImageProxy():
    __jsii_type__ = "@aws-cdk/aws-codebuild.IBuildImage"
    @property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        return jsii.get(self, "defaultComputeType")

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        return jsii.get(self, "imageId")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> typing.Any:
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None) -> typing.List[str]:
        build_environment: BuildEnvironment = {}

        if build_image is not None:
            build_environment["buildImage"] = build_image

        if compute_type is not None:
            build_environment["computeType"] = compute_type

        if environment_variables is not None:
            build_environment["environmentVariables"] = environment_variables

        if privileged is not None:
            build_environment["privileged"] = privileged

        return jsii.invoke(self, "validate", [build_environment])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IProject")
class IProject(aws_cdk.cdk.IConstruct, aws_cdk.aws_events.IEventRuleTarget, aws_cdk.aws_iam.IGrantable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IProjectProxy

    @property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ProjectImportProps":
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        ...


class _IProjectProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_events.IEventRuleTarget), jsii.proxy_for(aws_cdk.aws_iam.IGrantable)):
    __jsii_type__ = "@aws-cdk/aws-codebuild.IProject"
    @property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        return jsii.get(self, "projectArn")

    @property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        return jsii.get(self, "projectName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")

    @jsii.member(jsii_name="export")
    def export(self) -> "ProjectImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricBuilds", [props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricFailedBuilds", [props])

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricSucceededBuilds", [props])

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
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

        return jsii.invoke(self, "onBuildFailed", [name, target, options])

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
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

        return jsii.invoke(self, "onBuildStarted", [name, target, options])

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
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

        return jsii.invoke(self, "onBuildSucceeded", [name, target, options])

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
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

        return jsii.invoke(self, "onPhaseChange", [name, target, options])

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


@jsii.implements(IBuildImage)
class LinuxBuildImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.LinuxBuildImage"):
    @jsii.member(jsii_name="fromAsset")
    @classmethod
    def from_asset(cls, scope: aws_cdk.cdk.Construct, id: str, *, directory: str, repository_name: typing.Optional[str]=None) -> "LinuxBuildImage":
        props: aws_cdk.assets_docker.DockerImageAssetProps = {"directory": directory}

        if repository_name is not None:
            props["repositoryName"] = repository_name

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromDockerHub")
    @classmethod
    def from_docker_hub(cls, name: str) -> "LinuxBuildImage":
        return jsii.sinvoke(cls, "fromDockerHub", [name])

    @jsii.member(jsii_name="fromEcrRepository")
    @classmethod
    def from_ecr_repository(cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str]=None) -> "LinuxBuildImage":
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> typing.Any:
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None) -> typing.List[str]:
        _: BuildEnvironment = {}

        if build_image is not None:
            _["buildImage"] = build_image

        if compute_type is not None:
            _["computeType"] = compute_type

        if environment_variables is not None:
            _["environmentVariables"] = environment_variables

        if privileged is not None:
            _["privileged"] = privileged

        return jsii.invoke(self, "validate", [_])

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_ANDROID_JAVA8_24_4_1")
    def UBUNTU_14_04_ANDROID_JAV_A8_24_4_1(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_ANDROID_JAVA8_24_4_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_ANDROID_JAVA8_26_1_1")
    def UBUNTU_14_04_ANDROID_JAV_A8_26_1_1(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_ANDROID_JAVA8_26_1_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_BASE")
    def UBUNTU_14_04_BASE(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_BASE")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOCKER_17_09_0")
    def UBUNTU_14_04_DOCKER_17_09_0(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOCKER_17_09_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_1_1")
    def UBUNTU_14_04_DOTNET_CORE_1_1(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_1_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_2_0")
    def UBUNTU_14_04_DOTNET_CORE_2_0(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_2_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_2_1")
    def UBUNTU_14_04_DOTNET_CORE_2_1(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_2_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_GOLANG_1_10")
    def UBUNTU_14_04_GOLANG_1_10(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_GOLANG_1_10")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_10_1_0")
    def UBUNTU_14_04_NODEJS_10_1_0(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_10_1_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_6_3_1")
    def UBUNTU_14_04_NODEJS_6_3_1(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_6_3_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_8_11_0")
    def UBUNTU_14_04_NODEJS_8_11_0(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_8_11_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_8")
    def UBUNTU_14_04_OPEN_JDK_8(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_8")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_9")
    def UBUNTU_14_04_OPEN_JDK_9(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_9")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_5_6")
    def UBUNTU_14_04_PHP_5_6(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PHP_5_6")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_7_0")
    def UBUNTU_14_04_PHP_7_0(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PHP_7_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_2_7_12")
    def UBUNTU_14_04_PYTHON_2_7_12(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_2_7_12")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_3_6")
    def UBUNTU_14_04_PYTHON_3_3_6(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_3_6")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_4_5")
    def UBUNTU_14_04_PYTHON_3_4_5(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_4_5")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_5_2")
    def UBUNTU_14_04_PYTHON_3_5_2(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_5_2")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_6_5")
    def UBUNTU_14_04_PYTHON_3_6_5(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_6_5")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_2_5")
    def UBUNTU_14_04_RUBY_2_2_5(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_2_5")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_3_1")
    def UBUNTU_14_04_RUBY_2_3_1(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_3_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_5_1")
    def UBUNTU_14_04_RUBY_2_5_1(cls) -> "LinuxBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_5_1")

    @property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        return jsii.get(self, "defaultComputeType")

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        return jsii.get(self, "imageId")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")


class NoBuildArtifacts(BuildArtifacts, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.NoBuildArtifacts"):
    def __init__(self) -> None:
        jsii.create(NoBuildArtifacts, self, [])

    @property
    @jsii.member(jsii_name="type")
    def _type(self) -> str:
        return jsii.get(self, "type")


class NoSource(BuildSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.NoSource"):
    def __init__(self) -> None:
        jsii.create(NoSource, self, [])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceType":
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.PipelineProjectProps")
class PipelineProjectProps(CommonProjectProps, jsii.compat.TypedDict):
    pass

@jsii.implements(IProject)
class ProjectBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.ProjectBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ProjectBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(ProjectBase, self, [scope, id])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "ProjectImportProps":
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricBuilds", [props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricFailedBuilds", [props])

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricSucceededBuilds", [props])

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
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

        return jsii.invoke(self, "onBuildFailed", [name, target, options])

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
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

        return jsii.invoke(self, "onBuildStarted", [name, target, options])

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
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

        return jsii.invoke(self, "onBuildSucceeded", [name, target, options])

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
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

        return jsii.invoke(self, "onPhaseChange", [name, target, options])

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

    @property
    @jsii.member(jsii_name="grantPrincipal")
    @abc.abstractmethod
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        ...

    @property
    @jsii.member(jsii_name="projectArn")
    @abc.abstractmethod
    def project_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="projectName")
    @abc.abstractmethod
    def project_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="role")
    @abc.abstractmethod
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        ...


class _ProjectBaseProxy(ProjectBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "ProjectImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        return jsii.get(self, "projectArn")

    @property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        return jsii.get(self, "projectName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


class Project(ProjectBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.Project"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, artifacts: typing.Optional["BuildArtifacts"]=None, secondary_artifacts: typing.Optional[typing.List["BuildArtifacts"]]=None, secondary_sources: typing.Optional[typing.List["BuildSource"]]=None, source: typing.Optional["BuildSource"]=None, allow_all_outbound: typing.Optional[bool]=None, badge: typing.Optional[bool]=None, build_script_asset: typing.Optional[aws_cdk.assets.Asset]=None, build_script_asset_entrypoint: typing.Optional[str]=None, build_spec: typing.Any=None, cache_bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, cache_dir: typing.Optional[str]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, environment: typing.Optional["BuildEnvironment"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, project_name: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, timeout: typing.Optional[jsii.Number]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]=None) -> None:
        props: ProjectProps = {}

        if artifacts is not None:
            props["artifacts"] = artifacts

        if secondary_artifacts is not None:
            props["secondaryArtifacts"] = secondary_artifacts

        if secondary_sources is not None:
            props["secondarySources"] = secondary_sources

        if source is not None:
            props["source"] = source

        if allow_all_outbound is not None:
            props["allowAllOutbound"] = allow_all_outbound

        if badge is not None:
            props["badge"] = badge

        if build_script_asset is not None:
            props["buildScriptAsset"] = build_script_asset

        if build_script_asset_entrypoint is not None:
            props["buildScriptAssetEntrypoint"] = build_script_asset_entrypoint

        if build_spec is not None:
            props["buildSpec"] = build_spec

        if cache_bucket is not None:
            props["cacheBucket"] = cache_bucket

        if cache_dir is not None:
            props["cacheDir"] = cache_dir

        if description is not None:
            props["description"] = description

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if environment is not None:
            props["environment"] = environment

        if environment_variables is not None:
            props["environmentVariables"] = environment_variables

        if project_name is not None:
            props["projectName"] = project_name

        if role is not None:
            props["role"] = role

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if subnet_selection is not None:
            props["subnetSelection"] = subnet_selection

        if timeout is not None:
            props["timeout"] = timeout

        if vpc is not None:
            props["vpc"] = vpc

        jsii.create(Project, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, project_name: str) -> "IProject":
        props: ProjectImportProps = {"projectName": project_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addSecondaryArtifact")
    def add_secondary_artifact(self, secondary_artifact: "BuildArtifacts") -> typing.Any:
        return jsii.invoke(self, "addSecondaryArtifact", [secondary_artifact])

    @jsii.member(jsii_name="addSecondarySource")
    def add_secondary_source(self, secondary_source: "BuildSource") -> None:
        return jsii.invoke(self, "addSecondarySource", [secondary_source])

    @jsii.member(jsii_name="addToRoleInlinePolicy")
    def add_to_role_inline_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRoleInlinePolicy", [statement])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="export")
    def export(self) -> "ProjectImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        return jsii.get(self, "projectArn")

    @property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        return jsii.get(self, "projectName")

    @property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[aws_cdk.aws_ec2.ISecurityGroup]:
        return jsii.get(self, "securityGroups")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


class PipelineProject(Project, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.PipelineProject"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, allow_all_outbound: typing.Optional[bool]=None, badge: typing.Optional[bool]=None, build_script_asset: typing.Optional[aws_cdk.assets.Asset]=None, build_script_asset_entrypoint: typing.Optional[str]=None, build_spec: typing.Any=None, cache_bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, cache_dir: typing.Optional[str]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, environment: typing.Optional["BuildEnvironment"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, project_name: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, timeout: typing.Optional[jsii.Number]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]=None) -> None:
        props: PipelineProjectProps = {}

        if allow_all_outbound is not None:
            props["allowAllOutbound"] = allow_all_outbound

        if badge is not None:
            props["badge"] = badge

        if build_script_asset is not None:
            props["buildScriptAsset"] = build_script_asset

        if build_script_asset_entrypoint is not None:
            props["buildScriptAssetEntrypoint"] = build_script_asset_entrypoint

        if build_spec is not None:
            props["buildSpec"] = build_spec

        if cache_bucket is not None:
            props["cacheBucket"] = cache_bucket

        if cache_dir is not None:
            props["cacheDir"] = cache_dir

        if description is not None:
            props["description"] = description

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if environment is not None:
            props["environment"] = environment

        if environment_variables is not None:
            props["environmentVariables"] = environment_variables

        if project_name is not None:
            props["projectName"] = project_name

        if role is not None:
            props["role"] = role

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if subnet_selection is not None:
            props["subnetSelection"] = subnet_selection

        if timeout is not None:
            props["timeout"] = timeout

        if vpc is not None:
            props["vpc"] = vpc

        jsii.create(PipelineProject, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.ProjectImportProps")
class ProjectImportProps(jsii.compat.TypedDict):
    projectName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.ProjectProps")
class ProjectProps(CommonProjectProps, jsii.compat.TypedDict, total=False):
    artifacts: "BuildArtifacts"
    secondaryArtifacts: typing.List["BuildArtifacts"]
    secondarySources: typing.List["BuildSource"]
    source: "BuildSource"

class S3BucketBuildArtifacts(BuildArtifacts, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.S3BucketBuildArtifacts"):
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, name: str, include_build_id: typing.Optional[bool]=None, package_zip: typing.Optional[bool]=None, path: typing.Optional[str]=None, identifier: typing.Optional[str]=None) -> None:
        props: S3BucketBuildArtifactsProps = {"bucket": bucket, "name": name}

        if include_build_id is not None:
            props["includeBuildId"] = include_build_id

        if package_zip is not None:
            props["packageZip"] = package_zip

        if path is not None:
            props["path"] = path

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(S3BucketBuildArtifacts, self, [props])

    @jsii.member(jsii_name="toArtifactsProperty")
    def _to_artifacts_property(self) -> typing.Any:
        return jsii.invoke(self, "toArtifactsProperty", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "S3BucketBuildArtifactsProps":
        return jsii.get(self, "props")

    @property
    @jsii.member(jsii_name="type")
    def _type(self) -> str:
        return jsii.get(self, "type")


class _S3BucketBuildArtifactsProps(BuildArtifactsProps, jsii.compat.TypedDict, total=False):
    includeBuildId: bool
    packageZip: bool
    path: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.S3BucketBuildArtifactsProps")
class S3BucketBuildArtifactsProps(_S3BucketBuildArtifactsProps):
    bucket: aws_cdk.aws_s3.IBucket
    name: str

class S3BucketSource(BuildSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.S3BucketSource"):
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, path: str, identifier: typing.Optional[str]=None) -> None:
        props: S3BucketSourceProps = {"bucket": bucket, "path": path}

        if identifier is not None:
            props["identifier"] = identifier

        jsii.create(S3BucketSource, self, [props])

    @jsii.member(jsii_name="toSourceProperty")
    def _to_source_property(self) -> typing.Any:
        return jsii.invoke(self, "toSourceProperty", [])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "SourceType":
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.S3BucketSourceProps")
class S3BucketSourceProps(BuildSourceProps, jsii.compat.TypedDict):
    bucket: aws_cdk.aws_s3.IBucket
    path: str

@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.SourceType")
class SourceType(enum.Enum):
    None_ = "None"
    CodeCommit = "CodeCommit"
    CodePipeline = "CodePipeline"
    GitHub = "GitHub"
    GitHubEnterprise = "GitHubEnterprise"
    BitBucket = "BitBucket"
    S3 = "S3"

@jsii.implements(IBuildImage)
class WindowsBuildImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.WindowsBuildImage"):
    @jsii.member(jsii_name="fromAsset")
    @classmethod
    def from_asset(cls, scope: aws_cdk.cdk.Construct, id: str, *, directory: str, repository_name: typing.Optional[str]=None) -> "WindowsBuildImage":
        props: aws_cdk.assets_docker.DockerImageAssetProps = {"directory": directory}

        if repository_name is not None:
            props["repositoryName"] = repository_name

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromDockerHub")
    @classmethod
    def from_docker_hub(cls, name: str) -> "WindowsBuildImage":
        return jsii.sinvoke(cls, "fromDockerHub", [name])

    @jsii.member(jsii_name="fromEcrRepository")
    @classmethod
    def from_ecr_repository(cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str]=None) -> "WindowsBuildImage":
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> typing.Any:
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None) -> typing.List[str]:
        build_environment: BuildEnvironment = {}

        if build_image is not None:
            build_environment["buildImage"] = build_image

        if compute_type is not None:
            build_environment["computeType"] = compute_type

        if environment_variables is not None:
            build_environment["environmentVariables"] = environment_variables

        if privileged is not None:
            build_environment["privileged"] = privileged

        return jsii.invoke(self, "validate", [build_environment])

    @classproperty
    @jsii.member(jsii_name="WIN_SERVER_CORE_2016_BASE")
    def WIN_SERVER_CORE_2016_BASE(cls) -> "WindowsBuildImage":
        return jsii.sget(cls, "WIN_SERVER_CORE_2016_BASE")

    @property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        return jsii.get(self, "defaultComputeType")

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        return jsii.get(self, "imageId")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")


__all__ = ["BitBucketSource", "BitBucketSourceProps", "BuildArtifacts", "BuildArtifactsProps", "BuildEnvironment", "BuildEnvironmentVariable", "BuildEnvironmentVariableType", "BuildSource", "BuildSourceProps", "CfnProject", "CfnProjectProps", "CodeCommitSource", "CodeCommitSourceProps", "CodePipelineBuildArtifacts", "CodePipelineSource", "CommonProjectProps", "ComputeType", "GitBuildSource", "GitBuildSourceProps", "GitHubEnterpriseSource", "GitHubEnterpriseSourceProps", "GitHubSource", "GitHubSourceProps", "IBuildImage", "IProject", "LinuxBuildImage", "NoBuildArtifacts", "NoSource", "PipelineProject", "PipelineProjectProps", "Project", "ProjectBase", "ProjectImportProps", "ProjectProps", "S3BucketBuildArtifacts", "S3BucketBuildArtifactsProps", "S3BucketSource", "S3BucketSourceProps", "SourceType", "WindowsBuildImage", "__jsii_assembly__"]

publication.publish()
