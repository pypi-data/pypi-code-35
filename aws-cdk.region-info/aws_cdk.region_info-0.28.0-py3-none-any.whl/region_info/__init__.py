import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/region-info", "0.28.0", __name__, "region-info@0.28.0.jsii.tgz")
class Default(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/region-info.Default"):
    @jsii.member(jsii_name="servicePrincipal")
    @classmethod
    def service_principal(cls, service: str, region: str, url_suffix: str) -> str:
        return jsii.sinvoke(cls, "servicePrincipal", [service, region, url_suffix])


class Fact(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/region-info.Fact"):
    @jsii.member(jsii_name="find")
    @classmethod
    def find(cls, region: str, name: str) -> typing.Optional[str]:
        return jsii.sinvoke(cls, "find", [region, name])

    @jsii.member(jsii_name="register")
    @classmethod
    def register(cls, fact: "IFact", allow_replacing: typing.Optional[bool]=None) -> None:
        return jsii.sinvoke(cls, "register", [fact, allow_replacing])

    @jsii.member(jsii_name="unregister")
    @classmethod
    def unregister(cls, region: str, name: str, value: typing.Optional[str]=None) -> None:
        return jsii.sinvoke(cls, "unregister", [region, name, value])


class FactName(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/region-info.FactName"):
    def __init__(self) -> None:
        jsii.create(FactName, self, [])

    @jsii.member(jsii_name="servicePrincipal")
    @classmethod
    def service_principal(cls, service: str) -> str:
        return jsii.sinvoke(cls, "servicePrincipal", [service])

    @classproperty
    @jsii.member(jsii_name="cdkMetadataResourceAvailable")
    def CDK_METADATA_RESOURCE_AVAILABLE(cls) -> str:
        return jsii.sget(cls, "cdkMetadataResourceAvailable")

    @classproperty
    @jsii.member(jsii_name="domainSuffix")
    def DOMAIN_SUFFIX(cls) -> str:
        return jsii.sget(cls, "domainSuffix")

    @classproperty
    @jsii.member(jsii_name="partition")
    def PARTITION(cls) -> str:
        return jsii.sget(cls, "partition")

    @classproperty
    @jsii.member(jsii_name="s3StaticWebsiteEndpoint")
    def S3_STATIC_WEBSITE_ENDPOINT(cls) -> str:
        return jsii.sget(cls, "s3StaticWebsiteEndpoint")


@jsii.interface(jsii_type="@aws-cdk/region-info.IFact")
class IFact(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IFactProxy

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        ...


class _IFactProxy():
    __jsii_type__ = "@aws-cdk/region-info.IFact"
    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        return jsii.get(self, "region")

    @property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        return jsii.get(self, "value")


class RegionInfo(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/region-info.RegionInfo"):
    @jsii.member(jsii_name="get")
    @classmethod
    def get(cls, name: str) -> "RegionInfo":
        return jsii.sinvoke(cls, "get", [name])

    @jsii.member(jsii_name="servicePrincipal")
    def service_principal(self, service: str) -> typing.Optional[str]:
        return jsii.invoke(self, "servicePrincipal", [service])

    @property
    @jsii.member(jsii_name="cdkMetadataResourceAvailable")
    def cdk_metadata_resource_available(self) -> bool:
        return jsii.get(self, "cdkMetadataResourceAvailable")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @property
    @jsii.member(jsii_name="domainSuffix")
    def domain_suffix(self) -> typing.Optional[str]:
        return jsii.get(self, "domainSuffix")

    @property
    @jsii.member(jsii_name="partition")
    def partition(self) -> typing.Optional[str]:
        return jsii.get(self, "partition")

    @property
    @jsii.member(jsii_name="s3StaticWebsiteEndpoint")
    def s3_static_website_endpoint(self) -> typing.Optional[str]:
        return jsii.get(self, "s3StaticWebsiteEndpoint")


__all__ = ["Default", "Fact", "FactName", "IFact", "RegionInfo", "__jsii_assembly__"]

publication.publish()
