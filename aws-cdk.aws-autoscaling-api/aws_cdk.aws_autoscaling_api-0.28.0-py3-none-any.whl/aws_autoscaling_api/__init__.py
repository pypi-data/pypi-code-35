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
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscaling-api", "0.28.0", __name__, "aws-autoscaling-api@0.28.0.jsii.tgz")
@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling-api.ILifecycleHook")
class ILifecycleHook(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILifecycleHookProxy

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        ...


class _ILifecycleHookProxy():
    __jsii_type__ = "@aws-cdk/aws-autoscaling-api.ILifecycleHook"
    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "role")


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling-api.ILifecycleHookTarget")
class ILifecycleHookTarget(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILifecycleHookTargetProxy

    @jsii.member(jsii_name="asLifecycleHookTarget")
    def as_lifecycle_hook_target(self, lifecycle_hook: "ILifecycleHook") -> "LifecycleHookTargetProps":
        ...


class _ILifecycleHookTargetProxy():
    __jsii_type__ = "@aws-cdk/aws-autoscaling-api.ILifecycleHookTarget"
    @jsii.member(jsii_name="asLifecycleHookTarget")
    def as_lifecycle_hook_target(self, lifecycle_hook: "ILifecycleHook") -> "LifecycleHookTargetProps":
        return jsii.invoke(self, "asLifecycleHookTarget", [lifecycle_hook])


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-api.LifecycleHookTargetProps")
class LifecycleHookTargetProps(jsii.compat.TypedDict):
    notificationTargetArn: str

__all__ = ["ILifecycleHook", "ILifecycleHookTarget", "LifecycleHookTargetProps", "__jsii_assembly__"]

publication.publish()
