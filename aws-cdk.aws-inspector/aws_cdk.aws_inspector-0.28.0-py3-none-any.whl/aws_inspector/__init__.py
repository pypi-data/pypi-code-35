import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-inspector", "0.28.0", __name__, "aws-inspector@0.28.0.jsii.tgz")
class CfnAssessmentTarget(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-inspector.CfnAssessmentTarget"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, assessment_target_name: typing.Optional[str]=None, resource_group_arn: typing.Optional[str]=None) -> None:
        props: CfnAssessmentTargetProps = {}

        if assessment_target_name is not None:
            props["assessmentTargetName"] = assessment_target_name

        if resource_group_arn is not None:
            props["resourceGroupArn"] = resource_group_arn

        jsii.create(CfnAssessmentTarget, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="assessmentTargetArn")
    def assessment_target_arn(self) -> str:
        return jsii.get(self, "assessmentTargetArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAssessmentTargetProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-inspector.CfnAssessmentTargetProps")
class CfnAssessmentTargetProps(jsii.compat.TypedDict, total=False):
    assessmentTargetName: str
    resourceGroupArn: str

class CfnAssessmentTemplate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-inspector.CfnAssessmentTemplate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, assessment_target_arn: str, duration_in_seconds: typing.Union[jsii.Number, aws_cdk.cdk.Token], rules_package_arns: typing.List[str], assessment_template_name: typing.Optional[str]=None, user_attributes_for_findings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, aws_cdk.cdk.CfnTag]]]]=None) -> None:
        props: CfnAssessmentTemplateProps = {"assessmentTargetArn": assessment_target_arn, "durationInSeconds": duration_in_seconds, "rulesPackageArns": rules_package_arns}

        if assessment_template_name is not None:
            props["assessmentTemplateName"] = assessment_template_name

        if user_attributes_for_findings is not None:
            props["userAttributesForFindings"] = user_attributes_for_findings

        jsii.create(CfnAssessmentTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="assessmentTemplateArn")
    def assessment_template_arn(self) -> str:
        return jsii.get(self, "assessmentTemplateArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAssessmentTemplateProps":
        return jsii.get(self, "propertyOverrides")


class _CfnAssessmentTemplateProps(jsii.compat.TypedDict, total=False):
    assessmentTemplateName: str
    userAttributesForFindings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, aws_cdk.cdk.CfnTag]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-inspector.CfnAssessmentTemplateProps")
class CfnAssessmentTemplateProps(_CfnAssessmentTemplateProps):
    assessmentTargetArn: str
    durationInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    rulesPackageArns: typing.List[str]

class CfnResourceGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-inspector.CfnResourceGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_group_tags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, aws_cdk.cdk.CfnTag]]]) -> None:
        props: CfnResourceGroupProps = {"resourceGroupTags": resource_group_tags}

        jsii.create(CfnResourceGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResourceGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resourceGroupArn")
    def resource_group_arn(self) -> str:
        return jsii.get(self, "resourceGroupArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-inspector.CfnResourceGroupProps")
class CfnResourceGroupProps(jsii.compat.TypedDict):
    resourceGroupTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, aws_cdk.cdk.CfnTag]]]

__all__ = ["CfnAssessmentTarget", "CfnAssessmentTargetProps", "CfnAssessmentTemplate", "CfnAssessmentTemplateProps", "CfnResourceGroup", "CfnResourceGroupProps", "__jsii_assembly__"]

publication.publish()
