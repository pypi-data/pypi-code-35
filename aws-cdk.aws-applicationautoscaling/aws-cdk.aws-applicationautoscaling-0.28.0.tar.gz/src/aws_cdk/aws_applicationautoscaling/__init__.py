import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling_common
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-applicationautoscaling", "0.28.0", __name__, "aws-applicationautoscaling@0.28.0.jsii.tgz")
class _AdjustmentTier(jsii.compat.TypedDict, total=False):
    lowerBound: jsii.Number
    upperBound: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.AdjustmentTier")
class AdjustmentTier(_AdjustmentTier):
    adjustment: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.AdjustmentType")
class AdjustmentType(enum.Enum):
    ChangeInCapacity = "ChangeInCapacity"
    PercentChangeInCapacity = "PercentChangeInCapacity"
    ExactCapacity = "ExactCapacity"

class BaseScalableAttribute(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-applicationautoscaling.BaseScalableAttribute"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseScalableAttributeProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dimension: str, resource_id: str, role: aws_cdk.aws_iam.IRole, service_namespace: "ServiceNamespace", max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> None:
        props: BaseScalableAttributeProps = {"dimension": dimension, "resourceId": resource_id, "role": role, "serviceNamespace": service_namespace, "maxCapacity": max_capacity}

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        jsii.create(BaseScalableAttribute, self, [scope, id, props])

    @jsii.member(jsii_name="doScaleOnMetric")
    def _do_scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_sec: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        props: BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "doScaleOnMetric", [id, props])

    @jsii.member(jsii_name="doScaleOnSchedule")
    def _do_scale_on_schedule(self, id: str, *, schedule: str, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        props: ScalingSchedule = {"schedule": schedule}

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        return jsii.invoke(self, "doScaleOnSchedule", [id, props])

    @jsii.member(jsii_name="doScaleToTrackMetric")
    def _do_scale_to_track_metric(self, id: str, *, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.Metric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        props: BasicTargetTrackingScalingPolicyProps = {"targetValue": target_value}

        if custom_metric is not None:
            props["customMetric"] = custom_metric

        if predefined_metric is not None:
            props["predefinedMetric"] = predefined_metric

        if resource_label is not None:
            props["resourceLabel"] = resource_label

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "doScaleToTrackMetric", [id, props])

    @property
    @jsii.member(jsii_name="props")
    def _props(self) -> "BaseScalableAttributeProps":
        return jsii.get(self, "props")


class _BaseScalableAttributeProxy(BaseScalableAttribute):
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BaseTargetTrackingProps")
class BaseTargetTrackingProps(jsii.compat.TypedDict, total=False):
    disableScaleIn: bool
    policyName: str
    scaleInCooldownSec: jsii.Number
    scaleOutCooldownSec: jsii.Number

class _BasicStepScalingPolicyProps(jsii.compat.TypedDict, total=False):
    adjustmentType: "AdjustmentType"
    cooldownSec: jsii.Number
    minAdjustmentMagnitude: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BasicStepScalingPolicyProps")
class BasicStepScalingPolicyProps(_BasicStepScalingPolicyProps):
    metric: aws_cdk.aws_cloudwatch.Metric
    scalingSteps: typing.List["ScalingInterval"]

class _BasicTargetTrackingScalingPolicyProps(BaseTargetTrackingProps, jsii.compat.TypedDict, total=False):
    customMetric: aws_cdk.aws_cloudwatch.Metric
    predefinedMetric: "PredefinedMetric"
    resourceLabel: str

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BasicTargetTrackingScalingPolicyProps")
class BasicTargetTrackingScalingPolicyProps(_BasicTargetTrackingScalingPolicyProps):
    targetValue: jsii.Number

class CfnScalableTarget(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, max_capacity: typing.Union[jsii.Number, aws_cdk.cdk.Token], min_capacity: typing.Union[jsii.Number, aws_cdk.cdk.Token], resource_id: str, role_arn: str, scalable_dimension: str, service_namespace: str, scheduled_actions: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ScheduledActionProperty"]]]]=None) -> None:
        props: CfnScalableTargetProps = {"maxCapacity": max_capacity, "minCapacity": min_capacity, "resourceId": resource_id, "roleArn": role_arn, "scalableDimension": scalable_dimension, "serviceNamespace": service_namespace}

        if scheduled_actions is not None:
            props["scheduledActions"] = scheduled_actions

        jsii.create(CfnScalableTarget, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnScalableTargetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        return jsii.get(self, "scalableTargetId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget.ScalableTargetActionProperty")
    class ScalableTargetActionProperty(jsii.compat.TypedDict, total=False):
        maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _ScheduledActionProperty(jsii.compat.TypedDict, total=False):
        endTime: typing.Union[aws_cdk.cdk.Token, datetime.datetime]
        scalableTargetAction: typing.Union[aws_cdk.cdk.Token, "CfnScalableTarget.ScalableTargetActionProperty"]
        startTime: typing.Union[aws_cdk.cdk.Token, datetime.datetime]

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget.ScheduledActionProperty")
    class ScheduledActionProperty(_ScheduledActionProperty):
        schedule: str
        scheduledActionName: str


class _CfnScalableTargetProps(jsii.compat.TypedDict, total=False):
    scheduledActions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalableTarget.ScheduledActionProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTargetProps")
class CfnScalableTargetProps(_CfnScalableTargetProps):
    maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    resourceId: str
    roleArn: str
    scalableDimension: str
    serviceNamespace: str

class CfnScalingPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_name: str, policy_type: str, resource_id: typing.Optional[str]=None, scalable_dimension: typing.Optional[str]=None, scaling_target_id: typing.Optional[str]=None, service_namespace: typing.Optional[str]=None, step_scaling_policy_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "StepScalingPolicyConfigurationProperty"]]=None, target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TargetTrackingScalingPolicyConfigurationProperty"]]=None) -> None:
        props: CfnScalingPolicyProps = {"policyName": policy_name, "policyType": policy_type}

        if resource_id is not None:
            props["resourceId"] = resource_id

        if scalable_dimension is not None:
            props["scalableDimension"] = scalable_dimension

        if scaling_target_id is not None:
            props["scalingTargetId"] = scaling_target_id

        if service_namespace is not None:
            props["serviceNamespace"] = service_namespace

        if step_scaling_policy_configuration is not None:
            props["stepScalingPolicyConfiguration"] = step_scaling_policy_configuration

        if target_tracking_scaling_policy_configuration is not None:
            props["targetTrackingScalingPolicyConfiguration"] = target_tracking_scaling_policy_configuration

        jsii.create(CfnScalingPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnScalingPolicyProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        return jsii.get(self, "scalingPolicyArn")

    class _CustomizedMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.MetricDimensionProperty"]]]
        unit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.CustomizedMetricSpecificationProperty")
    class CustomizedMetricSpecificationProperty(_CustomizedMetricSpecificationProperty):
        metricName: str
        namespace: str
        statistic: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.MetricDimensionProperty")
    class MetricDimensionProperty(jsii.compat.TypedDict):
        name: str
        value: str

    class _PredefinedMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceLabel: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty")
    class PredefinedMetricSpecificationProperty(_PredefinedMetricSpecificationProperty):
        predefinedMetricType: str

    class _StepAdjustmentProperty(jsii.compat.TypedDict, total=False):
        metricIntervalLowerBound: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        metricIntervalUpperBound: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.StepAdjustmentProperty")
    class StepAdjustmentProperty(_StepAdjustmentProperty):
        scalingAdjustment: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.StepScalingPolicyConfigurationProperty")
    class StepScalingPolicyConfigurationProperty(jsii.compat.TypedDict, total=False):
        adjustmentType: str
        cooldown: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        metricAggregationType: str
        minAdjustmentMagnitude: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        stepAdjustments: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.StepAdjustmentProperty"]]]

    class _TargetTrackingScalingPolicyConfigurationProperty(jsii.compat.TypedDict, total=False):
        customizedMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.CustomizedMetricSpecificationProperty"]
        disableScaleIn: typing.Union[bool, aws_cdk.cdk.Token]
        predefinedMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.PredefinedMetricSpecificationProperty"]
        scaleInCooldown: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        scaleOutCooldown: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty")
    class TargetTrackingScalingPolicyConfigurationProperty(_TargetTrackingScalingPolicyConfigurationProperty):
        targetValue: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnScalingPolicyProps(jsii.compat.TypedDict, total=False):
    resourceId: str
    scalableDimension: str
    scalingTargetId: str
    serviceNamespace: str
    stepScalingPolicyConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.StepScalingPolicyConfigurationProperty"]
    targetTrackingScalingPolicyConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicyProps")
class CfnScalingPolicyProps(_CfnScalingPolicyProps):
    policyName: str
    policyType: str

class Cron(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.Cron"):
    def __init__(self) -> None:
        jsii.create(Cron, self, [])

    @jsii.member(jsii_name="dailyUtc")
    @classmethod
    def daily_utc(cls, hour: jsii.Number, minute: typing.Optional[jsii.Number]=None) -> str:
        return jsii.sinvoke(cls, "dailyUtc", [hour, minute])


class _EnableScalingProps(jsii.compat.TypedDict, total=False):
    minCapacity: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.EnableScalingProps")
class EnableScalingProps(_EnableScalingProps):
    maxCapacity: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BaseScalableAttributeProps")
class BaseScalableAttributeProps(EnableScalingProps, jsii.compat.TypedDict):
    dimension: str
    resourceId: str
    role: aws_cdk.aws_iam.IRole
    serviceNamespace: "ServiceNamespace"

@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.MetricAggregationType")
class MetricAggregationType(enum.Enum):
    Average = "Average"
    Minimum = "Minimum"
    Maximum = "Maximum"

@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.PredefinedMetric")
class PredefinedMetric(enum.Enum):
    DynamoDBReadCapacityUtilization = "DynamoDBReadCapacityUtilization"
    DynamoDBWriteCapacityUtilization = "DynamoDBWriteCapacityUtilization"
    ALBRequestCountPerTarget = "ALBRequestCountPerTarget"
    RDSReaderAverageCPUUtilization = "RDSReaderAverageCPUUtilization"
    RDSReaderAverageDatabaseConnections = "RDSReaderAverageDatabaseConnections"
    EC2SpotFleetRequestAverageCPUUtilization = "EC2SpotFleetRequestAverageCPUUtilization"
    EC2SpotFleetRequestAverageNetworkIn = "EC2SpotFleetRequestAverageNetworkIn"
    EC2SpotFleetRequestAverageNetworkOut = "EC2SpotFleetRequestAverageNetworkOut"
    SageMakerVariantInvocationsPerInstance = "SageMakerVariantInvocationsPerInstance"
    ECSServiceAverageCPUUtilization = "ECSServiceAverageCPUUtilization"
    ECSServiceAverageMemoryUtilization = "ECSServiceAverageMemoryUtilization"

class ScalableTarget(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.ScalableTarget"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, max_capacity: jsii.Number, min_capacity: jsii.Number, resource_id: str, scalable_dimension: str, service_namespace: "ServiceNamespace", role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        props: ScalableTargetProps = {"maxCapacity": max_capacity, "minCapacity": min_capacity, "resourceId": resource_id, "scalableDimension": scalable_dimension, "serviceNamespace": service_namespace}

        if role is not None:
            props["role"] = role

        jsii.create(ScalableTarget, self, [scope, id, props])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_sec: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        props: BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        action: ScalingSchedule = {"schedule": schedule}

        if end_time is not None:
            action["endTime"] = end_time

        if max_capacity is not None:
            action["maxCapacity"] = max_capacity

        if min_capacity is not None:
            action["minCapacity"] = min_capacity

        if start_time is not None:
            action["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, action])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.Metric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: BasicTargetTrackingScalingPolicyProps = {"targetValue": target_value}

        if custom_metric is not None:
            props["customMetric"] = custom_metric

        if predefined_metric is not None:
            props["predefinedMetric"] = predefined_metric

        if resource_label is not None:
            props["resourceLabel"] = resource_label

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "role")

    @property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        return jsii.get(self, "scalableTargetId")


class _ScalableTargetProps(jsii.compat.TypedDict, total=False):
    role: aws_cdk.aws_iam.IRole

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalableTargetProps")
class ScalableTargetProps(_ScalableTargetProps):
    maxCapacity: jsii.Number
    minCapacity: jsii.Number
    resourceId: str
    scalableDimension: str
    serviceNamespace: "ServiceNamespace"

class _ScalingInterval(jsii.compat.TypedDict, total=False):
    lower: jsii.Number
    upper: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalingInterval")
class ScalingInterval(_ScalingInterval):
    change: jsii.Number

class _ScalingSchedule(jsii.compat.TypedDict, total=False):
    endTime: datetime.datetime
    maxCapacity: jsii.Number
    minCapacity: jsii.Number
    startTime: datetime.datetime

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalingSchedule")
class ScalingSchedule(_ScalingSchedule):
    schedule: str

@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.ServiceNamespace")
class ServiceNamespace(enum.Enum):
    Ecs = "Ecs"
    ElasticMapReduce = "ElasticMapReduce"
    Ec2 = "Ec2"
    AppStream = "AppStream"
    DynamoDb = "DynamoDb"
    Rds = "Rds"
    SageMaker = "SageMaker"
    CustomResource = "CustomResource"

@jsii.implements(aws_cdk.aws_cloudwatch.IAlarmAction)
class StepScalingAction(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingAction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, scaling_target: "ScalableTarget", adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_sec: typing.Optional[jsii.Number]=None, metric_aggregation_type: typing.Optional["MetricAggregationType"]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, policy_name: typing.Optional[str]=None) -> None:
        props: StepScalingActionProps = {"scalingTarget": scaling_target}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if metric_aggregation_type is not None:
            props["metricAggregationType"] = metric_aggregation_type

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        if policy_name is not None:
            props["policyName"] = policy_name

        jsii.create(StepScalingAction, self, [scope, id, props])

    @jsii.member(jsii_name="addAdjustment")
    def add_adjustment(self, *, adjustment: jsii.Number, lower_bound: typing.Optional[jsii.Number]=None, upper_bound: typing.Optional[jsii.Number]=None) -> None:
        adjustment: AdjustmentTier = {"adjustment": adjustment}

        if lower_bound is not None:
            adjustment["lowerBound"] = lower_bound

        if upper_bound is not None:
            adjustment["upperBound"] = upper_bound

        return jsii.invoke(self, "addAdjustment", [adjustment])

    @property
    @jsii.member(jsii_name="alarmActionArn")
    def alarm_action_arn(self) -> str:
        return jsii.get(self, "alarmActionArn")

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        return jsii.get(self, "scalingPolicyArn")


class _StepScalingActionProps(jsii.compat.TypedDict, total=False):
    adjustmentType: "AdjustmentType"
    cooldownSec: jsii.Number
    metricAggregationType: "MetricAggregationType"
    minAdjustmentMagnitude: jsii.Number
    policyName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingActionProps")
class StepScalingActionProps(_StepScalingActionProps):
    scalingTarget: "ScalableTarget"

class StepScalingPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, scaling_target: "ScalableTarget", metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_sec: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        props: StepScalingPolicyProps = {"scalingTarget": scaling_target, "metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        jsii.create(StepScalingPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="lowerAction")
    def lower_action(self) -> typing.Optional["StepScalingAction"]:
        return jsii.get(self, "lowerAction")

    @property
    @jsii.member(jsii_name="lowerAlarm")
    def lower_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "lowerAlarm")

    @property
    @jsii.member(jsii_name="upperAction")
    def upper_action(self) -> typing.Optional["StepScalingAction"]:
        return jsii.get(self, "upperAction")

    @property
    @jsii.member(jsii_name="upperAlarm")
    def upper_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "upperAlarm")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingPolicyProps")
class StepScalingPolicyProps(BasicStepScalingPolicyProps, jsii.compat.TypedDict):
    scalingTarget: "ScalableTarget"

class TargetTrackingScalingPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.TargetTrackingScalingPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, scaling_target: "ScalableTarget", target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.Metric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        props: TargetTrackingScalingPolicyProps = {"scalingTarget": scaling_target, "targetValue": target_value}

        if custom_metric is not None:
            props["customMetric"] = custom_metric

        if predefined_metric is not None:
            props["predefinedMetric"] = predefined_metric

        if resource_label is not None:
            props["resourceLabel"] = resource_label

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        jsii.create(TargetTrackingScalingPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.TargetTrackingScalingPolicyProps")
class TargetTrackingScalingPolicyProps(BasicTargetTrackingScalingPolicyProps, jsii.compat.TypedDict):
    scalingTarget: "ScalableTarget"

__all__ = ["AdjustmentTier", "AdjustmentType", "BaseScalableAttribute", "BaseScalableAttributeProps", "BaseTargetTrackingProps", "BasicStepScalingPolicyProps", "BasicTargetTrackingScalingPolicyProps", "CfnScalableTarget", "CfnScalableTargetProps", "CfnScalingPolicy", "CfnScalingPolicyProps", "Cron", "EnableScalingProps", "MetricAggregationType", "PredefinedMetric", "ScalableTarget", "ScalableTargetProps", "ScalingInterval", "ScalingSchedule", "ServiceNamespace", "StepScalingAction", "StepScalingActionProps", "StepScalingPolicy", "StepScalingPolicyProps", "TargetTrackingScalingPolicy", "TargetTrackingScalingPolicyProps", "__jsii_assembly__"]

publication.publish()
