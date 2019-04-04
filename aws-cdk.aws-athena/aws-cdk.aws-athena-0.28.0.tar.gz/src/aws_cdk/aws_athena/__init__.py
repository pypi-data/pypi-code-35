import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-athena", "0.28.0", __name__, "aws-athena@0.28.0.jsii.tgz")
class CfnNamedQuery(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-athena.CfnNamedQuery"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, database: str, query_string: str, description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: CfnNamedQueryProps = {"database": database, "queryString": query_string}

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        jsii.create(CfnNamedQuery, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="namedQueryName")
    def named_query_name(self) -> str:
        return jsii.get(self, "namedQueryName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNamedQueryProps":
        return jsii.get(self, "propertyOverrides")


class _CfnNamedQueryProps(jsii.compat.TypedDict, total=False):
    description: str
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-athena.CfnNamedQueryProps")
class CfnNamedQueryProps(_CfnNamedQueryProps):
    database: str
    queryString: str

__all__ = ["CfnNamedQuery", "CfnNamedQueryProps", "__jsii_assembly__"]

publication.publish()
