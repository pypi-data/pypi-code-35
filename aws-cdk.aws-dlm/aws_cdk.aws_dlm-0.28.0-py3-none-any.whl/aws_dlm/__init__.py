import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-dlm", "0.28.0", __name__, "aws-dlm@0.28.0.jsii.tgz")
class CfnLifecyclePolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dlm.CfnLifecyclePolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, policy_details: typing.Optional[typing.Union["PolicyDetailsProperty", aws_cdk.cdk.Token]]=None, state: typing.Optional[str]=None) -> None:
        props: CfnLifecyclePolicyProps = {}

        if description is not None:
            props["description"] = description

        if execution_role_arn is not None:
            props["executionRoleArn"] = execution_role_arn

        if policy_details is not None:
            props["policyDetails"] = policy_details

        if state is not None:
            props["state"] = state

        jsii.create(CfnLifecyclePolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="lifecyclePolicyArn")
    def lifecycle_policy_arn(self) -> str:
        return jsii.get(self, "lifecyclePolicyArn")

    @property
    @jsii.member(jsii_name="lifecyclePolicyId")
    def lifecycle_policy_id(self) -> str:
        return jsii.get(self, "lifecyclePolicyId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLifecyclePolicyProps":
        return jsii.get(self, "propertyOverrides")

    class _CreateRuleProperty(jsii.compat.TypedDict, total=False):
        times: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dlm.CfnLifecyclePolicy.CreateRuleProperty")
    class CreateRuleProperty(_CreateRuleProperty):
        interval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        intervalUnit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-dlm.CfnLifecyclePolicy.PolicyDetailsProperty")
    class PolicyDetailsProperty(jsii.compat.TypedDict, total=False):
        resourceTypes: typing.List[str]
        schedules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLifecyclePolicy.ScheduleProperty"]]]
        targetTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, aws_cdk.cdk.CfnTag]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dlm.CfnLifecyclePolicy.RetainRuleProperty")
    class RetainRuleProperty(jsii.compat.TypedDict):
        count: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dlm.CfnLifecyclePolicy.ScheduleProperty")
    class ScheduleProperty(jsii.compat.TypedDict, total=False):
        copyTags: typing.Union[bool, aws_cdk.cdk.Token]
        createRule: typing.Union[aws_cdk.cdk.Token, "CfnLifecyclePolicy.CreateRuleProperty"]
        name: str
        retainRule: typing.Union[aws_cdk.cdk.Token, "CfnLifecyclePolicy.RetainRuleProperty"]
        tagsToAdd: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, aws_cdk.cdk.CfnTag]]]


@jsii.data_type(jsii_type="@aws-cdk/aws-dlm.CfnLifecyclePolicyProps")
class CfnLifecyclePolicyProps(jsii.compat.TypedDict, total=False):
    description: str
    executionRoleArn: str
    policyDetails: typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", aws_cdk.cdk.Token]
    state: str

__all__ = ["CfnLifecyclePolicy", "CfnLifecyclePolicyProps", "__jsii_assembly__"]

publication.publish()
