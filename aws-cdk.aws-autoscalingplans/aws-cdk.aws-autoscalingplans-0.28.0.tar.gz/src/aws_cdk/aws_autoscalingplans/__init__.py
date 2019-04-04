import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscalingplans", "0.28.0", __name__, "aws-autoscalingplans@0.28.0.jsii.tgz")
class CfnScalingPlan(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_source: typing.Union["ApplicationSourceProperty", aws_cdk.cdk.Token], scaling_instructions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ScalingInstructionProperty"]]]) -> None:
        props: CfnScalingPlanProps = {"applicationSource": application_source, "scalingInstructions": scaling_instructions}

        jsii.create(CfnScalingPlan, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnScalingPlanProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="scalingPlanArn")
    def scaling_plan_arn(self) -> str:
        return jsii.get(self, "scalingPlanArn")

    @property
    @jsii.member(jsii_name="scalingPlanName")
    def scaling_plan_name(self) -> str:
        return jsii.get(self, "scalingPlanName")

    @property
    @jsii.member(jsii_name="scalingPlanVersion")
    def scaling_plan_version(self) -> str:
        return jsii.get(self, "scalingPlanVersion")

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.ApplicationSourceProperty")
    class ApplicationSourceProperty(jsii.compat.TypedDict, total=False):
        cloudFormationStackArn: str
        tagFilters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.TagFilterProperty"]]]

    class _CustomizedLoadMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.MetricDimensionProperty"]]]
        unit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.CustomizedLoadMetricSpecificationProperty")
    class CustomizedLoadMetricSpecificationProperty(_CustomizedLoadMetricSpecificationProperty):
        metricName: str
        namespace: str
        statistic: str

    class _CustomizedScalingMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.MetricDimensionProperty"]]]
        unit: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.CustomizedScalingMetricSpecificationProperty")
    class CustomizedScalingMetricSpecificationProperty(_CustomizedScalingMetricSpecificationProperty):
        metricName: str
        namespace: str
        statistic: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.MetricDimensionProperty")
    class MetricDimensionProperty(jsii.compat.TypedDict):
        name: str
        value: str

    class _PredefinedLoadMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceLabel: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.PredefinedLoadMetricSpecificationProperty")
    class PredefinedLoadMetricSpecificationProperty(_PredefinedLoadMetricSpecificationProperty):
        predefinedLoadMetricType: str

    class _PredefinedScalingMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceLabel: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.PredefinedScalingMetricSpecificationProperty")
    class PredefinedScalingMetricSpecificationProperty(_PredefinedScalingMetricSpecificationProperty):
        predefinedScalingMetricType: str

    class _ScalingInstructionProperty(jsii.compat.TypedDict, total=False):
        customizedLoadMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.CustomizedLoadMetricSpecificationProperty"]
        disableDynamicScaling: typing.Union[bool, aws_cdk.cdk.Token]
        predefinedLoadMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.PredefinedLoadMetricSpecificationProperty"]
        predictiveScalingMaxCapacityBehavior: str
        predictiveScalingMaxCapacityBuffer: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        predictiveScalingMode: str
        scalingPolicyUpdateBehavior: str
        scheduledActionBufferTime: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.ScalingInstructionProperty")
    class ScalingInstructionProperty(_ScalingInstructionProperty):
        maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        resourceId: str
        scalableDimension: str
        serviceNamespace: str
        targetTrackingConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.TargetTrackingConfigurationProperty"]]]

    class _TagFilterProperty(jsii.compat.TypedDict, total=False):
        values: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.TagFilterProperty")
    class TagFilterProperty(_TagFilterProperty):
        key: str

    class _TargetTrackingConfigurationProperty(jsii.compat.TypedDict, total=False):
        customizedScalingMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.CustomizedScalingMetricSpecificationProperty"]
        disableScaleIn: typing.Union[bool, aws_cdk.cdk.Token]
        estimatedInstanceWarmup: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        predefinedScalingMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.PredefinedScalingMetricSpecificationProperty"]
        scaleInCooldown: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        scaleOutCooldown: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlan.TargetTrackingConfigurationProperty")
    class TargetTrackingConfigurationProperty(_TargetTrackingConfigurationProperty):
        targetValue: typing.Union[jsii.Number, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscalingplans.CfnScalingPlanProps")
class CfnScalingPlanProps(jsii.compat.TypedDict):
    applicationSource: typing.Union["CfnScalingPlan.ApplicationSourceProperty", aws_cdk.cdk.Token]
    scalingInstructions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPlan.ScalingInstructionProperty"]]]

__all__ = ["CfnScalingPlan", "CfnScalingPlanProps", "__jsii_assembly__"]

publication.publish()
