import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_codedeploy_api
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_route53
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticloadbalancingv2", "0.28.0", __name__, "aws-elasticloadbalancingv2@0.28.0.jsii.tgz")
class _AddNetworkTargetsProps(jsii.compat.TypedDict, total=False):
    deregistrationDelaySec: jsii.Number
    healthCheck: "HealthCheck"
    proxyProtocolV2: bool
    targetGroupName: str
    targets: typing.List["INetworkLoadBalancerTarget"]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddNetworkTargetsProps")
class AddNetworkTargetsProps(_AddNetworkTargetsProps):
    port: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddRuleProps")
class AddRuleProps(jsii.compat.TypedDict, total=False):
    hostHeader: str
    pathPattern: str
    priority: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationTargetGroupsProps")
class AddApplicationTargetGroupsProps(AddRuleProps, jsii.compat.TypedDict):
    targetGroups: typing.List["IApplicationTargetGroup"]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationTargetsProps")
class AddApplicationTargetsProps(AddRuleProps, jsii.compat.TypedDict, total=False):
    deregistrationDelaySec: jsii.Number
    healthCheck: "HealthCheck"
    port: jsii.Number
    protocol: "ApplicationProtocol"
    slowStartSec: jsii.Number
    stickinessCookieDurationSec: jsii.Number
    targetGroupName: str
    targets: typing.List["IApplicationLoadBalancerTarget"]

class ApplicationListenerCertificate(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerCertificate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, certificate_arns: typing.List[str], listener: "IApplicationListener") -> None:
        props: ApplicationListenerCertificateProps = {"certificateArns": certificate_arns, "listener": listener}

        jsii.create(ApplicationListenerCertificate, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerCertificateProps")
class ApplicationListenerCertificateProps(jsii.compat.TypedDict):
    certificateArns: typing.List[str]
    listener: "IApplicationListener"

class _ApplicationListenerImportProps(jsii.compat.TypedDict, total=False):
    defaultPort: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerImportProps")
class ApplicationListenerImportProps(_ApplicationListenerImportProps):
    listenerArn: str
    securityGroupId: str

class ApplicationListenerRule(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, listener: "IApplicationListener", priority: jsii.Number, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None) -> None:
        props: ApplicationListenerRuleProps = {"listener": listener, "priority": priority}

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if target_groups is not None:
            props["targetGroups"] = target_groups

        jsii.create(ApplicationListenerRule, self, [scope, id, props])

    @jsii.member(jsii_name="addTargetGroup")
    def add_target_group(self, target_group: "IApplicationTargetGroup") -> None:
        return jsii.invoke(self, "addTargetGroup", [target_group])

    @jsii.member(jsii_name="setCondition")
    def set_condition(self, field: str, values: typing.Optional[typing.List[str]]=None) -> None:
        return jsii.invoke(self, "setCondition", [field, values])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="listenerRuleArn")
    def listener_rule_arn(self) -> str:
        return jsii.get(self, "listenerRuleArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerImportProps")
class ApplicationLoadBalancerImportProps(jsii.compat.TypedDict):
    loadBalancerArn: str
    securityGroupId: str

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationProtocol")
class ApplicationProtocol(enum.Enum):
    Http = "Http"
    Https = "Https"

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseApplicationListenerProps")
class BaseApplicationListenerProps(jsii.compat.TypedDict, total=False):
    certificateArns: typing.List[str]
    defaultTargetGroups: typing.List["IApplicationTargetGroup"]
    open: bool
    port: jsii.Number
    protocol: "ApplicationProtocol"
    sslPolicy: "SslPolicy"

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerProps")
class ApplicationListenerProps(BaseApplicationListenerProps, jsii.compat.TypedDict):
    loadBalancer: "IApplicationLoadBalancer"

class _BaseApplicationListenerRuleProps(jsii.compat.TypedDict, total=False):
    hostHeader: str
    pathPattern: str
    targetGroups: typing.List["IApplicationTargetGroup"]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseApplicationListenerRuleProps")
class BaseApplicationListenerRuleProps(_BaseApplicationListenerRuleProps):
    priority: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerRuleProps")
class ApplicationListenerRuleProps(BaseApplicationListenerRuleProps, jsii.compat.TypedDict):
    listener: "IApplicationListener"

class BaseListener(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseListener"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseListenerProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, additional_props: typing.Any) -> None:
        jsii.create(BaseListener, self, [scope, id, additional_props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        return jsii.get(self, "listenerArn")


class _BaseListenerProxy(BaseListener):
    pass

@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class BaseLoadBalancer(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancer"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseLoadBalancerProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, base_props: "BaseLoadBalancerProps", additional_props: typing.Any) -> None:
        jsii.create(BaseLoadBalancer, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="asAliasRecordTarget")
    def as_alias_record_target(self) -> aws_cdk.aws_route53.AliasRecordTargetProps:
        return jsii.invoke(self, "asAliasRecordTarget", [])

    @jsii.member(jsii_name="removeAttribute")
    def remove_attribute(self, key: str) -> None:
        return jsii.invoke(self, "removeAttribute", [key])

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: str, value: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "setAttribute", [key, value])

    @property
    @jsii.member(jsii_name="canonicalHostedZoneId")
    def canonical_hosted_zone_id(self) -> str:
        return jsii.get(self, "canonicalHostedZoneId")

    @property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> str:
        return jsii.get(self, "dnsName")

    @property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> str:
        return jsii.get(self, "fullName")

    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        return jsii.get(self, "loadBalancerArn")

    @property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> str:
        return jsii.get(self, "loadBalancerName")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]:
        return jsii.get(self, "vpc")


class _BaseLoadBalancerProxy(BaseLoadBalancer):
    pass

class _BaseLoadBalancerProps(jsii.compat.TypedDict, total=False):
    deletionProtection: bool
    internetFacing: bool
    loadBalancerName: str
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancerProps")
class BaseLoadBalancerProps(_BaseLoadBalancerProps):
    vpc: aws_cdk.aws_ec2.IVpcNetwork

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerProps")
class ApplicationLoadBalancerProps(BaseLoadBalancerProps, jsii.compat.TypedDict, total=False):
    http2Enabled: bool
    idleTimeoutSecs: jsii.Number
    ipAddressType: "IpAddressType"
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup

class _BaseNetworkListenerProps(jsii.compat.TypedDict, total=False):
    defaultTargetGroups: typing.List["INetworkTargetGroup"]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseNetworkListenerProps")
class BaseNetworkListenerProps(_BaseNetworkListenerProps):
    port: jsii.Number

class _BaseTargetGroupProps(jsii.compat.TypedDict, total=False):
    deregistrationDelaySec: jsii.Number
    healthCheck: "HealthCheck"
    targetGroupName: str
    targetType: "TargetType"

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseTargetGroupProps")
class BaseTargetGroupProps(_BaseTargetGroupProps):
    vpc: aws_cdk.aws_ec2.IVpcNetwork

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationTargetGroupProps")
class ApplicationTargetGroupProps(BaseTargetGroupProps, jsii.compat.TypedDict, total=False):
    port: jsii.Number
    protocol: "ApplicationProtocol"
    slowStartSec: jsii.Number
    stickinessCookieDurationSec: jsii.Number
    targets: typing.List["IApplicationLoadBalancerTarget"]

class CfnListener(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, default_actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ActionProperty", aws_cdk.cdk.Token]]], load_balancer_arn: str, port: typing.Union[jsii.Number, aws_cdk.cdk.Token], protocol: str, certificates: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CertificateProperty"]]]]=None, ssl_policy: typing.Optional[str]=None) -> None:
        props: CfnListenerProps = {"defaultActions": default_actions, "loadBalancerArn": load_balancer_arn, "port": port, "protocol": protocol}

        if certificates is not None:
            props["certificates"] = certificates

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        jsii.create(CfnListener, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        return jsii.get(self, "listenerArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnListenerProps":
        return jsii.get(self, "propertyOverrides")

    class _ActionProperty(jsii.compat.TypedDict, total=False):
        authenticateCognitoConfig: typing.Union[aws_cdk.cdk.Token, "CfnListener.AuthenticateCognitoConfigProperty"]
        authenticateOidcConfig: typing.Union[aws_cdk.cdk.Token, "CfnListener.AuthenticateOidcConfigProperty"]
        fixedResponseConfig: typing.Union[aws_cdk.cdk.Token, "CfnListener.FixedResponseConfigProperty"]
        order: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        redirectConfig: typing.Union[aws_cdk.cdk.Token, "CfnListener.RedirectConfigProperty"]
        targetGroupArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.ActionProperty")
    class ActionProperty(_ActionProperty):
        type: str

    class _AuthenticateCognitoConfigProperty(jsii.compat.TypedDict, total=False):
        authenticationRequestExtraParams: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        onUnauthenticatedRequest: str
        scope: str
        sessionCookieName: str
        sessionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.AuthenticateCognitoConfigProperty")
    class AuthenticateCognitoConfigProperty(_AuthenticateCognitoConfigProperty):
        userPoolArn: str
        userPoolClientId: str
        userPoolDomain: str

    class _AuthenticateOidcConfigProperty(jsii.compat.TypedDict, total=False):
        authenticationRequestExtraParams: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        onUnauthenticatedRequest: str
        scope: str
        sessionCookieName: str
        sessionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.AuthenticateOidcConfigProperty")
    class AuthenticateOidcConfigProperty(_AuthenticateOidcConfigProperty):
        authorizationEndpoint: str
        clientId: str
        clientSecret: str
        issuer: str
        tokenEndpoint: str
        userInfoEndpoint: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.CertificateProperty")
    class CertificateProperty(jsii.compat.TypedDict, total=False):
        certificateArn: str

    class _FixedResponseConfigProperty(jsii.compat.TypedDict, total=False):
        contentType: str
        messageBody: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.FixedResponseConfigProperty")
    class FixedResponseConfigProperty(_FixedResponseConfigProperty):
        statusCode: str

    class _RedirectConfigProperty(jsii.compat.TypedDict, total=False):
        host: str
        path: str
        port: str
        protocol: str
        query: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.RedirectConfigProperty")
    class RedirectConfigProperty(_RedirectConfigProperty):
        statusCode: str


class CfnListenerCertificate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, certificates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CertificateProperty"]]], listener_arn: str) -> None:
        props: CfnListenerCertificateProps = {"certificates": certificates, "listenerArn": listener_arn}

        jsii.create(CfnListenerCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="listenerCertificateArn")
    def listener_certificate_arn(self) -> str:
        return jsii.get(self, "listenerCertificateArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnListenerCertificateProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificate.CertificateProperty")
    class CertificateProperty(jsii.compat.TypedDict, total=False):
        certificateArn: str


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificateProps")
class CfnListenerCertificateProps(jsii.compat.TypedDict):
    certificates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnListenerCertificate.CertificateProperty"]]]
    listenerArn: str

class _CfnListenerProps(jsii.compat.TypedDict, total=False):
    certificates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnListener.CertificateProperty"]]]
    sslPolicy: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerProps")
class CfnListenerProps(_CfnListenerProps):
    defaultActions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnListener.ActionProperty", aws_cdk.cdk.Token]]]
    loadBalancerArn: str
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    protocol: str

class CfnListenerRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ActionProperty"]]], conditions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "RuleConditionProperty"]]], listener_arn: str, priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]) -> None:
        props: CfnListenerRuleProps = {"actions": actions, "conditions": conditions, "listenerArn": listener_arn, "priority": priority}

        jsii.create(CfnListenerRule, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="listenerRuleArn")
    def listener_rule_arn(self) -> str:
        return jsii.get(self, "listenerRuleArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnListenerRuleProps":
        return jsii.get(self, "propertyOverrides")

    class _ActionProperty(jsii.compat.TypedDict, total=False):
        authenticateCognitoConfig: typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.AuthenticateCognitoConfigProperty"]
        authenticateOidcConfig: typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.AuthenticateOidcConfigProperty"]
        fixedResponseConfig: typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.FixedResponseConfigProperty"]
        order: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        redirectConfig: typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.RedirectConfigProperty"]
        targetGroupArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.ActionProperty")
    class ActionProperty(_ActionProperty):
        type: str

    class _AuthenticateCognitoConfigProperty(jsii.compat.TypedDict, total=False):
        authenticationRequestExtraParams: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        onUnauthenticatedRequest: str
        scope: str
        sessionCookieName: str
        sessionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.AuthenticateCognitoConfigProperty")
    class AuthenticateCognitoConfigProperty(_AuthenticateCognitoConfigProperty):
        userPoolArn: str
        userPoolClientId: str
        userPoolDomain: str

    class _AuthenticateOidcConfigProperty(jsii.compat.TypedDict, total=False):
        authenticationRequestExtraParams: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        onUnauthenticatedRequest: str
        scope: str
        sessionCookieName: str
        sessionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.AuthenticateOidcConfigProperty")
    class AuthenticateOidcConfigProperty(_AuthenticateOidcConfigProperty):
        authorizationEndpoint: str
        clientId: str
        clientSecret: str
        issuer: str
        tokenEndpoint: str
        userInfoEndpoint: str

    class _FixedResponseConfigProperty(jsii.compat.TypedDict, total=False):
        contentType: str
        messageBody: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.FixedResponseConfigProperty")
    class FixedResponseConfigProperty(_FixedResponseConfigProperty):
        statusCode: str

    class _RedirectConfigProperty(jsii.compat.TypedDict, total=False):
        host: str
        path: str
        port: str
        protocol: str
        query: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.RedirectConfigProperty")
    class RedirectConfigProperty(_RedirectConfigProperty):
        statusCode: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.RuleConditionProperty")
    class RuleConditionProperty(jsii.compat.TypedDict, total=False):
        field: str
        values: typing.List[str]


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRuleProps")
class CfnListenerRuleProps(jsii.compat.TypedDict):
    actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.ActionProperty"]]]
    conditions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.RuleConditionProperty"]]]
    listenerArn: str
    priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]

class CfnLoadBalancer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ip_address_type: typing.Optional[str]=None, load_balancer_attributes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "LoadBalancerAttributeProperty"]]]]=None, name: typing.Optional[str]=None, scheme: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, subnet_mappings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SubnetMappingProperty"]]]]=None, subnets: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, type: typing.Optional[str]=None) -> None:
        props: CfnLoadBalancerProps = {}

        if ip_address_type is not None:
            props["ipAddressType"] = ip_address_type

        if load_balancer_attributes is not None:
            props["loadBalancerAttributes"] = load_balancer_attributes

        if name is not None:
            props["name"] = name

        if scheme is not None:
            props["scheme"] = scheme

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if subnet_mappings is not None:
            props["subnetMappings"] = subnet_mappings

        if subnets is not None:
            props["subnets"] = subnets

        if tags is not None:
            props["tags"] = tags

        if type is not None:
            props["type"] = type

        jsii.create(CfnLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        return jsii.get(self, "loadBalancerArn")

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> str:
        return jsii.get(self, "loadBalancerCanonicalHostedZoneId")

    @property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        return jsii.get(self, "loadBalancerDnsName")

    @property
    @jsii.member(jsii_name="loadBalancerFullName")
    def load_balancer_full_name(self) -> str:
        return jsii.get(self, "loadBalancerFullName")

    @property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> str:
        return jsii.get(self, "loadBalancerName")

    @property
    @jsii.member(jsii_name="loadBalancerSecurityGroups")
    def load_balancer_security_groups(self) -> typing.List[str]:
        return jsii.get(self, "loadBalancerSecurityGroups")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLoadBalancerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer.LoadBalancerAttributeProperty")
    class LoadBalancerAttributeProperty(jsii.compat.TypedDict, total=False):
        key: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer.SubnetMappingProperty")
    class SubnetMappingProperty(jsii.compat.TypedDict):
        allocationId: str
        subnetId: str


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancerProps")
class CfnLoadBalancerProps(jsii.compat.TypedDict, total=False):
    ipAddressType: str
    loadBalancerAttributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.LoadBalancerAttributeProperty"]]]
    name: str
    scheme: str
    securityGroups: typing.List[str]
    subnetMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.SubnetMappingProperty"]]]
    subnets: typing.List[str]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    type: str

class CfnTargetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, health_check_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, health_check_interval_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, health_check_path: typing.Optional[str]=None, health_check_port: typing.Optional[str]=None, health_check_protocol: typing.Optional[str]=None, health_check_timeout_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, healthy_threshold_count: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, matcher: typing.Optional[typing.Union[aws_cdk.cdk.Token, "MatcherProperty"]]=None, name: typing.Optional[str]=None, port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, protocol: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, target_group_attributes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TargetGroupAttributeProperty"]]]]=None, targets: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TargetDescriptionProperty"]]]]=None, target_type: typing.Optional[str]=None, unhealthy_threshold_count: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, vpc_id: typing.Optional[str]=None) -> None:
        props: CfnTargetGroupProps = {}

        if health_check_enabled is not None:
            props["healthCheckEnabled"] = health_check_enabled

        if health_check_interval_seconds is not None:
            props["healthCheckIntervalSeconds"] = health_check_interval_seconds

        if health_check_path is not None:
            props["healthCheckPath"] = health_check_path

        if health_check_port is not None:
            props["healthCheckPort"] = health_check_port

        if health_check_protocol is not None:
            props["healthCheckProtocol"] = health_check_protocol

        if health_check_timeout_seconds is not None:
            props["healthCheckTimeoutSeconds"] = health_check_timeout_seconds

        if healthy_threshold_count is not None:
            props["healthyThresholdCount"] = healthy_threshold_count

        if matcher is not None:
            props["matcher"] = matcher

        if name is not None:
            props["name"] = name

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if tags is not None:
            props["tags"] = tags

        if target_group_attributes is not None:
            props["targetGroupAttributes"] = target_group_attributes

        if targets is not None:
            props["targets"] = targets

        if target_type is not None:
            props["targetType"] = target_type

        if unhealthy_threshold_count is not None:
            props["unhealthyThresholdCount"] = unhealthy_threshold_count

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(CfnTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTargetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        return jsii.get(self, "targetGroupArn")

    @property
    @jsii.member(jsii_name="targetGroupFullName")
    def target_group_full_name(self) -> str:
        return jsii.get(self, "targetGroupFullName")

    @property
    @jsii.member(jsii_name="targetGroupLoadBalancerArns")
    def target_group_load_balancer_arns(self) -> typing.List[str]:
        return jsii.get(self, "targetGroupLoadBalancerArns")

    @property
    @jsii.member(jsii_name="targetGroupName")
    def target_group_name(self) -> str:
        return jsii.get(self, "targetGroupName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.MatcherProperty")
    class MatcherProperty(jsii.compat.TypedDict):
        httpCode: str

    class _TargetDescriptionProperty(jsii.compat.TypedDict, total=False):
        availabilityZone: str
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.TargetDescriptionProperty")
    class TargetDescriptionProperty(_TargetDescriptionProperty):
        id: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.TargetGroupAttributeProperty")
    class TargetGroupAttributeProperty(jsii.compat.TypedDict, total=False):
        key: str
        value: str


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroupProps")
class CfnTargetGroupProps(jsii.compat.TypedDict, total=False):
    healthCheckEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    healthCheckIntervalSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    healthCheckPath: str
    healthCheckPort: str
    healthCheckProtocol: str
    healthCheckTimeoutSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    healthyThresholdCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    matcher: typing.Union[aws_cdk.cdk.Token, "CfnTargetGroup.MatcherProperty"]
    name: str
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    protocol: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    targetGroupAttributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTargetGroup.TargetGroupAttributeProperty"]]]
    targets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTargetGroup.TargetDescriptionProperty"]]]
    targetType: str
    unhealthyThresholdCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    vpcId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HealthCheck")
class HealthCheck(jsii.compat.TypedDict, total=False):
    healthyHttpCodes: str
    healthyThresholdCount: jsii.Number
    intervalSecs: jsii.Number
    path: str
    port: str
    protocol: "Protocol"
    timeoutSeconds: jsii.Number
    unhealthyThresholdCount: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HttpCodeElb")
class HttpCodeElb(enum.Enum):
    Elb3xxCount = "Elb3xxCount"
    Elb4xxCount = "Elb4xxCount"
    Elb5xxCount = "Elb5xxCount"

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HttpCodeTarget")
class HttpCodeTarget(enum.Enum):
    Target2xxCount = "Target2xxCount"
    Target3xxCount = "Target3xxCount"
    Target4xxCount = "Target4xxCount"
    Target5xxCount = "Target5xxCount"

@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationListener")
class IApplicationListener(aws_cdk.cdk.IConstruct, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IApplicationListenerProxy

    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        ...

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, id: str, arns: typing.List[str]) -> None:
        ...

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        ...

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start_sec: typing.Optional[jsii.Number]=None, stickiness_cookie_duration_sec: typing.Optional[jsii.Number]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ApplicationListenerImportProps":
        ...

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.IPortRange) -> None:
        ...


class _IApplicationListenerProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationListener"
    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        return jsii.get(self, "listenerArn")

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, id: str, arns: typing.List[str]) -> None:
        return jsii.invoke(self, "addCertificateArns", [id, arns])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        props: AddApplicationTargetGroupsProps = {"targetGroups": target_groups}

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        return jsii.invoke(self, "addTargetGroups", [id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start_sec: typing.Optional[jsii.Number]=None, stickiness_cookie_duration_sec: typing.Optional[jsii.Number]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        props: AddApplicationTargetsProps = {}

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if slow_start_sec is not None:
            props["slowStartSec"] = slow_start_sec

        if stickiness_cookie_duration_sec is not None:
            props["stickinessCookieDurationSec"] = stickiness_cookie_duration_sec

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if targets is not None:
            props["targets"] = targets

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "ApplicationListenerImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.IPortRange) -> None:
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])


@jsii.implements(IApplicationListener)
class ApplicationListener(BaseListener, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListener"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, load_balancer: "IApplicationLoadBalancer", certificate_arns: typing.Optional[typing.List[str]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> None:
        props: ApplicationListenerProps = {"loadBalancer": load_balancer}

        if certificate_arns is not None:
            props["certificateArns"] = certificate_arns

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if open is not None:
            props["open"] = open

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        jsii.create(ApplicationListener, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, listener_arn: str, security_group_id: str, default_port: typing.Optional[str]=None) -> "IApplicationListener":
        props: ApplicationListenerImportProps = {"listenerArn": listener_arn, "securityGroupId": security_group_id}

        if default_port is not None:
            props["defaultPort"] = default_port

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, _id: str, arns: typing.List[str]) -> None:
        return jsii.invoke(self, "addCertificateArns", [_id, arns])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        props: AddApplicationTargetGroupsProps = {"targetGroups": target_groups}

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        return jsii.invoke(self, "addTargetGroups", [id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start_sec: typing.Optional[jsii.Number]=None, stickiness_cookie_duration_sec: typing.Optional[jsii.Number]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        props: AddApplicationTargetsProps = {}

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if slow_start_sec is not None:
            props["slowStartSec"] = slow_start_sec

        if stickiness_cookie_duration_sec is not None:
            props["stickinessCookieDurationSec"] = stickiness_cookie_duration_sec

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if targets is not None:
            props["targets"] = targets

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "ApplicationListenerImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.IPortRange) -> None:
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "IApplicationLoadBalancer":
        return jsii.get(self, "loadBalancer")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancer")
class IApplicationLoadBalancer(aws_cdk.cdk.IConstruct, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IApplicationLoadBalancerProxy

    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]:
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ApplicationLoadBalancerImportProps":
        ...


class _IApplicationLoadBalancerProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancer"
    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        return jsii.get(self, "loadBalancerArn")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]:
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        props: BaseApplicationListenerProps = {}

        if certificate_arns is not None:
            props["certificateArns"] = certificate_arns

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if open is not None:
            props["open"] = open

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "ApplicationLoadBalancerImportProps":
        return jsii.invoke(self, "export", [])


@jsii.implements(IApplicationLoadBalancer)
class ApplicationLoadBalancer(BaseLoadBalancer, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, http2_enabled: typing.Optional[bool]=None, idle_timeout_secs: typing.Optional[jsii.Number]=None, ip_address_type: typing.Optional["IpAddressType"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc: aws_cdk.aws_ec2.IVpcNetwork, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        props: ApplicationLoadBalancerProps = {"vpc": vpc}

        if http2_enabled is not None:
            props["http2Enabled"] = http2_enabled

        if idle_timeout_secs is not None:
            props["idleTimeoutSecs"] = idle_timeout_secs

        if ip_address_type is not None:
            props["ipAddressType"] = ip_address_type

        if security_group is not None:
            props["securityGroup"] = security_group

        if deletion_protection is not None:
            props["deletionProtection"] = deletion_protection

        if internet_facing is not None:
            props["internetFacing"] = internet_facing

        if load_balancer_name is not None:
            props["loadBalancerName"] = load_balancer_name

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(ApplicationLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, load_balancer_arn: str, security_group_id: str) -> "IApplicationLoadBalancer":
        props: ApplicationLoadBalancerImportProps = {"loadBalancerArn": load_balancer_arn, "securityGroupId": security_group_id}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        props: BaseApplicationListenerProps = {}

        if certificate_arns is not None:
            props["certificateArns"] = certificate_arns

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if open is not None:
            props["open"] = open

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "ApplicationLoadBalancerImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="logAccessLogs")
    def log_access_logs(self, bucket: aws_cdk.aws_s3.IBucket, prefix: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "logAccessLogs", [bucket, prefix])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricActiveConnectionCount")
    def metric_active_connection_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricActiveConnectionCount", [props])

    @jsii.member(jsii_name="metricClientTlsNegotiationErrorCount")
    def metric_client_tls_negotiation_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricClientTlsNegotiationErrorCount", [props])

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricConsumedLCUs", [props])

    @jsii.member(jsii_name="metricElbAuthError")
    def metric_elb_auth_error(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricElbAuthError", [props])

    @jsii.member(jsii_name="metricElbAuthFailure")
    def metric_elb_auth_failure(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricElbAuthFailure", [props])

    @jsii.member(jsii_name="metricElbAuthLatency")
    def metric_elb_auth_latency(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricElbAuthLatency", [props])

    @jsii.member(jsii_name="metricElbAuthSuccess")
    def metric_elb_auth_success(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricElbAuthSuccess", [props])

    @jsii.member(jsii_name="metricHttpCodeElb")
    def metric_http_code_elb(self, code: "HttpCodeElb", *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpCodeElb", [code, props])

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(self, code: "HttpCodeTarget", *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpCodeTarget", [code, props])

    @jsii.member(jsii_name="metricHttpFixedResponseCount")
    def metric_http_fixed_response_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpFixedResponseCount", [props])

    @jsii.member(jsii_name="metricHttpRedirectCount")
    def metric_http_redirect_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpRedirectCount", [props])

    @jsii.member(jsii_name="metricHttpRedirectUrlLimitExceededCount")
    def metric_http_redirect_url_limit_exceeded_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpRedirectUrlLimitExceededCount", [props])

    @jsii.member(jsii_name="metricIPv6ProcessedBytes")
    def metric_i_pv6_processed_bytes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricIPv6ProcessedBytes", [props])

    @jsii.member(jsii_name="metricIPv6RequestCount")
    def metric_i_pv6_request_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricIPv6RequestCount", [props])

    @jsii.member(jsii_name="metricNewConnectionCount")
    def metric_new_connection_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricNewConnectionCount", [props])

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricProcessedBytes", [props])

    @jsii.member(jsii_name="metricRejectedConnectionCount")
    def metric_rejected_connection_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRejectedConnectionCount", [props])

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRequestCount", [props])

    @jsii.member(jsii_name="metricRuleEvaluations")
    def metric_rule_evaluations(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRuleEvaluations", [props])

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetConnectionErrorCount", [props])

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetResponseTime", [props])

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancerTarget")
class IApplicationLoadBalancerTarget(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IApplicationLoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "ApplicationTargetGroup") -> "LoadBalancerTargetProps":
        ...


class _IApplicationLoadBalancerTargetProxy():
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancerTarget"
    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "ApplicationTargetGroup") -> "LoadBalancerTargetProps":
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkListener")
class INetworkListener(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkListenerProxy

    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "NetworkListenerImportProps":
        ...


class _INetworkListenerProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkListener"
    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        return jsii.get(self, "listenerArn")

    @jsii.member(jsii_name="export")
    def export(self) -> "NetworkListenerImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancer")
class INetworkLoadBalancer(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkLoadBalancerProxy

    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]:
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None) -> "NetworkListener":
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "NetworkLoadBalancerImportProps":
        ...


class _INetworkLoadBalancerProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancer"
    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        return jsii.get(self, "loadBalancerArn")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]:
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None) -> "NetworkListener":
        props: BaseNetworkListenerProps = {"port": port}

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "NetworkLoadBalancerImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancerTarget")
class INetworkLoadBalancerTarget(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkLoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "NetworkTargetGroup") -> "LoadBalancerTargetProps":
        ...


class _INetworkLoadBalancerTargetProxy():
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancerTarget"
    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "NetworkTargetGroup") -> "LoadBalancerTargetProps":
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ITargetGroup")
class ITargetGroup(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ITargetGroupProxy

    @property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.cdk.IDependable:
        ...

    @property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "TargetGroupImportProps":
        ...


class _ITargetGroupProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.ITargetGroup"
    @property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        return jsii.get(self, "loadBalancerArns")

    @property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.cdk.IDependable:
        return jsii.get(self, "loadBalancerAttached")

    @property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        return jsii.get(self, "targetGroupArn")

    @jsii.member(jsii_name="export")
    def export(self) -> "TargetGroupImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationTargetGroup")
class IApplicationTargetGroup(ITargetGroup, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IApplicationTargetGroupProxy

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.cdk.IConstruct]=None) -> None:
        ...


class _IApplicationTargetGroupProxy(jsii.proxy_for(ITargetGroup)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationTargetGroup"
    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.cdk.IConstruct]=None) -> None:
        return jsii.invoke(self, "registerListener", [listener, associating_construct])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkTargetGroup")
class INetworkTargetGroup(ITargetGroup, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkTargetGroupProxy

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        ...


class _INetworkTargetGroupProxy(jsii.proxy_for(ITargetGroup)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkTargetGroup"
    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        return jsii.invoke(self, "registerListener", [listener])


@jsii.implements(IApplicationLoadBalancerTarget, INetworkLoadBalancerTarget)
class InstanceTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.InstanceTarget"):
    def __init__(self, instance_id: str, port: typing.Optional[jsii.Number]=None) -> None:
        jsii.create(InstanceTarget, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "ApplicationTargetGroup") -> "LoadBalancerTargetProps":
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "NetworkTargetGroup") -> "LoadBalancerTargetProps":
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "port")


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IpAddressType")
class IpAddressType(enum.Enum):
    Ipv4 = "Ipv4"
    DualStack = "DualStack"

@jsii.implements(IApplicationLoadBalancerTarget, INetworkLoadBalancerTarget)
class IpTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IpTarget"):
    def __init__(self, ip_address: str, port: typing.Optional[jsii.Number]=None, availability_zone: typing.Optional[str]=None) -> None:
        jsii.create(IpTarget, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "ApplicationTargetGroup") -> "LoadBalancerTargetProps":
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "NetworkTargetGroup") -> "LoadBalancerTargetProps":
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> str:
        return jsii.get(self, "ipAddress")

    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[str]:
        return jsii.get(self, "availabilityZone")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "port")


class _LoadBalancerTargetProps(jsii.compat.TypedDict, total=False):
    targetJson: typing.Any

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.LoadBalancerTargetProps")
class LoadBalancerTargetProps(_LoadBalancerTargetProps):
    targetType: "TargetType"

@jsii.implements(INetworkListener)
class NetworkListener(BaseListener, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListener"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, load_balancer: "INetworkLoadBalancer", port: jsii.Number, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None) -> None:
        props: NetworkListenerProps = {"loadBalancer": load_balancer, "port": port}

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        jsii.create(NetworkListener, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, listener_arn: str) -> "INetworkListener":
        props: NetworkListenerImportProps = {"listenerArn": listener_arn}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, _id: str, *target_groups: "INetworkTargetGroup") -> None:
        return jsii.invoke(self, "addTargetGroups", [_id, target_groups])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, port: jsii.Number, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, proxy_protocol_v2: typing.Optional[bool]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]]=None) -> "NetworkTargetGroup":
        props: AddNetworkTargetsProps = {"port": port}

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if proxy_protocol_v2 is not None:
            props["proxyProtocolV2"] = proxy_protocol_v2

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if targets is not None:
            props["targets"] = targets

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "NetworkListenerImportProps":
        return jsii.invoke(self, "export", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListenerImportProps")
class NetworkListenerImportProps(jsii.compat.TypedDict):
    listenerArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListenerProps")
class NetworkListenerProps(BaseNetworkListenerProps, jsii.compat.TypedDict):
    loadBalancer: "INetworkLoadBalancer"

@jsii.implements(INetworkLoadBalancer)
class NetworkLoadBalancer(BaseLoadBalancer, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cross_zone_enabled: typing.Optional[bool]=None, vpc: aws_cdk.aws_ec2.IVpcNetwork, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        props: NetworkLoadBalancerProps = {"vpc": vpc}

        if cross_zone_enabled is not None:
            props["crossZoneEnabled"] = cross_zone_enabled

        if deletion_protection is not None:
            props["deletionProtection"] = deletion_protection

        if internet_facing is not None:
            props["internetFacing"] = internet_facing

        if load_balancer_name is not None:
            props["loadBalancerName"] = load_balancer_name

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(NetworkLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, load_balancer_arn: str) -> "INetworkLoadBalancer":
        props: NetworkLoadBalancerImportProps = {"loadBalancerArn": load_balancer_arn}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None) -> "NetworkListener":
        props: BaseNetworkListenerProps = {"port": port}

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "NetworkLoadBalancerImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricActiveFlowCount")
    def metric_active_flow_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricActiveFlowCount", [props])

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricConsumedLCUs", [props])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricNewFlowCount")
    def metric_new_flow_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricNewFlowCount", [props])

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricProcessedBytes", [props])

    @jsii.member(jsii_name="metricTcpClientResetCount")
    def metric_tcp_client_reset_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTcpClientResetCount", [props])

    @jsii.member(jsii_name="metricTcpElbResetCount")
    def metric_tcp_elb_reset_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTcpElbResetCount", [props])

    @jsii.member(jsii_name="metricTcpTargetResetCount")
    def metric_tcp_target_reset_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTcpTargetResetCount", [props])

    @jsii.member(jsii_name="metricUnHealthyHostCount")
    def metric_un_healthy_host_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricUnHealthyHostCount", [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerImportProps")
class NetworkLoadBalancerImportProps(jsii.compat.TypedDict):
    loadBalancerArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerProps")
class NetworkLoadBalancerProps(BaseLoadBalancerProps, jsii.compat.TypedDict, total=False):
    crossZoneEnabled: bool

class _NetworkTargetGroupProps(BaseTargetGroupProps, jsii.compat.TypedDict, total=False):
    proxyProtocolV2: bool
    targets: typing.List["INetworkLoadBalancerTarget"]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkTargetGroupProps")
class NetworkTargetGroupProps(_NetworkTargetGroupProps):
    port: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.Protocol")
class Protocol(enum.Enum):
    Http = "Http"
    Https = "Https"
    Tcp = "Tcp"

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.SslPolicy")
class SslPolicy(enum.Enum):
    Recommended = "Recommended"
    ForwardSecrecy = "ForwardSecrecy"
    TLS12 = "TLS12"
    TLS12Ext = "TLS12Ext"
    TLS11 = "TLS11"
    Legacy = "Legacy"

@jsii.implements(ITargetGroup, aws_cdk.aws_codedeploy_api.ILoadBalancer)
class TargetGroupBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _TargetGroupBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, base_props: "BaseTargetGroupProps", additional_props: typing.Any) -> None:
        jsii.create(TargetGroupBase, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="addLoadBalancerTarget")
    def _add_load_balancer_target(self, *, target_type: "TargetType", target_json: typing.Any=None) -> None:
        props: LoadBalancerTargetProps = {"targetType": target_type}

        if target_json is not None:
            props["targetJson"] = target_json

        return jsii.invoke(self, "addLoadBalancerTarget", [props])

    @jsii.member(jsii_name="asCodeDeployLoadBalancer")
    def as_code_deploy_load_balancer(self) -> aws_cdk.aws_codedeploy_api.ILoadBalancerProps:
        return jsii.invoke(self, "asCodeDeployLoadBalancer", [])

    @jsii.member(jsii_name="configureHealthCheck")
    def configure_health_check(self, *, healthy_http_codes: typing.Optional[str]=None, healthy_threshold_count: typing.Optional[jsii.Number]=None, interval_secs: typing.Optional[jsii.Number]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional["Protocol"]=None, timeout_seconds: typing.Optional[jsii.Number]=None, unhealthy_threshold_count: typing.Optional[jsii.Number]=None) -> None:
        health_check: HealthCheck = {}

        if healthy_http_codes is not None:
            health_check["healthyHttpCodes"] = healthy_http_codes

        if healthy_threshold_count is not None:
            health_check["healthyThresholdCount"] = healthy_threshold_count

        if interval_secs is not None:
            health_check["intervalSecs"] = interval_secs

        if path is not None:
            health_check["path"] = path

        if port is not None:
            health_check["port"] = port

        if protocol is not None:
            health_check["protocol"] = protocol

        if timeout_seconds is not None:
            health_check["timeoutSeconds"] = timeout_seconds

        if unhealthy_threshold_count is not None:
            health_check["unhealthyThresholdCount"] = unhealthy_threshold_count

        return jsii.invoke(self, "configureHealthCheck", [health_check])

    @jsii.member(jsii_name="export")
    def export(self) -> "TargetGroupImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: str, value: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "setAttribute", [key, value])

    @property
    @jsii.member(jsii_name="defaultPort")
    def _default_port(self) -> str:
        return jsii.get(self, "defaultPort")

    @property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    @abc.abstractmethod
    def first_load_balancer_full_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        return jsii.get(self, "loadBalancerArns")

    @property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.cdk.IDependable:
        return jsii.get(self, "loadBalancerAttached")

    @property
    @jsii.member(jsii_name="loadBalancerAttachedDependencies")
    def _load_balancer_attached_dependencies(self) -> aws_cdk.cdk.ConcreteDependable:
        return jsii.get(self, "loadBalancerAttachedDependencies")

    @property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        return jsii.get(self, "targetGroupArn")

    @property
    @jsii.member(jsii_name="targetGroupFullName")
    def target_group_full_name(self) -> str:
        return jsii.get(self, "targetGroupFullName")

    @property
    @jsii.member(jsii_name="targetGroupLoadBalancerArns")
    def target_group_load_balancer_arns(self) -> typing.List[str]:
        return jsii.get(self, "targetGroupLoadBalancerArns")

    @property
    @jsii.member(jsii_name="targetGroupName")
    def target_group_name(self) -> str:
        return jsii.get(self, "targetGroupName")

    @property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> "HealthCheck":
        return jsii.get(self, "healthCheck")

    @health_check.setter
    def health_check(self, value: "HealthCheck"):
        return jsii.set(self, "healthCheck", value)


class _TargetGroupBaseProxy(TargetGroupBase):
    @property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.implements(IApplicationTargetGroup)
class ApplicationTargetGroup(TargetGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationTargetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start_sec: typing.Optional[jsii.Number]=None, stickiness_cookie_duration_sec: typing.Optional[jsii.Number]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, vpc: aws_cdk.aws_ec2.IVpcNetwork, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None) -> None:
        props: ApplicationTargetGroupProps = {"vpc": vpc}

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if slow_start_sec is not None:
            props["slowStartSec"] = slow_start_sec

        if stickiness_cookie_duration_sec is not None:
            props["stickinessCookieDurationSec"] = stickiness_cookie_duration_sec

        if targets is not None:
            props["targets"] = targets

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if target_type is not None:
            props["targetType"] = target_type

        jsii.create(ApplicationTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, default_port: str, target_group_arn: str, load_balancer_arns: typing.Optional[str]=None) -> "IApplicationTargetGroup":
        props: TargetGroupImportProps = {"defaultPort": default_port, "targetGroupArn": target_group_arn}

        if load_balancer_arns is not None:
            props["loadBalancerArns"] = load_balancer_arns

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "IApplicationLoadBalancerTarget") -> None:
        return jsii.invoke(self, "addTarget", [targets])

    @jsii.member(jsii_name="enableCookieStickiness")
    def enable_cookie_stickiness(self, duration_sec: jsii.Number) -> None:
        return jsii.invoke(self, "enableCookieStickiness", [duration_sec])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(self, code: "HttpCodeTarget", *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpCodeTarget", [code, props])

    @jsii.member(jsii_name="metricIPv6RequestCount")
    def metric_i_pv6_request_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricIPv6RequestCount", [props])

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRequestCount", [props])

    @jsii.member(jsii_name="metricRequestCountPerTarget")
    def metric_request_count_per_target(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRequestCountPerTarget", [props])

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetConnectionErrorCount", [props])

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetResponseTime", [props])

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props])

    @jsii.member(jsii_name="metricUnhealthyHostCount")
    def metric_unhealthy_host_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        props: aws_cdk.aws_cloudwatch.MetricCustomization = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricUnhealthyHostCount", [props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: typing.Optional[aws_cdk.aws_ec2.IPortRange]=None) -> None:
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.cdk.IConstruct]=None) -> None:
        return jsii.invoke(self, "registerListener", [listener, associating_construct])

    @property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.implements(INetworkTargetGroup)
class NetworkTargetGroup(TargetGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkTargetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, port: jsii.Number, proxy_protocol_v2: typing.Optional[bool]=None, targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]]=None, vpc: aws_cdk.aws_ec2.IVpcNetwork, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None) -> None:
        props: NetworkTargetGroupProps = {"port": port, "vpc": vpc}

        if proxy_protocol_v2 is not None:
            props["proxyProtocolV2"] = proxy_protocol_v2

        if targets is not None:
            props["targets"] = targets

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if target_type is not None:
            props["targetType"] = target_type

        jsii.create(NetworkTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, default_port: str, target_group_arn: str, load_balancer_arns: typing.Optional[str]=None) -> "INetworkTargetGroup":
        props: TargetGroupImportProps = {"defaultPort": default_port, "targetGroupArn": target_group_arn}

        if load_balancer_arns is not None:
            props["loadBalancerArns"] = load_balancer_arns

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "INetworkLoadBalancerTarget") -> None:
        return jsii.invoke(self, "addTarget", [targets])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        return jsii.invoke(self, "registerListener", [listener])

    @property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        return jsii.get(self, "firstLoadBalancerFullName")


class _TargetGroupImportProps(jsii.compat.TypedDict, total=False):
    loadBalancerArns: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupImportProps")
class TargetGroupImportProps(_TargetGroupImportProps):
    defaultPort: str
    targetGroupArn: str

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetType")
class TargetType(enum.Enum):
    Instance = "Instance"
    Ip = "Ip"

__all__ = ["AddApplicationTargetGroupsProps", "AddApplicationTargetsProps", "AddNetworkTargetsProps", "AddRuleProps", "ApplicationListener", "ApplicationListenerCertificate", "ApplicationListenerCertificateProps", "ApplicationListenerImportProps", "ApplicationListenerProps", "ApplicationListenerRule", "ApplicationListenerRuleProps", "ApplicationLoadBalancer", "ApplicationLoadBalancerImportProps", "ApplicationLoadBalancerProps", "ApplicationProtocol", "ApplicationTargetGroup", "ApplicationTargetGroupProps", "BaseApplicationListenerProps", "BaseApplicationListenerRuleProps", "BaseListener", "BaseLoadBalancer", "BaseLoadBalancerProps", "BaseNetworkListenerProps", "BaseTargetGroupProps", "CfnListener", "CfnListenerCertificate", "CfnListenerCertificateProps", "CfnListenerProps", "CfnListenerRule", "CfnListenerRuleProps", "CfnLoadBalancer", "CfnLoadBalancerProps", "CfnTargetGroup", "CfnTargetGroupProps", "HealthCheck", "HttpCodeElb", "HttpCodeTarget", "IApplicationListener", "IApplicationLoadBalancer", "IApplicationLoadBalancerTarget", "IApplicationTargetGroup", "INetworkListener", "INetworkLoadBalancer", "INetworkLoadBalancerTarget", "INetworkTargetGroup", "ITargetGroup", "InstanceTarget", "IpAddressType", "IpTarget", "LoadBalancerTargetProps", "NetworkListener", "NetworkListenerImportProps", "NetworkListenerProps", "NetworkLoadBalancer", "NetworkLoadBalancerImportProps", "NetworkLoadBalancerProps", "NetworkTargetGroup", "NetworkTargetGroupProps", "Protocol", "SslPolicy", "TargetGroupBase", "TargetGroupImportProps", "TargetType", "__jsii_assembly__"]

publication.publish()
