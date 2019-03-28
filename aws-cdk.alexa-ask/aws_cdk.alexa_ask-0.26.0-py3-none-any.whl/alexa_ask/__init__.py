import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_codepipeline_api
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/alexa-ask", "0.26.0", __name__, "alexa-ask@0.26.0.jsii.tgz")
class AlexaSkillDeployAction(aws_cdk.aws_codepipeline_api.DeployAction, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/alexa-ask.AlexaSkillDeployAction"):
    def __init__(self, *, client_id: aws_cdk.cdk.Secret, client_secret: aws_cdk.cdk.Secret, input_artifact: aws_cdk.aws_codepipeline_api.Artifact, refresh_token: aws_cdk.cdk.Secret, skill_id: str, parameter_overrides_artifact: typing.Optional[aws_cdk.aws_codepipeline_api.Artifact]=None) -> None:
        props: AlexaSkillDeployActionProps = {"clientId": client_id, "clientSecret": client_secret, "inputArtifact": input_artifact, "refreshToken": refresh_token, "skillId": skill_id}

        if parameter_overrides_artifact is not None:
            props["parameterOverridesArtifact"] = parameter_overrides_artifact

        jsii.create(AlexaSkillDeployAction, self, [props])

    @jsii.member(jsii_name="bind")
    def _bind(self, _stage: aws_cdk.aws_codepipeline_api.IStage, _scope: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [_stage, _scope])


class _AlexaSkillDeployActionProps(aws_cdk.aws_codepipeline_api.CommonActionProps, jsii.compat.TypedDict, total=False):
    parameterOverridesArtifact: aws_cdk.aws_codepipeline_api.Artifact

@jsii.data_type(jsii_type="@aws-cdk/alexa-ask.AlexaSkillDeployActionProps")
class AlexaSkillDeployActionProps(_AlexaSkillDeployActionProps):
    clientId: aws_cdk.cdk.Secret
    clientSecret: aws_cdk.cdk.Secret
    inputArtifact: aws_cdk.aws_codepipeline_api.Artifact
    refreshToken: aws_cdk.cdk.Secret
    skillId: str

class CfnSkill(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/alexa-ask.CfnSkill"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authentication_configuration: typing.Union["AuthenticationConfigurationProperty", aws_cdk.cdk.Token], skill_package: typing.Union[aws_cdk.cdk.Token, "SkillPackageProperty"], vendor_id: str) -> None:
        props: CfnSkillProps = {"authenticationConfiguration": authentication_configuration, "skillPackage": skill_package, "vendorId": vendor_id}

        jsii.create(CfnSkill, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSkillProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="skillId")
    def skill_id(self) -> str:
        return jsii.get(self, "skillId")

    @jsii.data_type(jsii_type="@aws-cdk/alexa-ask.CfnSkill.AuthenticationConfigurationProperty")
    class AuthenticationConfigurationProperty(jsii.compat.TypedDict):
        clientId: str
        clientSecret: str
        refreshToken: str

    @jsii.data_type(jsii_type="@aws-cdk/alexa-ask.CfnSkill.OverridesProperty")
    class OverridesProperty(jsii.compat.TypedDict, total=False):
        manifest: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

    class _SkillPackageProperty(jsii.compat.TypedDict, total=False):
        overrides: typing.Union[aws_cdk.cdk.Token, "CfnSkill.OverridesProperty"]
        s3BucketRole: str
        s3ObjectVersion: str

    @jsii.data_type(jsii_type="@aws-cdk/alexa-ask.CfnSkill.SkillPackageProperty")
    class SkillPackageProperty(_SkillPackageProperty):
        s3Bucket: str
        s3Key: str


@jsii.data_type(jsii_type="@aws-cdk/alexa-ask.CfnSkillProps")
class CfnSkillProps(jsii.compat.TypedDict):
    authenticationConfiguration: typing.Union["CfnSkill.AuthenticationConfigurationProperty", aws_cdk.cdk.Token]
    skillPackage: typing.Union[aws_cdk.cdk.Token, "CfnSkill.SkillPackageProperty"]
    vendorId: str

__all__ = ["AlexaSkillDeployAction", "AlexaSkillDeployActionProps", "CfnSkill", "CfnSkillProps", "__jsii_assembly__"]

publication.publish()
