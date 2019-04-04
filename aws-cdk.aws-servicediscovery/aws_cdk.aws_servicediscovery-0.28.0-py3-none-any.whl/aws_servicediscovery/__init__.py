import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_route53
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-servicediscovery", "0.28.0", __name__, "aws-servicediscovery@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.BaseInstanceProps")
class BaseInstanceProps(jsii.compat.TypedDict, total=False):
    customAttributes: typing.Mapping[str,str]
    instanceId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.AliasTargetInstanceProps")
class AliasTargetInstanceProps(BaseInstanceProps, jsii.compat.TypedDict):
    dnsName: str
    service: "IService"

class _BaseNamespaceProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.BaseNamespaceProps")
class BaseNamespaceProps(_BaseNamespaceProps):
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.BaseServiceProps")
class BaseServiceProps(jsii.compat.TypedDict, total=False):
    customHealthCheck: "HealthCheckCustomConfig"
    description: str
    healthCheck: "HealthCheckConfig"
    name: str

class CfnHttpNamespace(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnHttpNamespace"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, description: typing.Optional[str]=None) -> None:
        props: CfnHttpNamespaceProps = {"name": name}

        if description is not None:
            props["description"] = description

        jsii.create(CfnHttpNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="httpNamespaceArn")
    def http_namespace_arn(self) -> str:
        return jsii.get(self, "httpNamespaceArn")

    @property
    @jsii.member(jsii_name="httpNamespaceId")
    def http_namespace_id(self) -> str:
        return jsii.get(self, "httpNamespaceId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnHttpNamespaceProps":
        return jsii.get(self, "propertyOverrides")


class _CfnHttpNamespaceProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnHttpNamespaceProps")
class CfnHttpNamespaceProps(_CfnHttpNamespaceProps):
    name: str

class CfnInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_attributes: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], service_id: str, instance_id: typing.Optional[str]=None) -> None:
        props: CfnInstanceProps = {"instanceAttributes": instance_attributes, "serviceId": service_id}

        if instance_id is not None:
            props["instanceId"] = instance_id

        jsii.create(CfnInstance, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInstanceProps":
        return jsii.get(self, "propertyOverrides")


class _CfnInstanceProps(jsii.compat.TypedDict, total=False):
    instanceId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnInstanceProps")
class CfnInstanceProps(_CfnInstanceProps):
    instanceAttributes: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    serviceId: str

class CfnPrivateDnsNamespace(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespace"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, vpc: str, description: typing.Optional[str]=None) -> None:
        props: CfnPrivateDnsNamespaceProps = {"name": name, "vpc": vpc}

        if description is not None:
            props["description"] = description

        jsii.create(CfnPrivateDnsNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="privateDnsNamespaceArn")
    def private_dns_namespace_arn(self) -> str:
        return jsii.get(self, "privateDnsNamespaceArn")

    @property
    @jsii.member(jsii_name="privateDnsNamespaceId")
    def private_dns_namespace_id(self) -> str:
        return jsii.get(self, "privateDnsNamespaceId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPrivateDnsNamespaceProps":
        return jsii.get(self, "propertyOverrides")


class _CfnPrivateDnsNamespaceProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespaceProps")
class CfnPrivateDnsNamespaceProps(_CfnPrivateDnsNamespaceProps):
    name: str
    vpc: str

class CfnPublicDnsNamespace(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespace"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, description: typing.Optional[str]=None) -> None:
        props: CfnPublicDnsNamespaceProps = {"name": name}

        if description is not None:
            props["description"] = description

        jsii.create(CfnPublicDnsNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPublicDnsNamespaceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="publicDnsNamespaceArn")
    def public_dns_namespace_arn(self) -> str:
        return jsii.get(self, "publicDnsNamespaceArn")

    @property
    @jsii.member(jsii_name="publicDnsNamespaceId")
    def public_dns_namespace_id(self) -> str:
        return jsii.get(self, "publicDnsNamespaceId")


class _CfnPublicDnsNamespaceProps(jsii.compat.TypedDict, total=False):
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespaceProps")
class CfnPublicDnsNamespaceProps(_CfnPublicDnsNamespaceProps):
    name: str

class CfnService(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnService"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, dns_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DnsConfigProperty"]]=None, health_check_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "HealthCheckConfigProperty"]]=None, health_check_custom_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "HealthCheckCustomConfigProperty"]]=None, name: typing.Optional[str]=None, namespace_id: typing.Optional[str]=None) -> None:
        props: CfnServiceProps = {}

        if description is not None:
            props["description"] = description

        if dns_config is not None:
            props["dnsConfig"] = dns_config

        if health_check_config is not None:
            props["healthCheckConfig"] = health_check_config

        if health_check_custom_config is not None:
            props["healthCheckCustomConfig"] = health_check_custom_config

        if name is not None:
            props["name"] = name

        if namespace_id is not None:
            props["namespaceId"] = namespace_id

        jsii.create(CfnService, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnServiceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> str:
        return jsii.get(self, "serviceId")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        return jsii.get(self, "serviceName")

    class _DnsConfigProperty(jsii.compat.TypedDict, total=False):
        namespaceId: str
        routingPolicy: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnService.DnsConfigProperty")
    class DnsConfigProperty(_DnsConfigProperty):
        dnsRecords: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnService.DnsRecordProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnService.DnsRecordProperty")
    class DnsRecordProperty(jsii.compat.TypedDict):
        ttl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        type: str

    class _HealthCheckConfigProperty(jsii.compat.TypedDict, total=False):
        failureThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        resourcePath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnService.HealthCheckConfigProperty")
    class HealthCheckConfigProperty(_HealthCheckConfigProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnService.HealthCheckCustomConfigProperty")
    class HealthCheckCustomConfigProperty(jsii.compat.TypedDict, total=False):
        failureThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnServiceProps")
class CfnServiceProps(jsii.compat.TypedDict, total=False):
    description: str
    dnsConfig: typing.Union[aws_cdk.cdk.Token, "CfnService.DnsConfigProperty"]
    healthCheckConfig: typing.Union[aws_cdk.cdk.Token, "CfnService.HealthCheckConfigProperty"]
    healthCheckCustomConfig: typing.Union[aws_cdk.cdk.Token, "CfnService.HealthCheckCustomConfigProperty"]
    name: str
    namespaceId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CnameInstanceBaseProps")
class CnameInstanceBaseProps(BaseInstanceProps, jsii.compat.TypedDict):
    instanceCname: str

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CnameInstanceProps")
class CnameInstanceProps(CnameInstanceBaseProps, jsii.compat.TypedDict):
    service: "IService"

@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.DnsRecordType")
class DnsRecordType(enum.Enum):
    A = "A"
    AAAA = "AAAA"
    A_AAAA = "A_AAAA"
    SRV = "SRV"
    CNAME = "CNAME"

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.DnsServiceProps")
class DnsServiceProps(BaseServiceProps, jsii.compat.TypedDict, total=False):
    dnsRecordType: "DnsRecordType"
    dnsTtlSec: jsii.Number
    loadBalancer: bool
    routingPolicy: "RoutingPolicy"

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckConfig")
class HealthCheckConfig(jsii.compat.TypedDict, total=False):
    failureThreshold: jsii.Number
    resourcePath: str
    type: "HealthCheckType"

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckCustomConfig")
class HealthCheckCustomConfig(jsii.compat.TypedDict, total=False):
    failureThreshold: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckType")
class HealthCheckType(enum.Enum):
    Http = "Http"
    Https = "Https"
    Tcp = "Tcp"

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.HttpNamespaceProps")
class HttpNamespaceProps(BaseNamespaceProps, jsii.compat.TypedDict):
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IInstance")
class IInstance(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IInstanceProxy

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        ...


class _IInstanceProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.IInstance"
    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        return jsii.get(self, "service")


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.INamespace")
class INamespace(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _INamespaceProxy

    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "NamespaceImportProps":
        ...


class _INamespaceProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.INamespace"
    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        return jsii.get(self, "type")

    @jsii.member(jsii_name="export")
    def export(self) -> "NamespaceImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IService")
class IService(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IServiceProxy

    @property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> "DnsRecordType":
        ...

    @property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> "INamespace":
        ...

    @property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "RoutingPolicy":
        ...

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        ...


class _IServiceProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.IService"
    @property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> "DnsRecordType":
        return jsii.get(self, "dnsRecordType")

    @property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> "INamespace":
        return jsii.get(self, "namespace")

    @property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "RoutingPolicy":
        return jsii.get(self, "routingPolicy")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> str:
        return jsii.get(self, "serviceId")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        return jsii.get(self, "serviceName")


@jsii.implements(IInstance)
class InstanceBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-servicediscovery.InstanceBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _InstanceBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(InstanceBase, self, [scope, id])

    @jsii.member(jsii_name="uniqueInstanceId")
    def _unique_instance_id(self) -> str:
        return jsii.invoke(self, "uniqueInstanceId", [])

    @property
    @jsii.member(jsii_name="instanceId")
    @abc.abstractmethod
    def instance_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="service")
    @abc.abstractmethod
    def service(self) -> "IService":
        ...


class _InstanceBaseProxy(InstanceBase):
    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        return jsii.get(self, "service")


class AliasTargetInstance(InstanceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.AliasTargetInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dns_name: str, service: "IService", custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> None:
        props: AliasTargetInstanceProps = {"dnsName": dns_name, "service": service}

        if custom_attributes is not None:
            props["customAttributes"] = custom_attributes

        if instance_id is not None:
            props["instanceId"] = instance_id

        jsii.create(AliasTargetInstance, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> str:
        return jsii.get(self, "dnsName")

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        return jsii.get(self, "service")


class CnameInstance(InstanceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CnameInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service: "IService", instance_cname: str, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> None:
        props: CnameInstanceProps = {"service": service, "instanceCname": instance_cname}

        if custom_attributes is not None:
            props["customAttributes"] = custom_attributes

        if instance_id is not None:
            props["instanceId"] = instance_id

        jsii.create(CnameInstance, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="instanceCname")
    def instance_cname(self) -> str:
        return jsii.get(self, "instanceCname")

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        return jsii.get(self, "service")


class IpInstance(InstanceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.IpInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service: "IService", ipv4: typing.Optional[str]=None, ipv6: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> None:
        props: IpInstanceProps = {"service": service}

        if ipv4 is not None:
            props["ipv4"] = ipv4

        if ipv6 is not None:
            props["ipv6"] = ipv6

        if port is not None:
            props["port"] = port

        if custom_attributes is not None:
            props["customAttributes"] = custom_attributes

        if instance_id is not None:
            props["instanceId"] = instance_id

        jsii.create(IpInstance, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> str:
        return jsii.get(self, "ipv4")

    @property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> str:
        return jsii.get(self, "ipv6")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return jsii.get(self, "port")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        return jsii.get(self, "service")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.IpInstanceBaseProps")
class IpInstanceBaseProps(BaseInstanceProps, jsii.compat.TypedDict, total=False):
    ipv4: str
    ipv6: str
    port: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.IpInstanceProps")
class IpInstanceProps(IpInstanceBaseProps, jsii.compat.TypedDict):
    service: "IService"

class Namespace(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.Namespace"):
    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, namespace_arn: str, namespace_id: str, namespace_name: str, type: "NamespaceType") -> "INamespace":
        props: NamespaceImportProps = {"namespaceArn": namespace_arn, "namespaceId": namespace_id, "namespaceName": namespace_name, "type": type}

        return jsii.sinvoke(cls, "import", [scope, id, props])


@jsii.implements(INamespace)
class NamespaceBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-servicediscovery.NamespaceBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _NamespaceBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(NamespaceBase, self, [scope, id])

    @jsii.member(jsii_name="export")
    def export(self) -> "NamespaceImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="namespaceArn")
    @abc.abstractmethod
    def namespace_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="namespaceId")
    @abc.abstractmethod
    def namespace_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="namespaceName")
    @abc.abstractmethod
    def namespace_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> "NamespaceType":
        ...


class _NamespaceBaseProxy(NamespaceBase):
    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        return jsii.get(self, "type")


class HttpNamespace(NamespaceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.HttpNamespace"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, description: typing.Optional[str]=None) -> None:
        props: HttpNamespaceProps = {"name": name}

        if description is not None:
            props["description"] = description

        jsii.create(HttpNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="createService")
    def create_service(self, id: str, *, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None) -> "Service":
        props: BaseServiceProps = {}

        if custom_health_check is not None:
            props["customHealthCheck"] = custom_health_check

        if description is not None:
            props["description"] = description

        if health_check is not None:
            props["healthCheck"] = health_check

        if name is not None:
            props["name"] = name

        return jsii.invoke(self, "createService", [id, props])

    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.NamespaceImportProps")
class NamespaceImportProps(jsii.compat.TypedDict):
    namespaceArn: str
    namespaceId: str
    namespaceName: str
    type: "NamespaceType"

@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.NamespaceType")
class NamespaceType(enum.Enum):
    Http = "Http"
    DnsPrivate = "DnsPrivate"
    DnsPublic = "DnsPublic"

class NonIpInstance(InstanceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service: "IService", custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> None:
        props: NonIpInstanceProps = {"service": service}

        if custom_attributes is not None:
            props["customAttributes"] = custom_attributes

        if instance_id is not None:
            props["instanceId"] = instance_id

        jsii.create(NonIpInstance, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        return jsii.get(self, "service")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstanceBaseProps")
class NonIpInstanceBaseProps(BaseInstanceProps, jsii.compat.TypedDict):
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstanceProps")
class NonIpInstanceProps(NonIpInstanceBaseProps, jsii.compat.TypedDict):
    service: "IService"

class PrivateDnsNamespace(NamespaceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.PrivateDnsNamespace"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpcNetwork, name: str, description: typing.Optional[str]=None) -> None:
        props: PrivateDnsNamespaceProps = {"vpc": vpc, "name": name}

        if description is not None:
            props["description"] = description

        jsii.create(PrivateDnsNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="createService")
    def create_service(self, id: str, *, dns_record_type: typing.Optional["DnsRecordType"]=None, dns_ttl_sec: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[bool]=None, routing_policy: typing.Optional["RoutingPolicy"]=None, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None) -> "Service":
        props: DnsServiceProps = {}

        if dns_record_type is not None:
            props["dnsRecordType"] = dns_record_type

        if dns_ttl_sec is not None:
            props["dnsTtlSec"] = dns_ttl_sec

        if load_balancer is not None:
            props["loadBalancer"] = load_balancer

        if routing_policy is not None:
            props["routingPolicy"] = routing_policy

        if custom_health_check is not None:
            props["customHealthCheck"] = custom_health_check

        if description is not None:
            props["description"] = description

        if health_check is not None:
            props["healthCheck"] = health_check

        if name is not None:
            props["name"] = name

        return jsii.invoke(self, "createService", [id, props])

    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.PrivateDnsNamespaceProps")
class PrivateDnsNamespaceProps(BaseNamespaceProps, jsii.compat.TypedDict):
    vpc: aws_cdk.aws_ec2.IVpcNetwork

class PublicDnsNamespace(NamespaceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.PublicDnsNamespace"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, description: typing.Optional[str]=None) -> None:
        props: PublicDnsNamespaceProps = {"name": name}

        if description is not None:
            props["description"] = description

        jsii.create(PublicDnsNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="createService")
    def create_service(self, id: str, *, dns_record_type: typing.Optional["DnsRecordType"]=None, dns_ttl_sec: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[bool]=None, routing_policy: typing.Optional["RoutingPolicy"]=None, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None) -> "Service":
        props: DnsServiceProps = {}

        if dns_record_type is not None:
            props["dnsRecordType"] = dns_record_type

        if dns_ttl_sec is not None:
            props["dnsTtlSec"] = dns_ttl_sec

        if load_balancer is not None:
            props["loadBalancer"] = load_balancer

        if routing_policy is not None:
            props["routingPolicy"] = routing_policy

        if custom_health_check is not None:
            props["customHealthCheck"] = custom_health_check

        if description is not None:
            props["description"] = description

        if health_check is not None:
            props["healthCheck"] = health_check

        if name is not None:
            props["name"] = name

        return jsii.invoke(self, "createService", [id, props])

    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.PublicDnsNamespaceProps")
class PublicDnsNamespaceProps(BaseNamespaceProps, jsii.compat.TypedDict):
    pass

@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.RoutingPolicy")
class RoutingPolicy(enum.Enum):
    Weighted = "Weighted"
    Multivalue = "Multivalue"

@jsii.implements(IService)
class Service(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.Service"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, namespace: "INamespace", dns_record_type: typing.Optional["DnsRecordType"]=None, dns_ttl_sec: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[bool]=None, routing_policy: typing.Optional["RoutingPolicy"]=None, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None) -> None:
        props: ServiceProps = {"namespace": namespace}

        if dns_record_type is not None:
            props["dnsRecordType"] = dns_record_type

        if dns_ttl_sec is not None:
            props["dnsTtlSec"] = dns_ttl_sec

        if load_balancer is not None:
            props["loadBalancer"] = load_balancer

        if routing_policy is not None:
            props["routingPolicy"] = routing_policy

        if custom_health_check is not None:
            props["customHealthCheck"] = custom_health_check

        if description is not None:
            props["description"] = description

        if health_check is not None:
            props["healthCheck"] = health_check

        if name is not None:
            props["name"] = name

        jsii.create(Service, self, [scope, id, props])

    @jsii.member(jsii_name="registerCnameInstance")
    def register_cname_instance(self, *, instance_cname: str, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> "IInstance":
        props: CnameInstanceBaseProps = {"instanceCname": instance_cname}

        if custom_attributes is not None:
            props["customAttributes"] = custom_attributes

        if instance_id is not None:
            props["instanceId"] = instance_id

        return jsii.invoke(self, "registerCnameInstance", [props])

    @jsii.member(jsii_name="registerIpInstance")
    def register_ip_instance(self, *, ipv4: typing.Optional[str]=None, ipv6: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> "IInstance":
        props: IpInstanceBaseProps = {}

        if ipv4 is not None:
            props["ipv4"] = ipv4

        if ipv6 is not None:
            props["ipv6"] = ipv6

        if port is not None:
            props["port"] = port

        if custom_attributes is not None:
            props["customAttributes"] = custom_attributes

        if instance_id is not None:
            props["instanceId"] = instance_id

        return jsii.invoke(self, "registerIpInstance", [props])

    @jsii.member(jsii_name="registerLoadBalancer")
    def register_load_balancer(self, id: str, load_balancer: aws_cdk.aws_route53.IAliasRecordTarget, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None) -> "IInstance":
        return jsii.invoke(self, "registerLoadBalancer", [id, load_balancer, custom_attributes])

    @jsii.member(jsii_name="registerNonIpInstance")
    def register_non_ip_instance(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> "IInstance":
        props: NonIpInstanceBaseProps = {}

        if custom_attributes is not None:
            props["customAttributes"] = custom_attributes

        if instance_id is not None:
            props["instanceId"] = instance_id

        return jsii.invoke(self, "registerNonIpInstance", [props])

    @property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> "DnsRecordType":
        return jsii.get(self, "dnsRecordType")

    @property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> "INamespace":
        return jsii.get(self, "namespace")

    @property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "RoutingPolicy":
        return jsii.get(self, "routingPolicy")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> str:
        return jsii.get(self, "serviceId")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        return jsii.get(self, "serviceName")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.ServiceProps")
class ServiceProps(DnsServiceProps, jsii.compat.TypedDict):
    namespace: "INamespace"

__all__ = ["AliasTargetInstance", "AliasTargetInstanceProps", "BaseInstanceProps", "BaseNamespaceProps", "BaseServiceProps", "CfnHttpNamespace", "CfnHttpNamespaceProps", "CfnInstance", "CfnInstanceProps", "CfnPrivateDnsNamespace", "CfnPrivateDnsNamespaceProps", "CfnPublicDnsNamespace", "CfnPublicDnsNamespaceProps", "CfnService", "CfnServiceProps", "CnameInstance", "CnameInstanceBaseProps", "CnameInstanceProps", "DnsRecordType", "DnsServiceProps", "HealthCheckConfig", "HealthCheckCustomConfig", "HealthCheckType", "HttpNamespace", "HttpNamespaceProps", "IInstance", "INamespace", "IService", "InstanceBase", "IpInstance", "IpInstanceBaseProps", "IpInstanceProps", "Namespace", "NamespaceBase", "NamespaceImportProps", "NamespaceType", "NonIpInstance", "NonIpInstanceBaseProps", "NonIpInstanceProps", "PrivateDnsNamespace", "PrivateDnsNamespaceProps", "PublicDnsNamespace", "PublicDnsNamespaceProps", "RoutingPolicy", "Service", "ServiceProps", "__jsii_assembly__"]

publication.publish()
