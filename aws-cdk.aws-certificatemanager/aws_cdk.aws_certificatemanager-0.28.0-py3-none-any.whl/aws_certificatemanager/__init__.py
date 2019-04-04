import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_route53
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-certificatemanager", "0.28.0", __name__, "aws-certificatemanager@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.CertificateImportProps")
class CertificateImportProps(jsii.compat.TypedDict):
    certificateArn: str

class _CertificateProps(jsii.compat.TypedDict, total=False):
    subjectAlternativeNames: typing.List[str]
    validationDomains: typing.Mapping[str,str]

@jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.CertificateProps")
class CertificateProps(_CertificateProps):
    domainName: str

class CfnCertificate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain_name: str, domain_validation_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["DomainValidationOptionProperty", aws_cdk.cdk.Token]]]]=None, subject_alternative_names: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, validation_method: typing.Optional[str]=None) -> None:
        props: CfnCertificateProps = {"domainName": domain_name}

        if domain_validation_options is not None:
            props["domainValidationOptions"] = domain_validation_options

        if subject_alternative_names is not None:
            props["subjectAlternativeNames"] = subject_alternative_names

        if tags is not None:
            props["tags"] = tags

        if validation_method is not None:
            props["validationMethod"] = validation_method

        jsii.create(CfnCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        return jsii.get(self, "certificateArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCertificateProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificate.DomainValidationOptionProperty")
    class DomainValidationOptionProperty(jsii.compat.TypedDict):
        domainName: str
        validationDomain: str


class _CfnCertificateProps(jsii.compat.TypedDict, total=False):
    domainValidationOptions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnCertificate.DomainValidationOptionProperty", aws_cdk.cdk.Token]]]
    subjectAlternativeNames: typing.List[str]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    validationMethod: str

@jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificateProps")
class CfnCertificateProps(_CfnCertificateProps):
    domainName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-certificatemanager.DnsValidatedCertificateProps")
class DnsValidatedCertificateProps(CertificateProps, jsii.compat.TypedDict):
    hostedZone: aws_cdk.aws_route53.IHostedZone

@jsii.interface(jsii_type="@aws-cdk/aws-certificatemanager.ICertificate")
class ICertificate(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ICertificateProxy

    @property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "CertificateImportProps":
        ...


class _ICertificateProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-certificatemanager.ICertificate"
    @property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        return jsii.get(self, "certificateArn")

    @jsii.member(jsii_name="export")
    def export(self) -> "CertificateImportProps":
        return jsii.invoke(self, "export", [])


@jsii.implements(ICertificate)
class Certificate(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-certificatemanager.Certificate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        props: CertificateProps = {"domainName": domain_name}

        if subject_alternative_names is not None:
            props["subjectAlternativeNames"] = subject_alternative_names

        if validation_domains is not None:
            props["validationDomains"] = validation_domains

        jsii.create(Certificate, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, certificate_arn: str) -> "ICertificate":
        props: CertificateImportProps = {"certificateArn": certificate_arn}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "CertificateImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        return jsii.get(self, "certificateArn")


@jsii.implements(ICertificate)
class DnsValidatedCertificate(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-certificatemanager.DnsValidatedCertificate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, hosted_zone: aws_cdk.aws_route53.IHostedZone, domain_name: str, subject_alternative_names: typing.Optional[typing.List[str]]=None, validation_domains: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        props: DnsValidatedCertificateProps = {"hostedZone": hosted_zone, "domainName": domain_name}

        if subject_alternative_names is not None:
            props["subjectAlternativeNames"] = subject_alternative_names

        if validation_domains is not None:
            props["validationDomains"] = validation_domains

        jsii.create(DnsValidatedCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "CertificateImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        return jsii.get(self, "certificateArn")


__all__ = ["Certificate", "CertificateImportProps", "CertificateProps", "CfnCertificate", "CfnCertificateProps", "DnsValidatedCertificate", "DnsValidatedCertificateProps", "ICertificate", "__jsii_assembly__"]

publication.publish()
