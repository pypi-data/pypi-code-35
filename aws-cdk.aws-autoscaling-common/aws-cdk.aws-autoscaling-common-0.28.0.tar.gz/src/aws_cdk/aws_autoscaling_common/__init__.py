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
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscaling-common", "0.28.0", __name__, "aws-autoscaling-common@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.Alarms")
class Alarms(jsii.compat.TypedDict, total=False):
    lowerAlarmIntervalIndex: jsii.Number
    upperAlarmIntervalIndex: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.ArbitraryIntervals")
class ArbitraryIntervals(jsii.compat.TypedDict):
    absolute: bool
    intervals: typing.List["ScalingInterval"]

class _CompleteScalingInterval(jsii.compat.TypedDict, total=False):
    change: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.CompleteScalingInterval")
class CompleteScalingInterval(_CompleteScalingInterval):
    lower: jsii.Number
    upper: jsii.Number

@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling-common.IRandomGenerator")
class IRandomGenerator(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IRandomGeneratorProxy

    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> bool:
        ...

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        ...


class _IRandomGeneratorProxy():
    __jsii_type__ = "@aws-cdk/aws-autoscaling-common.IRandomGenerator"
    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> bool:
        return jsii.invoke(self, "nextBoolean", [])

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        return jsii.invoke(self, "nextInt", [min, max])


class _ScalingInterval(jsii.compat.TypedDict, total=False):
    lower: jsii.Number
    upper: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.ScalingInterval")
class ScalingInterval(_ScalingInterval):
    change: jsii.Number

__all__ = ["Alarms", "ArbitraryIntervals", "CompleteScalingInterval", "IRandomGenerator", "ScalingInterval", "__jsii_assembly__"]

publication.publish()
