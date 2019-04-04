import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloudformation", "0.28.0", __name__, "aws-cloudformation@0.28.0.jsii.tgz")
class CfnCustomResource(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnCustomResource"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service_token: str) -> None:
        props: CfnCustomResourceProps = {"serviceToken": service_token}

        jsii.create(CfnCustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCustomResourceProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CfnCustomResourceProps")
class CfnCustomResourceProps(jsii.compat.TypedDict):
    serviceToken: str

class CfnMacro(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnMacro"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, function_name: str, name: str, description: typing.Optional[str]=None, log_group_name: typing.Optional[str]=None, log_role_arn: typing.Optional[str]=None) -> None:
        props: CfnMacroProps = {"functionName": function_name, "name": name}

        if description is not None:
            props["description"] = description

        if log_group_name is not None:
            props["logGroupName"] = log_group_name

        if log_role_arn is not None:
            props["logRoleArn"] = log_role_arn

        jsii.create(CfnMacro, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="macroName")
    def macro_name(self) -> str:
        return jsii.get(self, "macroName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMacroProps":
        return jsii.get(self, "propertyOverrides")


class _CfnMacroProps(jsii.compat.TypedDict, total=False):
    description: str
    logGroupName: str
    logRoleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CfnMacroProps")
class CfnMacroProps(_CfnMacroProps):
    functionName: str
    name: str

class CfnStack(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnStack"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, template_url: str, notification_arns: typing.Optional[typing.List[str]]=None, parameters: typing.Optional[typing.Union[typing.Mapping[str,str], aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, timeout_in_minutes: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnStackProps = {"templateUrl": template_url}

        if notification_arns is not None:
            props["notificationArns"] = notification_arns

        if parameters is not None:
            props["parameters"] = parameters

        if tags is not None:
            props["tags"] = tags

        if timeout_in_minutes is not None:
            props["timeoutInMinutes"] = timeout_in_minutes

        jsii.create(CfnStack, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStackProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        return jsii.get(self, "stackId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnStackProps(jsii.compat.TypedDict, total=False):
    notificationArns: typing.List[str]
    parameters: typing.Union[typing.Mapping[str,str], aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    timeoutInMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CfnStackProps")
class CfnStackProps(_CfnStackProps):
    templateUrl: str

class CfnWaitCondition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnWaitCondition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, count: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, handle: typing.Optional[str]=None, timeout: typing.Optional[str]=None) -> None:
        props: CfnWaitConditionProps = {}

        if count is not None:
            props["count"] = count

        if handle is not None:
            props["handle"] = handle

        if timeout is not None:
            props["timeout"] = timeout

        jsii.create(CfnWaitCondition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnWaitConditionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="waitConditionData")
    def wait_condition_data(self) -> aws_cdk.cdk.Token:
        return jsii.get(self, "waitConditionData")

    @property
    @jsii.member(jsii_name="waitConditionName")
    def wait_condition_name(self) -> str:
        return jsii.get(self, "waitConditionName")


class CfnWaitConditionHandle(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CfnWaitConditionHandle"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(CfnWaitConditionHandle, self, [scope, id])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="waitConditionHandleUrl")
    def wait_condition_handle_url(self) -> str:
        return jsii.get(self, "waitConditionHandleUrl")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CfnWaitConditionProps")
class CfnWaitConditionProps(jsii.compat.TypedDict, total=False):
    count: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    handle: str
    timeout: str

@jsii.enum(jsii_type="@aws-cdk/aws-cloudformation.CloudFormationCapabilities")
class CloudFormationCapabilities(enum.Enum):
    None_ = "None"
    AnonymousIAM = "AnonymousIAM"
    NamedIAM = "NamedIAM"

class CustomResource(CfnCustomResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudformation.CustomResource"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, lambda_provider: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None, resource_type: typing.Optional[str]=None, topic_provider: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        props: CustomResourceProps = {}

        if lambda_provider is not None:
            props["lambdaProvider"] = lambda_provider

        if properties is not None:
            props["properties"] = properties

        if resource_type is not None:
            props["resourceType"] = resource_type

        if topic_provider is not None:
            props["topicProvider"] = topic_provider

        jsii.create(CustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProps")
class CustomResourceProps(jsii.compat.TypedDict, total=False):
    lambdaProvider: aws_cdk.aws_lambda.IFunction
    properties: typing.Mapping[str,typing.Any]
    resourceType: str
    topicProvider: aws_cdk.aws_sns.ITopic

__all__ = ["CfnCustomResource", "CfnCustomResourceProps", "CfnMacro", "CfnMacroProps", "CfnStack", "CfnStackProps", "CfnWaitCondition", "CfnWaitConditionHandle", "CfnWaitConditionProps", "CloudFormationCapabilities", "CustomResource", "CustomResourceProps", "__jsii_assembly__"]

publication.publish()
