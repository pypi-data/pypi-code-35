import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-route53resolver", "0.28.0", __name__, "aws-route53resolver@0.28.0.jsii.tgz")
class CfnResolverEndpoint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53resolver.CfnResolverEndpoint"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, direction: str, ip_addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["IpAddressRequestProperty", aws_cdk.cdk.Token]]], security_group_ids: typing.List[str], name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnResolverEndpointProps = {"direction": direction, "ipAddresses": ip_addresses, "securityGroupIds": security_group_ids}

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnResolverEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResolverEndpointProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resolverEndpointArn")
    def resolver_endpoint_arn(self) -> str:
        return jsii.get(self, "resolverEndpointArn")

    @property
    @jsii.member(jsii_name="resolverEndpointDirection")
    def resolver_endpoint_direction(self) -> str:
        return jsii.get(self, "resolverEndpointDirection")

    @property
    @jsii.member(jsii_name="resolverEndpointHostVpcId")
    def resolver_endpoint_host_vpc_id(self) -> str:
        return jsii.get(self, "resolverEndpointHostVpcId")

    @property
    @jsii.member(jsii_name="resolverEndpointId")
    def resolver_endpoint_id(self) -> str:
        return jsii.get(self, "resolverEndpointId")

    @property
    @jsii.member(jsii_name="resolverEndpointIpAddressCount")
    def resolver_endpoint_ip_address_count(self) -> str:
        return jsii.get(self, "resolverEndpointIpAddressCount")

    @property
    @jsii.member(jsii_name="resolverEndpointName")
    def resolver_endpoint_name(self) -> str:
        return jsii.get(self, "resolverEndpointName")

    @property
    @jsii.member(jsii_name="resolverEndpointObject")
    def resolver_endpoint_object(self) -> str:
        return jsii.get(self, "resolverEndpointObject")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _IpAddressRequestProperty(jsii.compat.TypedDict, total=False):
        ip: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53resolver.CfnResolverEndpoint.IpAddressRequestProperty")
    class IpAddressRequestProperty(_IpAddressRequestProperty):
        subnetId: str


class _CfnResolverEndpointProps(jsii.compat.TypedDict, total=False):
    name: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-route53resolver.CfnResolverEndpointProps")
class CfnResolverEndpointProps(_CfnResolverEndpointProps):
    direction: str
    ipAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", aws_cdk.cdk.Token]]]
    securityGroupIds: typing.List[str]

class CfnResolverRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain_name: str, rule_type: str, name: typing.Optional[str]=None, resolver_endpoint_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, target_ips: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TargetAddressProperty"]]]]=None) -> None:
        props: CfnResolverRuleProps = {"domainName": domain_name, "ruleType": rule_type}

        if name is not None:
            props["name"] = name

        if resolver_endpoint_id is not None:
            props["resolverEndpointId"] = resolver_endpoint_id

        if tags is not None:
            props["tags"] = tags

        if target_ips is not None:
            props["targetIps"] = target_ips

        jsii.create(CfnResolverRule, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResolverRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resolverRuleArn")
    def resolver_rule_arn(self) -> str:
        return jsii.get(self, "resolverRuleArn")

    @property
    @jsii.member(jsii_name="resolverRuleDomainName")
    def resolver_rule_domain_name(self) -> str:
        return jsii.get(self, "resolverRuleDomainName")

    @property
    @jsii.member(jsii_name="resolverRuleId")
    def resolver_rule_id(self) -> str:
        return jsii.get(self, "resolverRuleId")

    @property
    @jsii.member(jsii_name="resolverRuleName")
    def resolver_rule_name(self) -> str:
        return jsii.get(self, "resolverRuleName")

    @property
    @jsii.member(jsii_name="resolverRuleObject")
    def resolver_rule_object(self) -> str:
        return jsii.get(self, "resolverRuleObject")

    @property
    @jsii.member(jsii_name="resolverRuleResolverEndpointId")
    def resolver_rule_resolver_endpoint_id(self) -> str:
        return jsii.get(self, "resolverRuleResolverEndpointId")

    @property
    @jsii.member(jsii_name="resolverRuleTargetIps")
    def resolver_rule_target_ips(self) -> str:
        return jsii.get(self, "resolverRuleTargetIps")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRule.TargetAddressProperty")
    class TargetAddressProperty(jsii.compat.TypedDict):
        ip: str
        port: str


class CfnResolverRuleAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRuleAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resolver_rule_id: str, vpc_id: str, name: typing.Optional[str]=None) -> None:
        props: CfnResolverRuleAssociationProps = {"resolverRuleId": resolver_rule_id, "vpcId": vpc_id}

        if name is not None:
            props["name"] = name

        jsii.create(CfnResolverRuleAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnResolverRuleAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resolverRuleAssociationId")
    def resolver_rule_association_id(self) -> str:
        return jsii.get(self, "resolverRuleAssociationId")

    @property
    @jsii.member(jsii_name="resolverRuleAssociationName")
    def resolver_rule_association_name(self) -> str:
        return jsii.get(self, "resolverRuleAssociationName")

    @property
    @jsii.member(jsii_name="resolverRuleAssociationResolverRuleId")
    def resolver_rule_association_resolver_rule_id(self) -> str:
        return jsii.get(self, "resolverRuleAssociationResolverRuleId")

    @property
    @jsii.member(jsii_name="resolverRuleAssociationVpcId")
    def resolver_rule_association_vpc_id(self) -> str:
        return jsii.get(self, "resolverRuleAssociationVpcId")


class _CfnResolverRuleAssociationProps(jsii.compat.TypedDict, total=False):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRuleAssociationProps")
class CfnResolverRuleAssociationProps(_CfnResolverRuleAssociationProps):
    resolverRuleId: str
    vpcId: str

class _CfnResolverRuleProps(jsii.compat.TypedDict, total=False):
    name: str
    resolverEndpointId: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    targetIps: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnResolverRule.TargetAddressProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRuleProps")
class CfnResolverRuleProps(_CfnResolverRuleProps):
    domainName: str
    ruleType: str

__all__ = ["CfnResolverEndpoint", "CfnResolverEndpointProps", "CfnResolverRule", "CfnResolverRuleAssociation", "CfnResolverRuleAssociationProps", "CfnResolverRuleProps", "__jsii_assembly__"]

publication.publish()
