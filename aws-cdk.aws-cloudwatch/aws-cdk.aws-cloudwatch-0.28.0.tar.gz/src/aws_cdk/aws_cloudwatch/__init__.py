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
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloudwatch", "0.28.0", __name__, "aws-cloudwatch@0.28.0.jsii.tgz")
class Alarm(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Alarm"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, metric: "Metric", evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None) -> None:
        props: AlarmProps = {"metric": metric, "evaluationPeriods": evaluation_periods, "threshold": threshold}

        if actions_enabled is not None:
            props["actionsEnabled"] = actions_enabled

        if alarm_description is not None:
            props["alarmDescription"] = alarm_description

        if alarm_name is not None:
            props["alarmName"] = alarm_name

        if comparison_operator is not None:
            props["comparisonOperator"] = comparison_operator

        if datapoints_to_alarm is not None:
            props["datapointsToAlarm"] = datapoints_to_alarm

        if evaluate_low_sample_count_percentile is not None:
            props["evaluateLowSampleCountPercentile"] = evaluate_low_sample_count_percentile

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if treat_missing_data is not None:
            props["treatMissingData"] = treat_missing_data

        jsii.create(Alarm, self, [scope, id, props])

    @jsii.member(jsii_name="onAlarm")
    def on_alarm(self, *actions: "IAlarmAction") -> None:
        return jsii.invoke(self, "onAlarm", [actions])

    @jsii.member(jsii_name="onInsufficientData")
    def on_insufficient_data(self, *actions: "IAlarmAction") -> None:
        return jsii.invoke(self, "onInsufficientData", [actions])

    @jsii.member(jsii_name="onOk")
    def on_ok(self, *actions: "IAlarmAction") -> None:
        return jsii.invoke(self, "onOk", [actions])

    @jsii.member(jsii_name="toAnnotation")
    def to_annotation(self) -> "HorizontalAnnotation":
        return jsii.invoke(self, "toAnnotation", [])

    @property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        return jsii.get(self, "alarmArn")

    @property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        return jsii.get(self, "alarmName")

    @property
    @jsii.member(jsii_name="metric")
    def metric(self) -> "Metric":
        return jsii.get(self, "metric")


class _AlarmMetricJson(jsii.compat.TypedDict, total=False):
    dimensions: typing.List["Dimension"]
    extendedStatistic: str
    statistic: "Statistic"
    unit: "Unit"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmMetricJson")
class AlarmMetricJson(_AlarmMetricJson):
    metricName: str
    namespace: str
    period: jsii.Number

class CfnAlarm(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comparison_operator: str, evaluation_periods: typing.Union[jsii.Number, aws_cdk.cdk.Token], threshold: typing.Union[jsii.Number, aws_cdk.cdk.Token], actions_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, alarm_actions: typing.Optional[typing.List[str]]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, datapoints_to_alarm: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, dimensions: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "DimensionProperty"]]]]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, extended_statistic: typing.Optional[str]=None, insufficient_data_actions: typing.Optional[typing.List[str]]=None, metric_name: typing.Optional[str]=None, metrics: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "MetricDataQueryProperty"]]]]=None, namespace: typing.Optional[str]=None, ok_actions: typing.Optional[typing.List[str]]=None, period: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional[str]=None, unit: typing.Optional[str]=None) -> None:
        props: CfnAlarmProps = {"comparisonOperator": comparison_operator, "evaluationPeriods": evaluation_periods, "threshold": threshold}

        if actions_enabled is not None:
            props["actionsEnabled"] = actions_enabled

        if alarm_actions is not None:
            props["alarmActions"] = alarm_actions

        if alarm_description is not None:
            props["alarmDescription"] = alarm_description

        if alarm_name is not None:
            props["alarmName"] = alarm_name

        if datapoints_to_alarm is not None:
            props["datapointsToAlarm"] = datapoints_to_alarm

        if dimensions is not None:
            props["dimensions"] = dimensions

        if evaluate_low_sample_count_percentile is not None:
            props["evaluateLowSampleCountPercentile"] = evaluate_low_sample_count_percentile

        if extended_statistic is not None:
            props["extendedStatistic"] = extended_statistic

        if insufficient_data_actions is not None:
            props["insufficientDataActions"] = insufficient_data_actions

        if metric_name is not None:
            props["metricName"] = metric_name

        if metrics is not None:
            props["metrics"] = metrics

        if namespace is not None:
            props["namespace"] = namespace

        if ok_actions is not None:
            props["okActions"] = ok_actions

        if period is not None:
            props["period"] = period

        if statistic is not None:
            props["statistic"] = statistic

        if treat_missing_data is not None:
            props["treatMissingData"] = treat_missing_data

        if unit is not None:
            props["unit"] = unit

        jsii.create(CfnAlarm, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        return jsii.get(self, "alarmArn")

    @property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        return jsii.get(self, "alarmName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAlarmProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.DimensionProperty")
    class DimensionProperty(jsii.compat.TypedDict):
        name: str
        value: str

    class _MetricDataQueryProperty(jsii.compat.TypedDict, total=False):
        expression: str
        label: str
        metricStat: typing.Union[aws_cdk.cdk.Token, "CfnAlarm.MetricStatProperty"]
        returnData: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricDataQueryProperty")
    class MetricDataQueryProperty(_MetricDataQueryProperty):
        id: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricProperty")
    class MetricProperty(jsii.compat.TypedDict, total=False):
        dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAlarm.DimensionProperty"]]]
        metricName: str
        namespace: str

    class _MetricStatProperty(jsii.compat.TypedDict, total=False):
        unit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricStatProperty")
    class MetricStatProperty(_MetricStatProperty):
        metric: typing.Union[aws_cdk.cdk.Token, "CfnAlarm.MetricProperty"]
        period: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        stat: str


class _CfnAlarmProps(jsii.compat.TypedDict, total=False):
    actionsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    alarmActions: typing.List[str]
    alarmDescription: str
    alarmName: str
    datapointsToAlarm: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAlarm.DimensionProperty"]]]
    evaluateLowSampleCountPercentile: str
    extendedStatistic: str
    insufficientDataActions: typing.List[str]
    metricName: str
    metrics: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAlarm.MetricDataQueryProperty"]]]
    namespace: str
    okActions: typing.List[str]
    period: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    statistic: str
    treatMissingData: str
    unit: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarmProps")
class CfnAlarmProps(_CfnAlarmProps):
    comparisonOperator: str
    evaluationPeriods: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    threshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]

class CfnDashboard(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.CfnDashboard"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dashboard_body: str, dashboard_name: typing.Optional[str]=None) -> None:
        props: CfnDashboardProps = {"dashboardBody": dashboard_body}

        if dashboard_name is not None:
            props["dashboardName"] = dashboard_name

        jsii.create(CfnDashboard, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dashboardName")
    def dashboard_name(self) -> str:
        return jsii.get(self, "dashboardName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDashboardProps":
        return jsii.get(self, "propertyOverrides")


class _CfnDashboardProps(jsii.compat.TypedDict, total=False):
    dashboardName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnDashboardProps")
class CfnDashboardProps(_CfnDashboardProps):
    dashboardBody: str

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.ComparisonOperator")
class ComparisonOperator(enum.Enum):
    GreaterThanOrEqualToThreshold = "GreaterThanOrEqualToThreshold"
    GreaterThanThreshold = "GreaterThanThreshold"
    LessThanThreshold = "LessThanThreshold"
    LessThanOrEqualToThreshold = "LessThanOrEqualToThreshold"

class Dashboard(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Dashboard"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dashboard_name: typing.Optional[str]=None) -> None:
        props: DashboardProps = {}

        if dashboard_name is not None:
            props["dashboardName"] = dashboard_name

        jsii.create(Dashboard, self, [scope, id, props])

    @jsii.member(jsii_name="add")
    def add(self, *widgets: "IWidget") -> None:
        return jsii.invoke(self, "add", [widgets])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.DashboardProps")
class DashboardProps(jsii.compat.TypedDict, total=False):
    dashboardName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.Dimension")
class Dimension(jsii.compat.TypedDict):
    name: str
    value: typing.Any

class _HorizontalAnnotation(jsii.compat.TypedDict, total=False):
    color: str
    fill: "Shading"
    label: str
    visible: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.HorizontalAnnotation")
class HorizontalAnnotation(_HorizontalAnnotation):
    value: jsii.Number

@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IAlarmAction")
class IAlarmAction(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IAlarmActionProxy

    @property
    @jsii.member(jsii_name="alarmActionArn")
    def alarm_action_arn(self) -> str:
        ...


class _IAlarmActionProxy():
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IAlarmAction"
    @property
    @jsii.member(jsii_name="alarmActionArn")
    def alarm_action_arn(self) -> str:
        return jsii.get(self, "alarmActionArn")


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IWidget")
class IWidget(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IWidgetProxy

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        ...

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        ...

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        ...

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        ...


class _IWidgetProxy():
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IWidget"
    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return jsii.get(self, "width")

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])


@jsii.implements(IWidget)
class Column(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Column"):
    def __init__(self, *widgets: "IWidget") -> None:
        jsii.create(Column, self, [widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return jsii.get(self, "width")


@jsii.implements(IWidget)
class ConcreteWidget(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-cloudwatch.ConcreteWidget"):
    @staticmethod
    def __jsii_proxy_class__():
        return _ConcreteWidgetProxy

    def __init__(self, width: jsii.Number, height: jsii.Number) -> None:
        jsii.create(ConcreteWidget, self, [width, height])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    @abc.abstractmethod
    def to_json(self) -> typing.List[typing.Any]:
        ...

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return jsii.get(self, "width")

    @property
    @jsii.member(jsii_name="x")
    def _x(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "x")

    @_x.setter
    def _x(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "x", value)

    @property
    @jsii.member(jsii_name="y")
    def _y(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "y")

    @_y.setter
    def _y(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "y", value)


class _ConcreteWidgetProxy(ConcreteWidget):
    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])


class AlarmWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.AlarmWidget"):
    def __init__(self, *, alarm: "Alarm", left_axis_range: typing.Optional["YAxisRange"]=None, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        props: AlarmWidgetProps = {"alarm": alarm}

        if left_axis_range is not None:
            props["leftAxisRange"] = left_axis_range

        if height is not None:
            props["height"] = height

        if region is not None:
            props["region"] = region

        if title is not None:
            props["title"] = title

        if width is not None:
            props["width"] = width

        jsii.create(AlarmWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])


class GraphWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.GraphWidget"):
    def __init__(self, *, left: typing.Optional[typing.List["Metric"]]=None, left_annotations: typing.Optional[typing.List["HorizontalAnnotation"]]=None, left_axis_range: typing.Optional["YAxisRange"]=None, right: typing.Optional[typing.List["Metric"]]=None, right_annotations: typing.Optional[typing.List["HorizontalAnnotation"]]=None, right_axis_range: typing.Optional["YAxisRange"]=None, stacked: typing.Optional[bool]=None, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        props: GraphWidgetProps = {}

        if left is not None:
            props["left"] = left

        if left_annotations is not None:
            props["leftAnnotations"] = left_annotations

        if left_axis_range is not None:
            props["leftAxisRange"] = left_axis_range

        if right is not None:
            props["right"] = right

        if right_annotations is not None:
            props["rightAnnotations"] = right_annotations

        if right_axis_range is not None:
            props["rightAxisRange"] = right_axis_range

        if stacked is not None:
            props["stacked"] = stacked

        if height is not None:
            props["height"] = height

        if region is not None:
            props["region"] = region

        if title is not None:
            props["title"] = title

        if width is not None:
            props["width"] = width

        jsii.create(GraphWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])


class Metric(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Metric"):
    def __init__(self, *, metric_name: str, namespace: str, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None) -> None:
        props: MetricProps = {"metricName": metric_name, "namespace": namespace}

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

        jsii.create(Metric, self, [props])

    @jsii.member(jsii_name="grantPutMetricData")
    @classmethod
    def grant_put_metric_data(cls, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.sinvoke(cls, "grantPutMetricData", [grantee])

    @jsii.member(jsii_name="dimensionsAsList")
    def dimensions_as_list(self) -> typing.List["Dimension"]:
        return jsii.invoke(self, "dimensionsAsList", [])

    @jsii.member(jsii_name="newAlarm")
    def new_alarm(self, scope: aws_cdk.cdk.Construct, id: str, *, evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None) -> "Alarm":
        props: MetricAlarmProps = {"evaluationPeriods": evaluation_periods, "threshold": threshold}

        if actions_enabled is not None:
            props["actionsEnabled"] = actions_enabled

        if alarm_description is not None:
            props["alarmDescription"] = alarm_description

        if alarm_name is not None:
            props["alarmName"] = alarm_name

        if comparison_operator is not None:
            props["comparisonOperator"] = comparison_operator

        if datapoints_to_alarm is not None:
            props["datapointsToAlarm"] = datapoints_to_alarm

        if evaluate_low_sample_count_percentile is not None:
            props["evaluateLowSampleCountPercentile"] = evaluate_low_sample_count_percentile

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if treat_missing_data is not None:
            props["treatMissingData"] = treat_missing_data

        return jsii.invoke(self, "newAlarm", [scope, id, props])

    @jsii.member(jsii_name="with")
    def with_(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None) -> "Metric":
        props: MetricCustomization = {}

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

        return jsii.invoke(self, "with", [props])

    @property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> str:
        return jsii.get(self, "metricName")

    @property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> str:
        return jsii.get(self, "namespace")

    @property
    @jsii.member(jsii_name="periodSec")
    def period_sec(self) -> jsii.Number:
        return jsii.get(self, "periodSec")

    @property
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> str:
        return jsii.get(self, "statistic")

    @property
    @jsii.member(jsii_name="color")
    def color(self) -> typing.Optional[str]:
        return jsii.get(self, "color")

    @property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        return jsii.get(self, "dimensions")

    @property
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Optional[str]:
        return jsii.get(self, "label")

    @property
    @jsii.member(jsii_name="unit")
    def unit(self) -> typing.Optional["Unit"]:
        return jsii.get(self, "unit")


class _MetricAlarmProps(jsii.compat.TypedDict, total=False):
    actionsEnabled: bool
    alarmDescription: str
    alarmName: str
    comparisonOperator: "ComparisonOperator"
    datapointsToAlarm: jsii.Number
    evaluateLowSampleCountPercentile: str
    periodSec: jsii.Number
    statistic: str
    treatMissingData: "TreatMissingData"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricAlarmProps")
class MetricAlarmProps(_MetricAlarmProps):
    evaluationPeriods: jsii.Number
    threshold: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmProps")
class AlarmProps(MetricAlarmProps, jsii.compat.TypedDict):
    metric: "Metric"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricCustomization")
class MetricCustomization(jsii.compat.TypedDict, total=False):
    color: str
    dimensions: typing.Mapping[str,typing.Any]
    label: str
    periodSec: jsii.Number
    statistic: str
    unit: "Unit"

class _MetricProps(jsii.compat.TypedDict, total=False):
    color: str
    dimensions: typing.Mapping[str,typing.Any]
    label: str
    periodSec: jsii.Number
    statistic: str
    unit: "Unit"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricProps")
class MetricProps(_MetricProps):
    metricName: str
    namespace: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricWidgetProps")
class MetricWidgetProps(jsii.compat.TypedDict, total=False):
    height: jsii.Number
    region: str
    title: str
    width: jsii.Number

class _AlarmWidgetProps(MetricWidgetProps, jsii.compat.TypedDict, total=False):
    leftAxisRange: "YAxisRange"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmWidgetProps")
class AlarmWidgetProps(_AlarmWidgetProps):
    alarm: "Alarm"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.GraphWidgetProps")
class GraphWidgetProps(MetricWidgetProps, jsii.compat.TypedDict, total=False):
    left: typing.List["Metric"]
    leftAnnotations: typing.List["HorizontalAnnotation"]
    leftAxisRange: "YAxisRange"
    right: typing.List["Metric"]
    rightAnnotations: typing.List["HorizontalAnnotation"]
    rightAxisRange: "YAxisRange"
    stacked: bool

@jsii.implements(IWidget)
class Row(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Row"):
    def __init__(self, *widgets: "IWidget") -> None:
        jsii.create(Row, self, [widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return jsii.get(self, "width")


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Shading")
class Shading(enum.Enum):
    None_ = "None"
    Above = "Above"
    Below = "Below"

class SingleValueWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.SingleValueWidget"):
    def __init__(self, *, metrics: typing.List["Metric"], height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        props: SingleValueWidgetProps = {"metrics": metrics}

        if height is not None:
            props["height"] = height

        if region is not None:
            props["region"] = region

        if title is not None:
            props["title"] = title

        if width is not None:
            props["width"] = width

        jsii.create(SingleValueWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.SingleValueWidgetProps")
class SingleValueWidgetProps(MetricWidgetProps, jsii.compat.TypedDict):
    metrics: typing.List["Metric"]

@jsii.implements(IWidget)
class Spacer(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Spacer"):
    def __init__(self, *, height: typing.Optional[jsii.Number]=None, width: typing.Optional[jsii.Number]=None) -> None:
        props: SpacerProps = {}

        if height is not None:
            props["height"] = height

        if width is not None:
            props["width"] = width

        jsii.create(Spacer, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, _x: jsii.Number, _y: jsii.Number) -> None:
        return jsii.invoke(self, "position", [_x, _y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return jsii.get(self, "width")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.SpacerProps")
class SpacerProps(jsii.compat.TypedDict, total=False):
    height: jsii.Number
    width: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Statistic")
class Statistic(enum.Enum):
    SampleCount = "SampleCount"
    Average = "Average"
    Sum = "Sum"
    Minimum = "Minimum"
    Maximum = "Maximum"

class TextWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.TextWidget"):
    def __init__(self, *, markdown: str, height: typing.Optional[jsii.Number]=None, width: typing.Optional[jsii.Number]=None) -> None:
        props: TextWidgetProps = {"markdown": markdown}

        if height is not None:
            props["height"] = height

        if width is not None:
            props["width"] = width

        jsii.create(TextWidget, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        return jsii.invoke(self, "toJson", [])


class _TextWidgetProps(jsii.compat.TypedDict, total=False):
    height: jsii.Number
    width: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.TextWidgetProps")
class TextWidgetProps(_TextWidgetProps):
    markdown: str

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.TreatMissingData")
class TreatMissingData(enum.Enum):
    Breaching = "Breaching"
    NotBreaching = "NotBreaching"
    Ignore = "Ignore"
    Missing = "Missing"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Unit")
class Unit(enum.Enum):
    Seconds = "Seconds"
    Microseconds = "Microseconds"
    Milliseconds = "Milliseconds"
    Bytes_ = "Bytes_"
    Kilobytes = "Kilobytes"
    Megabytes = "Megabytes"
    Gigabytes = "Gigabytes"
    Terabytes = "Terabytes"
    Bits = "Bits"
    Kilobits = "Kilobits"
    Megabits = "Megabits"
    Gigabits = "Gigabits"
    Terabits = "Terabits"
    Percent = "Percent"
    Count = "Count"
    BytesPerSecond = "BytesPerSecond"
    KilobytesPerSecond = "KilobytesPerSecond"
    MegabytesPerSecond = "MegabytesPerSecond"
    GigabytesPerSecond = "GigabytesPerSecond"
    TerabytesPerSecond = "TerabytesPerSecond"
    BitsPerSecond = "BitsPerSecond"
    KilobitsPerSecond = "KilobitsPerSecond"
    MegabitsPerSecond = "MegabitsPerSecond"
    GigabitsPerSecond = "GigabitsPerSecond"
    TerabitsPerSecond = "TerabitsPerSecond"
    CountPerSecond = "CountPerSecond"
    None_ = "None"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.YAxisRange")
class YAxisRange(jsii.compat.TypedDict, total=False):
    max: jsii.Number
    min: jsii.Number

__all__ = ["Alarm", "AlarmMetricJson", "AlarmProps", "AlarmWidget", "AlarmWidgetProps", "CfnAlarm", "CfnAlarmProps", "CfnDashboard", "CfnDashboardProps", "Column", "ComparisonOperator", "ConcreteWidget", "Dashboard", "DashboardProps", "Dimension", "GraphWidget", "GraphWidgetProps", "HorizontalAnnotation", "IAlarmAction", "IWidget", "Metric", "MetricAlarmProps", "MetricCustomization", "MetricProps", "MetricWidgetProps", "Row", "Shading", "SingleValueWidget", "SingleValueWidgetProps", "Spacer", "SpacerProps", "Statistic", "TextWidget", "TextWidgetProps", "TreatMissingData", "Unit", "YAxisRange", "__jsii_assembly__"]

publication.publish()
