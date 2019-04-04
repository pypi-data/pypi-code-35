import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_route53
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloudfront", "0.28.0", __name__, "aws-cloudfront@0.28.0.jsii.tgz")
class _AliasConfiguration(jsii.compat.TypedDict, total=False):
    securityPolicy: "SecurityPolicyProtocol"
    sslMethod: "SSLMethod"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.AliasConfiguration")
class AliasConfiguration(_AliasConfiguration):
    acmCertRef: str
    names: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.Behavior")
class Behavior(jsii.compat.TypedDict, total=False):
    allowedMethods: "CloudFrontAllowedMethods"
    cachedMethods: "CloudFrontAllowedCachedMethods"
    compress: bool
    defaultTtlSeconds: jsii.Number
    forwardedValues: "CfnDistribution.ForwardedValuesProperty"
    isDefaultBehavior: bool
    maxTtlSeconds: jsii.Number
    minTtlSeconds: jsii.Number
    pathPattern: str
    trustedSigners: typing.List[str]

class CfnCloudFrontOriginAccessIdentity(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentity"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cloud_front_origin_access_identity_config: typing.Union["CloudFrontOriginAccessIdentityConfigProperty", aws_cdk.cdk.Token]) -> None:
        props: CfnCloudFrontOriginAccessIdentityProps = {"cloudFrontOriginAccessIdentityConfig": cloud_front_origin_access_identity_config}

        jsii.create(CfnCloudFrontOriginAccessIdentity, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="cloudFrontOriginAccessIdentityId")
    def cloud_front_origin_access_identity_id(self) -> str:
        return jsii.get(self, "cloudFrontOriginAccessIdentityId")

    @property
    @jsii.member(jsii_name="cloudFrontOriginAccessIdentityS3CanonicalUserId")
    def cloud_front_origin_access_identity_s3_canonical_user_id(self) -> str:
        return jsii.get(self, "cloudFrontOriginAccessIdentityS3CanonicalUserId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCloudFrontOriginAccessIdentityProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty")
    class CloudFrontOriginAccessIdentityConfigProperty(jsii.compat.TypedDict):
        comment: str


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentityProps")
class CfnCloudFrontOriginAccessIdentityProps(jsii.compat.TypedDict):
    cloudFrontOriginAccessIdentityConfig: typing.Union["CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty", aws_cdk.cdk.Token]

class CfnDistribution(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, distribution_config: typing.Union[aws_cdk.cdk.Token, "DistributionConfigProperty"], tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDistributionProps = {"distributionConfig": distribution_config}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDistribution, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> str:
        return jsii.get(self, "distributionDomainName")

    @property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> str:
        return jsii.get(self, "distributionId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDistributionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _CacheBehaviorProperty(jsii.compat.TypedDict, total=False):
        allowedMethods: typing.List[str]
        cachedMethods: typing.List[str]
        compress: typing.Union[bool, aws_cdk.cdk.Token]
        defaultTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        fieldLevelEncryptionId: str
        lambdaFunctionAssociations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.LambdaFunctionAssociationProperty"]]]
        maxTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        smoothStreaming: typing.Union[bool, aws_cdk.cdk.Token]
        trustedSigners: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CacheBehaviorProperty")
    class CacheBehaviorProperty(_CacheBehaviorProperty):
        forwardedValues: typing.Union["CfnDistribution.ForwardedValuesProperty", aws_cdk.cdk.Token]
        pathPattern: str
        targetOriginId: str
        viewerProtocolPolicy: str

    class _CookiesProperty(jsii.compat.TypedDict, total=False):
        whitelistedNames: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CookiesProperty")
    class CookiesProperty(_CookiesProperty):
        forward: str

    class _CustomErrorResponseProperty(jsii.compat.TypedDict, total=False):
        errorCachingMinTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        responseCode: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        responsePagePath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CustomErrorResponseProperty")
    class CustomErrorResponseProperty(_CustomErrorResponseProperty):
        errorCode: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _CustomOriginConfigProperty(jsii.compat.TypedDict, total=False):
        httpPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        httpsPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        originKeepaliveTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        originReadTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        originSslProtocols: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CustomOriginConfigProperty")
    class CustomOriginConfigProperty(_CustomOriginConfigProperty):
        originProtocolPolicy: str

    class _DefaultCacheBehaviorProperty(jsii.compat.TypedDict, total=False):
        allowedMethods: typing.List[str]
        cachedMethods: typing.List[str]
        compress: typing.Union[bool, aws_cdk.cdk.Token]
        defaultTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        fieldLevelEncryptionId: str
        lambdaFunctionAssociations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.LambdaFunctionAssociationProperty"]]]
        maxTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        smoothStreaming: typing.Union[bool, aws_cdk.cdk.Token]
        trustedSigners: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.DefaultCacheBehaviorProperty")
    class DefaultCacheBehaviorProperty(_DefaultCacheBehaviorProperty):
        forwardedValues: typing.Union["CfnDistribution.ForwardedValuesProperty", aws_cdk.cdk.Token]
        targetOriginId: str
        viewerProtocolPolicy: str

    class _DistributionConfigProperty(jsii.compat.TypedDict, total=False):
        aliases: typing.List[str]
        cacheBehaviors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.CacheBehaviorProperty"]]]
        comment: str
        customErrorResponses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnDistribution.CustomErrorResponseProperty", aws_cdk.cdk.Token]]]
        defaultCacheBehavior: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.DefaultCacheBehaviorProperty"]
        defaultRootObject: str
        httpVersion: str
        ipv6Enabled: typing.Union[bool, aws_cdk.cdk.Token]
        logging: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.LoggingProperty"]
        origins: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.OriginProperty"]]]
        priceClass: str
        restrictions: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.RestrictionsProperty"]
        viewerCertificate: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.ViewerCertificateProperty"]
        webAclId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.DistributionConfigProperty")
    class DistributionConfigProperty(_DistributionConfigProperty):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    class _ForwardedValuesProperty(jsii.compat.TypedDict, total=False):
        cookies: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.CookiesProperty"]
        headers: typing.List[str]
        queryStringCacheKeys: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.ForwardedValuesProperty")
    class ForwardedValuesProperty(_ForwardedValuesProperty):
        queryString: typing.Union[bool, aws_cdk.cdk.Token]

    class _GeoRestrictionProperty(jsii.compat.TypedDict, total=False):
        locations: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.GeoRestrictionProperty")
    class GeoRestrictionProperty(_GeoRestrictionProperty):
        restrictionType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.LambdaFunctionAssociationProperty")
    class LambdaFunctionAssociationProperty(jsii.compat.TypedDict, total=False):
        eventType: str
        lambdaFunctionArn: str

    class _LoggingProperty(jsii.compat.TypedDict, total=False):
        includeCookies: typing.Union[bool, aws_cdk.cdk.Token]
        prefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.LoggingProperty")
    class LoggingProperty(_LoggingProperty):
        bucket: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginCustomHeaderProperty")
    class OriginCustomHeaderProperty(jsii.compat.TypedDict):
        headerName: str
        headerValue: str

    class _OriginProperty(jsii.compat.TypedDict, total=False):
        customOriginConfig: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.CustomOriginConfigProperty"]
        originCustomHeaders: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.OriginCustomHeaderProperty"]]]
        originPath: str
        s3OriginConfig: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.S3OriginConfigProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginProperty")
    class OriginProperty(_OriginProperty):
        domainName: str
        id: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.RestrictionsProperty")
    class RestrictionsProperty(jsii.compat.TypedDict):
        geoRestriction: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.GeoRestrictionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.S3OriginConfigProperty")
    class S3OriginConfigProperty(jsii.compat.TypedDict, total=False):
        originAccessIdentity: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.ViewerCertificateProperty")
    class ViewerCertificateProperty(jsii.compat.TypedDict, total=False):
        acmCertificateArn: str
        cloudFrontDefaultCertificate: typing.Union[bool, aws_cdk.cdk.Token]
        iamCertificateId: str
        minimumProtocolVersion: str
        sslSupportMethod: str


class _CfnDistributionProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistributionProps")
class CfnDistributionProps(_CfnDistributionProps):
    distributionConfig: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.DistributionConfigProperty"]

class CfnStreamingDistribution(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, streaming_distribution_config: typing.Union[aws_cdk.cdk.Token, "StreamingDistributionConfigProperty"], tags: typing.List[aws_cdk.cdk.CfnTag]) -> None:
        props: CfnStreamingDistributionProps = {"streamingDistributionConfig": streaming_distribution_config, "tags": tags}

        jsii.create(CfnStreamingDistribution, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStreamingDistributionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="streamingDistributionDomainName")
    def streaming_distribution_domain_name(self) -> str:
        return jsii.get(self, "streamingDistributionDomainName")

    @property
    @jsii.member(jsii_name="streamingDistributionId")
    def streaming_distribution_id(self) -> str:
        return jsii.get(self, "streamingDistributionId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.LoggingProperty")
    class LoggingProperty(jsii.compat.TypedDict):
        bucket: str
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        prefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.S3OriginProperty")
    class S3OriginProperty(jsii.compat.TypedDict):
        domainName: str
        originAccessIdentity: str

    class _StreamingDistributionConfigProperty(jsii.compat.TypedDict, total=False):
        aliases: typing.List[str]
        logging: typing.Union[aws_cdk.cdk.Token, "CfnStreamingDistribution.LoggingProperty"]
        priceClass: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.StreamingDistributionConfigProperty")
    class StreamingDistributionConfigProperty(_StreamingDistributionConfigProperty):
        comment: str
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        s3Origin: typing.Union[aws_cdk.cdk.Token, "CfnStreamingDistribution.S3OriginProperty"]
        trustedSigners: typing.Union[aws_cdk.cdk.Token, "CfnStreamingDistribution.TrustedSignersProperty"]

    class _TrustedSignersProperty(jsii.compat.TypedDict, total=False):
        awsAccountNumbers: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.TrustedSignersProperty")
    class TrustedSignersProperty(_TrustedSignersProperty):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistributionProps")
class CfnStreamingDistributionProps(jsii.compat.TypedDict):
    streamingDistributionConfig: typing.Union[aws_cdk.cdk.Token, "CfnStreamingDistribution.StreamingDistributionConfigProperty"]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontAllowedCachedMethods")
class CloudFrontAllowedCachedMethods(enum.Enum):
    GET_HEAD = "GET_HEAD"
    GET_HEAD_OPTIONS = "GET_HEAD_OPTIONS"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontAllowedMethods")
class CloudFrontAllowedMethods(enum.Enum):
    GET_HEAD = "GET_HEAD"
    GET_HEAD_OPTIONS = "GET_HEAD_OPTIONS"
    ALL = "ALL"

@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class CloudFrontWebDistribution(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistribution"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, origin_configs: typing.List["SourceConfiguration"], alias_configuration: typing.Optional["AliasConfiguration"]=None, comment: typing.Optional[str]=None, default_root_object: typing.Optional[str]=None, enable_ip_v6: typing.Optional[bool]=None, error_configurations: typing.Optional[typing.List["CfnDistribution.CustomErrorResponseProperty"]]=None, http_version: typing.Optional["HttpVersion"]=None, logging_config: typing.Optional["LoggingConfiguration"]=None, price_class: typing.Optional["PriceClass"]=None, viewer_protocol_policy: typing.Optional["ViewerProtocolPolicy"]=None, web_acl_id: typing.Optional[str]=None) -> None:
        props: CloudFrontWebDistributionProps = {"originConfigs": origin_configs}

        if alias_configuration is not None:
            props["aliasConfiguration"] = alias_configuration

        if comment is not None:
            props["comment"] = comment

        if default_root_object is not None:
            props["defaultRootObject"] = default_root_object

        if enable_ip_v6 is not None:
            props["enableIpV6"] = enable_ip_v6

        if error_configurations is not None:
            props["errorConfigurations"] = error_configurations

        if http_version is not None:
            props["httpVersion"] = http_version

        if logging_config is not None:
            props["loggingConfig"] = logging_config

        if price_class is not None:
            props["priceClass"] = price_class

        if viewer_protocol_policy is not None:
            props["viewerProtocolPolicy"] = viewer_protocol_policy

        if web_acl_id is not None:
            props["webACLId"] = web_acl_id

        jsii.create(CloudFrontWebDistribution, self, [scope, id, props])

    @jsii.member(jsii_name="asAliasRecordTarget")
    def as_alias_record_target(self) -> aws_cdk.aws_route53.AliasRecordTargetProps:
        return jsii.invoke(self, "asAliasRecordTarget", [])

    @property
    @jsii.member(jsii_name="aliasHostedZoneId")
    def alias_hosted_zone_id(self) -> str:
        return jsii.get(self, "aliasHostedZoneId")

    @property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> str:
        return jsii.get(self, "distributionId")

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        return jsii.get(self, "domainName")

    @property
    @jsii.member(jsii_name="loggingBucket")
    def logging_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        return jsii.get(self, "loggingBucket")


class _CloudFrontWebDistributionProps(jsii.compat.TypedDict, total=False):
    aliasConfiguration: "AliasConfiguration"
    comment: str
    defaultRootObject: str
    enableIpV6: bool
    errorConfigurations: typing.List["CfnDistribution.CustomErrorResponseProperty"]
    httpVersion: "HttpVersion"
    loggingConfig: "LoggingConfiguration"
    priceClass: "PriceClass"
    viewerProtocolPolicy: "ViewerProtocolPolicy"
    webACLId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistributionProps")
class CloudFrontWebDistributionProps(_CloudFrontWebDistributionProps):
    originConfigs: typing.List["SourceConfiguration"]

class _CustomOriginConfig(jsii.compat.TypedDict, total=False):
    allowedOriginSSLVersions: typing.List["OriginSslPolicy"]
    httpPort: jsii.Number
    httpsPort: jsii.Number
    originKeepaliveTimeoutSeconds: jsii.Number
    originProtocolPolicy: "OriginProtocolPolicy"
    originReadTimeoutSeconds: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CustomOriginConfig")
class CustomOriginConfig(_CustomOriginConfig):
    domainName: str

class _ErrorConfiguration(jsii.compat.TypedDict, total=False):
    cacheTtl: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.ErrorConfiguration")
class ErrorConfiguration(_ErrorConfiguration):
    originErrorCode: jsii.Number
    respondWithErrorCode: jsii.Number
    respondWithPage: str

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.HttpVersion")
class HttpVersion(enum.Enum):
    HTTP1_1 = "HTTP1_1"
    HTTP2 = "HTTP2"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.LoggingConfiguration")
class LoggingConfiguration(jsii.compat.TypedDict, total=False):
    bucket: aws_cdk.aws_s3.IBucket
    includeCookies: bool
    prefix: str

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.OriginProtocolPolicy")
class OriginProtocolPolicy(enum.Enum):
    HttpOnly = "HttpOnly"
    MatchViewer = "MatchViewer"
    HttpsOnly = "HttpsOnly"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.OriginSslPolicy")
class OriginSslPolicy(enum.Enum):
    SSLv3 = "SSLv3"
    TLSv1 = "TLSv1"
    TLSv1_1 = "TLSv1_1"
    TLSv1_2 = "TLSv1_2"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.PriceClass")
class PriceClass(enum.Enum):
    PriceClass100 = "PriceClass100"
    PriceClass200 = "PriceClass200"
    PriceClassAll = "PriceClassAll"

class _S3OriginConfig(jsii.compat.TypedDict, total=False):
    originAccessIdentity: "CfnCloudFrontOriginAccessIdentity"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.S3OriginConfig")
class S3OriginConfig(_S3OriginConfig):
    s3BucketSource: aws_cdk.aws_s3.IBucket

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.SSLMethod")
class SSLMethod(enum.Enum):
    SNI = "SNI"
    VIP = "VIP"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.SecurityPolicyProtocol")
class SecurityPolicyProtocol(enum.Enum):
    SSLv3 = "SSLv3"
    TLSv1 = "TLSv1"
    TLSv1_2016 = "TLSv1_2016"
    TLSv1_1_2016 = "TLSv1_1_2016"
    TLSv1_2_2018 = "TLSv1_2_2018"

class _SourceConfiguration(jsii.compat.TypedDict, total=False):
    customOriginSource: "CustomOriginConfig"
    originHeaders: typing.Mapping[str,str]
    originPath: str
    s3OriginSource: "S3OriginConfig"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.SourceConfiguration")
class SourceConfiguration(_SourceConfiguration):
    behaviors: typing.List["Behavior"]

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.ViewerProtocolPolicy")
class ViewerProtocolPolicy(enum.Enum):
    HTTPSOnly = "HTTPSOnly"
    RedirectToHTTPS = "RedirectToHTTPS"
    AllowAll = "AllowAll"

__all__ = ["AliasConfiguration", "Behavior", "CfnCloudFrontOriginAccessIdentity", "CfnCloudFrontOriginAccessIdentityProps", "CfnDistribution", "CfnDistributionProps", "CfnStreamingDistribution", "CfnStreamingDistributionProps", "CloudFrontAllowedCachedMethods", "CloudFrontAllowedMethods", "CloudFrontWebDistribution", "CloudFrontWebDistributionProps", "CustomOriginConfig", "ErrorConfiguration", "HttpVersion", "LoggingConfiguration", "OriginProtocolPolicy", "OriginSslPolicy", "PriceClass", "S3OriginConfig", "SSLMethod", "SecurityPolicyProtocol", "SourceConfiguration", "ViewerProtocolPolicy", "__jsii_assembly__"]

publication.publish()
