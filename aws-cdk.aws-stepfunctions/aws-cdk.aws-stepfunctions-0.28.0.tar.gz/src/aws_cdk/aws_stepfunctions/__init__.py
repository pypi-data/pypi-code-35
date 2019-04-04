import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-stepfunctions", "0.28.0", __name__, "aws-stepfunctions@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.ActivityProps")
class ActivityProps(jsii.compat.TypedDict, total=False):
    activityName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.AfterwardsOptions")
class AfterwardsOptions(jsii.compat.TypedDict, total=False):
    includeErrorHandlers: bool
    includeOtherwise: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CatchProps")
class CatchProps(jsii.compat.TypedDict, total=False):
    errors: typing.List[str]
    resultPath: str

class CfnActivity(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.CfnActivity"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        props: CfnActivityProps = {"name": name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnActivity, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="activityArn")
    def activity_arn(self) -> str:
        return jsii.get(self, "activityArn")

    @property
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> str:
        return jsii.get(self, "activityName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnActivityProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnActivity.TagsEntryProperty")
    class TagsEntryProperty(jsii.compat.TypedDict):
        key: str
        value: str


class _CfnActivityProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnActivity.TagsEntryProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnActivityProps")
class CfnActivityProps(_CfnActivityProps):
    name: str

class CfnStateMachine(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachine"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, definition_string: str, role_arn: str, state_machine_name: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        props: CfnStateMachineProps = {"definitionString": definition_string, "roleArn": role_arn}

        if state_machine_name is not None:
            props["stateMachineName"] = state_machine_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnStateMachine, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStateMachineProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> str:
        return jsii.get(self, "stateMachineArn")

    @property
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> str:
        return jsii.get(self, "stateMachineName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachine.TagsEntryProperty")
    class TagsEntryProperty(jsii.compat.TypedDict):
        key: str
        value: str


class _CfnStateMachineProps(jsii.compat.TypedDict, total=False):
    stateMachineName: str
    tags: typing.List["CfnStateMachine.TagsEntryProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachineProps")
class CfnStateMachineProps(_CfnStateMachineProps):
    definitionString: str
    roleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.ChoiceProps")
class ChoiceProps(jsii.compat.TypedDict, total=False):
    comment: str
    inputPath: str
    outputPath: str

class Condition(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-stepfunctions.Condition"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ConditionProxy

    def __init__(self) -> None:
        jsii.create(Condition, self, [])

    @jsii.member(jsii_name="and")
    @classmethod
    def and_(cls, *conditions: "Condition") -> "Condition":
        return jsii.sinvoke(cls, "and", [conditions])

    @jsii.member(jsii_name="booleanEquals")
    @classmethod
    def boolean_equals(cls, variable: str, value: bool) -> "Condition":
        return jsii.sinvoke(cls, "booleanEquals", [variable, value])

    @jsii.member(jsii_name="not")
    @classmethod
    def not_(cls, condition: "Condition") -> "Condition":
        return jsii.sinvoke(cls, "not", [condition])

    @jsii.member(jsii_name="numberEquals")
    @classmethod
    def number_equals(cls, variable: str, value: jsii.Number) -> "Condition":
        return jsii.sinvoke(cls, "numberEquals", [variable, value])

    @jsii.member(jsii_name="numberGreaterThan")
    @classmethod
    def number_greater_than(cls, variable: str, value: jsii.Number) -> "Condition":
        return jsii.sinvoke(cls, "numberGreaterThan", [variable, value])

    @jsii.member(jsii_name="numberGreaterThanEquals")
    @classmethod
    def number_greater_than_equals(cls, variable: str, value: jsii.Number) -> "Condition":
        return jsii.sinvoke(cls, "numberGreaterThanEquals", [variable, value])

    @jsii.member(jsii_name="numberLessThan")
    @classmethod
    def number_less_than(cls, variable: str, value: jsii.Number) -> "Condition":
        return jsii.sinvoke(cls, "numberLessThan", [variable, value])

    @jsii.member(jsii_name="numberLessThanEquals")
    @classmethod
    def number_less_than_equals(cls, variable: str, value: jsii.Number) -> "Condition":
        return jsii.sinvoke(cls, "numberLessThanEquals", [variable, value])

    @jsii.member(jsii_name="or")
    @classmethod
    def or_(cls, *conditions: "Condition") -> "Condition":
        return jsii.sinvoke(cls, "or", [conditions])

    @jsii.member(jsii_name="stringEquals")
    @classmethod
    def string_equals(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "stringEquals", [variable, value])

    @jsii.member(jsii_name="stringGreaterThan")
    @classmethod
    def string_greater_than(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "stringGreaterThan", [variable, value])

    @jsii.member(jsii_name="stringGreaterThanEquals")
    @classmethod
    def string_greater_than_equals(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "stringGreaterThanEquals", [variable, value])

    @jsii.member(jsii_name="stringLessThan")
    @classmethod
    def string_less_than(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "stringLessThan", [variable, value])

    @jsii.member(jsii_name="stringLessThanEquals")
    @classmethod
    def string_less_than_equals(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "stringLessThanEquals", [variable, value])

    @jsii.member(jsii_name="timestampEquals")
    @classmethod
    def timestamp_equals(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "timestampEquals", [variable, value])

    @jsii.member(jsii_name="timestampGreaterThan")
    @classmethod
    def timestamp_greater_than(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "timestampGreaterThan", [variable, value])

    @jsii.member(jsii_name="timestampGreaterThanEquals")
    @classmethod
    def timestamp_greater_than_equals(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "timestampGreaterThanEquals", [variable, value])

    @jsii.member(jsii_name="timestampLessThan")
    @classmethod
    def timestamp_less_than(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "timestampLessThan", [variable, value])

    @jsii.member(jsii_name="timestampLessThanEquals")
    @classmethod
    def timestamp_less_than_equals(cls, variable: str, value: str) -> "Condition":
        return jsii.sinvoke(cls, "timestampLessThanEquals", [variable, value])

    @jsii.member(jsii_name="renderCondition")
    @abc.abstractmethod
    def render_condition(self) -> typing.Any:
        ...


class _ConditionProxy(Condition):
    @jsii.member(jsii_name="renderCondition")
    def render_condition(self) -> typing.Any:
        return jsii.invoke(self, "renderCondition", [])


class Errors(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Errors"):
    def __init__(self) -> None:
        jsii.create(Errors, self, [])

    @classproperty
    @jsii.member(jsii_name="All")
    def ALL(cls) -> str:
        return jsii.sget(cls, "All")

    @classproperty
    @jsii.member(jsii_name="BranchFailed")
    def BRANCH_FAILED(cls) -> str:
        return jsii.sget(cls, "BranchFailed")

    @classproperty
    @jsii.member(jsii_name="NoChoiceMatched")
    def NO_CHOICE_MATCHED(cls) -> str:
        return jsii.sget(cls, "NoChoiceMatched")

    @classproperty
    @jsii.member(jsii_name="Permissions")
    def PERMISSIONS(cls) -> str:
        return jsii.sget(cls, "Permissions")

    @classproperty
    @jsii.member(jsii_name="ResultPathMatchFailure")
    def RESULT_PATH_MATCH_FAILURE(cls) -> str:
        return jsii.sget(cls, "ResultPathMatchFailure")

    @classproperty
    @jsii.member(jsii_name="TaskFailed")
    def TASK_FAILED(cls) -> str:
        return jsii.sget(cls, "TaskFailed")

    @classproperty
    @jsii.member(jsii_name="Timeout")
    def TIMEOUT(cls) -> str:
        return jsii.sget(cls, "Timeout")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.FailProps")
class FailProps(jsii.compat.TypedDict, total=False):
    cause: str
    comment: str
    error: str

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.FindStateOptions")
class FindStateOptions(jsii.compat.TypedDict, total=False):
    includeErrorHandlers: bool

@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.IChainable")
class IChainable(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IChainableProxy

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        ...

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        ...


class _IChainableProxy():
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.IChainable"
    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        return jsii.get(self, "id")

    @property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        return jsii.get(self, "startState")


@jsii.implements(IChainable)
class Chain(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Chain"):
    @jsii.member(jsii_name="custom")
    @classmethod
    def custom(cls, start_state: "State", end_states: typing.List["INextable"], last_added: "IChainable") -> "Chain":
        return jsii.sinvoke(cls, "custom", [start_state, end_states, last_added])

    @jsii.member(jsii_name="sequence")
    @classmethod
    def sequence(cls, start: "IChainable", next: "IChainable") -> "Chain":
        return jsii.sinvoke(cls, "sequence", [start, next])

    @jsii.member(jsii_name="start")
    @classmethod
    def start(cls, state: "IChainable") -> "Chain":
        return jsii.sinvoke(cls, "start", [state])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toSingleState")
    def to_single_state(self, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None) -> "Parallel":
        props: ParallelProps = {}

        if comment is not None:
            props["comment"] = comment

        if input_path is not None:
            props["inputPath"] = input_path

        if output_path is not None:
            props["outputPath"] = output_path

        if result_path is not None:
            props["resultPath"] = result_path

        return jsii.invoke(self, "toSingleState", [id, props])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        return jsii.get(self, "id")

    @property
    @jsii.member(jsii_name="lastAdded")
    def last_added(self) -> "IChainable":
        return jsii.get(self, "lastAdded")

    @property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        return jsii.get(self, "startState")


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.INextable")
class INextable(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _INextableProxy

    @jsii.member(jsii_name="next")
    def next(self, state: "IChainable") -> "Chain":
        ...


class _INextableProxy():
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.INextable"
    @jsii.member(jsii_name="next")
    def next(self, state: "IChainable") -> "Chain":
        return jsii.invoke(self, "next", [state])


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.IStateMachine")
class IStateMachine(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IStateMachineProxy

    @property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "StateMachineImportProps":
        ...


class _IStateMachineProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.IStateMachine"
    @property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> str:
        return jsii.get(self, "stateMachineArn")

    @jsii.member(jsii_name="export")
    def export(self) -> "StateMachineImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.IStepFunctionsTaskResource")
class IStepFunctionsTaskResource(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IStepFunctionsTaskResourceProxy

    @jsii.member(jsii_name="asStepFunctionsTaskResource")
    def as_step_functions_task_resource(self, calling_task: "Task") -> "StepFunctionsTaskResourceProps":
        ...


class _IStepFunctionsTaskResourceProxy():
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.IStepFunctionsTaskResource"
    @jsii.member(jsii_name="asStepFunctionsTaskResource")
    def as_step_functions_task_resource(self, calling_task: "Task") -> "StepFunctionsTaskResourceProps":
        return jsii.invoke(self, "asStepFunctionsTaskResource", [calling_task])


@jsii.implements(IStepFunctionsTaskResource)
class Activity(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Activity"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, activity_name: typing.Optional[str]=None) -> None:
        props: ActivityProps = {}

        if activity_name is not None:
            props["activityName"] = activity_name

        jsii.create(Activity, self, [scope, id, props])

    @jsii.member(jsii_name="asStepFunctionsTaskResource")
    def as_step_functions_task_resource(self, _calling_task: "Task") -> "StepFunctionsTaskResourceProps":
        return jsii.invoke(self, "asStepFunctionsTaskResource", [_calling_task])

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

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricFailed", [props])

    @jsii.member(jsii_name="metricHeartbeatTimedOut")
    def metric_heartbeat_timed_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricHeartbeatTimedOut", [props])

    @jsii.member(jsii_name="metricRunTime")
    def metric_run_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricRunTime", [props])

    @jsii.member(jsii_name="metricScheduled")
    def metric_scheduled(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricScheduled", [props])

    @jsii.member(jsii_name="metricScheduleTime")
    def metric_schedule_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricScheduleTime", [props])

    @jsii.member(jsii_name="metricStarted")
    def metric_started(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricStarted", [props])

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSucceeded", [props])

    @jsii.member(jsii_name="metricTime")
    def metric_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTime", [props])

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTimedOut", [props])

    @property
    @jsii.member(jsii_name="activityArn")
    def activity_arn(self) -> str:
        return jsii.get(self, "activityArn")

    @property
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> str:
        return jsii.get(self, "activityName")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.ParallelProps")
class ParallelProps(jsii.compat.TypedDict, total=False):
    comment: str
    inputPath: str
    outputPath: str
    resultPath: str

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.PassProps")
class PassProps(jsii.compat.TypedDict, total=False):
    comment: str
    inputPath: str
    outputPath: str
    result: typing.Any
    resultPath: str

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.RetryProps")
class RetryProps(jsii.compat.TypedDict, total=False):
    backoffRate: jsii.Number
    errors: typing.List[str]
    intervalSeconds: jsii.Number
    maxAttempts: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.SingleStateOptions")
class SingleStateOptions(ParallelProps, jsii.compat.TypedDict, total=False):
    prefixStates: str
    stateId: str

@jsii.implements(IChainable)
class State(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-stepfunctions.State"):
    @staticmethod
    def __jsii_proxy_class__():
        return _StateProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str,typing.Any]]=None, result_path: typing.Optional[str]=None) -> None:
        props: StateProps = {}

        if comment is not None:
            props["comment"] = comment

        if input_path is not None:
            props["inputPath"] = input_path

        if output_path is not None:
            props["outputPath"] = output_path

        if parameters is not None:
            props["parameters"] = parameters

        if result_path is not None:
            props["resultPath"] = result_path

        jsii.create(State, self, [scope, id, props])

    @jsii.member(jsii_name="filterNextables")
    @classmethod
    def filter_nextables(cls, states: typing.List["State"]) -> typing.List["INextable"]:
        return jsii.sinvoke(cls, "filterNextables", [states])

    @jsii.member(jsii_name="findReachableEndStates")
    @classmethod
    def find_reachable_end_states(cls, start: "State", *, include_error_handlers: typing.Optional[bool]=None) -> typing.List["State"]:
        options: FindStateOptions = {}

        if include_error_handlers is not None:
            options["includeErrorHandlers"] = include_error_handlers

        return jsii.sinvoke(cls, "findReachableEndStates", [start, options])

    @jsii.member(jsii_name="prefixStates")
    @classmethod
    def prefix_states(cls, root: aws_cdk.cdk.IConstruct, prefix: str) -> None:
        return jsii.sinvoke(cls, "prefixStates", [root, prefix])

    @jsii.member(jsii_name="addBranch")
    def _add_branch(self, branch: "StateGraph") -> None:
        return jsii.invoke(self, "addBranch", [branch])

    @jsii.member(jsii_name="addChoice")
    def _add_choice(self, condition: "Condition", next: "State") -> None:
        return jsii.invoke(self, "addChoice", [condition, next])

    @jsii.member(jsii_name="addPrefix")
    def add_prefix(self, x: str) -> None:
        return jsii.invoke(self, "addPrefix", [x])

    @jsii.member(jsii_name="bindToGraph")
    def bind_to_graph(self, graph: "StateGraph") -> None:
        return jsii.invoke(self, "bindToGraph", [graph])

    @jsii.member(jsii_name="makeDefault")
    def _make_default(self, def_: "State") -> None:
        return jsii.invoke(self, "makeDefault", [def_])

    @jsii.member(jsii_name="makeNext")
    def _make_next(self, next: "State") -> None:
        return jsii.invoke(self, "makeNext", [next])

    @jsii.member(jsii_name="onBindToGraph")
    def _on_bind_to_graph(self, graph: "StateGraph") -> None:
        return jsii.invoke(self, "onBindToGraph", [graph])

    @jsii.member(jsii_name="renderBranches")
    def _render_branches(self) -> typing.Any:
        return jsii.invoke(self, "renderBranches", [])

    @jsii.member(jsii_name="renderChoices")
    def _render_choices(self) -> typing.Any:
        return jsii.invoke(self, "renderChoices", [])

    @jsii.member(jsii_name="renderInputOutput")
    def _render_input_output(self) -> typing.Any:
        return jsii.invoke(self, "renderInputOutput", [])

    @jsii.member(jsii_name="renderNextEnd")
    def _render_next_end(self) -> typing.Any:
        return jsii.invoke(self, "renderNextEnd", [])

    @jsii.member(jsii_name="renderRetryCatch")
    def _render_retry_catch(self) -> typing.Any:
        return jsii.invoke(self, "renderRetryCatch", [])

    @jsii.member(jsii_name="toStateJson")
    @abc.abstractmethod
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        ...

    @property
    @jsii.member(jsii_name="branches")
    def _branches(self) -> typing.List["StateGraph"]:
        return jsii.get(self, "branches")

    @property
    @jsii.member(jsii_name="endStates")
    @abc.abstractmethod
    def end_states(self) -> typing.List["INextable"]:
        ...

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        return jsii.get(self, "id")

    @property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        return jsii.get(self, "startState")

    @property
    @jsii.member(jsii_name="stateId")
    def state_id(self) -> str:
        return jsii.get(self, "stateId")

    @property
    @jsii.member(jsii_name="comment")
    def _comment(self) -> typing.Optional[str]:
        return jsii.get(self, "comment")

    @property
    @jsii.member(jsii_name="inputPath")
    def _input_path(self) -> typing.Optional[str]:
        return jsii.get(self, "inputPath")

    @property
    @jsii.member(jsii_name="outputPath")
    def _output_path(self) -> typing.Optional[str]:
        return jsii.get(self, "outputPath")

    @property
    @jsii.member(jsii_name="parameters")
    def _parameters(self) -> typing.Optional[typing.Mapping[typing.Any, typing.Any]]:
        return jsii.get(self, "parameters")

    @property
    @jsii.member(jsii_name="resultPath")
    def _result_path(self) -> typing.Optional[str]:
        return jsii.get(self, "resultPath")

    @property
    @jsii.member(jsii_name="defaultChoice")
    def _default_choice(self) -> typing.Optional["State"]:
        return jsii.get(self, "defaultChoice")

    @_default_choice.setter
    def _default_choice(self, value: typing.Optional["State"]):
        return jsii.set(self, "defaultChoice", value)


class _StateProxy(State):
    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toStateJson", [])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")


class Choice(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Choice"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None) -> None:
        props: ChoiceProps = {}

        if comment is not None:
            props["comment"] = comment

        if input_path is not None:
            props["inputPath"] = input_path

        if output_path is not None:
            props["outputPath"] = output_path

        jsii.create(Choice, self, [scope, id, props])

    @jsii.member(jsii_name="afterwards")
    def afterwards(self, *, include_error_handlers: typing.Optional[bool]=None, include_otherwise: typing.Optional[bool]=None) -> "Chain":
        options: AfterwardsOptions = {}

        if include_error_handlers is not None:
            options["includeErrorHandlers"] = include_error_handlers

        if include_otherwise is not None:
            options["includeOtherwise"] = include_otherwise

        return jsii.invoke(self, "afterwards", [options])

    @jsii.member(jsii_name="otherwise")
    def otherwise(self, def_: "IChainable") -> "Choice":
        return jsii.invoke(self, "otherwise", [def_])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toStateJson", [])

    @jsii.member(jsii_name="when")
    def when(self, condition: "Condition", next: "IChainable") -> "Choice":
        return jsii.invoke(self, "when", [condition, next])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")


class Fail(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Fail"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cause: typing.Optional[str]=None, comment: typing.Optional[str]=None, error: typing.Optional[str]=None) -> None:
        props: FailProps = {}

        if cause is not None:
            props["cause"] = cause

        if comment is not None:
            props["comment"] = comment

        if error is not None:
            props["error"] = error

        jsii.create(Fail, self, [scope, id, props])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toStateJson", [])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")


@jsii.implements(INextable)
class Parallel(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Parallel"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None) -> None:
        props: ParallelProps = {}

        if comment is not None:
            props["comment"] = comment

        if input_path is not None:
            props["inputPath"] = input_path

        if output_path is not None:
            props["outputPath"] = output_path

        if result_path is not None:
            props["resultPath"] = result_path

        jsii.create(Parallel, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(self, handler: "IChainable", *, errors: typing.Optional[typing.List[str]]=None, result_path: typing.Optional[str]=None) -> "Parallel":
        props: CatchProps = {}

        if errors is not None:
            props["errors"] = errors

        if result_path is not None:
            props["resultPath"] = result_path

        return jsii.invoke(self, "addCatch", [handler, props])

    @jsii.member(jsii_name="addRetry")
    def add_retry(self, *, backoff_rate: typing.Optional[jsii.Number]=None, errors: typing.Optional[typing.List[str]]=None, interval_seconds: typing.Optional[jsii.Number]=None, max_attempts: typing.Optional[jsii.Number]=None) -> "Parallel":
        props: RetryProps = {}

        if backoff_rate is not None:
            props["backoffRate"] = backoff_rate

        if errors is not None:
            props["errors"] = errors

        if interval_seconds is not None:
            props["intervalSeconds"] = interval_seconds

        if max_attempts is not None:
            props["maxAttempts"] = max_attempts

        return jsii.invoke(self, "addRetry", [props])

    @jsii.member(jsii_name="branch")
    def branch(self, *branches: "IChainable") -> "Parallel":
        return jsii.invoke(self, "branch", [branches])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toStateJson", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")


@jsii.implements(INextable)
class Pass(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Pass"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result: typing.Any=None, result_path: typing.Optional[str]=None) -> None:
        props: PassProps = {}

        if comment is not None:
            props["comment"] = comment

        if input_path is not None:
            props["inputPath"] = input_path

        if output_path is not None:
            props["outputPath"] = output_path

        if result is not None:
            props["result"] = result

        if result_path is not None:
            props["resultPath"] = result_path

        jsii.create(Pass, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toStateJson", [])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")


class StateGraph(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.StateGraph"):
    def __init__(self, start_state: "State", graph_description: str) -> None:
        jsii.create(StateGraph, self, [start_state, graph_description])

    @jsii.member(jsii_name="registerPolicyStatement")
    def register_policy_statement(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "registerPolicyStatement", [statement])

    @jsii.member(jsii_name="registerState")
    def register_state(self, state: "State") -> None:
        return jsii.invoke(self, "registerState", [state])

    @jsii.member(jsii_name="registerSuperGraph")
    def register_super_graph(self, graph: "StateGraph") -> None:
        return jsii.invoke(self, "registerSuperGraph", [graph])

    @jsii.member(jsii_name="toGraphJson")
    def to_graph_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toGraphJson", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="graphDescription")
    def graph_description(self) -> str:
        return jsii.get(self, "graphDescription")

    @property
    @jsii.member(jsii_name="policyStatements")
    def policy_statements(self) -> typing.List[aws_cdk.aws_iam.PolicyStatement]:
        return jsii.get(self, "policyStatements")

    @property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        return jsii.get(self, "startState")

    @property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "timeoutSeconds")

    @timeout_seconds.setter
    def timeout_seconds(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "timeoutSeconds", value)


@jsii.implements(IStateMachine, aws_cdk.aws_events.IEventRuleTarget)
class StateMachine(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.StateMachine"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, definition: "IChainable", role: typing.Optional[aws_cdk.aws_iam.Role]=None, state_machine_name: typing.Optional[str]=None, timeout_sec: typing.Optional[jsii.Number]=None) -> None:
        props: StateMachineProps = {"definition": definition}

        if role is not None:
            props["role"] = role

        if state_machine_name is not None:
            props["stateMachineName"] = state_machine_name

        if timeout_sec is not None:
            props["timeoutSec"] = timeout_sec

        jsii.create(StateMachine, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, state_machine_arn: str) -> "IStateMachine":
        props: StateMachineImportProps = {"stateMachineArn": state_machine_arn}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @jsii.member(jsii_name="export")
    def export(self) -> "StateMachineImportProps":
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

    @jsii.member(jsii_name="metricAborted")
    def metric_aborted(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricAborted", [props])

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricFailed", [props])

    @jsii.member(jsii_name="metricStarted")
    def metric_started(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricStarted", [props])

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSucceeded", [props])

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricThrottled", [props])

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTimedOut", [props])

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "role")

    @property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> str:
        return jsii.get(self, "stateMachineArn")

    @property
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> str:
        return jsii.get(self, "stateMachineName")


@jsii.implements(IChainable)
class StateMachineFragment(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-stepfunctions.StateMachineFragment"):
    @staticmethod
    def __jsii_proxy_class__():
        return _StateMachineFragmentProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(StateMachineFragment, self, [scope, id])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="prefixStates")
    def prefix_states(self, prefix: typing.Optional[str]=None) -> "StateMachineFragment":
        return jsii.invoke(self, "prefixStates", [prefix])

    @jsii.member(jsii_name="toSingleState")
    def to_single_state(self, *, prefix_states: typing.Optional[str]=None, state_id: typing.Optional[str]=None, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None) -> "Parallel":
        options: SingleStateOptions = {}

        if prefix_states is not None:
            options["prefixStates"] = prefix_states

        if state_id is not None:
            options["stateId"] = state_id

        if comment is not None:
            options["comment"] = comment

        if input_path is not None:
            options["inputPath"] = input_path

        if output_path is not None:
            options["outputPath"] = output_path

        if result_path is not None:
            options["resultPath"] = result_path

        return jsii.invoke(self, "toSingleState", [options])

    @property
    @jsii.member(jsii_name="endStates")
    @abc.abstractmethod
    def end_states(self) -> typing.List["INextable"]:
        ...

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        return jsii.get(self, "id")

    @property
    @jsii.member(jsii_name="startState")
    @abc.abstractmethod
    def start_state(self) -> "State":
        ...


class _StateMachineFragmentProxy(StateMachineFragment):
    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")

    @property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        return jsii.get(self, "startState")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.StateMachineImportProps")
class StateMachineImportProps(jsii.compat.TypedDict):
    stateMachineArn: str

class _StateMachineProps(jsii.compat.TypedDict, total=False):
    role: aws_cdk.aws_iam.Role
    stateMachineName: str
    timeoutSec: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.StateMachineProps")
class StateMachineProps(_StateMachineProps):
    definition: "IChainable"

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.StateProps")
class StateProps(jsii.compat.TypedDict, total=False):
    comment: str
    inputPath: str
    outputPath: str
    parameters: typing.Mapping[str,typing.Any]
    resultPath: str

class StateTransitionMetric(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.StateTransitionMetric"):
    def __init__(self) -> None:
        jsii.create(StateTransitionMetric, self, [])

    @jsii.member(jsii_name="metric")
    @classmethod
    def metric(cls, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricConsumedCapacity")
    @classmethod
    def metric_consumed_capacity(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricConsumedCapacity", [props])

    @jsii.member(jsii_name="metricProvisionedBucketSize")
    @classmethod
    def metric_provisioned_bucket_size(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricProvisionedBucketSize", [props])

    @jsii.member(jsii_name="metricProvisionedRefillRate")
    @classmethod
    def metric_provisioned_refill_rate(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricProvisionedRefillRate", [props])

    @jsii.member(jsii_name="metricThrottledEvents")
    @classmethod
    def metric_throttled_events(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricThrottledEvents", [props])


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions.StateType")
class StateType(enum.Enum):
    Pass = "Pass"
    Task = "Task"
    Choice = "Choice"
    Wait = "Wait"
    Succeed = "Succeed"
    Fail = "Fail"
    Parallel = "Parallel"

class _StepFunctionsTaskResourceProps(jsii.compat.TypedDict, total=False):
    metricDimensions: typing.Mapping[str,typing.Any]
    metricPrefixPlural: str
    metricPrefixSingular: str
    policyStatements: typing.List[aws_cdk.aws_iam.PolicyStatement]

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.StepFunctionsTaskResourceProps")
class StepFunctionsTaskResourceProps(_StepFunctionsTaskResourceProps):
    resourceArn: str

class Succeed(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Succeed"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None) -> None:
        props: SucceedProps = {}

        if comment is not None:
            props["comment"] = comment

        if input_path is not None:
            props["inputPath"] = input_path

        if output_path is not None:
            props["outputPath"] = output_path

        jsii.create(Succeed, self, [scope, id, props])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toStateJson", [])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.SucceedProps")
class SucceedProps(jsii.compat.TypedDict, total=False):
    comment: str
    inputPath: str
    outputPath: str

@jsii.implements(INextable)
class Task(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Task"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource: "IStepFunctionsTaskResource", comment: typing.Optional[str]=None, heartbeat_seconds: typing.Optional[jsii.Number]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str,typing.Any]]=None, result_path: typing.Optional[str]=None, timeout_seconds: typing.Optional[jsii.Number]=None) -> None:
        props: TaskProps = {"resource": resource}

        if comment is not None:
            props["comment"] = comment

        if heartbeat_seconds is not None:
            props["heartbeatSeconds"] = heartbeat_seconds

        if input_path is not None:
            props["inputPath"] = input_path

        if output_path is not None:
            props["outputPath"] = output_path

        if parameters is not None:
            props["parameters"] = parameters

        if result_path is not None:
            props["resultPath"] = result_path

        if timeout_seconds is not None:
            props["timeoutSeconds"] = timeout_seconds

        jsii.create(Task, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(self, handler: "IChainable", *, errors: typing.Optional[typing.List[str]]=None, result_path: typing.Optional[str]=None) -> "Task":
        props: CatchProps = {}

        if errors is not None:
            props["errors"] = errors

        if result_path is not None:
            props["resultPath"] = result_path

        return jsii.invoke(self, "addCatch", [handler, props])

    @jsii.member(jsii_name="addRetry")
    def add_retry(self, *, backoff_rate: typing.Optional[jsii.Number]=None, errors: typing.Optional[typing.List[str]]=None, interval_seconds: typing.Optional[jsii.Number]=None, max_attempts: typing.Optional[jsii.Number]=None) -> "Task":
        props: RetryProps = {}

        if backoff_rate is not None:
            props["backoffRate"] = backoff_rate

        if errors is not None:
            props["errors"] = errors

        if interval_seconds is not None:
            props["intervalSeconds"] = interval_seconds

        if max_attempts is not None:
            props["maxAttempts"] = max_attempts

        return jsii.invoke(self, "addRetry", [props])

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

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricFailed", [props])

    @jsii.member(jsii_name="metricHeartbeatTimedOut")
    def metric_heartbeat_timed_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricHeartbeatTimedOut", [props])

    @jsii.member(jsii_name="metricRunTime")
    def metric_run_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricRunTime", [props])

    @jsii.member(jsii_name="metricScheduled")
    def metric_scheduled(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricScheduled", [props])

    @jsii.member(jsii_name="metricScheduleTime")
    def metric_schedule_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricScheduleTime", [props])

    @jsii.member(jsii_name="metricStarted")
    def metric_started(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricStarted", [props])

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSucceeded", [props])

    @jsii.member(jsii_name="metricTime")
    def metric_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTime", [props])

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTimedOut", [props])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="onBindToGraph")
    def _on_bind_to_graph(self, graph: "StateGraph") -> None:
        return jsii.invoke(self, "onBindToGraph", [graph])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toStateJson", [])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")


class _TaskProps(jsii.compat.TypedDict, total=False):
    comment: str
    heartbeatSeconds: jsii.Number
    inputPath: str
    outputPath: str
    parameters: typing.Mapping[str,typing.Any]
    resultPath: str
    timeoutSeconds: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.TaskProps")
class TaskProps(_TaskProps):
    resource: "IStepFunctionsTaskResource"

@jsii.implements(INextable)
class Wait(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Wait"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comment: typing.Optional[str]=None, seconds: typing.Optional[jsii.Number]=None, seconds_path: typing.Optional[str]=None, timestamp: typing.Optional[str]=None, timestamp_path: typing.Optional[str]=None) -> None:
        props: WaitProps = {}

        if comment is not None:
            props["comment"] = comment

        if seconds is not None:
            props["seconds"] = seconds

        if seconds_path is not None:
            props["secondsPath"] = seconds_path

        if timestamp is not None:
            props["timestamp"] = timestamp

        if timestamp_path is not None:
            props["timestampPath"] = timestamp_path

        jsii.create(Wait, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.invoke(self, "toStateJson", [])

    @property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        return jsii.get(self, "endStates")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.WaitProps")
class WaitProps(jsii.compat.TypedDict, total=False):
    comment: str
    seconds: jsii.Number
    secondsPath: str
    timestamp: str
    timestampPath: str

__all__ = ["Activity", "ActivityProps", "AfterwardsOptions", "CatchProps", "CfnActivity", "CfnActivityProps", "CfnStateMachine", "CfnStateMachineProps", "Chain", "Choice", "ChoiceProps", "Condition", "Errors", "Fail", "FailProps", "FindStateOptions", "IChainable", "INextable", "IStateMachine", "IStepFunctionsTaskResource", "Parallel", "ParallelProps", "Pass", "PassProps", "RetryProps", "SingleStateOptions", "State", "StateGraph", "StateMachine", "StateMachineFragment", "StateMachineImportProps", "StateMachineProps", "StateProps", "StateTransitionMetric", "StateType", "StepFunctionsTaskResourceProps", "Succeed", "SucceedProps", "Task", "TaskProps", "Wait", "WaitProps", "__jsii_assembly__"]

publication.publish()
