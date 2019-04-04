import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling_api
import aws_cdk.aws_autoscaling_common
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_sns
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscaling", "0.28.0", __name__, "aws-autoscaling@0.28.0.jsii.tgz")
class _AdjustmentTier(jsii.compat.TypedDict, total=False):
    lowerBound: jsii.Number
    upperBound: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.AdjustmentTier")
class AdjustmentTier(_AdjustmentTier):
    adjustment: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.AdjustmentType")
class AdjustmentType(enum.Enum):
    ChangeInCapacity = "ChangeInCapacity"
    PercentChangeInCapacity = "PercentChangeInCapacity"
    ExactCapacity = "ExactCapacity"

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BaseTargetTrackingProps")
class BaseTargetTrackingProps(jsii.compat.TypedDict, total=False):
    cooldownSeconds: jsii.Number
    disableScaleIn: bool
    estimatedInstanceWarmupSeconds: jsii.Number

class _BasicLifecycleHookProps(jsii.compat.TypedDict, total=False):
    defaultResult: "DefaultResult"
    heartbeatTimeoutSec: jsii.Number
    lifecycleHookName: str
    notificationMetadata: str
    role: aws_cdk.aws_iam.IRole

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicLifecycleHookProps")
class BasicLifecycleHookProps(_BasicLifecycleHookProps):
    lifecycleTransition: "LifecycleTransition"
    notificationTarget: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget

class _BasicScheduledActionProps(jsii.compat.TypedDict, total=False):
    desiredCapacity: jsii.Number
    endTime: datetime.datetime
    maxCapacity: jsii.Number
    minCapacity: jsii.Number
    startTime: datetime.datetime

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicScheduledActionProps")
class BasicScheduledActionProps(_BasicScheduledActionProps):
    schedule: str

class _BasicStepScalingPolicyProps(jsii.compat.TypedDict, total=False):
    adjustmentType: "AdjustmentType"
    cooldownSeconds: jsii.Number
    estimatedInstanceWarmupSeconds: jsii.Number
    minAdjustmentMagnitude: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicStepScalingPolicyProps")
class BasicStepScalingPolicyProps(_BasicStepScalingPolicyProps):
    metric: aws_cdk.aws_cloudwatch.Metric
    scalingSteps: typing.List["ScalingInterval"]

class _BasicTargetTrackingScalingPolicyProps(BaseTargetTrackingProps, jsii.compat.TypedDict, total=False):
    customMetric: aws_cdk.aws_cloudwatch.Metric
    predefinedMetric: "PredefinedMetric"
    resourceLabel: str

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicTargetTrackingScalingPolicyProps")
class BasicTargetTrackingScalingPolicyProps(_BasicTargetTrackingScalingPolicyProps):
    targetValue: jsii.Number

class CfnAutoScalingGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, max_size: str, min_size: str, auto_scaling_group_name: typing.Optional[str]=None, availability_zones: typing.Optional[typing.List[str]]=None, cooldown: typing.Optional[str]=None, desired_capacity: typing.Optional[str]=None, health_check_grace_period: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, health_check_type: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, launch_configuration_name: typing.Optional[str]=None, launch_template: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LaunchTemplateSpecificationProperty"]]=None, lifecycle_hook_specification_list: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "LifecycleHookSpecificationProperty"]]]]=None, load_balancer_names: typing.Optional[typing.List[str]]=None, metrics_collection: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "MetricsCollectionProperty"]]]]=None, mixed_instances_policy: typing.Optional[typing.Union[aws_cdk.cdk.Token, "MixedInstancesPolicyProperty"]]=None, notification_configurations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "NotificationConfigurationProperty"]]]]=None, placement_group: typing.Optional[str]=None, service_linked_role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagPropertyProperty"]]=None, target_group_arns: typing.Optional[typing.List[str]]=None, termination_policies: typing.Optional[typing.List[str]]=None, vpc_zone_identifier: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnAutoScalingGroupProps = {"maxSize": max_size, "minSize": min_size}

        if auto_scaling_group_name is not None:
            props["autoScalingGroupName"] = auto_scaling_group_name

        if availability_zones is not None:
            props["availabilityZones"] = availability_zones

        if cooldown is not None:
            props["cooldown"] = cooldown

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if health_check_grace_period is not None:
            props["healthCheckGracePeriod"] = health_check_grace_period

        if health_check_type is not None:
            props["healthCheckType"] = health_check_type

        if instance_id is not None:
            props["instanceId"] = instance_id

        if launch_configuration_name is not None:
            props["launchConfigurationName"] = launch_configuration_name

        if launch_template is not None:
            props["launchTemplate"] = launch_template

        if lifecycle_hook_specification_list is not None:
            props["lifecycleHookSpecificationList"] = lifecycle_hook_specification_list

        if load_balancer_names is not None:
            props["loadBalancerNames"] = load_balancer_names

        if metrics_collection is not None:
            props["metricsCollection"] = metrics_collection

        if mixed_instances_policy is not None:
            props["mixedInstancesPolicy"] = mixed_instances_policy

        if notification_configurations is not None:
            props["notificationConfigurations"] = notification_configurations

        if placement_group is not None:
            props["placementGroup"] = placement_group

        if service_linked_role_arn is not None:
            props["serviceLinkedRoleArn"] = service_linked_role_arn

        if tags is not None:
            props["tags"] = tags

        if target_group_arns is not None:
            props["targetGroupArns"] = target_group_arns

        if termination_policies is not None:
            props["terminationPolicies"] = termination_policies

        if vpc_zone_identifier is not None:
            props["vpcZoneIdentifier"] = vpc_zone_identifier

        jsii.create(CfnAutoScalingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        return jsii.get(self, "autoScalingGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAutoScalingGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.InstancesDistributionProperty")
    class InstancesDistributionProperty(jsii.compat.TypedDict, total=False):
        onDemandAllocationStrategy: str
        onDemandBaseCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        onDemandPercentageAboveBaseCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        spotAllocationStrategy: str
        spotInstancePools: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        spotMaxPrice: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateOverridesProperty")
    class LaunchTemplateOverridesProperty(jsii.compat.TypedDict, total=False):
        instanceType: str

    class _LaunchTemplateProperty(jsii.compat.TypedDict, total=False):
        overrides: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LaunchTemplateOverridesProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateProperty")
    class LaunchTemplateProperty(_LaunchTemplateProperty):
        launchTemplateSpecification: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]

    class _LaunchTemplateSpecificationProperty(jsii.compat.TypedDict, total=False):
        launchTemplateId: str
        launchTemplateName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateSpecificationProperty")
    class LaunchTemplateSpecificationProperty(_LaunchTemplateSpecificationProperty):
        version: str

    class _LifecycleHookSpecificationProperty(jsii.compat.TypedDict, total=False):
        defaultResult: str
        heartbeatTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        notificationMetadata: str
        notificationTargetArn: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LifecycleHookSpecificationProperty")
    class LifecycleHookSpecificationProperty(_LifecycleHookSpecificationProperty):
        lifecycleHookName: str
        lifecycleTransition: str

    class _MetricsCollectionProperty(jsii.compat.TypedDict, total=False):
        metrics: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.MetricsCollectionProperty")
    class MetricsCollectionProperty(_MetricsCollectionProperty):
        granularity: str

    class _MixedInstancesPolicyProperty(jsii.compat.TypedDict, total=False):
        instancesDistribution: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.InstancesDistributionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.MixedInstancesPolicyProperty")
    class MixedInstancesPolicyProperty(_MixedInstancesPolicyProperty):
        launchTemplate: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LaunchTemplateProperty"]

    class _NotificationConfigurationProperty(jsii.compat.TypedDict, total=False):
        notificationTypes: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.NotificationConfigurationProperty")
    class NotificationConfigurationProperty(_NotificationConfigurationProperty):
        topicArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.TagPropertyProperty")
    class TagPropertyProperty(jsii.compat.TypedDict):
        key: str
        propagateAtLaunch: typing.Union[bool, aws_cdk.cdk.Token]
        value: str


class _CfnAutoScalingGroupProps(jsii.compat.TypedDict, total=False):
    autoScalingGroupName: str
    availabilityZones: typing.List[str]
    cooldown: str
    desiredCapacity: str
    healthCheckGracePeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    healthCheckType: str
    instanceId: str
    launchConfigurationName: str
    launchTemplate: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]
    lifecycleHookSpecificationList: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LifecycleHookSpecificationProperty"]]]
    loadBalancerNames: typing.List[str]
    metricsCollection: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.MetricsCollectionProperty"]]]
    mixedInstancesPolicy: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.MixedInstancesPolicyProperty"]
    notificationConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.NotificationConfigurationProperty"]]]
    placementGroup: str
    serviceLinkedRoleArn: str
    tags: typing.List["CfnAutoScalingGroup.TagPropertyProperty"]
    targetGroupArns: typing.List[str]
    terminationPolicies: typing.List[str]
    vpcZoneIdentifier: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroupProps")
class CfnAutoScalingGroupProps(_CfnAutoScalingGroupProps):
    maxSize: str
    minSize: str

class CfnLaunchConfiguration(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, image_id: str, instance_type: str, associate_public_ip_address: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, block_device_mappings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "BlockDeviceMappingProperty"]]]]=None, classic_link_vpc_id: typing.Optional[str]=None, classic_link_vpc_security_groups: typing.Optional[typing.List[str]]=None, ebs_optimized: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, iam_instance_profile: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, instance_monitoring: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, kernel_id: typing.Optional[str]=None, key_name: typing.Optional[str]=None, launch_configuration_name: typing.Optional[str]=None, placement_tenancy: typing.Optional[str]=None, ram_disk_id: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, spot_price: typing.Optional[str]=None, user_data: typing.Optional[str]=None) -> None:
        props: CfnLaunchConfigurationProps = {"imageId": image_id, "instanceType": instance_type}

        if associate_public_ip_address is not None:
            props["associatePublicIpAddress"] = associate_public_ip_address

        if block_device_mappings is not None:
            props["blockDeviceMappings"] = block_device_mappings

        if classic_link_vpc_id is not None:
            props["classicLinkVpcId"] = classic_link_vpc_id

        if classic_link_vpc_security_groups is not None:
            props["classicLinkVpcSecurityGroups"] = classic_link_vpc_security_groups

        if ebs_optimized is not None:
            props["ebsOptimized"] = ebs_optimized

        if iam_instance_profile is not None:
            props["iamInstanceProfile"] = iam_instance_profile

        if instance_id is not None:
            props["instanceId"] = instance_id

        if instance_monitoring is not None:
            props["instanceMonitoring"] = instance_monitoring

        if kernel_id is not None:
            props["kernelId"] = kernel_id

        if key_name is not None:
            props["keyName"] = key_name

        if launch_configuration_name is not None:
            props["launchConfigurationName"] = launch_configuration_name

        if placement_tenancy is not None:
            props["placementTenancy"] = placement_tenancy

        if ram_disk_id is not None:
            props["ramDiskId"] = ram_disk_id

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if spot_price is not None:
            props["spotPrice"] = spot_price

        if user_data is not None:
            props["userData"] = user_data

        jsii.create(CfnLaunchConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="launchConfigurationName")
    def launch_configuration_name(self) -> str:
        return jsii.get(self, "launchConfigurationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchConfigurationProps":
        return jsii.get(self, "propertyOverrides")

    class _BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        ebs: typing.Union[aws_cdk.cdk.Token, "CfnLaunchConfiguration.BlockDeviceProperty"]
        noDevice: typing.Union[bool, aws_cdk.cdk.Token]
        virtualName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.BlockDeviceMappingProperty")
    class BlockDeviceMappingProperty(_BlockDeviceMappingProperty):
        deviceName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.BlockDeviceProperty")
    class BlockDeviceProperty(jsii.compat.TypedDict, total=False):
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        snapshotId: str
        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str


class _CfnLaunchConfigurationProps(jsii.compat.TypedDict, total=False):
    associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
    blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchConfiguration.BlockDeviceMappingProperty"]]]
    classicLinkVpcId: str
    classicLinkVpcSecurityGroups: typing.List[str]
    ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
    iamInstanceProfile: str
    instanceId: str
    instanceMonitoring: typing.Union[bool, aws_cdk.cdk.Token]
    kernelId: str
    keyName: str
    launchConfigurationName: str
    placementTenancy: str
    ramDiskId: str
    securityGroups: typing.List[str]
    spotPrice: str
    userData: str

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfigurationProps")
class CfnLaunchConfigurationProps(_CfnLaunchConfigurationProps):
    imageId: str
    instanceType: str

class CfnLifecycleHook(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnLifecycleHook"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group_name: str, lifecycle_transition: str, default_result: typing.Optional[str]=None, heartbeat_timeout: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, notification_target_arn: typing.Optional[str]=None, role_arn: typing.Optional[str]=None) -> None:
        props: CfnLifecycleHookProps = {"autoScalingGroupName": auto_scaling_group_name, "lifecycleTransition": lifecycle_transition}

        if default_result is not None:
            props["defaultResult"] = default_result

        if heartbeat_timeout is not None:
            props["heartbeatTimeout"] = heartbeat_timeout

        if lifecycle_hook_name is not None:
            props["lifecycleHookName"] = lifecycle_hook_name

        if notification_metadata is not None:
            props["notificationMetadata"] = notification_metadata

        if notification_target_arn is not None:
            props["notificationTargetArn"] = notification_target_arn

        if role_arn is not None:
            props["roleArn"] = role_arn

        jsii.create(CfnLifecycleHook, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="lifecycleHookName")
    def lifecycle_hook_name(self) -> str:
        return jsii.get(self, "lifecycleHookName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLifecycleHookProps":
        return jsii.get(self, "propertyOverrides")


class _CfnLifecycleHookProps(jsii.compat.TypedDict, total=False):
    defaultResult: str
    heartbeatTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    lifecycleHookName: str
    notificationMetadata: str
    notificationTargetArn: str
    roleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLifecycleHookProps")
class CfnLifecycleHookProps(_CfnLifecycleHookProps):
    autoScalingGroupName: str
    lifecycleTransition: str

class CfnScalingPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group_name: str, adjustment_type: typing.Optional[str]=None, cooldown: typing.Optional[str]=None, estimated_instance_warmup: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, metric_aggregation_type: typing.Optional[str]=None, min_adjustment_magnitude: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, policy_type: typing.Optional[str]=None, scaling_adjustment: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, step_adjustments: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "StepAdjustmentProperty"]]]]=None, target_tracking_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TargetTrackingConfigurationProperty"]]=None) -> None:
        props: CfnScalingPolicyProps = {"autoScalingGroupName": auto_scaling_group_name}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown is not None:
            props["cooldown"] = cooldown

        if estimated_instance_warmup is not None:
            props["estimatedInstanceWarmup"] = estimated_instance_warmup

        if metric_aggregation_type is not None:
            props["metricAggregationType"] = metric_aggregation_type

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        if policy_type is not None:
            props["policyType"] = policy_type

        if scaling_adjustment is not None:
            props["scalingAdjustment"] = scaling_adjustment

        if step_adjustments is not None:
            props["stepAdjustments"] = step_adjustments

        if target_tracking_configuration is not None:
            props["targetTrackingConfiguration"] = target_tracking_configuration

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

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.CustomizedMetricSpecificationProperty")
    class CustomizedMetricSpecificationProperty(_CustomizedMetricSpecificationProperty):
        metricName: str
        namespace: str
        statistic: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.MetricDimensionProperty")
    class MetricDimensionProperty(jsii.compat.TypedDict):
        name: str
        value: str

    class _PredefinedMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceLabel: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty")
    class PredefinedMetricSpecificationProperty(_PredefinedMetricSpecificationProperty):
        predefinedMetricType: str

    class _StepAdjustmentProperty(jsii.compat.TypedDict, total=False):
        metricIntervalLowerBound: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        metricIntervalUpperBound: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.StepAdjustmentProperty")
    class StepAdjustmentProperty(_StepAdjustmentProperty):
        scalingAdjustment: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _TargetTrackingConfigurationProperty(jsii.compat.TypedDict, total=False):
        customizedMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.CustomizedMetricSpecificationProperty"]
        disableScaleIn: typing.Union[bool, aws_cdk.cdk.Token]
        predefinedMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.PredefinedMetricSpecificationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.TargetTrackingConfigurationProperty")
    class TargetTrackingConfigurationProperty(_TargetTrackingConfigurationProperty):
        targetValue: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnScalingPolicyProps(jsii.compat.TypedDict, total=False):
    adjustmentType: str
    cooldown: str
    estimatedInstanceWarmup: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    metricAggregationType: str
    minAdjustmentMagnitude: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    policyType: str
    scalingAdjustment: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    stepAdjustments: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.StepAdjustmentProperty"]]]
    targetTrackingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.TargetTrackingConfigurationProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicyProps")
class CfnScalingPolicyProps(_CfnScalingPolicyProps):
    autoScalingGroupName: str

class CfnScheduledAction(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnScheduledAction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group_name: str, desired_capacity: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, end_time: typing.Optional[str]=None, max_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, min_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, recurrence: typing.Optional[str]=None, start_time: typing.Optional[str]=None) -> None:
        props: CfnScheduledActionProps = {"autoScalingGroupName": auto_scaling_group_name}

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if end_time is not None:
            props["endTime"] = end_time

        if max_size is not None:
            props["maxSize"] = max_size

        if min_size is not None:
            props["minSize"] = min_size

        if recurrence is not None:
            props["recurrence"] = recurrence

        if start_time is not None:
            props["startTime"] = start_time

        jsii.create(CfnScheduledAction, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnScheduledActionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="scheduledActionName")
    def scheduled_action_name(self) -> str:
        return jsii.get(self, "scheduledActionName")


class _CfnScheduledActionProps(jsii.compat.TypedDict, total=False):
    desiredCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    endTime: str
    maxSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    minSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    recurrence: str
    startTime: str

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScheduledActionProps")
class CfnScheduledActionProps(_CfnScheduledActionProps):
    autoScalingGroupName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CommonAutoScalingGroupProps")
class CommonAutoScalingGroupProps(jsii.compat.TypedDict, total=False):
    allowAllOutbound: bool
    associatePublicIpAddress: bool
    cooldownSeconds: jsii.Number
    desiredCapacity: jsii.Number
    ignoreUnmodifiedSizeProperties: bool
    keyName: str
    maxCapacity: jsii.Number
    minCapacity: jsii.Number
    notificationsTopic: aws_cdk.aws_sns.ITopic
    replacingUpdateMinSuccessfulInstancesPercent: jsii.Number
    resourceSignalCount: jsii.Number
    resourceSignalTimeoutSec: jsii.Number
    rollingUpdateConfiguration: "RollingUpdateConfiguration"
    updateType: "UpdateType"
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection

class _AutoScalingGroupProps(CommonAutoScalingGroupProps, jsii.compat.TypedDict, total=False):
    role: aws_cdk.aws_iam.IRole

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.AutoScalingGroupProps")
class AutoScalingGroupProps(_AutoScalingGroupProps):
    instanceType: aws_cdk.aws_ec2.InstanceType
    machineImage: aws_cdk.aws_ec2.IMachineImageSource
    vpc: aws_cdk.aws_ec2.IVpcNetwork

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CpuUtilizationScalingProps")
class CpuUtilizationScalingProps(BaseTargetTrackingProps, jsii.compat.TypedDict):
    targetUtilizationPercent: jsii.Number

class Cron(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.Cron"):
    def __init__(self) -> None:
        jsii.create(Cron, self, [])

    @jsii.member(jsii_name="dailyUtc")
    @classmethod
    def daily_utc(cls, hour: jsii.Number, minute: typing.Optional[jsii.Number]=None) -> str:
        return jsii.sinvoke(cls, "dailyUtc", [hour, minute])


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.DefaultResult")
class DefaultResult(enum.Enum):
    Continue = "Continue"
    Abandon = "Abandon"

@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling.IAutoScalingGroup")
class IAutoScalingGroup(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IAutoScalingGroupProxy

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        ...

    @jsii.member(jsii_name="onLifecycleTransition")
    def on_lifecycle_transition(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout_sec: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        ...

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        ...

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        ...

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        ...

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        ...

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        ...

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, target_value: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        ...


class _IAutoScalingGroupProxy():
    __jsii_type__ = "@aws-cdk/aws-autoscaling.IAutoScalingGroup"
    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        return jsii.get(self, "autoScalingGroupName")

    @jsii.member(jsii_name="onLifecycleTransition")
    def on_lifecycle_transition(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout_sec: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        props: BasicLifecycleHookProps = {"lifecycleTransition": lifecycle_transition, "notificationTarget": notification_target}

        if default_result is not None:
            props["defaultResult"] = default_result

        if heartbeat_timeout_sec is not None:
            props["heartbeatTimeoutSec"] = heartbeat_timeout_sec

        if lifecycle_hook_name is not None:
            props["lifecycleHookName"] = lifecycle_hook_name

        if notification_metadata is not None:
            props["notificationMetadata"] = notification_metadata

        if role is not None:
            props["role"] = role

        return jsii.invoke(self, "onLifecycleTransition", [id, props])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: CpuUtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: NetworkUtilizationScalingProps = {"targetBytesPerSecond": target_bytes_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnIncomingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        props: BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: NetworkUtilizationScalingProps = {"targetBytesPerSecond": target_bytes_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnOutgoingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        props: BasicScheduledActionProps = {"schedule": schedule}

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, target_value: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: MetricTargetTrackingProps = {"metric": metric, "targetValue": target_value}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])


@jsii.implements(IAutoScalingGroup, aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget)
class AutoScalingGroup(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.AutoScalingGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_type: aws_cdk.aws_ec2.InstanceType, machine_image: aws_cdk.aws_ec2.IMachineImageSource, vpc: aws_cdk.aws_ec2.IVpcNetwork, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, desired_capacity: typing.Optional[jsii.Number]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout_sec: typing.Optional[jsii.Number]=None, rolling_update_configuration: typing.Optional["RollingUpdateConfiguration"]=None, update_type: typing.Optional["UpdateType"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        props: AutoScalingGroupProps = {"instanceType": instance_type, "machineImage": machine_image, "vpc": vpc}

        if role is not None:
            props["role"] = role

        if allow_all_outbound is not None:
            props["allowAllOutbound"] = allow_all_outbound

        if associate_public_ip_address is not None:
            props["associatePublicIpAddress"] = associate_public_ip_address

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if ignore_unmodified_size_properties is not None:
            props["ignoreUnmodifiedSizeProperties"] = ignore_unmodified_size_properties

        if key_name is not None:
            props["keyName"] = key_name

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if notifications_topic is not None:
            props["notificationsTopic"] = notifications_topic

        if replacing_update_min_successful_instances_percent is not None:
            props["replacingUpdateMinSuccessfulInstancesPercent"] = replacing_update_min_successful_instances_percent

        if resource_signal_count is not None:
            props["resourceSignalCount"] = resource_signal_count

        if resource_signal_timeout_sec is not None:
            props["resourceSignalTimeoutSec"] = resource_signal_timeout_sec

        if rolling_update_configuration is not None:
            props["rollingUpdateConfiguration"] = rolling_update_configuration

        if update_type is not None:
            props["updateType"] = update_type

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(AutoScalingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(self, security_group: aws_cdk.aws_ec2.ISecurityGroup) -> None:
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *script_lines: str) -> None:
        return jsii.invoke(self, "addUserData", [script_lines])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer) -> None:
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @jsii.member(jsii_name="onLifecycleTransition")
    def on_lifecycle_transition(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout_sec: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        props: BasicLifecycleHookProps = {"lifecycleTransition": lifecycle_transition, "notificationTarget": notification_target}

        if default_result is not None:
            props["defaultResult"] = default_result

        if heartbeat_timeout_sec is not None:
            props["heartbeatTimeoutSec"] = heartbeat_timeout_sec

        if lifecycle_hook_name is not None:
            props["lifecycleHookName"] = lifecycle_hook_name

        if notification_metadata is not None:
            props["notificationMetadata"] = notification_metadata

        if role is not None:
            props["role"] = role

        return jsii.invoke(self, "onLifecycleTransition", [id, props])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: CpuUtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: NetworkUtilizationScalingProps = {"targetBytesPerSecond": target_bytes_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnIncomingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        props: BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: NetworkUtilizationScalingProps = {"targetBytesPerSecond": target_bytes_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnOutgoingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnRequestCount")
    def scale_on_request_count(self, id: str, *, target_requests_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: RequestCountScalingProps = {"targetRequestsPerSecond": target_requests_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnRequestCount", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        props: BasicScheduledActionProps = {"schedule": schedule}

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, target_value: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        props: MetricTargetTrackingProps = {"metric": metric, "targetValue": target_value}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        return jsii.get(self, "autoScalingGroupName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> aws_cdk.aws_ec2.OperatingSystemType:
        return jsii.get(self, "osType")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "role")


@jsii.implements(aws_cdk.aws_autoscaling_api.ILifecycleHook)
class LifecycleHook(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.LifecycleHook"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", lifecycle_transition: "LifecycleTransition", notification_target: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout_sec: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        props: LifecycleHookProps = {"autoScalingGroup": auto_scaling_group, "lifecycleTransition": lifecycle_transition, "notificationTarget": notification_target}

        if default_result is not None:
            props["defaultResult"] = default_result

        if heartbeat_timeout_sec is not None:
            props["heartbeatTimeoutSec"] = heartbeat_timeout_sec

        if lifecycle_hook_name is not None:
            props["lifecycleHookName"] = lifecycle_hook_name

        if notification_metadata is not None:
            props["notificationMetadata"] = notification_metadata

        if role is not None:
            props["role"] = role

        jsii.create(LifecycleHook, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="lifecycleHookName")
    def lifecycle_hook_name(self) -> str:
        return jsii.get(self, "lifecycleHookName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.LifecycleHookProps")
class LifecycleHookProps(BasicLifecycleHookProps, jsii.compat.TypedDict):
    autoScalingGroup: "IAutoScalingGroup"

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.LifecycleTransition")
class LifecycleTransition(enum.Enum):
    InstanceLaunching = "InstanceLaunching"
    InstanceTerminating = "InstanceTerminating"

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.MetricAggregationType")
class MetricAggregationType(enum.Enum):
    Average = "Average"
    Minimum = "Minimum"
    Maximum = "Maximum"

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.MetricTargetTrackingProps")
class MetricTargetTrackingProps(BaseTargetTrackingProps, jsii.compat.TypedDict):
    metric: aws_cdk.aws_cloudwatch.Metric
    targetValue: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.NetworkUtilizationScalingProps")
class NetworkUtilizationScalingProps(BaseTargetTrackingProps, jsii.compat.TypedDict):
    targetBytesPerSecond: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.PredefinedMetric")
class PredefinedMetric(enum.Enum):
    ASGAverageCPUUtilization = "ASGAverageCPUUtilization"
    ASGAverageNetworkIn = "ASGAverageNetworkIn"
    ASGAverageNetworkOut = "ASGAverageNetworkOut"
    ALBRequestCountPerTarget = "ALBRequestCountPerTarget"

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.RequestCountScalingProps")
class RequestCountScalingProps(BaseTargetTrackingProps, jsii.compat.TypedDict):
    targetRequestsPerSecond: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.RollingUpdateConfiguration")
class RollingUpdateConfiguration(jsii.compat.TypedDict, total=False):
    maxBatchSize: jsii.Number
    minInstancesInService: jsii.Number
    minSuccessfulInstancesPercent: jsii.Number
    pauseTimeSec: jsii.Number
    suspendProcesses: typing.List["ScalingProcess"]
    waitOnResourceSignals: bool

class _ScalingInterval(jsii.compat.TypedDict, total=False):
    lower: jsii.Number
    upper: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.ScalingInterval")
class ScalingInterval(_ScalingInterval):
    change: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.ScalingProcess")
class ScalingProcess(enum.Enum):
    Launch = "Launch"
    Terminate = "Terminate"
    HealthCheck = "HealthCheck"
    ReplaceUnhealthy = "ReplaceUnhealthy"
    AZRebalance = "AZRebalance"
    AlarmNotification = "AlarmNotification"
    ScheduledActions = "ScheduledActions"
    AddToLoadBalancer = "AddToLoadBalancer"

class ScheduledAction(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.ScheduledAction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", schedule: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        props: ScheduledActionProps = {"autoScalingGroup": auto_scaling_group, "schedule": schedule}

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        jsii.create(ScheduledAction, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.ScheduledActionProps")
class ScheduledActionProps(BasicScheduledActionProps, jsii.compat.TypedDict):
    autoScalingGroup: "IAutoScalingGroup"

@jsii.implements(aws_cdk.aws_cloudwatch.IAlarmAction)
class StepScalingAction(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.StepScalingAction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, metric_aggregation_type: typing.Optional["MetricAggregationType"]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        props: StepScalingActionProps = {"autoScalingGroup": auto_scaling_group}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        if metric_aggregation_type is not None:
            props["metricAggregationType"] = metric_aggregation_type

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

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
    cooldownSeconds: jsii.Number
    estimatedInstanceWarmupSeconds: jsii.Number
    metricAggregationType: "MetricAggregationType"
    minAdjustmentMagnitude: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.StepScalingActionProps")
class StepScalingActionProps(_StepScalingActionProps):
    autoScalingGroup: "IAutoScalingGroup"

class StepScalingPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.StepScalingPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        props: StepScalingPolicyProps = {"autoScalingGroup": auto_scaling_group, "metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

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


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.StepScalingPolicyProps")
class StepScalingPolicyProps(BasicStepScalingPolicyProps, jsii.compat.TypedDict):
    autoScalingGroup: "IAutoScalingGroup"

class TargetTrackingScalingPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.TargetTrackingScalingPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.Metric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> None:
        props: TargetTrackingScalingPolicyProps = {"autoScalingGroup": auto_scaling_group, "targetValue": target_value}

        if custom_metric is not None:
            props["customMetric"] = custom_metric

        if predefined_metric is not None:
            props["predefinedMetric"] = predefined_metric

        if resource_label is not None:
            props["resourceLabel"] = resource_label

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        jsii.create(TargetTrackingScalingPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.TargetTrackingScalingPolicyProps")
class TargetTrackingScalingPolicyProps(BasicTargetTrackingScalingPolicyProps, jsii.compat.TypedDict):
    autoScalingGroup: "IAutoScalingGroup"

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.UpdateType")
class UpdateType(enum.Enum):
    None_ = "None"
    ReplacingUpdate = "ReplacingUpdate"
    RollingUpdate = "RollingUpdate"

__all__ = ["AdjustmentTier", "AdjustmentType", "AutoScalingGroup", "AutoScalingGroupProps", "BaseTargetTrackingProps", "BasicLifecycleHookProps", "BasicScheduledActionProps", "BasicStepScalingPolicyProps", "BasicTargetTrackingScalingPolicyProps", "CfnAutoScalingGroup", "CfnAutoScalingGroupProps", "CfnLaunchConfiguration", "CfnLaunchConfigurationProps", "CfnLifecycleHook", "CfnLifecycleHookProps", "CfnScalingPolicy", "CfnScalingPolicyProps", "CfnScheduledAction", "CfnScheduledActionProps", "CommonAutoScalingGroupProps", "CpuUtilizationScalingProps", "Cron", "DefaultResult", "IAutoScalingGroup", "LifecycleHook", "LifecycleHookProps", "LifecycleTransition", "MetricAggregationType", "MetricTargetTrackingProps", "NetworkUtilizationScalingProps", "PredefinedMetric", "RequestCountScalingProps", "RollingUpdateConfiguration", "ScalingInterval", "ScalingProcess", "ScheduledAction", "ScheduledActionProps", "StepScalingAction", "StepScalingActionProps", "StepScalingPolicy", "StepScalingPolicyProps", "TargetTrackingScalingPolicy", "TargetTrackingScalingPolicyProps", "UpdateType", "__jsii_assembly__"]

publication.publish()
