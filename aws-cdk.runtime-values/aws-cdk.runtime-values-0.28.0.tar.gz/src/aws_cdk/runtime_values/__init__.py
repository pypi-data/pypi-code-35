import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_ssm
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/runtime-values", "0.28.0", __name__, "runtime-values@0.28.0.jsii.tgz")
class RuntimeValue(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/runtime-values.RuntimeValue"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, package: str, value: typing.Any) -> None:
        props: RuntimeValueProps = {"package": package, "value": value}

        jsii.create(RuntimeValue, self, [scope, id, props])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [grantee])

    @classproperty
    @jsii.member(jsii_name="ENV_NAME")
    def ENV_NAME(cls) -> str:
        return jsii.sget(cls, "ENV_NAME")

    @property
    @jsii.member(jsii_name="envValue")
    def env_value(self) -> str:
        return jsii.get(self, "envValue")

    @property
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> str:
        return jsii.get(self, "parameterArn")

    @property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> str:
        return jsii.get(self, "parameterName")


@jsii.data_type(jsii_type="@aws-cdk/runtime-values.RuntimeValueProps")
class RuntimeValueProps(jsii.compat.TypedDict):
    package: str
    value: typing.Any

__all__ = ["RuntimeValue", "RuntimeValueProps", "__jsii_assembly__"]

publication.publish()
