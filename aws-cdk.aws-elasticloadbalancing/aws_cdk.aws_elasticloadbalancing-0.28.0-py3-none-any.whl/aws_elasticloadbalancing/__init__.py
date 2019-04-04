import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_codedeploy_api
import aws_cdk.aws_ec2
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticloadbalancing", "0.28.0", __name__, "aws-elasticloadbalancing@0.28.0.jsii.tgz")
class CfnLoadBalancer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, listeners: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ListenersProperty", aws_cdk.cdk.Token]]], access_logging_policy: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AccessLoggingPolicyProperty"]]=None, app_cookie_stickiness_policy: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "AppCookieStickinessPolicyProperty"]]]]=None, availability_zones: typing.Optional[typing.List[str]]=None, connection_draining_policy: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ConnectionDrainingPolicyProperty"]]=None, connection_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ConnectionSettingsProperty"]]=None, cross_zone: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, health_check: typing.Optional[typing.Union[aws_cdk.cdk.Token, "HealthCheckProperty"]]=None, instances: typing.Optional[typing.List[str]]=None, lb_cookie_stickiness_policy: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "LBCookieStickinessPolicyProperty"]]]]=None, load_balancer_name: typing.Optional[str]=None, policies: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PoliciesProperty"]]]]=None, scheme: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, subnets: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnLoadBalancerProps = {"listeners": listeners}

        if access_logging_policy is not None:
            props["accessLoggingPolicy"] = access_logging_policy

        if app_cookie_stickiness_policy is not None:
            props["appCookieStickinessPolicy"] = app_cookie_stickiness_policy

        if availability_zones is not None:
            props["availabilityZones"] = availability_zones

        if connection_draining_policy is not None:
            props["connectionDrainingPolicy"] = connection_draining_policy

        if connection_settings is not None:
            props["connectionSettings"] = connection_settings

        if cross_zone is not None:
            props["crossZone"] = cross_zone

        if health_check is not None:
            props["healthCheck"] = health_check

        if instances is not None:
            props["instances"] = instances

        if lb_cookie_stickiness_policy is not None:
            props["lbCookieStickinessPolicy"] = lb_cookie_stickiness_policy

        if load_balancer_name is not None:
            props["loadBalancerName"] = load_balancer_name

        if policies is not None:
            props["policies"] = policies

        if scheme is not None:
            props["scheme"] = scheme

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if subnets is not None:
            props["subnets"] = subnets

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneName")
    def load_balancer_canonical_hosted_zone_name(self) -> str:
        return jsii.get(self, "loadBalancerCanonicalHostedZoneName")

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneNameId")
    def load_balancer_canonical_hosted_zone_name_id(self) -> str:
        return jsii.get(self, "loadBalancerCanonicalHostedZoneNameId")

    @property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        return jsii.get(self, "loadBalancerDnsName")

    @property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> str:
        return jsii.get(self, "loadBalancerName")

    @property
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupGroupName")
    def load_balancer_source_security_group_group_name(self) -> str:
        return jsii.get(self, "loadBalancerSourceSecurityGroupGroupName")

    @property
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupOwnerAlias")
    def load_balancer_source_security_group_owner_alias(self) -> str:
        return jsii.get(self, "loadBalancerSourceSecurityGroupOwnerAlias")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLoadBalancerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _AccessLoggingPolicyProperty(jsii.compat.TypedDict, total=False):
        emitInterval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        s3BucketPrefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.AccessLoggingPolicyProperty")
    class AccessLoggingPolicyProperty(_AccessLoggingPolicyProperty):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        s3BucketName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.AppCookieStickinessPolicyProperty")
    class AppCookieStickinessPolicyProperty(jsii.compat.TypedDict):
        cookieName: str
        policyName: str

    class _ConnectionDrainingPolicyProperty(jsii.compat.TypedDict, total=False):
        timeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ConnectionDrainingPolicyProperty")
    class ConnectionDrainingPolicyProperty(_ConnectionDrainingPolicyProperty):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ConnectionSettingsProperty")
    class ConnectionSettingsProperty(jsii.compat.TypedDict):
        idleTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.HealthCheckProperty")
    class HealthCheckProperty(jsii.compat.TypedDict):
        healthyThreshold: str
        interval: str
        target: str
        timeout: str
        unhealthyThreshold: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.LBCookieStickinessPolicyProperty")
    class LBCookieStickinessPolicyProperty(jsii.compat.TypedDict, total=False):
        cookieExpirationPeriod: str
        policyName: str

    class _ListenersProperty(jsii.compat.TypedDict, total=False):
        instanceProtocol: str
        policyNames: typing.List[str]
        sslCertificateId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ListenersProperty")
    class ListenersProperty(_ListenersProperty):
        instancePort: str
        loadBalancerPort: str
        protocol: str

    class _PoliciesProperty(jsii.compat.TypedDict, total=False):
        instancePorts: typing.List[str]
        loadBalancerPorts: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.PoliciesProperty")
    class PoliciesProperty(_PoliciesProperty):
        attributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]]
        policyName: str
        policyType: str


class _CfnLoadBalancerProps(jsii.compat.TypedDict, total=False):
    accessLoggingPolicy: typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.AccessLoggingPolicyProperty"]
    appCookieStickinessPolicy: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.AppCookieStickinessPolicyProperty"]]]
    availabilityZones: typing.List[str]
    connectionDrainingPolicy: typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.ConnectionDrainingPolicyProperty"]
    connectionSettings: typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.ConnectionSettingsProperty"]
    crossZone: typing.Union[bool, aws_cdk.cdk.Token]
    healthCheck: typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.HealthCheckProperty"]
    instances: typing.List[str]
    lbCookieStickinessPolicy: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.LBCookieStickinessPolicyProperty"]]]
    loadBalancerName: str
    policies: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.PoliciesProperty"]]]
    scheme: str
    securityGroups: typing.List[str]
    subnets: typing.List[str]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancerProps")
class CfnLoadBalancerProps(_CfnLoadBalancerProps):
    listeners: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", aws_cdk.cdk.Token]]]

class _HealthCheck(jsii.compat.TypedDict, total=False):
    healthyThreshold: jsii.Number
    interval: jsii.Number
    path: str
    protocol: "LoadBalancingProtocol"
    timeout: jsii.Number
    unhealthyThreshold: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.HealthCheck")
class HealthCheck(_HealthCheck):
    port: jsii.Number

@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancing.ILoadBalancerTarget")
class ILoadBalancerTarget(aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: "LoadBalancer") -> None:
        ...


class _ILoadBalancerTargetProxy(jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancing.ILoadBalancerTarget"
    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: "LoadBalancer") -> None:
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class ListenerPort(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancing.ListenerPort"):
    def __init__(self, security_group: aws_cdk.aws_ec2.ISecurityGroup, default_port_range: aws_cdk.aws_ec2.IPortRange) -> None:
        jsii.create(ListenerPort, self, [security_group, default_port_range])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")


@jsii.implements(aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_codedeploy_api.ILoadBalancer)
class LoadBalancer(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpcNetwork, health_check: typing.Optional["HealthCheck"]=None, internet_facing: typing.Optional[bool]=None, listeners: typing.Optional[typing.List["LoadBalancerListener"]]=None, targets: typing.Optional[typing.List["ILoadBalancerTarget"]]=None) -> None:
        props: LoadBalancerProps = {"vpc": vpc}

        if health_check is not None:
            props["healthCheck"] = health_check

        if internet_facing is not None:
            props["internetFacing"] = internet_facing

        if listeners is not None:
            props["listeners"] = listeners

        if targets is not None:
            props["targets"] = targets

        jsii.create(LoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="addListener")
    def add_listener(self, *, external_port: jsii.Number, allow_connections_from: typing.Optional[typing.List[aws_cdk.aws_ec2.IConnectable]]=None, external_protocol: typing.Optional["LoadBalancingProtocol"]=None, internal_port: typing.Optional[jsii.Number]=None, internal_protocol: typing.Optional["LoadBalancingProtocol"]=None, policy_names: typing.Optional[typing.List[str]]=None, ssl_certificate_id: typing.Optional[str]=None) -> "ListenerPort":
        listener: LoadBalancerListener = {"externalPort": external_port}

        if allow_connections_from is not None:
            listener["allowConnectionsFrom"] = allow_connections_from

        if external_protocol is not None:
            listener["externalProtocol"] = external_protocol

        if internal_port is not None:
            listener["internalPort"] = internal_port

        if internal_protocol is not None:
            listener["internalProtocol"] = internal_protocol

        if policy_names is not None:
            listener["policyNames"] = policy_names

        if ssl_certificate_id is not None:
            listener["sslCertificateId"] = ssl_certificate_id

        return jsii.invoke(self, "addListener", [listener])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: "ILoadBalancerTarget") -> None:
        return jsii.invoke(self, "addTarget", [target])

    @jsii.member(jsii_name="asCodeDeployLoadBalancer")
    def as_code_deploy_load_balancer(self) -> aws_cdk.aws_codedeploy_api.ILoadBalancerProps:
        return jsii.invoke(self, "asCodeDeployLoadBalancer", [])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="listenerPorts")
    def listener_ports(self) -> typing.List["ListenerPort"]:
        return jsii.get(self, "listenerPorts")

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneName")
    def load_balancer_canonical_hosted_zone_name(self) -> str:
        return jsii.get(self, "loadBalancerCanonicalHostedZoneName")

    @property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        return jsii.get(self, "loadBalancerDnsName")

    @property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> str:
        return jsii.get(self, "loadBalancerName")

    @property
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupGroupName")
    def load_balancer_source_security_group_group_name(self) -> str:
        return jsii.get(self, "loadBalancerSourceSecurityGroupGroupName")

    @property
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupOwnerAlias")
    def load_balancer_source_security_group_owner_alias(self) -> str:
        return jsii.get(self, "loadBalancerSourceSecurityGroupOwnerAlias")


class _LoadBalancerListener(jsii.compat.TypedDict, total=False):
    allowConnectionsFrom: typing.List[aws_cdk.aws_ec2.IConnectable]
    externalProtocol: "LoadBalancingProtocol"
    internalPort: jsii.Number
    internalProtocol: "LoadBalancingProtocol"
    policyNames: typing.List[str]
    sslCertificateId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancerListener")
class LoadBalancerListener(_LoadBalancerListener):
    externalPort: jsii.Number

class _LoadBalancerProps(jsii.compat.TypedDict, total=False):
    healthCheck: "HealthCheck"
    internetFacing: bool
    listeners: typing.List["LoadBalancerListener"]
    targets: typing.List["ILoadBalancerTarget"]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancerProps")
class LoadBalancerProps(_LoadBalancerProps):
    vpc: aws_cdk.aws_ec2.IVpcNetwork

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancingProtocol")
class LoadBalancingProtocol(enum.Enum):
    Tcp = "Tcp"
    Ssl = "Ssl"
    Http = "Http"
    Https = "Https"

__all__ = ["CfnLoadBalancer", "CfnLoadBalancerProps", "HealthCheck", "ILoadBalancerTarget", "ListenerPort", "LoadBalancer", "LoadBalancerListener", "LoadBalancerProps", "LoadBalancingProtocol", "__jsii_assembly__"]

publication.publish()
