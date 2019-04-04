import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-events", "0.28.0", __name__, "aws-events@0.28.0.jsii.tgz")
class CfnEventBusPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.CfnEventBusPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, action: str, principal: str, statement_id: str, condition: typing.Optional[typing.Union["ConditionProperty", aws_cdk.cdk.Token]]=None) -> None:
        props: CfnEventBusPolicyProps = {"action": action, "principal": principal, "statementId": statement_id}

        if condition is not None:
            props["condition"] = condition

        jsii.create(CfnEventBusPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="eventBusPolicyId")
    def event_bus_policy_id(self) -> str:
        return jsii.get(self, "eventBusPolicyId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEventBusPolicyProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnEventBusPolicy.ConditionProperty")
    class ConditionProperty(jsii.compat.TypedDict, total=False):
        key: str
        type: str
        value: str


class _CfnEventBusPolicyProps(jsii.compat.TypedDict, total=False):
    condition: typing.Union["CfnEventBusPolicy.ConditionProperty", aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnEventBusPolicyProps")
class CfnEventBusPolicyProps(_CfnEventBusPolicyProps):
    action: str
    principal: str
    statementId: str

class CfnRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.CfnRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, name: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, state: typing.Optional[str]=None, targets: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TargetProperty"]]]]=None) -> None:
        props: CfnRuleProps = {}

        if description is not None:
            props["description"] = description

        if event_pattern is not None:
            props["eventPattern"] = event_pattern

        if name is not None:
            props["name"] = name

        if role_arn is not None:
            props["roleArn"] = role_arn

        if schedule_expression is not None:
            props["scheduleExpression"] = schedule_expression

        if state is not None:
            props["state"] = state

        if targets is not None:
            props["targets"] = targets

        jsii.create(CfnRule, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        return jsii.get(self, "ruleArn")

    @property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> str:
        return jsii.get(self, "ruleId")

    class _EcsParametersProperty(jsii.compat.TypedDict, total=False):
        taskCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.EcsParametersProperty")
    class EcsParametersProperty(_EcsParametersProperty):
        taskDefinitionArn: str

    class _InputTransformerProperty(jsii.compat.TypedDict, total=False):
        inputPathsMap: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.InputTransformerProperty")
    class InputTransformerProperty(_InputTransformerProperty):
        inputTemplate: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.KinesisParametersProperty")
    class KinesisParametersProperty(jsii.compat.TypedDict):
        partitionKeyPath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.RunCommandParametersProperty")
    class RunCommandParametersProperty(jsii.compat.TypedDict):
        runCommandTargets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRule.RunCommandTargetProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.RunCommandTargetProperty")
    class RunCommandTargetProperty(jsii.compat.TypedDict):
        key: str
        values: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.SqsParametersProperty")
    class SqsParametersProperty(jsii.compat.TypedDict):
        messageGroupId: str

    class _TargetProperty(jsii.compat.TypedDict, total=False):
        ecsParameters: typing.Union["CfnRule.EcsParametersProperty", aws_cdk.cdk.Token]
        input: str
        inputPath: str
        inputTransformer: typing.Union[aws_cdk.cdk.Token, "CfnRule.InputTransformerProperty"]
        kinesisParameters: typing.Union["CfnRule.KinesisParametersProperty", aws_cdk.cdk.Token]
        roleArn: str
        runCommandParameters: typing.Union["CfnRule.RunCommandParametersProperty", aws_cdk.cdk.Token]
        sqsParameters: typing.Union[aws_cdk.cdk.Token, "CfnRule.SqsParametersProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.TargetProperty")
    class TargetProperty(_TargetProperty):
        arn: str
        id: str


@jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRuleProps")
class CfnRuleProps(jsii.compat.TypedDict, total=False):
    description: str
    eventPattern: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    name: str
    roleArn: str
    scheduleExpression: str
    state: str
    targets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRule.TargetProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventPattern")
class EventPattern(jsii.compat.TypedDict, total=False):
    account: typing.List[str]
    detail: typing.Any
    detailType: typing.List[str]
    id: typing.List[str]
    region: typing.List[str]
    resources: typing.List[str]
    source: typing.List[str]
    time: typing.List[str]
    version: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventRuleImportProps")
class EventRuleImportProps(jsii.compat.TypedDict):
    eventRuleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventRuleProps")
class EventRuleProps(jsii.compat.TypedDict, total=False):
    description: str
    enabled: bool
    eventPattern: "EventPattern"
    ruleName: str
    scheduleExpression: str
    targets: typing.List["IEventRuleTarget"]

class _EventRuleTargetProps(jsii.compat.TypedDict, total=False):
    ecsParameters: "CfnRule.EcsParametersProperty"
    kinesisParameters: "CfnRule.KinesisParametersProperty"
    roleArn: str
    runCommandParameters: "CfnRule.RunCommandParametersProperty"

@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventRuleTargetProps")
class EventRuleTargetProps(_EventRuleTargetProps):
    arn: str
    id: str

@jsii.interface(jsii_type="@aws-cdk/aws-events.IEventRule")
class IEventRule(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IEventRuleProxy

    @property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "EventRuleImportProps":
        ...


class _IEventRuleProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-events.IEventRule"
    @property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        return jsii.get(self, "ruleArn")

    @jsii.member(jsii_name="export")
    def export(self) -> "EventRuleImportProps":
        return jsii.invoke(self, "export", [])


@jsii.implements(IEventRule)
class EventRule(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.EventRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional["EventPattern"]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List["IEventRuleTarget"]]=None) -> None:
        props: EventRuleProps = {}

        if description is not None:
            props["description"] = description

        if enabled is not None:
            props["enabled"] = enabled

        if event_pattern is not None:
            props["eventPattern"] = event_pattern

        if rule_name is not None:
            props["ruleName"] = rule_name

        if schedule_expression is not None:
            props["scheduleExpression"] = schedule_expression

        if targets is not None:
            props["targets"] = targets

        jsii.create(EventRule, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, event_rule_arn: str) -> "IEventRule":
        props: EventRuleImportProps = {"eventRuleArn": event_rule_arn}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addEventPattern")
    def add_event_pattern(self, *, account: typing.Optional[typing.List[str]]=None, detail: typing.Any=None, detail_type: typing.Optional[typing.List[str]]=None, id: typing.Optional[typing.List[str]]=None, region: typing.Optional[typing.List[str]]=None, resources: typing.Optional[typing.List[str]]=None, source: typing.Optional[typing.List[str]]=None, time: typing.Optional[typing.List[str]]=None, version: typing.Optional[typing.List[str]]=None) -> None:
        event_pattern: EventPattern = {}

        if account is not None:
            event_pattern["account"] = account

        if detail is not None:
            event_pattern["detail"] = detail

        if detail_type is not None:
            event_pattern["detailType"] = detail_type

        if id is not None:
            event_pattern["id"] = id

        if region is not None:
            event_pattern["region"] = region

        if resources is not None:
            event_pattern["resources"] = resources

        if source is not None:
            event_pattern["source"] = source

        if time is not None:
            event_pattern["time"] = time

        if version is not None:
            event_pattern["version"] = version

        return jsii.invoke(self, "addEventPattern", [event_pattern])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: typing.Optional["IEventRuleTarget"]=None, *, json_template: typing.Any=None, paths_map: typing.Optional[typing.Mapping[str,str]]=None, text_template: typing.Optional[str]=None) -> None:
        input_options: TargetInputTemplate = {}

        if json_template is not None:
            input_options["jsonTemplate"] = json_template

        if paths_map is not None:
            input_options["pathsMap"] = paths_map

        if text_template is not None:
            input_options["textTemplate"] = text_template

        return jsii.invoke(self, "addTarget", [target, input_options])

    @jsii.member(jsii_name="export")
    def export(self) -> "EventRuleImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        return jsii.get(self, "ruleArn")


@jsii.interface(jsii_type="@aws-cdk/aws-events.IEventRuleTarget")
class IEventRuleTarget(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IEventRuleTargetProxy

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, rule_arn: str, rule_unique_id: str) -> "EventRuleTargetProps":
        ...


class _IEventRuleTargetProxy():
    __jsii_type__ = "@aws-cdk/aws-events.IEventRuleTarget"
    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, rule_arn: str, rule_unique_id: str) -> "EventRuleTargetProps":
        return jsii.invoke(self, "asEventRuleTarget", [rule_arn, rule_unique_id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events.TargetInputTemplate")
class TargetInputTemplate(jsii.compat.TypedDict, total=False):
    jsonTemplate: typing.Any
    pathsMap: typing.Mapping[str,str]
    textTemplate: str

__all__ = ["CfnEventBusPolicy", "CfnEventBusPolicyProps", "CfnRule", "CfnRuleProps", "EventPattern", "EventRule", "EventRuleImportProps", "EventRuleProps", "EventRuleTargetProps", "IEventRule", "IEventRuleTarget", "TargetInputTemplate", "__jsii_assembly__"]

publication.publish()
