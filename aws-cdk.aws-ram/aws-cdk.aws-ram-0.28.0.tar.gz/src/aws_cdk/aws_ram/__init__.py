import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ram", "0.28.0", __name__, "aws-ram@0.28.0.jsii.tgz")
class CfnResourceShare(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ram.CfnResourceShare"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, allow_external_principals: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, principals: typing.Optional[typing.List[str]]=None, resource_arns: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnResourceShareProps = {"name": name}

        if allow_external_principals is not None:
            props["allowExternalPrincipals"] = allow_external_principals

        if principals is not None:
            props["principals"] = principals

        if resource_arns is not None:
            props["resourceArns"] = resource_arns

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnResourceShare, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResourceShareProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resourceShareArn")
    def resource_share_arn(self) -> str:
        return jsii.get(self, "resourceShareArn")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnResourceShareProps(jsii.compat.TypedDict, total=False):
    allowExternalPrincipals: typing.Union[bool, aws_cdk.cdk.Token]
    principals: typing.List[str]
    resourceArns: typing.List[str]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ram.CfnResourceShareProps")
class CfnResourceShareProps(_CfnResourceShareProps):
    name: str

__all__ = ["CfnResourceShare", "CfnResourceShareProps", "__jsii_assembly__"]

publication.publish()
