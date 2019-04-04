import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-directoryservice", "0.28.0", __name__, "aws-directoryservice@0.28.0.jsii.tgz")
class CfnMicrosoftAD(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-directoryservice.CfnMicrosoftAD"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, password: str, vpc_settings: typing.Union["VpcSettingsProperty", aws_cdk.cdk.Token], create_alias: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, edition: typing.Optional[str]=None, enable_sso: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, short_name: typing.Optional[str]=None) -> None:
        props: CfnMicrosoftADProps = {"name": name, "password": password, "vpcSettings": vpc_settings}

        if create_alias is not None:
            props["createAlias"] = create_alias

        if edition is not None:
            props["edition"] = edition

        if enable_sso is not None:
            props["enableSso"] = enable_sso

        if short_name is not None:
            props["shortName"] = short_name

        jsii.create(CfnMicrosoftAD, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="microsoftAdAlias")
    def microsoft_ad_alias(self) -> str:
        return jsii.get(self, "microsoftAdAlias")

    @property
    @jsii.member(jsii_name="microsoftAdDnsIpAddresses")
    def microsoft_ad_dns_ip_addresses(self) -> typing.List[str]:
        return jsii.get(self, "microsoftAdDnsIpAddresses")

    @property
    @jsii.member(jsii_name="microsoftAdId")
    def microsoft_ad_id(self) -> str:
        return jsii.get(self, "microsoftAdId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMicrosoftADProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-directoryservice.CfnMicrosoftAD.VpcSettingsProperty")
    class VpcSettingsProperty(jsii.compat.TypedDict):
        subnetIds: typing.List[str]
        vpcId: str


class _CfnMicrosoftADProps(jsii.compat.TypedDict, total=False):
    createAlias: typing.Union[bool, aws_cdk.cdk.Token]
    edition: str
    enableSso: typing.Union[bool, aws_cdk.cdk.Token]
    shortName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-directoryservice.CfnMicrosoftADProps")
class CfnMicrosoftADProps(_CfnMicrosoftADProps):
    name: str
    password: str
    vpcSettings: typing.Union["CfnMicrosoftAD.VpcSettingsProperty", aws_cdk.cdk.Token]

class CfnSimpleAD(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-directoryservice.CfnSimpleAD"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, password: str, size: str, vpc_settings: typing.Union[aws_cdk.cdk.Token, "VpcSettingsProperty"], create_alias: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, description: typing.Optional[str]=None, enable_sso: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, short_name: typing.Optional[str]=None) -> None:
        props: CfnSimpleADProps = {"name": name, "password": password, "size": size, "vpcSettings": vpc_settings}

        if create_alias is not None:
            props["createAlias"] = create_alias

        if description is not None:
            props["description"] = description

        if enable_sso is not None:
            props["enableSso"] = enable_sso

        if short_name is not None:
            props["shortName"] = short_name

        jsii.create(CfnSimpleAD, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSimpleADProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="simpleAdAlias")
    def simple_ad_alias(self) -> str:
        return jsii.get(self, "simpleAdAlias")

    @property
    @jsii.member(jsii_name="simpleAdDnsIpAddresses")
    def simple_ad_dns_ip_addresses(self) -> typing.List[str]:
        return jsii.get(self, "simpleAdDnsIpAddresses")

    @property
    @jsii.member(jsii_name="simpleAdId")
    def simple_ad_id(self) -> str:
        return jsii.get(self, "simpleAdId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-directoryservice.CfnSimpleAD.VpcSettingsProperty")
    class VpcSettingsProperty(jsii.compat.TypedDict):
        subnetIds: typing.List[str]
        vpcId: str


class _CfnSimpleADProps(jsii.compat.TypedDict, total=False):
    createAlias: typing.Union[bool, aws_cdk.cdk.Token]
    description: str
    enableSso: typing.Union[bool, aws_cdk.cdk.Token]
    shortName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-directoryservice.CfnSimpleADProps")
class CfnSimpleADProps(_CfnSimpleADProps):
    name: str
    password: str
    size: str
    vpcSettings: typing.Union[aws_cdk.cdk.Token, "CfnSimpleAD.VpcSettingsProperty"]

__all__ = ["CfnMicrosoftAD", "CfnMicrosoftADProps", "CfnSimpleAD", "CfnSimpleADProps", "__jsii_assembly__"]

publication.publish()
