import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sdb", "0.28.0", __name__, "aws-sdb@0.28.0.jsii.tgz")
class CfnDomain(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sdb.CfnDomain"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None) -> None:
        props: CfnDomainProps = {}

        if description is not None:
            props["description"] = description

        jsii.create(CfnDomain, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDomainProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-sdb.CfnDomainProps")
class CfnDomainProps(jsii.compat.TypedDict, total=False):
    description: str

__all__ = ["CfnDomain", "CfnDomainProps", "__jsii_assembly__"]

publication.publish()
