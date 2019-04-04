import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_ec2
import aws_cdk.aws_logs
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-route53", "0.28.0", __name__, "aws-route53@0.28.0.jsii.tgz")
class AliasRecord(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.AliasRecord"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, record_name: str, target: "IAliasRecordTarget", zone: "IHostedZone") -> None:
        props: AliasRecordProps = {"recordName": record_name, "target": target, "zone": zone}

        jsii.create(AliasRecord, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.AliasRecordProps")
class AliasRecordProps(jsii.compat.TypedDict):
    recordName: str
    target: "IAliasRecordTarget"
    zone: "IHostedZone"

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.AliasRecordTargetProps")
class AliasRecordTargetProps(jsii.compat.TypedDict):
    dnsName: str
    hostedZoneId: str

class CfnHealthCheck(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnHealthCheck"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, health_check_config: typing.Union["HealthCheckConfigProperty", aws_cdk.cdk.Token], health_check_tags: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "HealthCheckTagProperty"]]]]=None) -> None:
        props: CfnHealthCheckProps = {"healthCheckConfig": health_check_config}

        if health_check_tags is not None:
            props["healthCheckTags"] = health_check_tags

        jsii.create(CfnHealthCheck, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> str:
        return jsii.get(self, "healthCheckId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnHealthCheckProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.AlarmIdentifierProperty")
    class AlarmIdentifierProperty(jsii.compat.TypedDict):
        name: str
        region: str

    class _HealthCheckConfigProperty(jsii.compat.TypedDict, total=False):
        alarmIdentifier: typing.Union[aws_cdk.cdk.Token, "CfnHealthCheck.AlarmIdentifierProperty"]
        childHealthChecks: typing.List[str]
        enableSni: typing.Union[bool, aws_cdk.cdk.Token]
        failureThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        fullyQualifiedDomainName: str
        healthThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        insufficientDataHealthStatus: str
        inverted: typing.Union[bool, aws_cdk.cdk.Token]
        ipAddress: str
        measureLatency: typing.Union[bool, aws_cdk.cdk.Token]
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        regions: typing.List[str]
        requestInterval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        resourcePath: str
        searchString: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.HealthCheckConfigProperty")
    class HealthCheckConfigProperty(_HealthCheckConfigProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.HealthCheckTagProperty")
    class HealthCheckTagProperty(jsii.compat.TypedDict):
        key: str
        value: str


class _CfnHealthCheckProps(jsii.compat.TypedDict, total=False):
    healthCheckTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnHealthCheck.HealthCheckTagProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheckProps")
class CfnHealthCheckProps(_CfnHealthCheckProps):
    healthCheckConfig: typing.Union["CfnHealthCheck.HealthCheckConfigProperty", aws_cdk.cdk.Token]

class CfnHostedZone(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnHostedZone"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, hosted_zone_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "HostedZoneConfigProperty"]]=None, hosted_zone_tags: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "HostedZoneTagProperty"]]]]=None, query_logging_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "QueryLoggingConfigProperty"]]=None, vpcs: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["VPCProperty", aws_cdk.cdk.Token]]]]=None) -> None:
        props: CfnHostedZoneProps = {"name": name}

        if hosted_zone_config is not None:
            props["hostedZoneConfig"] = hosted_zone_config

        if hosted_zone_tags is not None:
            props["hostedZoneTags"] = hosted_zone_tags

        if query_logging_config is not None:
            props["queryLoggingConfig"] = query_logging_config

        if vpcs is not None:
            props["vpcs"] = vpcs

        jsii.create(CfnHostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        return jsii.get(self, "hostedZoneId")

    @property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.List[str]:
        return jsii.get(self, "hostedZoneNameServers")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnHostedZoneProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.HostedZoneConfigProperty")
    class HostedZoneConfigProperty(jsii.compat.TypedDict, total=False):
        comment: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.HostedZoneTagProperty")
    class HostedZoneTagProperty(jsii.compat.TypedDict):
        key: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.QueryLoggingConfigProperty")
    class QueryLoggingConfigProperty(jsii.compat.TypedDict):
        cloudWatchLogsLogGroupArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.VPCProperty")
    class VPCProperty(jsii.compat.TypedDict):
        vpcId: str
        vpcRegion: str


class _CfnHostedZoneProps(jsii.compat.TypedDict, total=False):
    hostedZoneConfig: typing.Union[aws_cdk.cdk.Token, "CfnHostedZone.HostedZoneConfigProperty"]
    hostedZoneTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnHostedZone.HostedZoneTagProperty"]]]
    queryLoggingConfig: typing.Union[aws_cdk.cdk.Token, "CfnHostedZone.QueryLoggingConfigProperty"]
    vpcs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnHostedZone.VPCProperty", aws_cdk.cdk.Token]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZoneProps")
class CfnHostedZoneProps(_CfnHostedZoneProps):
    name: str

class CfnRecordSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnRecordSet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, type: str, alias_target: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AliasTargetProperty"]]=None, comment: typing.Optional[str]=None, failover: typing.Optional[str]=None, geo_location: typing.Optional[typing.Union[aws_cdk.cdk.Token, "GeoLocationProperty"]]=None, health_check_id: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, multi_value_answer: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, region: typing.Optional[str]=None, resource_records: typing.Optional[typing.List[str]]=None, set_identifier: typing.Optional[str]=None, ttl: typing.Optional[str]=None, weight: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnRecordSetProps = {"name": name, "type": type}

        if alias_target is not None:
            props["aliasTarget"] = alias_target

        if comment is not None:
            props["comment"] = comment

        if failover is not None:
            props["failover"] = failover

        if geo_location is not None:
            props["geoLocation"] = geo_location

        if health_check_id is not None:
            props["healthCheckId"] = health_check_id

        if hosted_zone_id is not None:
            props["hostedZoneId"] = hosted_zone_id

        if hosted_zone_name is not None:
            props["hostedZoneName"] = hosted_zone_name

        if multi_value_answer is not None:
            props["multiValueAnswer"] = multi_value_answer

        if region is not None:
            props["region"] = region

        if resource_records is not None:
            props["resourceRecords"] = resource_records

        if set_identifier is not None:
            props["setIdentifier"] = set_identifier

        if ttl is not None:
            props["ttl"] = ttl

        if weight is not None:
            props["weight"] = weight

        jsii.create(CfnRecordSet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRecordSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="recordSetDomainName")
    def record_set_domain_name(self) -> str:
        return jsii.get(self, "recordSetDomainName")

    class _AliasTargetProperty(jsii.compat.TypedDict, total=False):
        evaluateTargetHealth: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSet.AliasTargetProperty")
    class AliasTargetProperty(_AliasTargetProperty):
        dnsName: str
        hostedZoneId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSet.GeoLocationProperty")
    class GeoLocationProperty(jsii.compat.TypedDict, total=False):
        continentCode: str
        countryCode: str
        subdivisionCode: str


class CfnRecordSetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comment: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, record_sets: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "RecordSetProperty"]]]]=None) -> None:
        props: CfnRecordSetGroupProps = {}

        if comment is not None:
            props["comment"] = comment

        if hosted_zone_id is not None:
            props["hostedZoneId"] = hosted_zone_id

        if hosted_zone_name is not None:
            props["hostedZoneName"] = hosted_zone_name

        if record_sets is not None:
            props["recordSets"] = record_sets

        jsii.create(CfnRecordSetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRecordSetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="recordSetGroupName")
    def record_set_group_name(self) -> str:
        return jsii.get(self, "recordSetGroupName")

    class _AliasTargetProperty(jsii.compat.TypedDict, total=False):
        evaluateTargetHealth: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.AliasTargetProperty")
    class AliasTargetProperty(_AliasTargetProperty):
        dnsName: str
        hostedZoneId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.GeoLocationProperty")
    class GeoLocationProperty(jsii.compat.TypedDict, total=False):
        continentCode: str
        countryCode: str
        subdivisionCode: str

    class _RecordSetProperty(jsii.compat.TypedDict, total=False):
        aliasTarget: typing.Union[aws_cdk.cdk.Token, "CfnRecordSetGroup.AliasTargetProperty"]
        comment: str
        failover: str
        geoLocation: typing.Union[aws_cdk.cdk.Token, "CfnRecordSetGroup.GeoLocationProperty"]
        healthCheckId: str
        hostedZoneId: str
        hostedZoneName: str
        multiValueAnswer: typing.Union[bool, aws_cdk.cdk.Token]
        region: str
        resourceRecords: typing.List[str]
        setIdentifier: str
        ttl: str
        weight: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.RecordSetProperty")
    class RecordSetProperty(_RecordSetProperty):
        name: str
        type: str


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroupProps")
class CfnRecordSetGroupProps(jsii.compat.TypedDict, total=False):
    comment: str
    hostedZoneId: str
    hostedZoneName: str
    recordSets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRecordSetGroup.RecordSetProperty"]]]

class _CfnRecordSetProps(jsii.compat.TypedDict, total=False):
    aliasTarget: typing.Union[aws_cdk.cdk.Token, "CfnRecordSet.AliasTargetProperty"]
    comment: str
    failover: str
    geoLocation: typing.Union[aws_cdk.cdk.Token, "CfnRecordSet.GeoLocationProperty"]
    healthCheckId: str
    hostedZoneId: str
    hostedZoneName: str
    multiValueAnswer: typing.Union[bool, aws_cdk.cdk.Token]
    region: str
    resourceRecords: typing.List[str]
    setIdentifier: str
    ttl: str
    weight: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetProps")
class CfnRecordSetProps(_CfnRecordSetProps):
    name: str
    type: str

class CnameRecord(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CnameRecord"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, record_name: str, record_value: str, zone: "IHostedZone", ttl: typing.Optional[jsii.Number]=None) -> None:
        props: CnameRecordProps = {"recordName": record_name, "recordValue": record_value, "zone": zone}

        if ttl is not None:
            props["ttl"] = ttl

        jsii.create(CnameRecord, self, [scope, id, props])


class _CnameRecordProps(jsii.compat.TypedDict, total=False):
    ttl: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CnameRecordProps")
class CnameRecordProps(_CnameRecordProps):
    recordName: str
    recordValue: str
    zone: "IHostedZone"

class _CommonHostedZoneProps(jsii.compat.TypedDict, total=False):
    comment: str
    queryLogsLogGroupArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CommonHostedZoneProps")
class CommonHostedZoneProps(_CommonHostedZoneProps):
    zoneName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneImportProps")
class HostedZoneImportProps(jsii.compat.TypedDict):
    hostedZoneId: str
    zoneName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneProps")
class HostedZoneProps(CommonHostedZoneProps, jsii.compat.TypedDict, total=False):
    vpcs: typing.List[aws_cdk.aws_ec2.IVpcNetwork]

class HostedZoneProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.HostedZoneProvider"):
    def __init__(self, context: aws_cdk.cdk.Construct, *, domain_name: str, private_zone: typing.Optional[bool]=None, vpc_id: typing.Optional[str]=None) -> None:
        props: HostedZoneProviderProps = {"domainName": domain_name}

        if private_zone is not None:
            props["privateZone"] = private_zone

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(HostedZoneProvider, self, [context, props])

    @jsii.member(jsii_name="findAndImport")
    def find_and_import(self, scope: aws_cdk.cdk.Construct, id: str) -> "IHostedZone":
        return jsii.invoke(self, "findAndImport", [scope, id])

    @jsii.member(jsii_name="findHostedZone")
    def find_hosted_zone(self) -> "HostedZoneImportProps":
        return jsii.invoke(self, "findHostedZone", [])


class _HostedZoneProviderProps(jsii.compat.TypedDict, total=False):
    privateZone: bool
    vpcId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneProviderProps")
class HostedZoneProviderProps(_HostedZoneProviderProps):
    domainName: str

@jsii.interface(jsii_type="@aws-cdk/aws-route53.IAliasRecordTarget")
class IAliasRecordTarget(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IAliasRecordTargetProxy

    @jsii.member(jsii_name="asAliasRecordTarget")
    def as_alias_record_target(self) -> "AliasRecordTargetProps":
        ...


class _IAliasRecordTargetProxy():
    __jsii_type__ = "@aws-cdk/aws-route53.IAliasRecordTarget"
    @jsii.member(jsii_name="asAliasRecordTarget")
    def as_alias_record_target(self) -> "AliasRecordTargetProps":
        return jsii.invoke(self, "asAliasRecordTarget", [])


@jsii.interface(jsii_type="@aws-cdk/aws-route53.IHostedZone")
class IHostedZone(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IHostedZoneProxy

    @property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "HostedZoneImportProps":
        ...


class _IHostedZoneProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-route53.IHostedZone"
    @property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        return jsii.get(self, "hostedZoneId")

    @property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        return jsii.get(self, "zoneName")

    @property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "hostedZoneNameServers")

    @jsii.member(jsii_name="export")
    def export(self) -> "HostedZoneImportProps":
        return jsii.invoke(self, "export", [])


@jsii.implements(IHostedZone)
class HostedZone(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.HostedZone"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpcs: typing.Optional[typing.List[aws_cdk.aws_ec2.IVpcNetwork]]=None, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        props: HostedZoneProps = {"zoneName": zone_name}

        if vpcs is not None:
            props["vpcs"] = vpcs

        if comment is not None:
            props["comment"] = comment

        if query_logs_log_group_arn is not None:
            props["queryLogsLogGroupArn"] = query_logs_log_group_arn

        jsii.create(HostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, hosted_zone_id: str, zone_name: str) -> "IHostedZone":
        props: HostedZoneImportProps = {"hostedZoneId": hosted_zone_id, "zoneName": zone_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addVpc")
    def add_vpc(self, vpc: aws_cdk.aws_ec2.IVpcNetwork) -> None:
        return jsii.invoke(self, "addVpc", [vpc])

    @jsii.member(jsii_name="export")
    def export(self) -> "HostedZoneImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        return jsii.get(self, "hostedZoneId")

    @property
    @jsii.member(jsii_name="vpcs")
    def _vpcs(self) -> typing.List["CfnHostedZone.VPCProperty"]:
        return jsii.get(self, "vpcs")

    @property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        return jsii.get(self, "zoneName")

    @property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        return jsii.get(self, "hostedZoneNameServers")


class PrivateHostedZone(HostedZone, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.PrivateHostedZone"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpcNetwork, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        props: PrivateHostedZoneProps = {"vpc": vpc, "zoneName": zone_name}

        if comment is not None:
            props["comment"] = comment

        if query_logs_log_group_arn is not None:
            props["queryLogsLogGroupArn"] = query_logs_log_group_arn

        jsii.create(PrivateHostedZone, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.PrivateHostedZoneProps")
class PrivateHostedZoneProps(CommonHostedZoneProps, jsii.compat.TypedDict):
    vpc: aws_cdk.aws_ec2.IVpcNetwork

class PublicHostedZone(HostedZone, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.PublicHostedZone"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        props: PublicHostedZoneProps = {"zoneName": zone_name}

        if comment is not None:
            props["comment"] = comment

        if query_logs_log_group_arn is not None:
            props["queryLogsLogGroupArn"] = query_logs_log_group_arn

        jsii.create(PublicHostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="addDelegation")
    def add_delegation(self, delegate: "PublicHostedZone", *, comment: typing.Optional[str]=None, ttl: typing.Optional[jsii.Number]=None) -> None:
        opts: ZoneDelegationOptions = {}

        if comment is not None:
            opts["comment"] = comment

        if ttl is not None:
            opts["ttl"] = ttl

        return jsii.invoke(self, "addDelegation", [delegate, opts])

    @jsii.member(jsii_name="addVpc")
    def add_vpc(self, _vpc: aws_cdk.aws_ec2.IVpcNetwork) -> None:
        return jsii.invoke(self, "addVpc", [_vpc])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.PublicHostedZoneProps")
class PublicHostedZoneProps(CommonHostedZoneProps, jsii.compat.TypedDict):
    pass

class TxtRecord(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.TxtRecord"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, record_name: str, record_value: str, zone: "IHostedZone", ttl: typing.Optional[jsii.Number]=None) -> None:
        props: TxtRecordProps = {"recordName": record_name, "recordValue": record_value, "zone": zone}

        if ttl is not None:
            props["ttl"] = ttl

        jsii.create(TxtRecord, self, [scope, id, props])


class _TxtRecordProps(jsii.compat.TypedDict, total=False):
    ttl: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.TxtRecordProps")
class TxtRecordProps(_TxtRecordProps):
    recordName: str
    recordValue: str
    zone: "IHostedZone"

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.ZoneDelegationOptions")
class ZoneDelegationOptions(jsii.compat.TypedDict, total=False):
    comment: str
    ttl: jsii.Number

class ZoneDelegationRecord(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.ZoneDelegationRecord"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, delegated_zone_name: str, name_servers: typing.List[str], zone: "IHostedZone", comment: typing.Optional[str]=None, ttl: typing.Optional[jsii.Number]=None) -> None:
        props: ZoneDelegationRecordProps = {"delegatedZoneName": delegated_zone_name, "nameServers": name_servers, "zone": zone}

        if comment is not None:
            props["comment"] = comment

        if ttl is not None:
            props["ttl"] = ttl

        jsii.create(ZoneDelegationRecord, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.ZoneDelegationRecordProps")
class ZoneDelegationRecordProps(ZoneDelegationOptions, jsii.compat.TypedDict):
    delegatedZoneName: str
    nameServers: typing.List[str]
    zone: "IHostedZone"

__all__ = ["AliasRecord", "AliasRecordProps", "AliasRecordTargetProps", "CfnHealthCheck", "CfnHealthCheckProps", "CfnHostedZone", "CfnHostedZoneProps", "CfnRecordSet", "CfnRecordSetGroup", "CfnRecordSetGroupProps", "CfnRecordSetProps", "CnameRecord", "CnameRecordProps", "CommonHostedZoneProps", "HostedZone", "HostedZoneImportProps", "HostedZoneProps", "HostedZoneProvider", "HostedZoneProviderProps", "IAliasRecordTarget", "IHostedZone", "PrivateHostedZone", "PrivateHostedZoneProps", "PublicHostedZone", "PublicHostedZoneProps", "TxtRecord", "TxtRecordProps", "ZoneDelegationOptions", "ZoneDelegationRecord", "ZoneDelegationRecordProps", "__jsii_assembly__"]

publication.publish()
