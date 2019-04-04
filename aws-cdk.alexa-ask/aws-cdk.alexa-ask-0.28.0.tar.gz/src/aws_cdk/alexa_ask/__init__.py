import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/alexa-ask", "0.28.0", __name__, "alexa-ask@0.28.0.jsii.tgz")
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

__all__ = ["CfnSkill", "CfnSkillProps", "__jsii_assembly__"]

publication.publish()
