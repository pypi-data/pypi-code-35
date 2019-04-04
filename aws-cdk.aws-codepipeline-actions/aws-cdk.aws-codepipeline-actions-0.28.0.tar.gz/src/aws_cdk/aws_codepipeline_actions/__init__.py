import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_codebuild
import aws_cdk.aws_codecommit
import aws_cdk.aws_codedeploy
import aws_cdk.aws_codepipeline
import aws_cdk.aws_ecr
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codepipeline-actions", "0.28.0", __name__, "aws-codepipeline-actions@0.28.0.jsii.tgz")
class AlexaSkillDeployAction(aws_cdk.aws_codepipeline.DeployAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.AlexaSkillDeployAction"):
    def __init__(self, *, client_id: str, client_secret: aws_cdk.cdk.SecretValue, input_artifact: aws_cdk.aws_codepipeline.Artifact, refresh_token: aws_cdk.cdk.SecretValue, skill_id: str, parameter_overrides_artifact: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: AlexaSkillDeployActionProps = {"clientId": client_id, "clientSecret": client_secret, "inputArtifact": input_artifact, "refreshToken": refresh_token, "skillId": skill_id, "actionName": action_name}

        if parameter_overrides_artifact is not None:
            props["parameterOverridesArtifact"] = parameter_overrides_artifact

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(AlexaSkillDeployAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        _info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [_info])


class _AlexaSkillDeployActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    parameterOverridesArtifact: aws_cdk.aws_codepipeline.Artifact

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.AlexaSkillDeployActionProps")
class AlexaSkillDeployActionProps(_AlexaSkillDeployActionProps):
    clientId: str
    clientSecret: aws_cdk.cdk.SecretValue
    inputArtifact: aws_cdk.aws_codepipeline.Artifact
    refreshToken: aws_cdk.cdk.SecretValue
    skillId: str

class CloudFormationAction(aws_cdk.aws_codepipeline.Action, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _CloudFormationActionProxy

    def __init__(self, props: "CloudFormationActionProps", configuration: typing.Any=None) -> None:
        jsii.create(CloudFormationAction, self, [props, configuration])

    @property
    @jsii.member(jsii_name="outputArtifact")
    def output_artifact(self) -> typing.Optional[aws_cdk.aws_codepipeline.Artifact]:
        return jsii.get(self, "outputArtifact")

    @output_artifact.setter
    def output_artifact(self, value: typing.Optional[aws_cdk.aws_codepipeline.Artifact]):
        return jsii.set(self, "outputArtifact", value)


class _CloudFormationActionProxy(CloudFormationAction, jsii.proxy_for(aws_cdk.aws_codepipeline.Action)):
    pass

class _CloudFormationActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    outputArtifactName: str
    outputFileName: str
    region: str
    role: aws_cdk.aws_iam.IRole

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationActionProps")
class CloudFormationActionProps(_CloudFormationActionProps):
    stackName: str

class CloudFormationDeployAction(CloudFormationAction, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationDeployAction"):
    @staticmethod
    def __jsii_proxy_class__():
        return _CloudFormationDeployActionProxy

    def __init__(self, props: "CloudFormationDeployActionProps", configuration: typing.Any) -> None:
        jsii.create(CloudFormationDeployAction, self, [props, configuration])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> bool:
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])

    @property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "deploymentRole")


class _CloudFormationDeployActionProxy(CloudFormationDeployAction, jsii.proxy_for(CloudFormationAction)):
    pass

class CloudFormationCreateReplaceChangeSetAction(CloudFormationDeployAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationCreateReplaceChangeSetAction"):
    def __init__(self, *, change_set_name: str, template_path: aws_cdk.aws_codepipeline.ArtifactPath, admin_permissions: bool, additional_input_artifacts: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, capabilities: typing.Optional[aws_cdk.aws_cloudformation.CloudFormationCapabilities]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None, stack_name: str, output_artifact_name: typing.Optional[str]=None, output_file_name: typing.Optional[str]=None, region: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: CloudFormationCreateReplaceChangeSetActionProps = {"changeSetName": change_set_name, "templatePath": template_path, "adminPermissions": admin_permissions, "stackName": stack_name, "actionName": action_name}

        if additional_input_artifacts is not None:
            props["additionalInputArtifacts"] = additional_input_artifacts

        if capabilities is not None:
            props["capabilities"] = capabilities

        if deployment_role is not None:
            props["deploymentRole"] = deployment_role

        if parameter_overrides is not None:
            props["parameterOverrides"] = parameter_overrides

        if template_configuration is not None:
            props["templateConfiguration"] = template_configuration

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if output_file_name is not None:
            props["outputFileName"] = output_file_name

        if region is not None:
            props["region"] = region

        if role is not None:
            props["role"] = role

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(CloudFormationCreateReplaceChangeSetAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class CloudFormationCreateUpdateStackAction(CloudFormationDeployAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationCreateUpdateStackAction"):
    def __init__(self, *, template_path: aws_cdk.aws_codepipeline.ArtifactPath, replace_on_failure: typing.Optional[bool]=None, admin_permissions: bool, additional_input_artifacts: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, capabilities: typing.Optional[aws_cdk.aws_cloudformation.CloudFormationCapabilities]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None, stack_name: str, output_artifact_name: typing.Optional[str]=None, output_file_name: typing.Optional[str]=None, region: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: CloudFormationCreateUpdateStackActionProps = {"templatePath": template_path, "adminPermissions": admin_permissions, "stackName": stack_name, "actionName": action_name}

        if replace_on_failure is not None:
            props["replaceOnFailure"] = replace_on_failure

        if additional_input_artifacts is not None:
            props["additionalInputArtifacts"] = additional_input_artifacts

        if capabilities is not None:
            props["capabilities"] = capabilities

        if deployment_role is not None:
            props["deploymentRole"] = deployment_role

        if parameter_overrides is not None:
            props["parameterOverrides"] = parameter_overrides

        if template_configuration is not None:
            props["templateConfiguration"] = template_configuration

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if output_file_name is not None:
            props["outputFileName"] = output_file_name

        if region is not None:
            props["region"] = region

        if role is not None:
            props["role"] = role

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(CloudFormationCreateUpdateStackAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class CloudFormationDeleteStackAction(CloudFormationDeployAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationDeleteStackAction"):
    def __init__(self, *, admin_permissions: bool, additional_input_artifacts: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, capabilities: typing.Optional[aws_cdk.aws_cloudformation.CloudFormationCapabilities]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None, stack_name: str, output_artifact_name: typing.Optional[str]=None, output_file_name: typing.Optional[str]=None, region: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: CloudFormationDeleteStackActionProps = {"adminPermissions": admin_permissions, "stackName": stack_name, "actionName": action_name}

        if additional_input_artifacts is not None:
            props["additionalInputArtifacts"] = additional_input_artifacts

        if capabilities is not None:
            props["capabilities"] = capabilities

        if deployment_role is not None:
            props["deploymentRole"] = deployment_role

        if parameter_overrides is not None:
            props["parameterOverrides"] = parameter_overrides

        if template_configuration is not None:
            props["templateConfiguration"] = template_configuration

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if output_file_name is not None:
            props["outputFileName"] = output_file_name

        if region is not None:
            props["region"] = region

        if role is not None:
            props["role"] = role

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(CloudFormationDeleteStackAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class _CloudFormationDeployActionProps(CloudFormationActionProps, jsii.compat.TypedDict, total=False):
    additionalInputArtifacts: typing.List[aws_cdk.aws_codepipeline.Artifact]
    capabilities: aws_cdk.aws_cloudformation.CloudFormationCapabilities
    deploymentRole: aws_cdk.aws_iam.IRole
    parameterOverrides: typing.Mapping[str,typing.Any]
    templateConfiguration: aws_cdk.aws_codepipeline.ArtifactPath

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationDeployActionProps")
class CloudFormationDeployActionProps(_CloudFormationDeployActionProps):
    adminPermissions: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationCreateReplaceChangeSetActionProps")
class CloudFormationCreateReplaceChangeSetActionProps(CloudFormationDeployActionProps, jsii.compat.TypedDict):
    changeSetName: str
    templatePath: aws_cdk.aws_codepipeline.ArtifactPath

class _CloudFormationCreateUpdateStackActionProps(CloudFormationDeployActionProps, jsii.compat.TypedDict, total=False):
    replaceOnFailure: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationCreateUpdateStackActionProps")
class CloudFormationCreateUpdateStackActionProps(_CloudFormationCreateUpdateStackActionProps):
    templatePath: aws_cdk.aws_codepipeline.ArtifactPath

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationDeleteStackActionProps")
class CloudFormationDeleteStackActionProps(CloudFormationDeployActionProps, jsii.compat.TypedDict):
    pass

class CloudFormationExecuteChangeSetAction(CloudFormationAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationExecuteChangeSetAction"):
    def __init__(self, *, change_set_name: str, stack_name: str, output_artifact_name: typing.Optional[str]=None, output_file_name: typing.Optional[str]=None, region: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: CloudFormationExecuteChangeSetActionProps = {"changeSetName": change_set_name, "stackName": stack_name, "actionName": action_name}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if output_file_name is not None:
            props["outputFileName"] = output_file_name

        if region is not None:
            props["region"] = region

        if role is not None:
            props["role"] = role

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(CloudFormationExecuteChangeSetAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationExecuteChangeSetActionProps")
class CloudFormationExecuteChangeSetActionProps(CloudFormationActionProps, jsii.compat.TypedDict):
    changeSetName: str

class CodeBuildBuildAction(aws_cdk.aws_codepipeline.BuildAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CodeBuildBuildAction"):
    def __init__(self, *, output_artifact_name: typing.Optional[str]=None, input_artifact: aws_cdk.aws_codepipeline.Artifact, project: aws_cdk.aws_codebuild.IProject, additional_input_artifacts: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, additional_output_artifact_names: typing.Optional[typing.List[str]]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: CodeBuildBuildActionProps = {"inputArtifact": input_artifact, "project": project, "actionName": action_name}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if additional_input_artifacts is not None:
            props["additionalInputArtifacts"] = additional_input_artifacts

        if additional_output_artifact_names is not None:
            props["additionalOutputArtifactNames"] = additional_output_artifact_names

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(CodeBuildBuildAction, self, [props])

    @jsii.member(jsii_name="additionalOutputArtifact")
    def additional_output_artifact(self, name: str) -> aws_cdk.aws_codepipeline.Artifact:
        return jsii.invoke(self, "additionalOutputArtifact", [name])

    @jsii.member(jsii_name="additionalOutputArtifacts")
    def additional_output_artifacts(self) -> typing.List[aws_cdk.aws_codepipeline.Artifact]:
        return jsii.invoke(self, "additionalOutputArtifacts", [])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class CodeBuildTestAction(aws_cdk.aws_codepipeline.TestAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CodeBuildTestAction"):
    def __init__(self, *, output_artifact_name: typing.Optional[str]=None, input_artifact: aws_cdk.aws_codepipeline.Artifact, project: aws_cdk.aws_codebuild.IProject, additional_input_artifacts: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, additional_output_artifact_names: typing.Optional[typing.List[str]]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: CodeBuildTestActionProps = {"inputArtifact": input_artifact, "project": project, "actionName": action_name}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if additional_input_artifacts is not None:
            props["additionalInputArtifacts"] = additional_input_artifacts

        if additional_output_artifact_names is not None:
            props["additionalOutputArtifactNames"] = additional_output_artifact_names

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(CodeBuildTestAction, self, [props])

    @jsii.member(jsii_name="additionalOutputArtifact")
    def additional_output_artifact(self, name: str) -> aws_cdk.aws_codepipeline.Artifact:
        return jsii.invoke(self, "additionalOutputArtifact", [name])

    @jsii.member(jsii_name="additionalOutputArtifacts")
    def additional_output_artifacts(self) -> typing.List[aws_cdk.aws_codepipeline.Artifact]:
        return jsii.invoke(self, "additionalOutputArtifacts", [])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class CodeCommitSourceAction(aws_cdk.aws_codepipeline.SourceAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CodeCommitSourceAction"):
    def __init__(self, *, repository: aws_cdk.aws_codecommit.IRepository, branch: typing.Optional[str]=None, output_artifact_name: typing.Optional[str]=None, poll_for_source_changes: typing.Optional[bool]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: CodeCommitSourceActionProps = {"repository": repository, "actionName": action_name}

        if branch is not None:
            props["branch"] = branch

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if poll_for_source_changes is not None:
            props["pollForSourceChanges"] = poll_for_source_changes

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(CodeCommitSourceAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class _CodeCommitSourceActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    branch: str
    outputArtifactName: str
    pollForSourceChanges: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeCommitSourceActionProps")
class CodeCommitSourceActionProps(_CodeCommitSourceActionProps):
    repository: aws_cdk.aws_codecommit.IRepository

class CodeDeployServerDeployAction(aws_cdk.aws_codepipeline.DeployAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CodeDeployServerDeployAction"):
    def __init__(self, *, deployment_group: aws_cdk.aws_codedeploy.IServerDeploymentGroup, input_artifact: aws_cdk.aws_codepipeline.Artifact, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: CodeDeployServerDeployActionProps = {"deploymentGroup": deployment_group, "inputArtifact": input_artifact, "actionName": action_name}

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(CodeDeployServerDeployAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeDeployServerDeployActionProps")
class CodeDeployServerDeployActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict):
    deploymentGroup: aws_cdk.aws_codedeploy.IServerDeploymentGroup
    inputArtifact: aws_cdk.aws_codepipeline.Artifact

class _CommonCodeBuildActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    additionalInputArtifacts: typing.List[aws_cdk.aws_codepipeline.Artifact]
    additionalOutputArtifactNames: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CommonCodeBuildActionProps")
class CommonCodeBuildActionProps(_CommonCodeBuildActionProps):
    inputArtifact: aws_cdk.aws_codepipeline.Artifact
    project: aws_cdk.aws_codebuild.IProject

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeBuildBuildActionProps")
class CodeBuildBuildActionProps(CommonCodeBuildActionProps, jsii.compat.TypedDict, total=False):
    outputArtifactName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeBuildTestActionProps")
class CodeBuildTestActionProps(CommonCodeBuildActionProps, jsii.compat.TypedDict, total=False):
    outputArtifactName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CommonJenkinsActionProps")
class CommonJenkinsActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict):
    inputArtifact: aws_cdk.aws_codepipeline.Artifact
    jenkinsProvider: "IJenkinsProvider"
    projectName: str

class EcrSourceAction(aws_cdk.aws_codepipeline.SourceAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.EcrSourceAction"):
    def __init__(self, *, repository: aws_cdk.aws_ecr.IRepository, image_tag: typing.Optional[str]=None, output_artifact_name: typing.Optional[str]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: EcrSourceActionProps = {"repository": repository, "actionName": action_name}

        if image_tag is not None:
            props["imageTag"] = image_tag

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(EcrSourceAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class _EcrSourceActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    imageTag: str
    outputArtifactName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.EcrSourceActionProps")
class EcrSourceActionProps(_EcrSourceActionProps):
    repository: aws_cdk.aws_ecr.IRepository

class GitHubSourceAction(aws_cdk.aws_codepipeline.SourceAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.GitHubSourceAction"):
    def __init__(self, *, oauth_token: aws_cdk.cdk.SecretValue, output_artifact_name: str, owner: str, repo: str, branch: typing.Optional[str]=None, poll_for_source_changes: typing.Optional[bool]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: GitHubSourceActionProps = {"oauthToken": oauth_token, "outputArtifactName": output_artifact_name, "owner": owner, "repo": repo, "actionName": action_name}

        if branch is not None:
            props["branch"] = branch

        if poll_for_source_changes is not None:
            props["pollForSourceChanges"] = poll_for_source_changes

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(GitHubSourceAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class _GitHubSourceActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    branch: str
    pollForSourceChanges: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.GitHubSourceActionProps")
class GitHubSourceActionProps(_GitHubSourceActionProps):
    oauthToken: aws_cdk.cdk.SecretValue
    outputArtifactName: str
    owner: str
    repo: str

@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline-actions.IJenkinsProvider")
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


class _IJenkinsProviderProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-codepipeline-actions.IJenkinsProvider"
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


@jsii.implements(IJenkinsProvider)
class BaseJenkinsProvider(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-actions.BaseJenkinsProvider"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseJenkinsProviderProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, version: typing.Optional[str]=None) -> None:
        jsii.create(BaseJenkinsProvider, self, [scope, id, version])

    @jsii.member(jsii_name="export")
    def export(self) -> "JenkinsProviderImportProps":
        return jsii.invoke(self, "export", [])

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


class JenkinsBuildAction(aws_cdk.aws_codepipeline.BuildAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsBuildAction"):
    def __init__(self, *, output_artifact_name: typing.Optional[str]=None, input_artifact: aws_cdk.aws_codepipeline.Artifact, jenkins_provider: "IJenkinsProvider", project_name: str, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: JenkinsBuildActionProps = {"inputArtifact": input_artifact, "jenkinsProvider": jenkins_provider, "projectName": project_name, "actionName": action_name}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(JenkinsBuildAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        _info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [_info])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsBuildActionProps")
class JenkinsBuildActionProps(CommonJenkinsActionProps, jsii.compat.TypedDict, total=False):
    outputArtifactName: str

class JenkinsProvider(BaseJenkinsProvider, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsProvider"):
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

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsProviderImportProps")
class JenkinsProviderImportProps(_JenkinsProviderImportProps):
    providerName: str
    serverUrl: str

class _JenkinsProviderProps(jsii.compat.TypedDict, total=False):
    forBuild: bool
    forTest: bool
    version: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsProviderProps")
class JenkinsProviderProps(_JenkinsProviderProps):
    providerName: str
    serverUrl: str

class JenkinsTestAction(aws_cdk.aws_codepipeline.TestAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsTestAction"):
    def __init__(self, *, output_artifact_name: typing.Optional[str]=None, input_artifact: aws_cdk.aws_codepipeline.Artifact, jenkins_provider: "IJenkinsProvider", project_name: str, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: JenkinsTestActionProps = {"inputArtifact": input_artifact, "jenkinsProvider": jenkins_provider, "projectName": project_name, "actionName": action_name}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(JenkinsTestAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        _info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [_info])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsTestActionProps")
class JenkinsTestActionProps(CommonJenkinsActionProps, jsii.compat.TypedDict, total=False):
    outputArtifactName: str

class LambdaInvokeAction(aws_cdk.aws_codepipeline.Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.LambdaInvokeAction"):
    def __init__(self, *, lambda_: aws_cdk.aws_lambda.IFunction, add_put_job_result_policy: typing.Optional[bool]=None, input_artifacts: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, output_artifact_names: typing.Optional[typing.List[str]]=None, user_parameters: typing.Any=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: LambdaInvokeActionProps = {"lambda": lambda_, "actionName": action_name}

        if add_put_job_result_policy is not None:
            props["addPutJobResultPolicy"] = add_put_job_result_policy

        if input_artifacts is not None:
            props["inputArtifacts"] = input_artifacts

        if output_artifact_names is not None:
            props["outputArtifactNames"] = output_artifact_names

        if user_parameters is not None:
            props["userParameters"] = user_parameters

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(LambdaInvokeAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])

    @jsii.member(jsii_name="outputArtifact")
    def output_artifact(self, artifact_name: str) -> aws_cdk.aws_codepipeline.Artifact:
        return jsii.invoke(self, "outputArtifact", [artifact_name])

    @jsii.member(jsii_name="outputArtifacts")
    def output_artifacts(self) -> typing.List[aws_cdk.aws_codepipeline.Artifact]:
        return jsii.invoke(self, "outputArtifacts", [])


class _LambdaInvokeActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    addPutJobResultPolicy: bool
    inputArtifacts: typing.List[aws_cdk.aws_codepipeline.Artifact]
    outputArtifactNames: typing.List[str]
    userParameters: typing.Any

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.LambdaInvokeActionProps")
class LambdaInvokeActionProps(_LambdaInvokeActionProps):
    lambda_: aws_cdk.aws_lambda.IFunction

class ManualApprovalAction(aws_cdk.aws_codepipeline.Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.ManualApprovalAction"):
    def __init__(self, *, additional_information: typing.Optional[str]=None, notification_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, notify_emails: typing.Optional[typing.List[str]]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: ManualApprovalActionProps = {"actionName": action_name}

        if additional_information is not None:
            props["additionalInformation"] = additional_information

        if notification_topic is not None:
            props["notificationTopic"] = notification_topic

        if notify_emails is not None:
            props["notifyEmails"] = notify_emails

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(ManualApprovalAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])

    @property
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        return jsii.get(self, "notificationTopic")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.ManualApprovalActionProps")
class ManualApprovalActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    additionalInformation: str
    notificationTopic: aws_cdk.aws_sns.ITopic
    notifyEmails: typing.List[str]

class S3DeployAction(aws_cdk.aws_codepipeline.DeployAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.S3DeployAction"):
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, input_artifact: aws_cdk.aws_codepipeline.Artifact, extract: typing.Optional[bool]=None, object_key: typing.Optional[str]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: S3DeployActionProps = {"bucket": bucket, "inputArtifact": input_artifact, "actionName": action_name}

        if extract is not None:
            props["extract"] = extract

        if object_key is not None:
            props["objectKey"] = object_key

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(S3DeployAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class _S3DeployActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    extract: bool
    objectKey: str

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.S3DeployActionProps")
class S3DeployActionProps(_S3DeployActionProps):
    bucket: aws_cdk.aws_s3.IBucket
    inputArtifact: aws_cdk.aws_codepipeline.Artifact

class S3SourceAction(aws_cdk.aws_codepipeline.SourceAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.S3SourceAction"):
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, bucket_key: str, output_artifact_name: typing.Optional[str]=None, poll_for_source_changes: typing.Optional[bool]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        props: S3SourceActionProps = {"bucket": bucket, "bucketKey": bucket_key, "actionName": action_name}

        if output_artifact_name is not None:
            props["outputArtifactName"] = output_artifact_name

        if poll_for_source_changes is not None:
            props["pollForSourceChanges"] = poll_for_source_changes

        if run_order is not None:
            props["runOrder"] = run_order

        jsii.create(S3SourceAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, *, pipeline: aws_cdk.aws_codepipeline.IPipeline, role: aws_cdk.aws_iam.IRole, scope: aws_cdk.cdk.Construct, stage: aws_cdk.aws_codepipeline.IStage) -> None:
        info: aws_cdk.aws_codepipeline.ActionBind = {"pipeline": pipeline, "role": role, "scope": scope, "stage": stage}

        return jsii.invoke(self, "bind", [info])


class _S3SourceActionProps(aws_cdk.aws_codepipeline.CommonActionProps, jsii.compat.TypedDict, total=False):
    outputArtifactName: str
    pollForSourceChanges: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.S3SourceActionProps")
class S3SourceActionProps(_S3SourceActionProps):
    bucket: aws_cdk.aws_s3.IBucket
    bucketKey: str

__all__ = ["AlexaSkillDeployAction", "AlexaSkillDeployActionProps", "BaseJenkinsProvider", "CloudFormationAction", "CloudFormationActionProps", "CloudFormationCreateReplaceChangeSetAction", "CloudFormationCreateReplaceChangeSetActionProps", "CloudFormationCreateUpdateStackAction", "CloudFormationCreateUpdateStackActionProps", "CloudFormationDeleteStackAction", "CloudFormationDeleteStackActionProps", "CloudFormationDeployAction", "CloudFormationDeployActionProps", "CloudFormationExecuteChangeSetAction", "CloudFormationExecuteChangeSetActionProps", "CodeBuildBuildAction", "CodeBuildBuildActionProps", "CodeBuildTestAction", "CodeBuildTestActionProps", "CodeCommitSourceAction", "CodeCommitSourceActionProps", "CodeDeployServerDeployAction", "CodeDeployServerDeployActionProps", "CommonCodeBuildActionProps", "CommonJenkinsActionProps", "EcrSourceAction", "EcrSourceActionProps", "GitHubSourceAction", "GitHubSourceActionProps", "IJenkinsProvider", "JenkinsBuildAction", "JenkinsBuildActionProps", "JenkinsProvider", "JenkinsProviderImportProps", "JenkinsProviderProps", "JenkinsTestAction", "JenkinsTestActionProps", "LambdaInvokeAction", "LambdaInvokeActionProps", "ManualApprovalAction", "ManualApprovalActionProps", "S3DeployAction", "S3DeployActionProps", "S3SourceAction", "S3SourceActionProps", "__jsii_assembly__"]

publication.publish()
