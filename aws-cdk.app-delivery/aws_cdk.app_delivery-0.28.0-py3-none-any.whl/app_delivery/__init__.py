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
import aws_cdk.aws_codepipeline
import aws_cdk.aws_codepipeline_actions
import aws_cdk.aws_iam
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/app-delivery", "0.28.0", __name__, "app-delivery@0.28.0.jsii.tgz")
class PipelineDeployStackAction(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/app-delivery.PipelineDeployStackAction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, admin_permissions: bool, input_artifact: aws_cdk.aws_codepipeline.Artifact, stack: aws_cdk.cdk.Stack, stage: aws_cdk.aws_codepipeline.IStage, capabilities: typing.Optional[aws_cdk.aws_cloudformation.CloudFormationCapabilities]=None, change_set_name: typing.Optional[str]=None, create_change_set_run_order: typing.Optional[jsii.Number]=None, execute_change_set_run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        props: PipelineDeployStackActionProps = {"adminPermissions": admin_permissions, "inputArtifact": input_artifact, "stack": stack, "stage": stage}

        if capabilities is not None:
            props["capabilities"] = capabilities

        if change_set_name is not None:
            props["changeSetName"] = change_set_name

        if create_change_set_run_order is not None:
            props["createChangeSetRunOrder"] = create_change_set_run_order

        if execute_change_set_run_order is not None:
            props["executeChangeSetRunOrder"] = execute_change_set_run_order

        if role is not None:
            props["role"] = role

        jsii.create(PipelineDeployStackAction, self, [scope, id, props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "deploymentRole")


class _PipelineDeployStackActionProps(jsii.compat.TypedDict, total=False):
    capabilities: aws_cdk.aws_cloudformation.CloudFormationCapabilities
    changeSetName: str
    createChangeSetRunOrder: jsii.Number
    executeChangeSetRunOrder: jsii.Number
    role: aws_cdk.aws_iam.IRole

@jsii.data_type(jsii_type="@aws-cdk/app-delivery.PipelineDeployStackActionProps")
class PipelineDeployStackActionProps(_PipelineDeployStackActionProps):
    adminPermissions: bool
    inputArtifact: aws_cdk.aws_codepipeline.Artifact
    stack: aws_cdk.cdk.Stack
    stage: aws_cdk.aws_codepipeline.IStage

__all__ = ["PipelineDeployStackAction", "PipelineDeployStackActionProps", "__jsii_assembly__"]

publication.publish()
