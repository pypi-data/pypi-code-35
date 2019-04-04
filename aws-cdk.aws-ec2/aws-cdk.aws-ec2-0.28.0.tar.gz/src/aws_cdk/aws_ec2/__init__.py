import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ec2", "0.28.0", __name__, "aws-ec2@0.28.0.jsii.tgz")
@jsii.enum(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxEdition")
class AmazonLinuxEdition(enum.Enum):
    Standard = "Standard"
    Minimal = "Minimal"

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxGeneration")
class AmazonLinuxGeneration(enum.Enum):
    AmazonLinux = "AmazonLinux"
    AmazonLinux2 = "AmazonLinux2"

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxImageProps")
class AmazonLinuxImageProps(jsii.compat.TypedDict, total=False):
    edition: "AmazonLinuxEdition"
    generation: "AmazonLinuxGeneration"
    storage: "AmazonLinuxStorage"
    virtualization: "AmazonLinuxVirt"

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxStorage")
class AmazonLinuxStorage(enum.Enum):
    EBS = "EBS"
    GeneralPurpose = "GeneralPurpose"

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxVirt")
class AmazonLinuxVirt(enum.Enum):
    HVM = "HVM"
    PV = "PV"

class CfnCustomerGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnCustomerGateway"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, bgp_asn: typing.Union[jsii.Number, aws_cdk.cdk.Token], ip_address: str, type: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnCustomerGatewayProps = {"bgpAsn": bgp_asn, "ipAddress": ip_address, "type": type}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCustomerGateway, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="customerGatewayName")
    def customer_gateway_name(self) -> str:
        return jsii.get(self, "customerGatewayName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCustomerGatewayProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnCustomerGatewayProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnCustomerGatewayProps")
class CfnCustomerGatewayProps(_CfnCustomerGatewayProps):
    bgpAsn: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    ipAddress: str
    type: str

class CfnDHCPOptions(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnDHCPOptions"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain_name: typing.Optional[str]=None, domain_name_servers: typing.Optional[typing.List[str]]=None, netbios_name_servers: typing.Optional[typing.List[str]]=None, netbios_node_type: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, ntp_servers: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDHCPOptionsProps = {}

        if domain_name is not None:
            props["domainName"] = domain_name

        if domain_name_servers is not None:
            props["domainNameServers"] = domain_name_servers

        if netbios_name_servers is not None:
            props["netbiosNameServers"] = netbios_name_servers

        if netbios_node_type is not None:
            props["netbiosNodeType"] = netbios_node_type

        if ntp_servers is not None:
            props["ntpServers"] = ntp_servers

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDHCPOptions, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dhcpOptionsName")
    def dhcp_options_name(self) -> str:
        return jsii.get(self, "dhcpOptionsName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDHCPOptionsProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnDHCPOptionsProps")
class CfnDHCPOptionsProps(jsii.compat.TypedDict, total=False):
    domainName: str
    domainNameServers: typing.List[str]
    netbiosNameServers: typing.List[str]
    netbiosNodeType: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    ntpServers: typing.List[str]
    tags: typing.List[aws_cdk.cdk.CfnTag]

class CfnEC2Fleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, launch_template_configs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "FleetLaunchTemplateConfigRequestProperty"]]], target_capacity_specification: typing.Union[aws_cdk.cdk.Token, "TargetCapacitySpecificationRequestProperty"], excess_capacity_termination_policy: typing.Optional[str]=None, on_demand_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, "OnDemandOptionsRequestProperty"]]=None, replace_unhealthy_instances: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, spot_options: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SpotOptionsRequestProperty"]]=None, tag_specifications: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "TagSpecificationProperty"]]]]=None, terminate_instances_with_expiration: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, type: typing.Optional[str]=None, valid_from: typing.Optional[str]=None, valid_until: typing.Optional[str]=None) -> None:
        props: CfnEC2FleetProps = {"launchTemplateConfigs": launch_template_configs, "targetCapacitySpecification": target_capacity_specification}

        if excess_capacity_termination_policy is not None:
            props["excessCapacityTerminationPolicy"] = excess_capacity_termination_policy

        if on_demand_options is not None:
            props["onDemandOptions"] = on_demand_options

        if replace_unhealthy_instances is not None:
            props["replaceUnhealthyInstances"] = replace_unhealthy_instances

        if spot_options is not None:
            props["spotOptions"] = spot_options

        if tag_specifications is not None:
            props["tagSpecifications"] = tag_specifications

        if terminate_instances_with_expiration is not None:
            props["terminateInstancesWithExpiration"] = terminate_instances_with_expiration

        if type is not None:
            props["type"] = type

        if valid_from is not None:
            props["validFrom"] = valid_from

        if valid_until is not None:
            props["validUntil"] = valid_until

        jsii.create(CfnEC2Fleet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="ec2FleetId")
    def ec2_fleet_id(self) -> str:
        return jsii.get(self, "ec2FleetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEC2FleetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.FleetLaunchTemplateConfigRequestProperty")
    class FleetLaunchTemplateConfigRequestProperty(jsii.compat.TypedDict, total=False):
        launchTemplateSpecification: typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.FleetLaunchTemplateSpecificationRequestProperty"]
        overrides: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty")
    class FleetLaunchTemplateOverridesRequestProperty(jsii.compat.TypedDict, total=False):
        availabilityZone: str
        instanceType: str
        maxPrice: str
        priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        subnetId: str
        weightedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.FleetLaunchTemplateSpecificationRequestProperty")
    class FleetLaunchTemplateSpecificationRequestProperty(jsii.compat.TypedDict, total=False):
        launchTemplateId: str
        launchTemplateName: str
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.OnDemandOptionsRequestProperty")
    class OnDemandOptionsRequestProperty(jsii.compat.TypedDict, total=False):
        allocationStrategy: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.SpotOptionsRequestProperty")
    class SpotOptionsRequestProperty(jsii.compat.TypedDict, total=False):
        allocationStrategy: str
        instanceInterruptionBehavior: str
        instancePoolsToUseCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.TagRequestProperty")
    class TagRequestProperty(jsii.compat.TypedDict, total=False):
        key: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.TagSpecificationProperty")
    class TagSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceType: str
        tags: typing.List["CfnEC2Fleet.TagRequestProperty"]

    class _TargetCapacitySpecificationRequestProperty(jsii.compat.TypedDict, total=False):
        defaultTargetCapacityType: str
        onDemandTargetCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        spotTargetCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.TargetCapacitySpecificationRequestProperty")
    class TargetCapacitySpecificationRequestProperty(_TargetCapacitySpecificationRequestProperty):
        totalTargetCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnEC2FleetProps(jsii.compat.TypedDict, total=False):
    excessCapacityTerminationPolicy: str
    onDemandOptions: typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.OnDemandOptionsRequestProperty"]
    replaceUnhealthyInstances: typing.Union[bool, aws_cdk.cdk.Token]
    spotOptions: typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.SpotOptionsRequestProperty"]
    tagSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.TagSpecificationProperty"]]]
    terminateInstancesWithExpiration: typing.Union[bool, aws_cdk.cdk.Token]
    type: str
    validFrom: str
    validUntil: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2FleetProps")
class CfnEC2FleetProps(_CfnEC2FleetProps):
    launchTemplateConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.FleetLaunchTemplateConfigRequestProperty"]]]
    targetCapacitySpecification: typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.TargetCapacitySpecificationRequestProperty"]

class CfnEIP(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnEIP"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, public_ipv4_pool: typing.Optional[str]=None) -> None:
        props: CfnEIPProps = {}

        if domain is not None:
            props["domain"] = domain

        if instance_id is not None:
            props["instanceId"] = instance_id

        if public_ipv4_pool is not None:
            props["publicIpv4Pool"] = public_ipv4_pool

        jsii.create(CfnEIP, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="eipAllocationId")
    def eip_allocation_id(self) -> str:
        return jsii.get(self, "eipAllocationId")

    @property
    @jsii.member(jsii_name="eipIp")
    def eip_ip(self) -> str:
        return jsii.get(self, "eipIp")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEIPProps":
        return jsii.get(self, "propertyOverrides")


class CfnEIPAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnEIPAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, allocation_id: typing.Optional[str]=None, eip: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, network_interface_id: typing.Optional[str]=None, private_ip_address: typing.Optional[str]=None) -> None:
        props: CfnEIPAssociationProps = {}

        if allocation_id is not None:
            props["allocationId"] = allocation_id

        if eip is not None:
            props["eip"] = eip

        if instance_id is not None:
            props["instanceId"] = instance_id

        if network_interface_id is not None:
            props["networkInterfaceId"] = network_interface_id

        if private_ip_address is not None:
            props["privateIpAddress"] = private_ip_address

        jsii.create(CfnEIPAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="eipAssociationName")
    def eip_association_name(self) -> str:
        return jsii.get(self, "eipAssociationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEIPAssociationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEIPAssociationProps")
class CfnEIPAssociationProps(jsii.compat.TypedDict, total=False):
    allocationId: str
    eip: str
    instanceId: str
    networkInterfaceId: str
    privateIpAddress: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEIPProps")
class CfnEIPProps(jsii.compat.TypedDict, total=False):
    domain: str
    instanceId: str
    publicIpv4Pool: str

class CfnEgressOnlyInternetGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnEgressOnlyInternetGateway"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str) -> None:
        props: CfnEgressOnlyInternetGatewayProps = {"vpcId": vpc_id}

        jsii.create(CfnEgressOnlyInternetGateway, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="egressOnlyInternetGatewayId")
    def egress_only_internet_gateway_id(self) -> str:
        return jsii.get(self, "egressOnlyInternetGatewayId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEgressOnlyInternetGatewayProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEgressOnlyInternetGatewayProps")
class CfnEgressOnlyInternetGatewayProps(jsii.compat.TypedDict):
    vpcId: str

class CfnFlowLog(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnFlowLog"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_id: str, resource_type: str, traffic_type: str, deliver_logs_permission_arn: typing.Optional[str]=None, log_destination: typing.Optional[str]=None, log_destination_type: typing.Optional[str]=None, log_group_name: typing.Optional[str]=None) -> None:
        props: CfnFlowLogProps = {"resourceId": resource_id, "resourceType": resource_type, "trafficType": traffic_type}

        if deliver_logs_permission_arn is not None:
            props["deliverLogsPermissionArn"] = deliver_logs_permission_arn

        if log_destination is not None:
            props["logDestination"] = log_destination

        if log_destination_type is not None:
            props["logDestinationType"] = log_destination_type

        if log_group_name is not None:
            props["logGroupName"] = log_group_name

        jsii.create(CfnFlowLog, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="flowLogId")
    def flow_log_id(self) -> str:
        return jsii.get(self, "flowLogId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFlowLogProps":
        return jsii.get(self, "propertyOverrides")


class _CfnFlowLogProps(jsii.compat.TypedDict, total=False):
    deliverLogsPermissionArn: str
    logDestination: str
    logDestinationType: str
    logGroupName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnFlowLogProps")
class CfnFlowLogProps(_CfnFlowLogProps):
    resourceId: str
    resourceType: str
    trafficType: str

class CfnHost(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnHost"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, instance_type: str, auto_placement: typing.Optional[str]=None) -> None:
        props: CfnHostProps = {"availabilityZone": availability_zone, "instanceType": instance_type}

        if auto_placement is not None:
            props["autoPlacement"] = auto_placement

        jsii.create(CfnHost, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="hostId")
    def host_id(self) -> str:
        return jsii.get(self, "hostId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnHostProps":
        return jsii.get(self, "propertyOverrides")


class _CfnHostProps(jsii.compat.TypedDict, total=False):
    autoPlacement: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnHostProps")
class CfnHostProps(_CfnHostProps):
    availabilityZone: str
    instanceType: str

class CfnInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, additional_info: typing.Optional[str]=None, affinity: typing.Optional[str]=None, availability_zone: typing.Optional[str]=None, block_device_mappings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "BlockDeviceMappingProperty"]]]]=None, credit_specification: typing.Optional[typing.Union[aws_cdk.cdk.Token, "CreditSpecificationProperty"]]=None, disable_api_termination: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, ebs_optimized: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, elastic_gpu_specifications: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ElasticGpuSpecificationProperty"]]]]=None, elastic_inference_accelerators: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ElasticInferenceAcceleratorProperty"]]]]=None, host_id: typing.Optional[str]=None, iam_instance_profile: typing.Optional[str]=None, image_id: typing.Optional[str]=None, instance_initiated_shutdown_behavior: typing.Optional[str]=None, instance_type: typing.Optional[str]=None, ipv6_address_count: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, ipv6_addresses: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "InstanceIpv6AddressProperty"]]]]=None, kernel_id: typing.Optional[str]=None, key_name: typing.Optional[str]=None, launch_template: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LaunchTemplateSpecificationProperty"]]=None, license_specifications: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "LicenseSpecificationProperty"]]]]=None, monitoring: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, network_interfaces: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "NetworkInterfaceProperty"]]]]=None, placement_group_name: typing.Optional[str]=None, private_ip_address: typing.Optional[str]=None, ramdisk_id: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, security_groups: typing.Optional[typing.List[str]]=None, source_dest_check: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, ssm_associations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SsmAssociationProperty"]]]]=None, subnet_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, tenancy: typing.Optional[str]=None, user_data: typing.Optional[str]=None, volumes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "VolumeProperty"]]]]=None) -> None:
        props: CfnInstanceProps = {}

        if additional_info is not None:
            props["additionalInfo"] = additional_info

        if affinity is not None:
            props["affinity"] = affinity

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if block_device_mappings is not None:
            props["blockDeviceMappings"] = block_device_mappings

        if credit_specification is not None:
            props["creditSpecification"] = credit_specification

        if disable_api_termination is not None:
            props["disableApiTermination"] = disable_api_termination

        if ebs_optimized is not None:
            props["ebsOptimized"] = ebs_optimized

        if elastic_gpu_specifications is not None:
            props["elasticGpuSpecifications"] = elastic_gpu_specifications

        if elastic_inference_accelerators is not None:
            props["elasticInferenceAccelerators"] = elastic_inference_accelerators

        if host_id is not None:
            props["hostId"] = host_id

        if iam_instance_profile is not None:
            props["iamInstanceProfile"] = iam_instance_profile

        if image_id is not None:
            props["imageId"] = image_id

        if instance_initiated_shutdown_behavior is not None:
            props["instanceInitiatedShutdownBehavior"] = instance_initiated_shutdown_behavior

        if instance_type is not None:
            props["instanceType"] = instance_type

        if ipv6_address_count is not None:
            props["ipv6AddressCount"] = ipv6_address_count

        if ipv6_addresses is not None:
            props["ipv6Addresses"] = ipv6_addresses

        if kernel_id is not None:
            props["kernelId"] = kernel_id

        if key_name is not None:
            props["keyName"] = key_name

        if launch_template is not None:
            props["launchTemplate"] = launch_template

        if license_specifications is not None:
            props["licenseSpecifications"] = license_specifications

        if monitoring is not None:
            props["monitoring"] = monitoring

        if network_interfaces is not None:
            props["networkInterfaces"] = network_interfaces

        if placement_group_name is not None:
            props["placementGroupName"] = placement_group_name

        if private_ip_address is not None:
            props["privateIpAddress"] = private_ip_address

        if ramdisk_id is not None:
            props["ramdiskId"] = ramdisk_id

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if source_dest_check is not None:
            props["sourceDestCheck"] = source_dest_check

        if ssm_associations is not None:
            props["ssmAssociations"] = ssm_associations

        if subnet_id is not None:
            props["subnetId"] = subnet_id

        if tags is not None:
            props["tags"] = tags

        if tenancy is not None:
            props["tenancy"] = tenancy

        if user_data is not None:
            props["userData"] = user_data

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(CfnInstance, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="instanceAvailabilityZone")
    def instance_availability_zone(self) -> str:
        return jsii.get(self, "instanceAvailabilityZone")

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="instancePrivateDnsName")
    def instance_private_dns_name(self) -> str:
        return jsii.get(self, "instancePrivateDnsName")

    @property
    @jsii.member(jsii_name="instancePrivateIp")
    def instance_private_ip(self) -> str:
        return jsii.get(self, "instancePrivateIp")

    @property
    @jsii.member(jsii_name="instancePublicDnsName")
    def instance_public_dns_name(self) -> str:
        return jsii.get(self, "instancePublicDnsName")

    @property
    @jsii.member(jsii_name="instancePublicIp")
    def instance_public_ip(self) -> str:
        return jsii.get(self, "instancePublicIp")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInstanceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.AssociationParameterProperty")
    class AssociationParameterProperty(jsii.compat.TypedDict):
        key: str
        value: typing.List[str]

    class _BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        ebs: typing.Union[aws_cdk.cdk.Token, "CfnInstance.EbsProperty"]
        noDevice: typing.Union[aws_cdk.cdk.Token, "CfnInstance.NoDeviceProperty"]
        virtualName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.BlockDeviceMappingProperty")
    class BlockDeviceMappingProperty(_BlockDeviceMappingProperty):
        deviceName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.CreditSpecificationProperty")
    class CreditSpecificationProperty(jsii.compat.TypedDict, total=False):
        cpuCredits: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.EbsProperty")
    class EbsProperty(jsii.compat.TypedDict, total=False):
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        snapshotId: str
        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.ElasticGpuSpecificationProperty")
    class ElasticGpuSpecificationProperty(jsii.compat.TypedDict):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.ElasticInferenceAcceleratorProperty")
    class ElasticInferenceAcceleratorProperty(jsii.compat.TypedDict):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.InstanceIpv6AddressProperty")
    class InstanceIpv6AddressProperty(jsii.compat.TypedDict):
        ipv6Address: str

    class _LaunchTemplateSpecificationProperty(jsii.compat.TypedDict, total=False):
        launchTemplateId: str
        launchTemplateName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.LaunchTemplateSpecificationProperty")
    class LaunchTemplateSpecificationProperty(_LaunchTemplateSpecificationProperty):
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.LicenseSpecificationProperty")
    class LicenseSpecificationProperty(jsii.compat.TypedDict):
        licenseConfigurationArn: str

    class _NetworkInterfaceProperty(jsii.compat.TypedDict, total=False):
        associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        description: str
        groupSet: typing.List[str]
        ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        ipv6Addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.InstanceIpv6AddressProperty"]]]
        networkInterfaceId: str
        privateIpAddress: str
        privateIpAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.PrivateIpAddressSpecificationProperty"]]]
        secondaryPrivateIpAddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        subnetId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.NetworkInterfaceProperty")
    class NetworkInterfaceProperty(_NetworkInterfaceProperty):
        deviceIndex: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.NoDeviceProperty")
    class NoDeviceProperty(jsii.compat.TypedDict):
        pass

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.PrivateIpAddressSpecificationProperty")
    class PrivateIpAddressSpecificationProperty(jsii.compat.TypedDict):
        primary: typing.Union[bool, aws_cdk.cdk.Token]
        privateIpAddress: str

    class _SsmAssociationProperty(jsii.compat.TypedDict, total=False):
        associationParameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.AssociationParameterProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.SsmAssociationProperty")
    class SsmAssociationProperty(_SsmAssociationProperty):
        documentName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.VolumeProperty")
    class VolumeProperty(jsii.compat.TypedDict):
        device: str
        volumeId: str


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstanceProps")
class CfnInstanceProps(jsii.compat.TypedDict, total=False):
    additionalInfo: str
    affinity: str
    availabilityZone: str
    blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.BlockDeviceMappingProperty"]]]
    creditSpecification: typing.Union[aws_cdk.cdk.Token, "CfnInstance.CreditSpecificationProperty"]
    disableApiTermination: typing.Union[bool, aws_cdk.cdk.Token]
    ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
    elasticGpuSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.ElasticGpuSpecificationProperty"]]]
    elasticInferenceAccelerators: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.ElasticInferenceAcceleratorProperty"]]]
    hostId: str
    iamInstanceProfile: str
    imageId: str
    instanceInitiatedShutdownBehavior: str
    instanceType: str
    ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    ipv6Addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.InstanceIpv6AddressProperty"]]]
    kernelId: str
    keyName: str
    launchTemplate: typing.Union[aws_cdk.cdk.Token, "CfnInstance.LaunchTemplateSpecificationProperty"]
    licenseSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.LicenseSpecificationProperty"]]]
    monitoring: typing.Union[bool, aws_cdk.cdk.Token]
    networkInterfaces: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.NetworkInterfaceProperty"]]]
    placementGroupName: str
    privateIpAddress: str
    ramdiskId: str
    securityGroupIds: typing.List[str]
    securityGroups: typing.List[str]
    sourceDestCheck: typing.Union[bool, aws_cdk.cdk.Token]
    ssmAssociations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.SsmAssociationProperty"]]]
    subnetId: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    tenancy: str
    userData: str
    volumes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.VolumeProperty"]]]

class CfnInternetGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnInternetGateway"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnInternetGatewayProps = {}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnInternetGateway, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="internetGatewayName")
    def internet_gateway_name(self) -> str:
        return jsii.get(self, "internetGatewayName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInternetGatewayProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInternetGatewayProps")
class CfnInternetGatewayProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

class CfnLaunchTemplate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, launch_template_data: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LaunchTemplateDataProperty"]]=None, launch_template_name: typing.Optional[str]=None) -> None:
        props: CfnLaunchTemplateProps = {}

        if launch_template_data is not None:
            props["launchTemplateData"] = launch_template_data

        if launch_template_name is not None:
            props["launchTemplateName"] = launch_template_name

        jsii.create(CfnLaunchTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="launchTemplateDefaultVersionNumber")
    def launch_template_default_version_number(self) -> str:
        return jsii.get(self, "launchTemplateDefaultVersionNumber")

    @property
    @jsii.member(jsii_name="launchTemplateId")
    def launch_template_id(self) -> str:
        return jsii.get(self, "launchTemplateId")

    @property
    @jsii.member(jsii_name="launchTemplateLatestVersionNumber")
    def launch_template_latest_version_number(self) -> str:
        return jsii.get(self, "launchTemplateLatestVersionNumber")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchTemplateProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.BlockDeviceMappingProperty")
    class BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        deviceName: str
        ebs: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.EbsProperty"]
        noDevice: str
        virtualName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.CapacityReservationSpecificationProperty")
    class CapacityReservationSpecificationProperty(jsii.compat.TypedDict, total=False):
        capacityReservationPreference: str
        capacityReservationTarget: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.CapacityReservationTargetProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.CapacityReservationTargetProperty")
    class CapacityReservationTargetProperty(jsii.compat.TypedDict, total=False):
        capacityReservationId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.CpuOptionsProperty")
    class CpuOptionsProperty(jsii.compat.TypedDict, total=False):
        coreCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        threadsPerCore: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.CreditSpecificationProperty")
    class CreditSpecificationProperty(jsii.compat.TypedDict, total=False):
        cpuCredits: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.EbsProperty")
    class EbsProperty(jsii.compat.TypedDict, total=False):
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        kmsKeyId: str
        snapshotId: str
        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.ElasticGpuSpecificationProperty")
    class ElasticGpuSpecificationProperty(jsii.compat.TypedDict, total=False):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.HibernationOptionsProperty")
    class HibernationOptionsProperty(jsii.compat.TypedDict, total=False):
        configured: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.IamInstanceProfileProperty")
    class IamInstanceProfileProperty(jsii.compat.TypedDict, total=False):
        arn: str
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.InstanceMarketOptionsProperty")
    class InstanceMarketOptionsProperty(jsii.compat.TypedDict, total=False):
        marketType: str
        spotOptions: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.SpotOptionsProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.Ipv6AddProperty")
    class Ipv6AddProperty(jsii.compat.TypedDict, total=False):
        ipv6Address: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.LaunchTemplateDataProperty")
    class LaunchTemplateDataProperty(jsii.compat.TypedDict, total=False):
        blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.BlockDeviceMappingProperty"]]]
        capacityReservationSpecification: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.CapacityReservationSpecificationProperty"]
        cpuOptions: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.CpuOptionsProperty"]
        creditSpecification: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.CreditSpecificationProperty"]
        disableApiTermination: typing.Union[bool, aws_cdk.cdk.Token]
        ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
        elasticGpuSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.ElasticGpuSpecificationProperty"]]]
        elasticInferenceAccelerators: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.LaunchTemplateElasticInferenceAcceleratorProperty"]]]
        hibernationOptions: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.HibernationOptionsProperty"]
        iamInstanceProfile: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.IamInstanceProfileProperty"]
        imageId: str
        instanceInitiatedShutdownBehavior: str
        instanceMarketOptions: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.InstanceMarketOptionsProperty"]
        instanceType: str
        kernelId: str
        keyName: str
        licenseSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.LicenseSpecificationProperty"]]]
        monitoring: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.MonitoringProperty"]
        networkInterfaces: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.NetworkInterfaceProperty"]]]
        placement: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.PlacementProperty"]
        ramDiskId: str
        securityGroupIds: typing.List[str]
        securityGroups: typing.List[str]
        tagSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.TagSpecificationProperty"]]]
        userData: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.LaunchTemplateElasticInferenceAcceleratorProperty")
    class LaunchTemplateElasticInferenceAcceleratorProperty(jsii.compat.TypedDict, total=False):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.LicenseSpecificationProperty")
    class LicenseSpecificationProperty(jsii.compat.TypedDict, total=False):
        licenseConfigurationArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.MonitoringProperty")
    class MonitoringProperty(jsii.compat.TypedDict, total=False):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.NetworkInterfaceProperty")
    class NetworkInterfaceProperty(jsii.compat.TypedDict, total=False):
        associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        description: str
        deviceIndex: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        groups: typing.List[str]
        ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        ipv6Addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.Ipv6AddProperty"]]]
        networkInterfaceId: str
        privateIpAddress: str
        privateIpAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.PrivateIpAddProperty"]]]
        secondaryPrivateIpAddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        subnetId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.PlacementProperty")
    class PlacementProperty(jsii.compat.TypedDict, total=False):
        affinity: str
        availabilityZone: str
        groupName: str
        hostId: str
        tenancy: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.PrivateIpAddProperty")
    class PrivateIpAddProperty(jsii.compat.TypedDict, total=False):
        primary: typing.Union[bool, aws_cdk.cdk.Token]
        privateIpAddress: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.SpotOptionsProperty")
    class SpotOptionsProperty(jsii.compat.TypedDict, total=False):
        instanceInterruptionBehavior: str
        maxPrice: str
        spotInstanceType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.TagSpecificationProperty")
    class TagSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceType: str
        tags: typing.List[aws_cdk.cdk.CfnTag]


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplateProps")
class CfnLaunchTemplateProps(jsii.compat.TypedDict, total=False):
    launchTemplateData: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.LaunchTemplateDataProperty"]
    launchTemplateName: str

class CfnNatGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNatGateway"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, allocation_id: str, subnet_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnNatGatewayProps = {"allocationId": allocation_id, "subnetId": subnet_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnNatGateway, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="natGatewayId")
    def nat_gateway_id(self) -> str:
        return jsii.get(self, "natGatewayId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNatGatewayProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnNatGatewayProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNatGatewayProps")
class CfnNatGatewayProps(_CfnNatGatewayProps):
    allocationId: str
    subnetId: str

class CfnNetworkAcl(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkAcl"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnNetworkAclProps = {"vpcId": vpc_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnNetworkAcl, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="networkAclName")
    def network_acl_name(self) -> str:
        return jsii.get(self, "networkAclName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkAclProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnNetworkAclEntry(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclEntry"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, network_acl_id: str, protocol: typing.Union[jsii.Number, aws_cdk.cdk.Token], rule_action: str, rule_number: typing.Union[jsii.Number, aws_cdk.cdk.Token], cidr_block: typing.Optional[str]=None, egress: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, icmp: typing.Optional[typing.Union[aws_cdk.cdk.Token, "IcmpProperty"]]=None, ipv6_cidr_block: typing.Optional[str]=None, port_range: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PortRangeProperty"]]=None) -> None:
        props: CfnNetworkAclEntryProps = {"networkAclId": network_acl_id, "protocol": protocol, "ruleAction": rule_action, "ruleNumber": rule_number}

        if cidr_block is not None:
            props["cidrBlock"] = cidr_block

        if egress is not None:
            props["egress"] = egress

        if icmp is not None:
            props["icmp"] = icmp

        if ipv6_cidr_block is not None:
            props["ipv6CidrBlock"] = ipv6_cidr_block

        if port_range is not None:
            props["portRange"] = port_range

        jsii.create(CfnNetworkAclEntry, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="networkAclEntryName")
    def network_acl_entry_name(self) -> str:
        return jsii.get(self, "networkAclEntryName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkAclEntryProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclEntry.IcmpProperty")
    class IcmpProperty(jsii.compat.TypedDict, total=False):
        code: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        type: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclEntry.PortRangeProperty")
    class PortRangeProperty(jsii.compat.TypedDict, total=False):
        from_: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        to: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnNetworkAclEntryProps(jsii.compat.TypedDict, total=False):
    cidrBlock: str
    egress: typing.Union[bool, aws_cdk.cdk.Token]
    icmp: typing.Union[aws_cdk.cdk.Token, "CfnNetworkAclEntry.IcmpProperty"]
    ipv6CidrBlock: str
    portRange: typing.Union[aws_cdk.cdk.Token, "CfnNetworkAclEntry.PortRangeProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclEntryProps")
class CfnNetworkAclEntryProps(_CfnNetworkAclEntryProps):
    networkAclId: str
    protocol: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    ruleAction: str
    ruleNumber: typing.Union[jsii.Number, aws_cdk.cdk.Token]

class _CfnNetworkAclProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclProps")
class CfnNetworkAclProps(_CfnNetworkAclProps):
    vpcId: str

class CfnNetworkInterface(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterface"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, subnet_id: str, description: typing.Optional[str]=None, group_set: typing.Optional[typing.List[str]]=None, interface_type: typing.Optional[str]=None, ipv6_address_count: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, ipv6_addresses: typing.Optional[typing.Union[aws_cdk.cdk.Token, "InstanceIpv6AddressProperty"]]=None, private_ip_address: typing.Optional[str]=None, private_ip_addresses: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "PrivateIpAddressSpecificationProperty"]]]]=None, secondary_private_ip_address_count: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, source_dest_check: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnNetworkInterfaceProps = {"subnetId": subnet_id}

        if description is not None:
            props["description"] = description

        if group_set is not None:
            props["groupSet"] = group_set

        if interface_type is not None:
            props["interfaceType"] = interface_type

        if ipv6_address_count is not None:
            props["ipv6AddressCount"] = ipv6_address_count

        if ipv6_addresses is not None:
            props["ipv6Addresses"] = ipv6_addresses

        if private_ip_address is not None:
            props["privateIpAddress"] = private_ip_address

        if private_ip_addresses is not None:
            props["privateIpAddresses"] = private_ip_addresses

        if secondary_private_ip_address_count is not None:
            props["secondaryPrivateIpAddressCount"] = secondary_private_ip_address_count

        if source_dest_check is not None:
            props["sourceDestCheck"] = source_dest_check

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnNetworkInterface, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="networkInterfaceName")
    def network_interface_name(self) -> str:
        return jsii.get(self, "networkInterfaceName")

    @property
    @jsii.member(jsii_name="networkInterfacePrimaryPrivateIpAddress")
    def network_interface_primary_private_ip_address(self) -> str:
        return jsii.get(self, "networkInterfacePrimaryPrivateIpAddress")

    @property
    @jsii.member(jsii_name="networkInterfaceSecondaryPrivateIpAddresses")
    def network_interface_secondary_private_ip_addresses(self) -> typing.List[str]:
        return jsii.get(self, "networkInterfaceSecondaryPrivateIpAddresses")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkInterfaceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterface.InstanceIpv6AddressProperty")
    class InstanceIpv6AddressProperty(jsii.compat.TypedDict):
        ipv6Address: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterface.PrivateIpAddressSpecificationProperty")
    class PrivateIpAddressSpecificationProperty(jsii.compat.TypedDict):
        primary: typing.Union[bool, aws_cdk.cdk.Token]
        privateIpAddress: str


class CfnNetworkInterfaceAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfaceAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, device_index: str, instance_id: str, network_interface_id: str, delete_on_termination: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnNetworkInterfaceAttachmentProps = {"deviceIndex": device_index, "instanceId": instance_id, "networkInterfaceId": network_interface_id}

        if delete_on_termination is not None:
            props["deleteOnTermination"] = delete_on_termination

        jsii.create(CfnNetworkInterfaceAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="networkInterfaceAttachmentName")
    def network_interface_attachment_name(self) -> str:
        return jsii.get(self, "networkInterfaceAttachmentName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkInterfaceAttachmentProps":
        return jsii.get(self, "propertyOverrides")


class _CfnNetworkInterfaceAttachmentProps(jsii.compat.TypedDict, total=False):
    deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfaceAttachmentProps")
class CfnNetworkInterfaceAttachmentProps(_CfnNetworkInterfaceAttachmentProps):
    deviceIndex: str
    instanceId: str
    networkInterfaceId: str

class CfnNetworkInterfacePermission(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfacePermission"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, aws_account_id: str, network_interface_id: str, permission: str) -> None:
        props: CfnNetworkInterfacePermissionProps = {"awsAccountId": aws_account_id, "networkInterfaceId": network_interface_id, "permission": permission}

        jsii.create(CfnNetworkInterfacePermission, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="networkInterfacePermissionId")
    def network_interface_permission_id(self) -> str:
        return jsii.get(self, "networkInterfacePermissionId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkInterfacePermissionProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfacePermissionProps")
class CfnNetworkInterfacePermissionProps(jsii.compat.TypedDict):
    awsAccountId: str
    networkInterfaceId: str
    permission: str

class _CfnNetworkInterfaceProps(jsii.compat.TypedDict, total=False):
    description: str
    groupSet: typing.List[str]
    interfaceType: str
    ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    ipv6Addresses: typing.Union[aws_cdk.cdk.Token, "CfnNetworkInterface.InstanceIpv6AddressProperty"]
    privateIpAddress: str
    privateIpAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnNetworkInterface.PrivateIpAddressSpecificationProperty"]]]
    secondaryPrivateIpAddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    sourceDestCheck: typing.Union[bool, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfaceProps")
class CfnNetworkInterfaceProps(_CfnNetworkInterfaceProps):
    subnetId: str

class CfnPlacementGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnPlacementGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, strategy: typing.Optional[str]=None) -> None:
        props: CfnPlacementGroupProps = {}

        if strategy is not None:
            props["strategy"] = strategy

        jsii.create(CfnPlacementGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="placementGroupName")
    def placement_group_name(self) -> str:
        return jsii.get(self, "placementGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPlacementGroupProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnPlacementGroupProps")
class CfnPlacementGroupProps(jsii.compat.TypedDict, total=False):
    strategy: str

class CfnRoute(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnRoute"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, route_table_id: str, destination_cidr_block: typing.Optional[str]=None, destination_ipv6_cidr_block: typing.Optional[str]=None, egress_only_internet_gateway_id: typing.Optional[str]=None, gateway_id: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, nat_gateway_id: typing.Optional[str]=None, network_interface_id: typing.Optional[str]=None, vpc_peering_connection_id: typing.Optional[str]=None) -> None:
        props: CfnRouteProps = {"routeTableId": route_table_id}

        if destination_cidr_block is not None:
            props["destinationCidrBlock"] = destination_cidr_block

        if destination_ipv6_cidr_block is not None:
            props["destinationIpv6CidrBlock"] = destination_ipv6_cidr_block

        if egress_only_internet_gateway_id is not None:
            props["egressOnlyInternetGatewayId"] = egress_only_internet_gateway_id

        if gateway_id is not None:
            props["gatewayId"] = gateway_id

        if instance_id is not None:
            props["instanceId"] = instance_id

        if nat_gateway_id is not None:
            props["natGatewayId"] = nat_gateway_id

        if network_interface_id is not None:
            props["networkInterfaceId"] = network_interface_id

        if vpc_peering_connection_id is not None:
            props["vpcPeeringConnectionId"] = vpc_peering_connection_id

        jsii.create(CfnRoute, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRouteProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> str:
        return jsii.get(self, "routeName")


class _CfnRouteProps(jsii.compat.TypedDict, total=False):
    destinationCidrBlock: str
    destinationIpv6CidrBlock: str
    egressOnlyInternetGatewayId: str
    gatewayId: str
    instanceId: str
    natGatewayId: str
    networkInterfaceId: str
    vpcPeeringConnectionId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnRouteProps")
class CfnRouteProps(_CfnRouteProps):
    routeTableId: str

class CfnRouteTable(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnRouteTable"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnRouteTableProps = {"vpcId": vpc_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnRouteTable, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnRouteTableProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> str:
        return jsii.get(self, "routeTableId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnRouteTableProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnRouteTableProps")
class CfnRouteTableProps(_CfnRouteTableProps):
    vpcId: str

class CfnSecurityGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_description: str, group_name: typing.Optional[str]=None, security_group_egress: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "EgressProperty"]]]]=None, security_group_ingress: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "IngressProperty"]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_id: typing.Optional[str]=None) -> None:
        props: CfnSecurityGroupProps = {"groupDescription": group_description}

        if group_name is not None:
            props["groupName"] = group_name

        if security_group_egress is not None:
            props["securityGroupEgress"] = security_group_egress

        if security_group_ingress is not None:
            props["securityGroupIngress"] = security_group_ingress

        if tags is not None:
            props["tags"] = tags

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(CfnSecurityGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSecurityGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        return jsii.get(self, "securityGroupId")

    @property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> str:
        return jsii.get(self, "securityGroupName")

    @property
    @jsii.member(jsii_name="securityGroupVpcId")
    def security_group_vpc_id(self) -> str:
        return jsii.get(self, "securityGroupVpcId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _EgressProperty(jsii.compat.TypedDict, total=False):
        cidrIp: str
        cidrIpv6: str
        description: str
        destinationPrefixListId: str
        destinationSecurityGroupId: str
        fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroup.EgressProperty")
    class EgressProperty(_EgressProperty):
        ipProtocol: str

    class _IngressProperty(jsii.compat.TypedDict, total=False):
        cidrIp: str
        cidrIpv6: str
        description: str
        fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        sourcePrefixListId: str
        sourceSecurityGroupId: str
        sourceSecurityGroupName: str
        sourceSecurityGroupOwnerId: str
        toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroup.IngressProperty")
    class IngressProperty(_IngressProperty):
        ipProtocol: str


class CfnSecurityGroupEgress(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupEgress"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_id: str, ip_protocol: str, cidr_ip: typing.Optional[str]=None, cidr_ipv6: typing.Optional[str]=None, description: typing.Optional[str]=None, destination_prefix_list_id: typing.Optional[str]=None, destination_security_group_id: typing.Optional[str]=None, from_port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, to_port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnSecurityGroupEgressProps = {"groupId": group_id, "ipProtocol": ip_protocol}

        if cidr_ip is not None:
            props["cidrIp"] = cidr_ip

        if cidr_ipv6 is not None:
            props["cidrIpv6"] = cidr_ipv6

        if description is not None:
            props["description"] = description

        if destination_prefix_list_id is not None:
            props["destinationPrefixListId"] = destination_prefix_list_id

        if destination_security_group_id is not None:
            props["destinationSecurityGroupId"] = destination_security_group_id

        if from_port is not None:
            props["fromPort"] = from_port

        if to_port is not None:
            props["toPort"] = to_port

        jsii.create(CfnSecurityGroupEgress, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSecurityGroupEgressProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="securityGroupEgressId")
    def security_group_egress_id(self) -> str:
        return jsii.get(self, "securityGroupEgressId")


class _CfnSecurityGroupEgressProps(jsii.compat.TypedDict, total=False):
    cidrIp: str
    cidrIpv6: str
    description: str
    destinationPrefixListId: str
    destinationSecurityGroupId: str
    fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupEgressProps")
class CfnSecurityGroupEgressProps(_CfnSecurityGroupEgressProps):
    groupId: str
    ipProtocol: str

class CfnSecurityGroupIngress(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupIngress"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ip_protocol: str, cidr_ip: typing.Optional[str]=None, cidr_ipv6: typing.Optional[str]=None, description: typing.Optional[str]=None, from_port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, group_id: typing.Optional[str]=None, group_name: typing.Optional[str]=None, source_prefix_list_id: typing.Optional[str]=None, source_security_group_id: typing.Optional[str]=None, source_security_group_name: typing.Optional[str]=None, source_security_group_owner_id: typing.Optional[str]=None, to_port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnSecurityGroupIngressProps = {"ipProtocol": ip_protocol}

        if cidr_ip is not None:
            props["cidrIp"] = cidr_ip

        if cidr_ipv6 is not None:
            props["cidrIpv6"] = cidr_ipv6

        if description is not None:
            props["description"] = description

        if from_port is not None:
            props["fromPort"] = from_port

        if group_id is not None:
            props["groupId"] = group_id

        if group_name is not None:
            props["groupName"] = group_name

        if source_prefix_list_id is not None:
            props["sourcePrefixListId"] = source_prefix_list_id

        if source_security_group_id is not None:
            props["sourceSecurityGroupId"] = source_security_group_id

        if source_security_group_name is not None:
            props["sourceSecurityGroupName"] = source_security_group_name

        if source_security_group_owner_id is not None:
            props["sourceSecurityGroupOwnerId"] = source_security_group_owner_id

        if to_port is not None:
            props["toPort"] = to_port

        jsii.create(CfnSecurityGroupIngress, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSecurityGroupIngressProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="securityGroupIngressId")
    def security_group_ingress_id(self) -> str:
        return jsii.get(self, "securityGroupIngressId")


class _CfnSecurityGroupIngressProps(jsii.compat.TypedDict, total=False):
    cidrIp: str
    cidrIpv6: str
    description: str
    fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    groupId: str
    groupName: str
    sourcePrefixListId: str
    sourceSecurityGroupId: str
    sourceSecurityGroupName: str
    sourceSecurityGroupOwnerId: str
    toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupIngressProps")
class CfnSecurityGroupIngressProps(_CfnSecurityGroupIngressProps):
    ipProtocol: str

class _CfnSecurityGroupProps(jsii.compat.TypedDict, total=False):
    groupName: str
    securityGroupEgress: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSecurityGroup.EgressProperty"]]]
    securityGroupIngress: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSecurityGroup.IngressProperty"]]]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupProps")
class CfnSecurityGroupProps(_CfnSecurityGroupProps):
    groupDescription: str

class CfnSpotFleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, spot_fleet_request_config_data: typing.Union[aws_cdk.cdk.Token, "SpotFleetRequestConfigDataProperty"]) -> None:
        props: CfnSpotFleetProps = {"spotFleetRequestConfigData": spot_fleet_request_config_data}

        jsii.create(CfnSpotFleet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSpotFleetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="spotFleetName")
    def spot_fleet_name(self) -> str:
        return jsii.get(self, "spotFleetName")

    class _BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        ebs: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.EbsBlockDeviceProperty"]
        noDevice: str
        virtualName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.BlockDeviceMappingProperty")
    class BlockDeviceMappingProperty(_BlockDeviceMappingProperty):
        deviceName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.ClassicLoadBalancerProperty")
    class ClassicLoadBalancerProperty(jsii.compat.TypedDict):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.ClassicLoadBalancersConfigProperty")
    class ClassicLoadBalancersConfigProperty(jsii.compat.TypedDict):
        classicLoadBalancers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.ClassicLoadBalancerProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.EbsBlockDeviceProperty")
    class EbsBlockDeviceProperty(jsii.compat.TypedDict, total=False):
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        snapshotId: str
        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str

    class _FleetLaunchTemplateSpecificationProperty(jsii.compat.TypedDict, total=False):
        launchTemplateId: str
        launchTemplateName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.FleetLaunchTemplateSpecificationProperty")
    class FleetLaunchTemplateSpecificationProperty(_FleetLaunchTemplateSpecificationProperty):
        version: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.GroupIdentifierProperty")
    class GroupIdentifierProperty(jsii.compat.TypedDict):
        groupId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.IamInstanceProfileSpecificationProperty")
    class IamInstanceProfileSpecificationProperty(jsii.compat.TypedDict, total=False):
        arn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.InstanceIpv6AddressProperty")
    class InstanceIpv6AddressProperty(jsii.compat.TypedDict):
        ipv6Address: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty")
    class InstanceNetworkInterfaceSpecificationProperty(jsii.compat.TypedDict, total=False):
        associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        description: str
        deviceIndex: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        groups: typing.List[str]
        ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        ipv6Addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.InstanceIpv6AddressProperty"]]]
        networkInterfaceId: str
        privateIpAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.PrivateIpAddressSpecificationProperty"]]]
        secondaryPrivateIpAddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        subnetId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.LaunchTemplateConfigProperty")
    class LaunchTemplateConfigProperty(jsii.compat.TypedDict, total=False):
        launchTemplateSpecification: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.FleetLaunchTemplateSpecificationProperty"]
        overrides: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.LaunchTemplateOverridesProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.LaunchTemplateOverridesProperty")
    class LaunchTemplateOverridesProperty(jsii.compat.TypedDict, total=False):
        availabilityZone: str
        instanceType: str
        spotPrice: str
        subnetId: str
        weightedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.LoadBalancersConfigProperty")
    class LoadBalancersConfigProperty(jsii.compat.TypedDict, total=False):
        classicLoadBalancersConfig: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.ClassicLoadBalancersConfigProperty"]
        targetGroupsConfig: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.TargetGroupsConfigProperty"]

    class _PrivateIpAddressSpecificationProperty(jsii.compat.TypedDict, total=False):
        primary: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.PrivateIpAddressSpecificationProperty")
    class PrivateIpAddressSpecificationProperty(_PrivateIpAddressSpecificationProperty):
        privateIpAddress: str

    class _SpotFleetLaunchSpecificationProperty(jsii.compat.TypedDict, total=False):
        blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.BlockDeviceMappingProperty"]]]
        ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
        iamInstanceProfile: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.IamInstanceProfileSpecificationProperty"]
        kernelId: str
        keyName: str
        monitoring: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotFleetMonitoringProperty"]
        networkInterfaces: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty"]]]
        placement: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotPlacementProperty"]
        ramdiskId: str
        securityGroups: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.GroupIdentifierProperty"]]]
        spotPrice: str
        subnetId: str
        tagSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotFleetTagSpecificationProperty"]]]
        userData: str
        weightedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty")
    class SpotFleetLaunchSpecificationProperty(_SpotFleetLaunchSpecificationProperty):
        imageId: str
        instanceType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotFleetMonitoringProperty")
    class SpotFleetMonitoringProperty(jsii.compat.TypedDict, total=False):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    class _SpotFleetRequestConfigDataProperty(jsii.compat.TypedDict, total=False):
        allocationStrategy: str
        excessCapacityTerminationPolicy: str
        instanceInterruptionBehavior: str
        launchSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotFleetLaunchSpecificationProperty"]]]
        launchTemplateConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.LaunchTemplateConfigProperty"]]]
        loadBalancersConfig: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.LoadBalancersConfigProperty"]
        replaceUnhealthyInstances: typing.Union[bool, aws_cdk.cdk.Token]
        spotPrice: str
        terminateInstancesWithExpiration: typing.Union[bool, aws_cdk.cdk.Token]
        type: str
        validFrom: str
        validUntil: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotFleetRequestConfigDataProperty")
    class SpotFleetRequestConfigDataProperty(_SpotFleetRequestConfigDataProperty):
        iamFleetRole: str
        targetCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotFleetTagSpecificationProperty")
    class SpotFleetTagSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceType: str
        tags: typing.List[aws_cdk.cdk.CfnTag]

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotPlacementProperty")
    class SpotPlacementProperty(jsii.compat.TypedDict, total=False):
        availabilityZone: str
        groupName: str
        tenancy: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.TargetGroupProperty")
    class TargetGroupProperty(jsii.compat.TypedDict):
        arn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.TargetGroupsConfigProperty")
    class TargetGroupsConfigProperty(jsii.compat.TypedDict):
        targetGroups: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.TargetGroupProperty"]]]


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleetProps")
class CfnSpotFleetProps(jsii.compat.TypedDict):
    spotFleetRequestConfigData: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotFleetRequestConfigDataProperty"]

class CfnSubnet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSubnet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cidr_block: str, vpc_id: str, assign_ipv6_address_on_creation: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, availability_zone: typing.Optional[str]=None, ipv6_cidr_block: typing.Optional[str]=None, map_public_ip_on_launch: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnSubnetProps = {"cidrBlock": cidr_block, "vpcId": vpc_id}

        if assign_ipv6_address_on_creation is not None:
            props["assignIpv6AddressOnCreation"] = assign_ipv6_address_on_creation

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if ipv6_cidr_block is not None:
            props["ipv6CidrBlock"] = ipv6_cidr_block

        if map_public_ip_on_launch is not None:
            props["mapPublicIpOnLaunch"] = map_public_ip_on_launch

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnSubnet, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubnetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetAvailabilityZone")
    def subnet_availability_zone(self) -> str:
        return jsii.get(self, "subnetAvailabilityZone")

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        return jsii.get(self, "subnetId")

    @property
    @jsii.member(jsii_name="subnetIpv6CidrBlocks")
    def subnet_ipv6_cidr_blocks(self) -> typing.List[str]:
        return jsii.get(self, "subnetIpv6CidrBlocks")

    @property
    @jsii.member(jsii_name="subnetNetworkAclAssociationId")
    def subnet_network_acl_association_id(self) -> str:
        return jsii.get(self, "subnetNetworkAclAssociationId")

    @property
    @jsii.member(jsii_name="subnetVpcId")
    def subnet_vpc_id(self) -> str:
        return jsii.get(self, "subnetVpcId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnSubnetCidrBlock(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSubnetCidrBlock"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ipv6_cidr_block: str, subnet_id: str) -> None:
        props: CfnSubnetCidrBlockProps = {"ipv6CidrBlock": ipv6_cidr_block, "subnetId": subnet_id}

        jsii.create(CfnSubnetCidrBlock, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubnetCidrBlockProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetCidrBlockId")
    def subnet_cidr_block_id(self) -> str:
        return jsii.get(self, "subnetCidrBlockId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSubnetCidrBlockProps")
class CfnSubnetCidrBlockProps(jsii.compat.TypedDict):
    ipv6CidrBlock: str
    subnetId: str

class CfnSubnetNetworkAclAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSubnetNetworkAclAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, network_acl_id: str, subnet_id: str) -> None:
        props: CfnSubnetNetworkAclAssociationProps = {"networkAclId": network_acl_id, "subnetId": subnet_id}

        jsii.create(CfnSubnetNetworkAclAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubnetNetworkAclAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetNetworkAclAssociationAssociationId")
    def subnet_network_acl_association_association_id(self) -> str:
        return jsii.get(self, "subnetNetworkAclAssociationAssociationId")

    @property
    @jsii.member(jsii_name="subnetNetworkAclAssociationName")
    def subnet_network_acl_association_name(self) -> str:
        return jsii.get(self, "subnetNetworkAclAssociationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSubnetNetworkAclAssociationProps")
class CfnSubnetNetworkAclAssociationProps(jsii.compat.TypedDict):
    networkAclId: str
    subnetId: str

class _CfnSubnetProps(jsii.compat.TypedDict, total=False):
    assignIpv6AddressOnCreation: typing.Union[bool, aws_cdk.cdk.Token]
    availabilityZone: str
    ipv6CidrBlock: str
    mapPublicIpOnLaunch: typing.Union[bool, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSubnetProps")
class CfnSubnetProps(_CfnSubnetProps):
    cidrBlock: str
    vpcId: str

class CfnSubnetRouteTableAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSubnetRouteTableAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, route_table_id: str, subnet_id: str) -> None:
        props: CfnSubnetRouteTableAssociationProps = {"routeTableId": route_table_id, "subnetId": subnet_id}

        jsii.create(CfnSubnetRouteTableAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubnetRouteTableAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetRouteTableAssociationName")
    def subnet_route_table_association_name(self) -> str:
        return jsii.get(self, "subnetRouteTableAssociationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSubnetRouteTableAssociationProps")
class CfnSubnetRouteTableAssociationProps(jsii.compat.TypedDict):
    routeTableId: str
    subnetId: str

class CfnTransitGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGateway"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, amazon_side_asn: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, auto_accept_shared_attachments: typing.Optional[str]=None, default_route_table_association: typing.Optional[str]=None, default_route_table_propagation: typing.Optional[str]=None, description: typing.Optional[str]=None, dns_support: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpn_ecmp_support: typing.Optional[str]=None) -> None:
        props: CfnTransitGatewayProps = {}

        if amazon_side_asn is not None:
            props["amazonSideAsn"] = amazon_side_asn

        if auto_accept_shared_attachments is not None:
            props["autoAcceptSharedAttachments"] = auto_accept_shared_attachments

        if default_route_table_association is not None:
            props["defaultRouteTableAssociation"] = default_route_table_association

        if default_route_table_propagation is not None:
            props["defaultRouteTablePropagation"] = default_route_table_propagation

        if description is not None:
            props["description"] = description

        if dns_support is not None:
            props["dnsSupport"] = dns_support

        if tags is not None:
            props["tags"] = tags

        if vpn_ecmp_support is not None:
            props["vpnEcmpSupport"] = vpn_ecmp_support

        jsii.create(CfnTransitGateway, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTransitGatewayProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="transitGatewayId")
    def transit_gateway_id(self) -> str:
        return jsii.get(self, "transitGatewayId")


class CfnTransitGatewayAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, subnet_ids: typing.List[str], transit_gateway_id: str, vpc_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnTransitGatewayAttachmentProps = {"subnetIds": subnet_ids, "transitGatewayId": transit_gateway_id, "vpcId": vpc_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnTransitGatewayAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTransitGatewayAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> str:
        return jsii.get(self, "transitGatewayAttachmentId")


class _CfnTransitGatewayAttachmentProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayAttachmentProps")
class CfnTransitGatewayAttachmentProps(_CfnTransitGatewayAttachmentProps):
    subnetIds: typing.List[str]
    transitGatewayId: str
    vpcId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayProps")
class CfnTransitGatewayProps(jsii.compat.TypedDict, total=False):
    amazonSideAsn: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    autoAcceptSharedAttachments: str
    defaultRouteTableAssociation: str
    defaultRouteTablePropagation: str
    description: str
    dnsSupport: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpnEcmpSupport: str

class CfnTransitGatewayRoute(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRoute"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, transit_gateway_route_table_id: str, blackhole: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, destination_cidr_block: typing.Optional[str]=None, transit_gateway_attachment_id: typing.Optional[str]=None) -> None:
        props: CfnTransitGatewayRouteProps = {"transitGatewayRouteTableId": transit_gateway_route_table_id}

        if blackhole is not None:
            props["blackhole"] = blackhole

        if destination_cidr_block is not None:
            props["destinationCidrBlock"] = destination_cidr_block

        if transit_gateway_attachment_id is not None:
            props["transitGatewayAttachmentId"] = transit_gateway_attachment_id

        jsii.create(CfnTransitGatewayRoute, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTransitGatewayRouteProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="transitGatewayRouteId")
    def transit_gateway_route_id(self) -> str:
        return jsii.get(self, "transitGatewayRouteId")


class _CfnTransitGatewayRouteProps(jsii.compat.TypedDict, total=False):
    blackhole: typing.Union[bool, aws_cdk.cdk.Token]
    destinationCidrBlock: str
    transitGatewayAttachmentId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteProps")
class CfnTransitGatewayRouteProps(_CfnTransitGatewayRouteProps):
    transitGatewayRouteTableId: str

class CfnTransitGatewayRouteTable(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTable"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, transit_gateway_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnTransitGatewayRouteTableProps = {"transitGatewayId": transit_gateway_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnTransitGatewayRouteTable, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTransitGatewayRouteTableProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="transitGatewayRouteTableId")
    def transit_gateway_route_table_id(self) -> str:
        return jsii.get(self, "transitGatewayRouteTableId")


class CfnTransitGatewayRouteTableAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTableAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, transit_gateway_attachment_id: str, transit_gateway_route_table_id: str) -> None:
        props: CfnTransitGatewayRouteTableAssociationProps = {"transitGatewayAttachmentId": transit_gateway_attachment_id, "transitGatewayRouteTableId": transit_gateway_route_table_id}

        jsii.create(CfnTransitGatewayRouteTableAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTransitGatewayRouteTableAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="transitGatewayRouteTableAssociationId")
    def transit_gateway_route_table_association_id(self) -> str:
        return jsii.get(self, "transitGatewayRouteTableAssociationId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTableAssociationProps")
class CfnTransitGatewayRouteTableAssociationProps(jsii.compat.TypedDict):
    transitGatewayAttachmentId: str
    transitGatewayRouteTableId: str

class CfnTransitGatewayRouteTablePropagation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTablePropagation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, transit_gateway_attachment_id: str, transit_gateway_route_table_id: str) -> None:
        props: CfnTransitGatewayRouteTablePropagationProps = {"transitGatewayAttachmentId": transit_gateway_attachment_id, "transitGatewayRouteTableId": transit_gateway_route_table_id}

        jsii.create(CfnTransitGatewayRouteTablePropagation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTransitGatewayRouteTablePropagationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="transitGatewayRouteTablePropagationId")
    def transit_gateway_route_table_propagation_id(self) -> str:
        return jsii.get(self, "transitGatewayRouteTablePropagationId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTablePropagationProps")
class CfnTransitGatewayRouteTablePropagationProps(jsii.compat.TypedDict):
    transitGatewayAttachmentId: str
    transitGatewayRouteTableId: str

class _CfnTransitGatewayRouteTableProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTableProps")
class CfnTransitGatewayRouteTableProps(_CfnTransitGatewayRouteTableProps):
    transitGatewayId: str

class CfnTrunkInterfaceAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTrunkInterfaceAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, branch_interface_id: str, trunk_interface_id: str, gre_key: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, vlan_id: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnTrunkInterfaceAssociationProps = {"branchInterfaceId": branch_interface_id, "trunkInterfaceId": trunk_interface_id}

        if gre_key is not None:
            props["greKey"] = gre_key

        if vlan_id is not None:
            props["vlanId"] = vlan_id

        jsii.create(CfnTrunkInterfaceAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTrunkInterfaceAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="trunkInterfaceAssociationId")
    def trunk_interface_association_id(self) -> str:
        return jsii.get(self, "trunkInterfaceAssociationId")


class _CfnTrunkInterfaceAssociationProps(jsii.compat.TypedDict, total=False):
    greKey: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    vlanId: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTrunkInterfaceAssociationProps")
class CfnTrunkInterfaceAssociationProps(_CfnTrunkInterfaceAssociationProps):
    branchInterfaceId: str
    trunkInterfaceId: str

class CfnVPC(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPC"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cidr_block: str, enable_dns_hostnames: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, enable_dns_support: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, instance_tenancy: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnVPCProps = {"cidrBlock": cidr_block}

        if enable_dns_hostnames is not None:
            props["enableDnsHostnames"] = enable_dns_hostnames

        if enable_dns_support is not None:
            props["enableDnsSupport"] = enable_dns_support

        if instance_tenancy is not None:
            props["instanceTenancy"] = instance_tenancy

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVPC, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="vpcCidrBlock")
    def vpc_cidr_block(self) -> str:
        return jsii.get(self, "vpcCidrBlock")

    @property
    @jsii.member(jsii_name="vpcCidrBlockAssociations")
    def vpc_cidr_block_associations(self) -> typing.List[str]:
        return jsii.get(self, "vpcCidrBlockAssociations")

    @property
    @jsii.member(jsii_name="vpcDefaultNetworkAcl")
    def vpc_default_network_acl(self) -> str:
        return jsii.get(self, "vpcDefaultNetworkAcl")

    @property
    @jsii.member(jsii_name="vpcDefaultSecurityGroup")
    def vpc_default_security_group(self) -> str:
        return jsii.get(self, "vpcDefaultSecurityGroup")

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        return jsii.get(self, "vpcId")

    @property
    @jsii.member(jsii_name="vpcIpv6CidrBlocks")
    def vpc_ipv6_cidr_blocks(self) -> typing.List[str]:
        return jsii.get(self, "vpcIpv6CidrBlocks")


class CfnVPCCidrBlock(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCCidrBlock"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str, amazon_provided_ipv6_cidr_block: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, cidr_block: typing.Optional[str]=None) -> None:
        props: CfnVPCCidrBlockProps = {"vpcId": vpc_id}

        if amazon_provided_ipv6_cidr_block is not None:
            props["amazonProvidedIpv6CidrBlock"] = amazon_provided_ipv6_cidr_block

        if cidr_block is not None:
            props["cidrBlock"] = cidr_block

        jsii.create(CfnVPCCidrBlock, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCCidrBlockProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcCidrBlockId")
    def vpc_cidr_block_id(self) -> str:
        return jsii.get(self, "vpcCidrBlockId")


class _CfnVPCCidrBlockProps(jsii.compat.TypedDict, total=False):
    amazonProvidedIpv6CidrBlock: typing.Union[bool, aws_cdk.cdk.Token]
    cidrBlock: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCCidrBlockProps")
class CfnVPCCidrBlockProps(_CfnVPCCidrBlockProps):
    vpcId: str

class CfnVPCDHCPOptionsAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCDHCPOptionsAssociation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dhcp_options_id: str, vpc_id: str) -> None:
        props: CfnVPCDHCPOptionsAssociationProps = {"dhcpOptionsId": dhcp_options_id, "vpcId": vpc_id}

        jsii.create(CfnVPCDHCPOptionsAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCDHCPOptionsAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcdhcpOptionsAssociationName")
    def vpcdhcp_options_association_name(self) -> str:
        return jsii.get(self, "vpcdhcpOptionsAssociationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCDHCPOptionsAssociationProps")
class CfnVPCDHCPOptionsAssociationProps(jsii.compat.TypedDict):
    dhcpOptionsId: str
    vpcId: str

class CfnVPCEndpoint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpoint"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service_name: str, vpc_id: str, policy_document: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, private_dns_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, route_table_ids: typing.Optional[typing.List[str]]=None, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_ids: typing.Optional[typing.List[str]]=None, vpc_endpoint_type: typing.Optional[str]=None) -> None:
        props: CfnVPCEndpointProps = {"serviceName": service_name, "vpcId": vpc_id}

        if policy_document is not None:
            props["policyDocument"] = policy_document

        if private_dns_enabled is not None:
            props["privateDnsEnabled"] = private_dns_enabled

        if route_table_ids is not None:
            props["routeTableIds"] = route_table_ids

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if subnet_ids is not None:
            props["subnetIds"] = subnet_ids

        if vpc_endpoint_type is not None:
            props["vpcEndpointType"] = vpc_endpoint_type

        jsii.create(CfnVPCEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCEndpointProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcEndpointCreationTimestamp")
    def vpc_endpoint_creation_timestamp(self) -> str:
        return jsii.get(self, "vpcEndpointCreationTimestamp")

    @property
    @jsii.member(jsii_name="vpcEndpointDnsEntries")
    def vpc_endpoint_dns_entries(self) -> typing.List[str]:
        return jsii.get(self, "vpcEndpointDnsEntries")

    @property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> str:
        return jsii.get(self, "vpcEndpointId")

    @property
    @jsii.member(jsii_name="vpcEndpointNetworkInterfaceIds")
    def vpc_endpoint_network_interface_ids(self) -> typing.List[str]:
        return jsii.get(self, "vpcEndpointNetworkInterfaceIds")


class CfnVPCEndpointConnectionNotification(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointConnectionNotification"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, connection_events: typing.List[str], connection_notification_arn: str, service_id: typing.Optional[str]=None, vpc_endpoint_id: typing.Optional[str]=None) -> None:
        props: CfnVPCEndpointConnectionNotificationProps = {"connectionEvents": connection_events, "connectionNotificationArn": connection_notification_arn}

        if service_id is not None:
            props["serviceId"] = service_id

        if vpc_endpoint_id is not None:
            props["vpcEndpointId"] = vpc_endpoint_id

        jsii.create(CfnVPCEndpointConnectionNotification, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCEndpointConnectionNotificationProps":
        return jsii.get(self, "propertyOverrides")


class _CfnVPCEndpointConnectionNotificationProps(jsii.compat.TypedDict, total=False):
    serviceId: str
    vpcEndpointId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointConnectionNotificationProps")
class CfnVPCEndpointConnectionNotificationProps(_CfnVPCEndpointConnectionNotificationProps):
    connectionEvents: typing.List[str]
    connectionNotificationArn: str

class _CfnVPCEndpointProps(jsii.compat.TypedDict, total=False):
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    privateDnsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    routeTableIds: typing.List[str]
    securityGroupIds: typing.List[str]
    subnetIds: typing.List[str]
    vpcEndpointType: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointProps")
class CfnVPCEndpointProps(_CfnVPCEndpointProps):
    serviceName: str
    vpcId: str

class CfnVPCEndpointService(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointService"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, network_load_balancer_arns: typing.List[str], acceptance_required: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnVPCEndpointServiceProps = {"networkLoadBalancerArns": network_load_balancer_arns}

        if acceptance_required is not None:
            props["acceptanceRequired"] = acceptance_required

        jsii.create(CfnVPCEndpointService, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCEndpointServiceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcEndpointServiceId")
    def vpc_endpoint_service_id(self) -> str:
        return jsii.get(self, "vpcEndpointServiceId")


class CfnVPCEndpointServicePermissions(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointServicePermissions"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service_id: str, allowed_principals: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnVPCEndpointServicePermissionsProps = {"serviceId": service_id}

        if allowed_principals is not None:
            props["allowedPrincipals"] = allowed_principals

        jsii.create(CfnVPCEndpointServicePermissions, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCEndpointServicePermissionsProps":
        return jsii.get(self, "propertyOverrides")


class _CfnVPCEndpointServicePermissionsProps(jsii.compat.TypedDict, total=False):
    allowedPrincipals: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointServicePermissionsProps")
class CfnVPCEndpointServicePermissionsProps(_CfnVPCEndpointServicePermissionsProps):
    serviceId: str

class _CfnVPCEndpointServiceProps(jsii.compat.TypedDict, total=False):
    acceptanceRequired: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointServiceProps")
class CfnVPCEndpointServiceProps(_CfnVPCEndpointServiceProps):
    networkLoadBalancerArns: typing.List[str]

class CfnVPCGatewayAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCGatewayAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str, internet_gateway_id: typing.Optional[str]=None, vpn_gateway_id: typing.Optional[str]=None) -> None:
        props: CfnVPCGatewayAttachmentProps = {"vpcId": vpc_id}

        if internet_gateway_id is not None:
            props["internetGatewayId"] = internet_gateway_id

        if vpn_gateway_id is not None:
            props["vpnGatewayId"] = vpn_gateway_id

        jsii.create(CfnVPCGatewayAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCGatewayAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcGatewayAttachmentName")
    def vpc_gateway_attachment_name(self) -> str:
        return jsii.get(self, "vpcGatewayAttachmentName")


class _CfnVPCGatewayAttachmentProps(jsii.compat.TypedDict, total=False):
    internetGatewayId: str
    vpnGatewayId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCGatewayAttachmentProps")
class CfnVPCGatewayAttachmentProps(_CfnVPCGatewayAttachmentProps):
    vpcId: str

class CfnVPCPeeringConnection(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCPeeringConnection"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, peer_vpc_id: str, vpc_id: str, peer_owner_id: typing.Optional[str]=None, peer_region: typing.Optional[str]=None, peer_role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnVPCPeeringConnectionProps = {"peerVpcId": peer_vpc_id, "vpcId": vpc_id}

        if peer_owner_id is not None:
            props["peerOwnerId"] = peer_owner_id

        if peer_region is not None:
            props["peerRegion"] = peer_region

        if peer_role_arn is not None:
            props["peerRoleArn"] = peer_role_arn

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVPCPeeringConnection, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPCPeeringConnectionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="vpcPeeringConnectionName")
    def vpc_peering_connection_name(self) -> str:
        return jsii.get(self, "vpcPeeringConnectionName")


class _CfnVPCPeeringConnectionProps(jsii.compat.TypedDict, total=False):
    peerOwnerId: str
    peerRegion: str
    peerRoleArn: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCPeeringConnectionProps")
class CfnVPCPeeringConnectionProps(_CfnVPCPeeringConnectionProps):
    peerVpcId: str
    vpcId: str

class _CfnVPCProps(jsii.compat.TypedDict, total=False):
    enableDnsHostnames: typing.Union[bool, aws_cdk.cdk.Token]
    enableDnsSupport: typing.Union[bool, aws_cdk.cdk.Token]
    instanceTenancy: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCProps")
class CfnVPCProps(_CfnVPCProps):
    cidrBlock: str

class CfnVPNConnection(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPNConnection"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, customer_gateway_id: str, type: str, vpn_gateway_id: str, static_routes_only: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpn_tunnel_options_specifications: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "VpnTunnelOptionsSpecificationProperty"]]]]=None) -> None:
        props: CfnVPNConnectionProps = {"customerGatewayId": customer_gateway_id, "type": type, "vpnGatewayId": vpn_gateway_id}

        if static_routes_only is not None:
            props["staticRoutesOnly"] = static_routes_only

        if tags is not None:
            props["tags"] = tags

        if vpn_tunnel_options_specifications is not None:
            props["vpnTunnelOptionsSpecifications"] = vpn_tunnel_options_specifications

        jsii.create(CfnVPNConnection, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPNConnectionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="vpnConnectionName")
    def vpn_connection_name(self) -> str:
        return jsii.get(self, "vpnConnectionName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNConnection.VpnTunnelOptionsSpecificationProperty")
    class VpnTunnelOptionsSpecificationProperty(jsii.compat.TypedDict, total=False):
        preSharedKey: str
        tunnelInsideCidr: str


class _CfnVPNConnectionProps(jsii.compat.TypedDict, total=False):
    staticRoutesOnly: typing.Union[bool, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpnTunnelOptionsSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnVPNConnection.VpnTunnelOptionsSpecificationProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNConnectionProps")
class CfnVPNConnectionProps(_CfnVPNConnectionProps):
    customerGatewayId: str
    type: str
    vpnGatewayId: str

class CfnVPNConnectionRoute(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPNConnectionRoute"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, destination_cidr_block: str, vpn_connection_id: str) -> None:
        props: CfnVPNConnectionRouteProps = {"destinationCidrBlock": destination_cidr_block, "vpnConnectionId": vpn_connection_id}

        jsii.create(CfnVPNConnectionRoute, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPNConnectionRouteProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpnConnectionRouteName")
    def vpn_connection_route_name(self) -> str:
        return jsii.get(self, "vpnConnectionRouteName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNConnectionRouteProps")
class CfnVPNConnectionRouteProps(jsii.compat.TypedDict):
    destinationCidrBlock: str
    vpnConnectionId: str

class CfnVPNGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPNGateway"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, type: str, amazon_side_asn: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnVPNGatewayProps = {"type": type}

        if amazon_side_asn is not None:
            props["amazonSideAsn"] = amazon_side_asn

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVPNGateway, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPNGatewayProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="vpnGatewayName")
    def vpn_gateway_name(self) -> str:
        return jsii.get(self, "vpnGatewayName")


class _CfnVPNGatewayProps(jsii.compat.TypedDict, total=False):
    amazonSideAsn: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNGatewayProps")
class CfnVPNGatewayProps(_CfnVPNGatewayProps):
    type: str

class CfnVPNGatewayRoutePropagation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPNGatewayRoutePropagation"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, route_table_ids: typing.List[str], vpn_gateway_id: str) -> None:
        props: CfnVPNGatewayRoutePropagationProps = {"routeTableIds": route_table_ids, "vpnGatewayId": vpn_gateway_id}

        jsii.create(CfnVPNGatewayRoutePropagation, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVPNGatewayRoutePropagationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpnGatewayRoutePropagationName")
    def vpn_gateway_route_propagation_name(self) -> str:
        return jsii.get(self, "vpnGatewayRoutePropagationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNGatewayRoutePropagationProps")
class CfnVPNGatewayRoutePropagationProps(jsii.compat.TypedDict):
    routeTableIds: typing.List[str]
    vpnGatewayId: str

class CfnVolume(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVolume"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, auto_enable_io: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, encrypted: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, iops: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, kms_key_id: typing.Optional[str]=None, size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, snapshot_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, volume_type: typing.Optional[str]=None) -> None:
        props: CfnVolumeProps = {"availabilityZone": availability_zone}

        if auto_enable_io is not None:
            props["autoEnableIo"] = auto_enable_io

        if encrypted is not None:
            props["encrypted"] = encrypted

        if iops is not None:
            props["iops"] = iops

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if size is not None:
            props["size"] = size

        if snapshot_id is not None:
            props["snapshotId"] = snapshot_id

        if tags is not None:
            props["tags"] = tags

        if volume_type is not None:
            props["volumeType"] = volume_type

        jsii.create(CfnVolume, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVolumeProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> str:
        return jsii.get(self, "volumeId")


class CfnVolumeAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVolumeAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, device: str, instance_id: str, volume_id: str) -> None:
        props: CfnVolumeAttachmentProps = {"device": device, "instanceId": instance_id, "volumeId": volume_id}

        jsii.create(CfnVolumeAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVolumeAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="volumeAttachmentId")
    def volume_attachment_id(self) -> str:
        return jsii.get(self, "volumeAttachmentId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVolumeAttachmentProps")
class CfnVolumeAttachmentProps(jsii.compat.TypedDict):
    device: str
    instanceId: str
    volumeId: str

class _CfnVolumeProps(jsii.compat.TypedDict, total=False):
    autoEnableIo: typing.Union[bool, aws_cdk.cdk.Token]
    encrypted: typing.Union[bool, aws_cdk.cdk.Token]
    iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    kmsKeyId: str
    size: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    snapshotId: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    volumeType: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVolumeProps")
class CfnVolumeProps(_CfnVolumeProps):
    availabilityZone: str

class _ConnectionRule(jsii.compat.TypedDict, total=False):
    description: str
    protocol: str
    toPort: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.ConnectionRule")
class ConnectionRule(_ConnectionRule):
    fromPort: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.ConnectionsProps")
class ConnectionsProps(jsii.compat.TypedDict, total=False):
    defaultPortRange: "IPortRange"
    securityGroupRule: "ISecurityGroupRule"
    securityGroups: typing.List["ISecurityGroup"]

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.DefaultInstanceTenancy")
class DefaultInstanceTenancy(enum.Enum):
    Default = "Default"
    Dedicated = "Dedicated"

@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IConnectable")
class IConnectable(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IConnectableProxy

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        ...


class _IConnectableProxy():
    __jsii_type__ = "@aws-cdk/aws-ec2.IConnectable"
    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")


@jsii.implements(IConnectable)
class Connections(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.Connections"):
    def __init__(self, *, default_port_range: typing.Optional["IPortRange"]=None, security_group_rule: typing.Optional["ISecurityGroupRule"]=None, security_groups: typing.Optional[typing.List["ISecurityGroup"]]=None) -> None:
        props: ConnectionsProps = {}

        if default_port_range is not None:
            props["defaultPortRange"] = default_port_range

        if security_group_rule is not None:
            props["securityGroupRule"] = security_group_rule

        if security_groups is not None:
            props["securityGroups"] = security_groups

        jsii.create(Connections, self, [props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(self, *security_groups: "ISecurityGroup") -> None:
        return jsii.invoke(self, "addSecurityGroup", [security_groups])

    @jsii.member(jsii_name="allowDefaultPortFrom")
    def allow_default_port_from(self, other: "IConnectable", description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowDefaultPortFrom", [other, description])

    @jsii.member(jsii_name="allowDefaultPortFromAnyIpv4")
    def allow_default_port_from_any_ipv4(self, description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowDefaultPortFromAnyIpv4", [description])

    @jsii.member(jsii_name="allowDefaultPortInternally")
    def allow_default_port_internally(self, description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowDefaultPortInternally", [description])

    @jsii.member(jsii_name="allowDefaultPortTo")
    def allow_default_port_to(self, other: "IConnectable", description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowDefaultPortTo", [other, description])

    @jsii.member(jsii_name="allowFrom")
    def allow_from(self, other: "IConnectable", port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowFrom", [other, port_range, description])

    @jsii.member(jsii_name="allowFromAnyIPv4")
    def allow_from_any_i_pv4(self, port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowFromAnyIPv4", [port_range, description])

    @jsii.member(jsii_name="allowInternally")
    def allow_internally(self, port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowInternally", [port_range, description])

    @jsii.member(jsii_name="allowTo")
    def allow_to(self, other: "IConnectable", port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowTo", [other, port_range, description])

    @jsii.member(jsii_name="allowToAnyIPv4")
    def allow_to_any_i_pv4(self, port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowToAnyIPv4", [port_range, description])

    @jsii.member(jsii_name="allowToDefaultPort")
    def allow_to_default_port(self, other: "IConnectable", description: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "allowToDefaultPort", [other, description])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List["ISecurityGroup"]:
        return jsii.get(self, "securityGroups")

    @property
    @jsii.member(jsii_name="defaultPortRange")
    def default_port_range(self) -> typing.Optional["IPortRange"]:
        return jsii.get(self, "defaultPortRange")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IMachineImageSource")
class IMachineImageSource(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IMachineImageSourceProxy

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        ...


class _IMachineImageSourceProxy():
    __jsii_type__ = "@aws-cdk/aws-ec2.IMachineImageSource"
    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        return jsii.invoke(self, "getImage", [scope])


@jsii.implements(IMachineImageSource)
class AmazonLinuxImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.AmazonLinuxImage"):
    def __init__(self, *, edition: typing.Optional["AmazonLinuxEdition"]=None, generation: typing.Optional["AmazonLinuxGeneration"]=None, storage: typing.Optional["AmazonLinuxStorage"]=None, virtualization: typing.Optional["AmazonLinuxVirt"]=None) -> None:
        props: AmazonLinuxImageProps = {}

        if edition is not None:
            props["edition"] = edition

        if generation is not None:
            props["generation"] = generation

        if storage is not None:
            props["storage"] = storage

        if virtualization is not None:
            props["virtualization"] = virtualization

        jsii.create(AmazonLinuxImage, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        return jsii.invoke(self, "getImage", [scope])


@jsii.implements(IMachineImageSource)
class GenericLinuxImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.GenericLinuxImage"):
    def __init__(self, ami_map: typing.Mapping[str,str]) -> None:
        jsii.create(GenericLinuxImage, self, [ami_map])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        return jsii.invoke(self, "getImage", [scope])

    @property
    @jsii.member(jsii_name="amiMap")
    def ami_map(self) -> typing.Mapping[str,str]:
        return jsii.get(self, "amiMap")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IPortRange")
class IPortRange(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPortRangeProxy

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        ...

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        ...


class _IPortRangeProxy():
    __jsii_type__ = "@aws-cdk/aws-ec2.IPortRange"
    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])


@jsii.implements(IPortRange)
class AllTraffic(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.AllTraffic"):
    def __init__(self) -> None:
        jsii.create(AllTraffic, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.ISecurityGroupRule")
class ISecurityGroupRule(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecurityGroupRuleProxy

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        ...

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        ...

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        ...

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        ...


class _ISecurityGroupRuleProxy():
    __jsii_type__ = "@aws-cdk/aws-ec2.ISecurityGroupRule"
    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        return jsii.get(self, "uniqueId")

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toIngressRuleJSON", [])


@jsii.implements(ISecurityGroupRule, IConnectable)
class CidrIPv4(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CidrIPv4"):
    def __init__(self, cidr_ip: str) -> None:
        jsii.create(CidrIPv4, self, [cidr_ip])

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toIngressRuleJSON", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="cidrIp")
    def cidr_ip(self) -> str:
        return jsii.get(self, "cidrIp")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        return jsii.get(self, "uniqueId")


class AnyIPv4(CidrIPv4, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.AnyIPv4"):
    def __init__(self) -> None:
        jsii.create(AnyIPv4, self, [])


@jsii.implements(ISecurityGroupRule, IConnectable)
class CidrIPv6(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CidrIPv6"):
    def __init__(self, cidr_ipv6: str) -> None:
        jsii.create(CidrIPv6, self, [cidr_ipv6])

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toIngressRuleJSON", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="cidrIpv6")
    def cidr_ipv6(self) -> str:
        return jsii.get(self, "cidrIpv6")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        return jsii.get(self, "uniqueId")


class AnyIPv6(CidrIPv6, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.AnyIPv6"):
    def __init__(self) -> None:
        jsii.create(AnyIPv6, self, [])


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.ISecurityGroup")
class ISecurityGroup(aws_cdk.cdk.IConstruct, ISecurityGroupRule, IConnectable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecurityGroupProxy

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        ...

    @jsii.member(jsii_name="addEgressRule")
    def add_egress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        ...

    @jsii.member(jsii_name="addIngressRule")
    def add_ingress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "SecurityGroupImportProps":
        ...


class _ISecurityGroupProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(ISecurityGroupRule), jsii.proxy_for(IConnectable)):
    __jsii_type__ = "@aws-cdk/aws-ec2.ISecurityGroup"
    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        return jsii.get(self, "securityGroupId")

    @jsii.member(jsii_name="addEgressRule")
    def add_egress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "addEgressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="addIngressRule")
    def add_ingress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "addIngressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="export")
    def export(self) -> "SecurityGroupImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IVpcNetwork")
class IVpcNetwork(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IVpcNetworkProxy

    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        ...

    @property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List["IVpcSubnet"]:
        ...

    @property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List["IVpcSubnet"]:
        ...

    @property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List["IVpcSubnet"]:
        ...

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="vpcRegion")
    def vpc_region(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> typing.Optional[str]:
        ...

    @jsii.member(jsii_name="addVpnConnection")
    def add_vpn_connection(self, id: str, *, ip: str, asn: typing.Optional[jsii.Number]=None, static_routes: typing.Optional[typing.List[str]]=None, tunnel_options: typing.Optional[typing.List["VpnTunnelOption"]]=None) -> "VpnConnection":
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "VpcNetworkImportProps":
        ...

    @jsii.member(jsii_name="isPublicSubnets")
    def is_public_subnets(self, subnet_ids: typing.List[str]) -> bool:
        ...

    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self, *, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> typing.List[str]:
        ...

    @jsii.member(jsii_name="subnetInternetDependencies")
    def subnet_internet_dependencies(self, *, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> aws_cdk.cdk.IDependable:
        ...


class _IVpcNetworkProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ec2.IVpcNetwork"
    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        return jsii.get(self, "availabilityZones")

    @property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "isolatedSubnets")

    @property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "privateSubnets")

    @property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "publicSubnets")

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        return jsii.get(self, "vpcId")

    @property
    @jsii.member(jsii_name="vpcRegion")
    def vpc_region(self) -> str:
        return jsii.get(self, "vpcRegion")

    @property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> typing.Optional[str]:
        return jsii.get(self, "vpnGatewayId")

    @jsii.member(jsii_name="addVpnConnection")
    def add_vpn_connection(self, id: str, *, ip: str, asn: typing.Optional[jsii.Number]=None, static_routes: typing.Optional[typing.List[str]]=None, tunnel_options: typing.Optional[typing.List["VpnTunnelOption"]]=None) -> "VpnConnection":
        options: VpnConnectionOptions = {"ip": ip}

        if asn is not None:
            options["asn"] = asn

        if static_routes is not None:
            options["staticRoutes"] = static_routes

        if tunnel_options is not None:
            options["tunnelOptions"] = tunnel_options

        return jsii.invoke(self, "addVpnConnection", [id, options])

    @jsii.member(jsii_name="export")
    def export(self) -> "VpcNetworkImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="isPublicSubnets")
    def is_public_subnets(self, subnet_ids: typing.List[str]) -> bool:
        return jsii.invoke(self, "isPublicSubnets", [subnet_ids])

    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self, *, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> typing.List[str]:
        selection: SubnetSelection = {}

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "subnetIds", [selection])

    @jsii.member(jsii_name="subnetInternetDependencies")
    def subnet_internet_dependencies(self, *, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> aws_cdk.cdk.IDependable:
        selection: SubnetSelection = {}

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "subnetInternetDependencies", [selection])


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IVpcSubnet")
class IVpcSubnet(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IVpcSubnetProxy

    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> aws_cdk.cdk.IDependable:
        ...

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "VpcSubnetImportProps":
        ...


class _IVpcSubnetProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ec2.IVpcSubnet"
    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> str:
        return jsii.get(self, "availabilityZone")

    @property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> aws_cdk.cdk.IDependable:
        return jsii.get(self, "internetConnectivityEstablished")

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        return jsii.get(self, "subnetId")

    @jsii.member(jsii_name="export")
    def export(self) -> "VpcSubnetImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IVpnConnection")
class IVpnConnection(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IVpnConnectionProxy

    @property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        ...

    @property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="vpnId")
    def vpn_id(self) -> str:
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricTunnelDataIn")
    def metric_tunnel_data_in(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricTunnelDataOut")
    def metric_tunnel_data_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricTunnelState")
    def metric_tunnel_state(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...


class _IVpnConnectionProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ec2.IVpnConnection"
    @property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        return jsii.get(self, "customerGatewayAsn")

    @property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> str:
        return jsii.get(self, "customerGatewayId")

    @property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> str:
        return jsii.get(self, "customerGatewayIp")

    @property
    @jsii.member(jsii_name="vpnId")
    def vpn_id(self) -> str:
        return jsii.get(self, "vpnId")

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

    @jsii.member(jsii_name="metricTunnelDataIn")
    def metric_tunnel_data_in(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTunnelDataIn", [props])

    @jsii.member(jsii_name="metricTunnelDataOut")
    def metric_tunnel_data_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTunnelDataOut", [props])

    @jsii.member(jsii_name="metricTunnelState")
    def metric_tunnel_state(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTunnelState", [props])


@jsii.implements(IPortRange)
class IcmpAllTypeCodes(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.IcmpAllTypeCodes"):
    def __init__(self, type: jsii.Number) -> None:
        jsii.create(IcmpAllTypeCodes, self, [type])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return jsii.get(self, "type")


@jsii.implements(IPortRange)
class IcmpAllTypesAndCodes(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.IcmpAllTypesAndCodes"):
    def __init__(self) -> None:
        jsii.create(IcmpAllTypesAndCodes, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")


@jsii.implements(IPortRange)
class IcmpPing(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.IcmpPing"):
    def __init__(self) -> None:
        jsii.create(IcmpPing, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")


@jsii.implements(IPortRange)
class IcmpTypeAndCode(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.IcmpTypeAndCode"):
    def __init__(self, type: jsii.Number, code: jsii.Number) -> None:
        jsii.create(IcmpTypeAndCode, self, [type, code])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return jsii.get(self, "code")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return jsii.get(self, "type")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.InstanceClass")
class InstanceClass(enum.Enum):
    Standard3 = "Standard3"
    Standard4 = "Standard4"
    Standard5 = "Standard5"
    Memory3 = "Memory3"
    Memory4 = "Memory4"
    Compute3 = "Compute3"
    Compute4 = "Compute4"
    Compute5 = "Compute5"
    Storage2 = "Storage2"
    StorageCompute1 = "StorageCompute1"
    Io3 = "Io3"
    Burstable2 = "Burstable2"
    Burstable3 = "Burstable3"
    MemoryIntensive1 = "MemoryIntensive1"
    MemoryIntensive1Extended = "MemoryIntensive1Extended"
    Fpga1 = "Fpga1"
    Graphics3 = "Graphics3"
    Parallel2 = "Parallel2"
    Parallel3 = "Parallel3"

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.InstanceSize")
class InstanceSize(enum.Enum):
    None_ = "None"
    Micro = "Micro"
    Small = "Small"
    Medium = "Medium"
    Large = "Large"
    XLarge = "XLarge"
    XLarge2 = "XLarge2"
    XLarge4 = "XLarge4"
    XLarge8 = "XLarge8"
    XLarge9 = "XLarge9"
    XLarge10 = "XLarge10"
    XLarge12 = "XLarge12"
    XLarge16 = "XLarge16"
    XLarge18 = "XLarge18"
    XLarge24 = "XLarge24"
    XLarge32 = "XLarge32"

class InstanceType(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.InstanceType"):
    def __init__(self, instance_type_identifier: str) -> None:
        jsii.create(InstanceType, self, [instance_type_identifier])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="instanceTypeIdentifier")
    def instance_type_identifier(self) -> str:
        return jsii.get(self, "instanceTypeIdentifier")


class InstanceTypePair(InstanceType, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.InstanceTypePair"):
    def __init__(self, instance_class: "InstanceClass", instance_size: "InstanceSize") -> None:
        jsii.create(InstanceTypePair, self, [instance_class, instance_size])

    @property
    @jsii.member(jsii_name="instanceClass")
    def instance_class(self) -> "InstanceClass":
        return jsii.get(self, "instanceClass")

    @property
    @jsii.member(jsii_name="instanceSize")
    def instance_size(self) -> "InstanceSize":
        return jsii.get(self, "instanceSize")


class MachineImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.MachineImage"):
    def __init__(self, image_id: str, os: "OperatingSystem") -> None:
        jsii.create(MachineImage, self, [image_id, os])

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        return jsii.get(self, "imageId")

    @property
    @jsii.member(jsii_name="os")
    def os(self) -> "OperatingSystem":
        return jsii.get(self, "os")


class OperatingSystem(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ec2.OperatingSystem"):
    @staticmethod
    def __jsii_proxy_class__():
        return _OperatingSystemProxy

    def __init__(self) -> None:
        jsii.create(OperatingSystem, self, [])

    @jsii.member(jsii_name="createUserData")
    @abc.abstractmethod
    def create_user_data(self, scripts: typing.List[str]) -> str:
        ...

    @property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> "OperatingSystemType":
        ...


class _OperatingSystemProxy(OperatingSystem):
    @jsii.member(jsii_name="createUserData")
    def create_user_data(self, scripts: typing.List[str]) -> str:
        return jsii.invoke(self, "createUserData", [scripts])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "OperatingSystemType":
        return jsii.get(self, "type")


class LinuxOS(OperatingSystem, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.LinuxOS"):
    def __init__(self) -> None:
        jsii.create(LinuxOS, self, [])

    @jsii.member(jsii_name="createUserData")
    def create_user_data(self, scripts: typing.List[str]) -> str:
        return jsii.invoke(self, "createUserData", [scripts])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "OperatingSystemType":
        return jsii.get(self, "type")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.OperatingSystemType")
class OperatingSystemType(enum.Enum):
    Linux = "Linux"
    Windows = "Windows"

@jsii.implements(ISecurityGroupRule, IConnectable)
class PrefixList(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.PrefixList"):
    def __init__(self, prefix_list_id: str) -> None:
        jsii.create(PrefixList, self, [prefix_list_id])

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toIngressRuleJSON", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="prefixListId")
    def prefix_list_id(self) -> str:
        return jsii.get(self, "prefixListId")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        return jsii.get(self, "uniqueId")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.Protocol")
class Protocol(enum.Enum):
    All = "All"
    Tcp = "Tcp"
    Udp = "Udp"
    Icmp = "Icmp"
    Icmpv6 = "Icmpv6"

@jsii.implements(ISecurityGroup)
class SecurityGroupBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ec2.SecurityGroupBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _SecurityGroupBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(SecurityGroupBase, self, [scope, id])

    @jsii.member(jsii_name="isSecurityGroup")
    @classmethod
    def is_security_group(cls, construct: typing.Any) -> bool:
        return jsii.sinvoke(cls, "isSecurityGroup", [construct])

    @jsii.member(jsii_name="addEgressRule")
    def add_egress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "addEgressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="addIngressRule")
    def add_ingress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "addIngressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "SecurityGroupImportProps":
        ...

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toIngressRuleJSON", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="securityGroupId")
    @abc.abstractmethod
    def security_group_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        return jsii.get(self, "uniqueId")

    @property
    @jsii.member(jsii_name="defaultPortRange")
    def default_port_range(self) -> typing.Optional["IPortRange"]:
        return jsii.get(self, "defaultPortRange")


class _SecurityGroupBaseProxy(SecurityGroupBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "SecurityGroupImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        return jsii.get(self, "securityGroupId")


class SecurityGroup(SecurityGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.SecurityGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: "IVpcNetwork", allow_all_outbound: typing.Optional[bool]=None, description: typing.Optional[str]=None, group_name: typing.Optional[str]=None) -> None:
        props: SecurityGroupProps = {"vpc": vpc}

        if allow_all_outbound is not None:
            props["allowAllOutbound"] = allow_all_outbound

        if description is not None:
            props["description"] = description

        if group_name is not None:
            props["groupName"] = group_name

        jsii.create(SecurityGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, security_group_id: str) -> "ISecurityGroup":
        props: SecurityGroupImportProps = {"securityGroupId": security_group_id}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addEgressRule")
    def add_egress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "addEgressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="addIngressRule")
    def add_ingress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "addIngressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="export")
    def export(self) -> "SecurityGroupImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> str:
        return jsii.get(self, "groupName")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        return jsii.get(self, "securityGroupId")

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        return jsii.get(self, "vpcId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SecurityGroupImportProps")
class SecurityGroupImportProps(jsii.compat.TypedDict):
    securityGroupId: str

class _SecurityGroupProps(jsii.compat.TypedDict, total=False):
    allowAllOutbound: bool
    description: str
    groupName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SecurityGroupProps")
class SecurityGroupProps(_SecurityGroupProps):
    vpc: "IVpcNetwork"

class _SubnetConfiguration(jsii.compat.TypedDict, total=False):
    cidrMask: jsii.Number
    reserved: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SubnetConfiguration")
class SubnetConfiguration(_SubnetConfiguration):
    name: str
    subnetType: "SubnetType"

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SubnetSelection")
class SubnetSelection(jsii.compat.TypedDict, total=False):
    subnetName: str
    subnetType: "SubnetType"

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.SubnetType")
class SubnetType(enum.Enum):
    Isolated = "Isolated"
    Private = "Private"
    Public = "Public"

@jsii.implements(IPortRange)
class TcpAllPorts(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.TcpAllPorts"):
    def __init__(self) -> None:
        jsii.create(TcpAllPorts, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")


@jsii.implements(IPortRange)
class TcpPort(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.TcpPort"):
    def __init__(self, port: jsii.Number) -> None:
        jsii.create(TcpPort, self, [port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return jsii.get(self, "port")


@jsii.implements(IPortRange)
class TcpPortFromAttribute(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.TcpPortFromAttribute"):
    def __init__(self, port: str) -> None:
        jsii.create(TcpPortFromAttribute, self, [port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> str:
        return jsii.get(self, "port")


@jsii.implements(IPortRange)
class TcpPortRange(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.TcpPortRange"):
    def __init__(self, start_port: jsii.Number, end_port: jsii.Number) -> None:
        jsii.create(TcpPortRange, self, [start_port, end_port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="endPort")
    def end_port(self) -> jsii.Number:
        return jsii.get(self, "endPort")

    @property
    @jsii.member(jsii_name="startPort")
    def start_port(self) -> jsii.Number:
        return jsii.get(self, "startPort")


@jsii.implements(IPortRange)
class UdpAllPorts(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.UdpAllPorts"):
    def __init__(self) -> None:
        jsii.create(UdpAllPorts, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")


@jsii.implements(IPortRange)
class UdpPort(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.UdpPort"):
    def __init__(self, port: jsii.Number) -> None:
        jsii.create(UdpPort, self, [port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return jsii.get(self, "port")


@jsii.implements(IPortRange)
class UdpPortFromAttribute(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.UdpPortFromAttribute"):
    def __init__(self, port: str) -> None:
        jsii.create(UdpPortFromAttribute, self, [port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> str:
        return jsii.get(self, "port")


@jsii.implements(IPortRange)
class UdpPortRange(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.UdpPortRange"):
    def __init__(self, start_port: jsii.Number, end_port: jsii.Number) -> None:
        jsii.create(UdpPortRange, self, [start_port, end_port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="endPort")
    def end_port(self) -> jsii.Number:
        return jsii.get(self, "endPort")

    @property
    @jsii.member(jsii_name="startPort")
    def start_port(self) -> jsii.Number:
        return jsii.get(self, "startPort")


@jsii.implements(IVpcNetwork)
class VpcNetworkBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ec2.VpcNetworkBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _VpcNetworkBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(VpcNetworkBase, self, [scope, id])

    @jsii.member(jsii_name="addVpnConnection")
    def add_vpn_connection(self, id: str, *, ip: str, asn: typing.Optional[jsii.Number]=None, static_routes: typing.Optional[typing.List[str]]=None, tunnel_options: typing.Optional[typing.List["VpnTunnelOption"]]=None) -> "VpnConnection":
        options: VpnConnectionOptions = {"ip": ip}

        if asn is not None:
            options["asn"] = asn

        if static_routes is not None:
            options["staticRoutes"] = static_routes

        if tunnel_options is not None:
            options["tunnelOptions"] = tunnel_options

        return jsii.invoke(self, "addVpnConnection", [id, options])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "VpcNetworkImportProps":
        ...

    @jsii.member(jsii_name="isPublicSubnets")
    def is_public_subnets(self, subnet_ids: typing.List[str]) -> bool:
        return jsii.invoke(self, "isPublicSubnets", [subnet_ids])

    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self, *, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> typing.List[str]:
        selection: SubnetSelection = {}

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "subnetIds", [selection])

    @jsii.member(jsii_name="subnetInternetDependencies")
    def subnet_internet_dependencies(self, *, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> aws_cdk.cdk.IDependable:
        selection: SubnetSelection = {}

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "subnetInternetDependencies", [selection])

    @jsii.member(jsii_name="subnets")
    def _subnets(self, *, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> typing.List["IVpcSubnet"]:
        selection: SubnetSelection = {}

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "subnets", [selection])

    @property
    @jsii.member(jsii_name="availabilityZones")
    @abc.abstractmethod
    def availability_zones(self) -> typing.List[str]:
        ...

    @property
    @jsii.member(jsii_name="internetDependencies")
    def internet_dependencies(self) -> typing.List[aws_cdk.cdk.IConstruct]:
        return jsii.get(self, "internetDependencies")

    @property
    @jsii.member(jsii_name="isolatedSubnets")
    @abc.abstractmethod
    def isolated_subnets(self) -> typing.List["IVpcSubnet"]:
        ...

    @property
    @jsii.member(jsii_name="natDependencies")
    def nat_dependencies(self) -> typing.List[aws_cdk.cdk.IConstruct]:
        return jsii.get(self, "natDependencies")

    @property
    @jsii.member(jsii_name="privateSubnets")
    @abc.abstractmethod
    def private_subnets(self) -> typing.List["IVpcSubnet"]:
        ...

    @property
    @jsii.member(jsii_name="publicSubnets")
    @abc.abstractmethod
    def public_subnets(self) -> typing.List["IVpcSubnet"]:
        ...

    @property
    @jsii.member(jsii_name="vpcId")
    @abc.abstractmethod
    def vpc_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="vpcRegion")
    def vpc_region(self) -> str:
        return jsii.get(self, "vpcRegion")

    @property
    @jsii.member(jsii_name="vpnGatewayId")
    @abc.abstractmethod
    def vpn_gateway_id(self) -> typing.Optional[str]:
        ...


class _VpcNetworkBaseProxy(VpcNetworkBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "VpcNetworkImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        return jsii.get(self, "availabilityZones")

    @property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "isolatedSubnets")

    @property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "privateSubnets")

    @property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "publicSubnets")

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        return jsii.get(self, "vpcId")

    @property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> typing.Optional[str]:
        return jsii.get(self, "vpnGatewayId")


class VpcNetwork(VpcNetworkBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.VpcNetwork"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cidr: typing.Optional[str]=None, default_instance_tenancy: typing.Optional["DefaultInstanceTenancy"]=None, enable_dns_hostnames: typing.Optional[bool]=None, enable_dns_support: typing.Optional[bool]=None, max_a_zs: typing.Optional[jsii.Number]=None, nat_gateways: typing.Optional[jsii.Number]=None, nat_gateway_subnets: typing.Optional["SubnetSelection"]=None, subnet_configuration: typing.Optional[typing.List["SubnetConfiguration"]]=None, vpn_connections: typing.Optional[typing.Mapping[str,"VpnConnectionOptions"]]=None, vpn_gateway: typing.Optional[bool]=None, vpn_gateway_asn: typing.Optional[jsii.Number]=None, vpn_route_propagation: typing.Optional[typing.List["SubnetType"]]=None) -> None:
        props: VpcNetworkProps = {}

        if cidr is not None:
            props["cidr"] = cidr

        if default_instance_tenancy is not None:
            props["defaultInstanceTenancy"] = default_instance_tenancy

        if enable_dns_hostnames is not None:
            props["enableDnsHostnames"] = enable_dns_hostnames

        if enable_dns_support is not None:
            props["enableDnsSupport"] = enable_dns_support

        if max_a_zs is not None:
            props["maxAZs"] = max_a_zs

        if nat_gateways is not None:
            props["natGateways"] = nat_gateways

        if nat_gateway_subnets is not None:
            props["natGatewaySubnets"] = nat_gateway_subnets

        if subnet_configuration is not None:
            props["subnetConfiguration"] = subnet_configuration

        if vpn_connections is not None:
            props["vpnConnections"] = vpn_connections

        if vpn_gateway is not None:
            props["vpnGateway"] = vpn_gateway

        if vpn_gateway_asn is not None:
            props["vpnGatewayAsn"] = vpn_gateway_asn

        if vpn_route_propagation is not None:
            props["vpnRoutePropagation"] = vpn_route_propagation

        jsii.create(VpcNetwork, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, availability_zones: typing.List[str], vpc_id: str, isolated_subnet_ids: typing.Optional[typing.List[str]]=None, isolated_subnet_names: typing.Optional[typing.List[str]]=None, private_subnet_ids: typing.Optional[typing.List[str]]=None, private_subnet_names: typing.Optional[typing.List[str]]=None, public_subnet_ids: typing.Optional[typing.List[str]]=None, public_subnet_names: typing.Optional[typing.List[str]]=None, vpn_gateway_id: typing.Optional[str]=None) -> "IVpcNetwork":
        props: VpcNetworkImportProps = {"availabilityZones": availability_zones, "vpcId": vpc_id}

        if isolated_subnet_ids is not None:
            props["isolatedSubnetIds"] = isolated_subnet_ids

        if isolated_subnet_names is not None:
            props["isolatedSubnetNames"] = isolated_subnet_names

        if private_subnet_ids is not None:
            props["privateSubnetIds"] = private_subnet_ids

        if private_subnet_names is not None:
            props["privateSubnetNames"] = private_subnet_names

        if public_subnet_ids is not None:
            props["publicSubnetIds"] = public_subnet_ids

        if public_subnet_names is not None:
            props["publicSubnetNames"] = public_subnet_names

        if vpn_gateway_id is not None:
            props["vpnGatewayId"] = vpn_gateway_id

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="importFromContext")
    @classmethod
    def import_from_context(cls, scope: aws_cdk.cdk.Construct, id: str, *, is_default: typing.Optional[bool]=None, tags: typing.Optional[typing.Mapping[str,str]]=None, vpc_id: typing.Optional[str]=None, vpc_name: typing.Optional[str]=None) -> "IVpcNetwork":
        props: VpcNetworkProviderProps = {}

        if is_default is not None:
            props["isDefault"] = is_default

        if tags is not None:
            props["tags"] = tags

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        if vpc_name is not None:
            props["vpcName"] = vpc_name

        return jsii.sinvoke(cls, "importFromContext", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "VpcNetworkImportProps":
        return jsii.invoke(self, "export", [])

    @classproperty
    @jsii.member(jsii_name="DEFAULT_CIDR_RANGE")
    def DEFAULT_CIDR_RANGE(cls) -> str:
        return jsii.sget(cls, "DEFAULT_CIDR_RANGE")

    @classproperty
    @jsii.member(jsii_name="DEFAULT_SUBNETS")
    def DEFAULT_SUBNETS(cls) -> typing.List["SubnetConfiguration"]:
        return jsii.sget(cls, "DEFAULT_SUBNETS")

    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        return jsii.get(self, "availabilityZones")

    @property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> str:
        return jsii.get(self, "cidr")

    @property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "isolatedSubnets")

    @property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "privateSubnets")

    @property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List["IVpcSubnet"]:
        return jsii.get(self, "publicSubnets")

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        return jsii.get(self, "vpcId")

    @property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> typing.Optional[str]:
        return jsii.get(self, "vpnGatewayId")


class _VpcNetworkImportProps(jsii.compat.TypedDict, total=False):
    isolatedSubnetIds: typing.List[str]
    isolatedSubnetNames: typing.List[str]
    privateSubnetIds: typing.List[str]
    privateSubnetNames: typing.List[str]
    publicSubnetIds: typing.List[str]
    publicSubnetNames: typing.List[str]
    vpnGatewayId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpcNetworkImportProps")
class VpcNetworkImportProps(_VpcNetworkImportProps):
    availabilityZones: typing.List[str]
    vpcId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpcNetworkProps")
class VpcNetworkProps(jsii.compat.TypedDict, total=False):
    cidr: str
    defaultInstanceTenancy: "DefaultInstanceTenancy"
    enableDnsHostnames: bool
    enableDnsSupport: bool
    maxAZs: jsii.Number
    natGateways: jsii.Number
    natGatewaySubnets: "SubnetSelection"
    subnetConfiguration: typing.List["SubnetConfiguration"]
    vpnConnections: typing.Mapping[str,"VpnConnectionOptions"]
    vpnGateway: bool
    vpnGatewayAsn: jsii.Number
    vpnRoutePropagation: typing.List["SubnetType"]

class VpcNetworkProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.VpcNetworkProvider"):
    def __init__(self, context: aws_cdk.cdk.Construct, *, is_default: typing.Optional[bool]=None, tags: typing.Optional[typing.Mapping[str,str]]=None, vpc_id: typing.Optional[str]=None, vpc_name: typing.Optional[str]=None) -> None:
        props: VpcNetworkProviderProps = {}

        if is_default is not None:
            props["isDefault"] = is_default

        if tags is not None:
            props["tags"] = tags

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        if vpc_name is not None:
            props["vpcName"] = vpc_name

        jsii.create(VpcNetworkProvider, self, [context, props])

    @property
    @jsii.member(jsii_name="vpcProps")
    def vpc_props(self) -> "VpcNetworkImportProps":
        return jsii.get(self, "vpcProps")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpcNetworkProviderProps")
class VpcNetworkProviderProps(jsii.compat.TypedDict, total=False):
    isDefault: bool
    tags: typing.Mapping[str,str]
    vpcId: str
    vpcName: str

@jsii.implements(IVpcSubnet)
class VpcSubnet(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.VpcSubnet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, cidr_block: str, vpc_id: str, map_public_ip_on_launch: typing.Optional[bool]=None) -> None:
        props: VpcSubnetProps = {"availabilityZone": availability_zone, "cidrBlock": cidr_block, "vpcId": vpc_id}

        if map_public_ip_on_launch is not None:
            props["mapPublicIpOnLaunch"] = map_public_ip_on_launch

        jsii.create(VpcSubnet, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, subnet_id: str) -> "IVpcSubnet":
        props: VpcSubnetImportProps = {"availabilityZone": availability_zone, "subnetId": subnet_id}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addDefaultRouteToIGW")
    def _add_default_route_to_igw(self, gateway: "CfnInternetGateway", gateway_attachment: "CfnVPCGatewayAttachment") -> None:
        return jsii.invoke(self, "addDefaultRouteToIGW", [gateway, gateway_attachment])

    @jsii.member(jsii_name="addDefaultRouteToNAT")
    def _add_default_route_to_nat(self, nat_gateway_id: str) -> None:
        return jsii.invoke(self, "addDefaultRouteToNAT", [nat_gateway_id])

    @jsii.member(jsii_name="export")
    def export(self) -> "VpcSubnetImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> str:
        return jsii.get(self, "availabilityZone")

    @property
    @jsii.member(jsii_name="dependencyElements")
    def dependency_elements(self) -> typing.List[aws_cdk.cdk.IDependable]:
        return jsii.get(self, "dependencyElements")

    @property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> aws_cdk.cdk.IDependable:
        return jsii.get(self, "internetConnectivityEstablished")

    @property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> str:
        return jsii.get(self, "routeTableId")

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        return jsii.get(self, "subnetId")


class VpcPrivateSubnet(VpcSubnet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.VpcPrivateSubnet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, cidr_block: str, vpc_id: str, map_public_ip_on_launch: typing.Optional[bool]=None) -> None:
        props: VpcSubnetProps = {"availabilityZone": availability_zone, "cidrBlock": cidr_block, "vpcId": vpc_id}

        if map_public_ip_on_launch is not None:
            props["mapPublicIpOnLaunch"] = map_public_ip_on_launch

        jsii.create(VpcPrivateSubnet, self, [scope, id, props])

    @jsii.member(jsii_name="addDefaultNatRouteEntry")
    def add_default_nat_route_entry(self, nat_gateway_id: str) -> None:
        return jsii.invoke(self, "addDefaultNatRouteEntry", [nat_gateway_id])


class VpcPublicSubnet(VpcSubnet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.VpcPublicSubnet"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, cidr_block: str, vpc_id: str, map_public_ip_on_launch: typing.Optional[bool]=None) -> None:
        props: VpcSubnetProps = {"availabilityZone": availability_zone, "cidrBlock": cidr_block, "vpcId": vpc_id}

        if map_public_ip_on_launch is not None:
            props["mapPublicIpOnLaunch"] = map_public_ip_on_launch

        jsii.create(VpcPublicSubnet, self, [scope, id, props])

    @jsii.member(jsii_name="addDefaultIGWRouteEntry")
    def add_default_igw_route_entry(self, gateway: "CfnInternetGateway", gateway_attachment: "CfnVPCGatewayAttachment") -> None:
        return jsii.invoke(self, "addDefaultIGWRouteEntry", [gateway, gateway_attachment])

    @jsii.member(jsii_name="addNatGateway")
    def add_nat_gateway(self) -> "CfnNatGateway":
        return jsii.invoke(self, "addNatGateway", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpcSubnetImportProps")
class VpcSubnetImportProps(jsii.compat.TypedDict):
    availabilityZone: str
    subnetId: str

class _VpcSubnetProps(jsii.compat.TypedDict, total=False):
    mapPublicIpOnLaunch: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpcSubnetProps")
class VpcSubnetProps(_VpcSubnetProps):
    availabilityZone: str
    cidrBlock: str
    vpcId: str

@jsii.implements(IVpnConnection)
class VpnConnection(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.VpnConnection"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: "IVpcNetwork", ip: str, asn: typing.Optional[jsii.Number]=None, static_routes: typing.Optional[typing.List[str]]=None, tunnel_options: typing.Optional[typing.List["VpnTunnelOption"]]=None) -> None:
        props: VpnConnectionProps = {"vpc": vpc, "ip": ip}

        if asn is not None:
            props["asn"] = asn

        if static_routes is not None:
            props["staticRoutes"] = static_routes

        if tunnel_options is not None:
            props["tunnelOptions"] = tunnel_options

        jsii.create(VpnConnection, self, [scope, id, props])

    @jsii.member(jsii_name="metricAll")
    @classmethod
    def metric_all(cls, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAll", [metric_name, props])

    @jsii.member(jsii_name="metricAllTunnelDataIn")
    @classmethod
    def metric_all_tunnel_data_in(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllTunnelDataIn", [props])

    @jsii.member(jsii_name="metricAllTunnelDataOut")
    @classmethod
    def metric_all_tunnel_data_out(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllTunnelDataOut", [props])

    @jsii.member(jsii_name="metricAllTunnelState")
    @classmethod
    def metric_all_tunnel_state(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllTunnelState", [props])

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

    @jsii.member(jsii_name="metricTunnelDataIn")
    def metric_tunnel_data_in(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTunnelDataIn", [props])

    @jsii.member(jsii_name="metricTunnelDataOut")
    def metric_tunnel_data_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTunnelDataOut", [props])

    @jsii.member(jsii_name="metricTunnelState")
    def metric_tunnel_state(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricTunnelState", [props])

    @property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        return jsii.get(self, "customerGatewayAsn")

    @property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> str:
        return jsii.get(self, "customerGatewayId")

    @property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> str:
        return jsii.get(self, "customerGatewayIp")

    @property
    @jsii.member(jsii_name="vpnId")
    def vpn_id(self) -> str:
        return jsii.get(self, "vpnId")


class _VpnConnectionOptions(jsii.compat.TypedDict, total=False):
    asn: jsii.Number
    staticRoutes: typing.List[str]
    tunnelOptions: typing.List["VpnTunnelOption"]

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpnConnectionOptions")
class VpnConnectionOptions(_VpnConnectionOptions):
    ip: str

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpnConnectionProps")
class VpnConnectionProps(VpnConnectionOptions, jsii.compat.TypedDict):
    vpc: "IVpcNetwork"

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.VpnConnectionType")
class VpnConnectionType(enum.Enum):
    IPsec1 = "IPsec1"
    Dummy = "Dummy"

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpnTunnelOption")
class VpnTunnelOption(jsii.compat.TypedDict, total=False):
    preSharedKey: str
    tunnelInsideCidr: str

@jsii.implements(IMachineImageSource)
class WindowsImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.WindowsImage"):
    def __init__(self, version: "WindowsVersion") -> None:
        jsii.create(WindowsImage, self, [version])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        return jsii.invoke(self, "getImage", [scope])

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> "WindowsVersion":
        return jsii.get(self, "version")


class WindowsOS(OperatingSystem, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.WindowsOS"):
    def __init__(self) -> None:
        jsii.create(WindowsOS, self, [])

    @jsii.member(jsii_name="createUserData")
    def create_user_data(self, scripts: typing.List[str]) -> str:
        return jsii.invoke(self, "createUserData", [scripts])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "OperatingSystemType":
        return jsii.get(self, "type")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.WindowsVersion")
class WindowsVersion(enum.Enum):
    WindowsServer2008SP2English64BitSQL2008SP4Express = "WindowsServer2008SP2English64BitSQL2008SP4Express"
    WindowsServer2012R2RTMChineseSimplified64BitBase = "WindowsServer2012R2RTMChineseSimplified64BitBase"
    WindowsServer2012R2RTMChineseTraditional64BitBase = "WindowsServer2012R2RTMChineseTraditional64BitBase"
    WindowsServer2012R2RTMDutch64BitBase = "WindowsServer2012R2RTMDutch64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP2Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2014SP2Enterprise"
    WindowsServer2012R2RTMHungarian64BitBase = "WindowsServer2012R2RTMHungarian64BitBase"
    WindowsServer2012R2RTMJapanese64BitBase = "WindowsServer2012R2RTMJapanese64BitBase"
    WindowsServer2016EnglishCoreContainers = "WindowsServer2016EnglishCoreContainers"
    WindowsServer2016EnglishCoreSQL2016SP1Web = "WindowsServer2016EnglishCoreSQL2016SP1Web"
    WindowsServer2016GermanFullBase = "WindowsServer2016GermanFullBase"
    WindowsServer2003R2SP2LanguagePacks32BitBase = "WindowsServer2003R2SP2LanguagePacks32BitBase"
    WindowsServer2008R2SP1English64BitSQL2008R2SP3Web = "WindowsServer2008R2SP1English64BitSQL2008R2SP3Web"
    WindowsServer2008R2SP1English64BitSQL2012SP4Express = "WindowsServer2008R2SP1English64BitSQL2012SP4Express"
    WindowsServer2008R2SP1PortugueseBrazil64BitCore = "WindowsServer2008R2SP1PortugueseBrazil64BitCore"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP2Standard = "WindowsServer2012R2RTMEnglish64BitSQL2016SP2Standard"
    WindowsServer2012RTMEnglish64BitSQL2014SP2Express = "WindowsServer2012RTMEnglish64BitSQL2014SP2Express"
    WindowsServer2012RTMItalian64BitBase = "WindowsServer2012RTMItalian64BitBase"
    WindowsServer2016EnglishCoreSQL2016SP1Express = "WindowsServer2016EnglishCoreSQL2016SP1Express"
    WindowsServer2016EnglishDeepLearning = "WindowsServer2016EnglishDeepLearning"
    WindowsServer2019ItalianFullBase = "WindowsServer2019ItalianFullBase"
    WindowsServer2008R2SP1Korean64BitBase = "WindowsServer2008R2SP1Korean64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP1Express = "WindowsServer2012R2RTMEnglish64BitSQL2016SP1Express"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP2Web = "WindowsServer2012R2RTMJapanese64BitSQL2016SP2Web"
    WindowsServer2016JapaneseFullSQL2016SP2Web = "WindowsServer2016JapaneseFullSQL2016SP2Web"
    WindowsServer2016KoreanFullBase = "WindowsServer2016KoreanFullBase"
    WindowsServer2016KoreanFullSQL2016SP2Standard = "WindowsServer2016KoreanFullSQL2016SP2Standard"
    WindowsServer2016PortuguesePortugalFullBase = "WindowsServer2016PortuguesePortugalFullBase"
    WindowsServer2019EnglishFullSQL2017Web = "WindowsServer2019EnglishFullSQL2017Web"
    WindowsServer2019FrenchFullBase = "WindowsServer2019FrenchFullBase"
    WindowsServer2019KoreanFullBase = "WindowsServer2019KoreanFullBase"
    WindowsServer2008R2SP1ChineseHongKongSAR64BitBase = "WindowsServer2008R2SP1ChineseHongKongSAR64BitBase"
    WindowsServer2008R2SP1ChinesePRC64BitBase = "WindowsServer2008R2SP1ChinesePRC64BitBase"
    WindowsServer2012RTMFrench64BitBase = "WindowsServer2012RTMFrench64BitBase"
    WindowsServer2016EnglishFullContainers = "WindowsServer2016EnglishFullContainers"
    WindowsServer2016EnglishFullSQL2016SP1Standard = "WindowsServer2016EnglishFullSQL2016SP1Standard"
    WindowsServer2016RussianFullBase = "WindowsServer2016RussianFullBase"
    WindowsServer2019ChineseSimplifiedFullBase = "WindowsServer2019ChineseSimplifiedFullBase"
    WindowsServer2019EnglishFullSQL2016SP2Standard = "WindowsServer2019EnglishFullSQL2016SP2Standard"
    WindowsServer2019HungarianFullBase = "WindowsServer2019HungarianFullBase"
    WindowsServer2008R2SP1English64BitSQL2008R2SP3Express = "WindowsServer2008R2SP1English64BitSQL2008R2SP3Express"
    WindowsServer2008R2SP1LanguagePacks64BitBase = "WindowsServer2008R2SP1LanguagePacks64BitBase"
    WindowsServer2008SP2English32BitBase = "WindowsServer2008SP2English32BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2012SP4Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2012SP4Enterprise"
    WindowsServer2012RTMChineseTraditional64BitBase = "WindowsServer2012RTMChineseTraditional64BitBase"
    WindowsServer2012RTMEnglish64BitSQL2008R2SP3Express = "WindowsServer2012RTMEnglish64BitSQL2008R2SP3Express"
    WindowsServer2012RTMEnglish64BitSQL2014SP2Standard = "WindowsServer2012RTMEnglish64BitSQL2014SP2Standard"
    WindowsServer2012RTMJapanese64BitSQL2014SP2Express = "WindowsServer2012RTMJapanese64BitSQL2014SP2Express"
    WindowsServer2016PolishFullBase = "WindowsServer2016PolishFullBase"
    WindowsServer2019EnglishFullSQL2016SP2Web = "WindowsServer2019EnglishFullSQL2016SP2Web"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP3Standard = "WindowsServer2012R2RTMEnglish64BitSQL2014SP3Standard"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP2Express = "WindowsServer2012R2RTMEnglish64BitSQL2016SP2Express"
    WindowsServer2012R2RTMEnglishDeepLearning = "WindowsServer2012R2RTMEnglishDeepLearning"
    WindowsServer2012R2RTMGerman64BitBase = "WindowsServer2012R2RTMGerman64BitBase"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP1Express = "WindowsServer2012R2RTMJapanese64BitSQL2016SP1Express"
    WindowsServer2012R2RTMRussian64BitBase = "WindowsServer2012R2RTMRussian64BitBase"
    WindowsServer2012RTMChineseTraditionalHongKongSAR64BitBase = "WindowsServer2012RTMChineseTraditionalHongKongSAR64BitBase"
    WindowsServer2012RTMHungarian64BitBase = "WindowsServer2012RTMHungarian64BitBase"
    WindowsServer2012RTMJapanese64BitSQL2014SP3Standard = "WindowsServer2012RTMJapanese64BitSQL2014SP3Standard"
    WindowsServer2019EnglishFullHyperV = "WindowsServer2019EnglishFullHyperV"
    WindowsServer2003R2SP2English64BitSQL2005SP4Express = "WindowsServer2003R2SP2English64BitSQL2005SP4Express"
    WindowsServer2008R2SP1Japanese64BitSQL2012SP4Express = "WindowsServer2008R2SP1Japanese64BitSQL2012SP4Express"
    WindowsServer2012RTMGerman64BitBase = "WindowsServer2012RTMGerman64BitBase"
    WindowsServer2012RTMJapanese64BitSQL2008R2SP3Standard = "WindowsServer2012RTMJapanese64BitSQL2008R2SP3Standard"
    WindowsServer2016EnglishFullSQL2016SP2Standard = "WindowsServer2016EnglishFullSQL2016SP2Standard"
    WindowsServer2019EnglishFullSQL2017Express = "WindowsServer2019EnglishFullSQL2017Express"
    WindowsServer2019JapaneseFullBase = "WindowsServer2019JapaneseFullBase"
    WindowsServer2019RussianFullBase = "WindowsServer2019RussianFullBase"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP2Standard = "WindowsServer2012R2RTMEnglish64BitSQL2014SP2Standard"
    WindowsServer2012R2RTMItalian64BitBase = "WindowsServer2012R2RTMItalian64BitBase"
    WindowsServer2012RTMEnglish64BitBase = "WindowsServer2012RTMEnglish64BitBase"
    WindowsServer2012RTMEnglish64BitSQL2008R2SP3Standard = "WindowsServer2012RTMEnglish64BitSQL2008R2SP3Standard"
    WindowsServer2016EnglishFullHyperV = "WindowsServer2016EnglishFullHyperV"
    WindowsServer2016EnglishFullSQL2016SP2Enterprise = "WindowsServer2016EnglishFullSQL2016SP2Enterprise"
    WindowsServer2019ChineseTraditionalFullBase = "WindowsServer2019ChineseTraditionalFullBase"
    WindowsServer2019EnglishCoreBase = "WindowsServer2019EnglishCoreBase"
    WindowsServer2019EnglishCoreContainersLatest = "WindowsServer2019EnglishCoreContainersLatest"
    WindowsServer2008SP2English64BitBase = "WindowsServer2008SP2English64BitBase"
    WindowsServer2012R2RTMFrench64BitBase = "WindowsServer2012R2RTMFrench64BitBase"
    WindowsServer2012R2RTMPolish64BitBase = "WindowsServer2012R2RTMPolish64BitBase"
    WindowsServer2012RTMEnglish64BitSQL2012SP4Express = "WindowsServer2012RTMEnglish64BitSQL2012SP4Express"
    WindowsServer2012RTMEnglish64BitSQL2014SP3Standard = "WindowsServer2012RTMEnglish64BitSQL2014SP3Standard"
    WindowsServer2012RTMJapanese64BitSQL2012SP4Standard = "WindowsServer2012RTMJapanese64BitSQL2012SP4Standard"
    WindowsServer2016EnglishCoreContainersLatest = "WindowsServer2016EnglishCoreContainersLatest"
    WindowsServer2019EnglishFullSQL2016SP2Express = "WindowsServer2019EnglishFullSQL2016SP2Express"
    WindowsServer2019TurkishFullBase = "WindowsServer2019TurkishFullBase"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP2Express = "WindowsServer2012R2RTMEnglish64BitSQL2014SP2Express"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP3Web = "WindowsServer2012R2RTMEnglish64BitSQL2014SP3Web"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP1Web = "WindowsServer2012R2RTMJapanese64BitSQL2016SP1Web"
    WindowsServer2012R2RTMPortugueseBrazil64BitBase = "WindowsServer2012R2RTMPortugueseBrazil64BitBase"
    WindowsServer2012R2RTMPortuguesePortugal64BitBase = "WindowsServer2012R2RTMPortuguesePortugal64BitBase"
    WindowsServer2012R2RTMSwedish64BitBase = "WindowsServer2012R2RTMSwedish64BitBase"
    WindowsServer2016EnglishFullSQL2016SP1Express = "WindowsServer2016EnglishFullSQL2016SP1Express"
    WindowsServer2016ItalianFullBase = "WindowsServer2016ItalianFullBase"
    WindowsServer2016SpanishFullBase = "WindowsServer2016SpanishFullBase"
    WindowsServer2019EnglishFullSQL2017Standard = "WindowsServer2019EnglishFullSQL2017Standard"
    WindowsServer2003R2SP2LanguagePacks64BitSQL2005SP4Standard = "WindowsServer2003R2SP2LanguagePacks64BitSQL2005SP4Standard"
    WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Standard = "WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Standard"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP1Standard = "WindowsServer2012R2RTMJapanese64BitSQL2016SP1Standard"
    WindowsServer2012RTMEnglish64BitSQL2008R2SP3Web = "WindowsServer2012RTMEnglish64BitSQL2008R2SP3Web"
    WindowsServer2012RTMJapanese64BitSQL2014SP2Web = "WindowsServer2012RTMJapanese64BitSQL2014SP2Web"
    WindowsServer2016EnglishCoreSQL2016SP2Enterprise = "WindowsServer2016EnglishCoreSQL2016SP2Enterprise"
    WindowsServer2016PortugueseBrazilFullBase = "WindowsServer2016PortugueseBrazilFullBase"
    WindowsServer2019EnglishFullBase = "WindowsServer2019EnglishFullBase"
    WindowsServer2003R2SP2English32BitBase = "WindowsServer2003R2SP2English32BitBase"
    WindowsServer2012R2RTMCzech64BitBase = "WindowsServer2012R2RTMCzech64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP1Standard = "WindowsServer2012R2RTMEnglish64BitSQL2016SP1Standard"
    WindowsServer2012R2RTMJapanese64BitSQL2014SP2Express = "WindowsServer2012R2RTMJapanese64BitSQL2014SP2Express"
    WindowsServer2012RTMEnglish64BitSQL2012SP4Standard = "WindowsServer2012RTMEnglish64BitSQL2012SP4Standard"
    WindowsServer2016EnglishCoreSQL2016SP1Enterprise = "WindowsServer2016EnglishCoreSQL2016SP1Enterprise"
    WindowsServer2016JapaneseFullSQL2016SP1Web = "WindowsServer2016JapaneseFullSQL2016SP1Web"
    WindowsServer2016SwedishFullBase = "WindowsServer2016SwedishFullBase"
    WindowsServer2016TurkishFullBase = "WindowsServer2016TurkishFullBase"
    WindowsServer2008R2SP1English64BitCoreSQL2012SP4Standard = "WindowsServer2008R2SP1English64BitCoreSQL2012SP4Standard"
    WindowsServer2008R2SP1LanguagePacks64BitSQL2008R2SP3Standard = "WindowsServer2008R2SP1LanguagePacks64BitSQL2008R2SP3Standard"
    WindowsServer2012RTMCzech64BitBase = "WindowsServer2012RTMCzech64BitBase"
    WindowsServer2012RTMTurkish64BitBase = "WindowsServer2012RTMTurkish64BitBase"
    WindowsServer2016DutchFullBase = "WindowsServer2016DutchFullBase"
    WindowsServer2016EnglishFullSQL2016SP2Express = "WindowsServer2016EnglishFullSQL2016SP2Express"
    WindowsServer2016EnglishFullSQL2017Enterprise = "WindowsServer2016EnglishFullSQL2017Enterprise"
    WindowsServer2016HungarianFullBase = "WindowsServer2016HungarianFullBase"
    WindowsServer2016KoreanFullSQL2016SP1Standard = "WindowsServer2016KoreanFullSQL2016SP1Standard"
    WindowsServer2019SpanishFullBase = "WindowsServer2019SpanishFullBase"
    WindowsServer2003R2SP2English64BitBase = "WindowsServer2003R2SP2English64BitBase"
    WindowsServer2008R2SP1English64BitBase = "WindowsServer2008R2SP1English64BitBase"
    WindowsServer2008R2SP1LanguagePacks64BitSQL2008R2SP3Express = "WindowsServer2008R2SP1LanguagePacks64BitSQL2008R2SP3Express"
    WindowsServer2008SP2PortugueseBrazil64BitBase = "WindowsServer2008SP2PortugueseBrazil64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP1Web = "WindowsServer2012R2RTMEnglish64BitSQL2016SP1Web"
    WindowsServer2012R2RTMJapanese64BitSQL2014SP3Express = "WindowsServer2012R2RTMJapanese64BitSQL2014SP3Express"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP2Enterprise = "WindowsServer2012R2RTMJapanese64BitSQL2016SP2Enterprise"
    WindowsServer2012RTMJapanese64BitBase = "WindowsServer2012RTMJapanese64BitBase"
    WindowsServer2019EnglishFullContainersLatest = "WindowsServer2019EnglishFullContainersLatest"
    WindowsServer2019EnglishFullSQL2017Enterprise = "WindowsServer2019EnglishFullSQL2017Enterprise"
    WindowsServer1709EnglishCoreContainersLatest = "WindowsServer1709EnglishCoreContainersLatest"
    WindowsServer1803EnglishCoreBase = "WindowsServer1803EnglishCoreBase"
    WindowsServer2008R2SP1English64BitSQL2012SP4Web = "WindowsServer2008R2SP1English64BitSQL2012SP4Web"
    WindowsServer2008R2SP1Japanese64BitBase = "WindowsServer2008R2SP1Japanese64BitBase"
    WindowsServer2008SP2English64BitSQL2008SP4Standard = "WindowsServer2008SP2English64BitSQL2008SP4Standard"
    WindowsServer2012R2RTMEnglish64BitBase = "WindowsServer2012R2RTMEnglish64BitBase"
    WindowsServer2012RTMPortugueseBrazil64BitBase = "WindowsServer2012RTMPortugueseBrazil64BitBase"
    WindowsServer2016EnglishFullSQL2016SP1Web = "WindowsServer2016EnglishFullSQL2016SP1Web"
    WindowsServer2016EnglishP3 = "WindowsServer2016EnglishP3"
    WindowsServer2016JapaneseFullSQL2016SP1Enterprise = "WindowsServer2016JapaneseFullSQL2016SP1Enterprise"
    WindowsServer2003R2SP2LanguagePacks64BitBase = "WindowsServer2003R2SP2LanguagePacks64BitBase"
    WindowsServer2012R2RTMChineseTraditionalHongKong64BitBase = "WindowsServer2012R2RTMChineseTraditionalHongKong64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP3Express = "WindowsServer2012R2RTMEnglish64BitSQL2014SP3Express"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP2Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2016SP2Enterprise"
    WindowsServer2012RTMChineseSimplified64BitBase = "WindowsServer2012RTMChineseSimplified64BitBase"
    WindowsServer2012RTMEnglish64BitSQL2012SP4Web = "WindowsServer2012RTMEnglish64BitSQL2012SP4Web"
    WindowsServer2012RTMJapanese64BitSQL2014SP3Web = "WindowsServer2012RTMJapanese64BitSQL2014SP3Web"
    WindowsServer2016JapaneseFullBase = "WindowsServer2016JapaneseFullBase"
    WindowsServer2016JapaneseFullSQL2016SP1Express = "WindowsServer2016JapaneseFullSQL2016SP1Express"
    WindowsServer1803EnglishCoreContainersLatest = "WindowsServer1803EnglishCoreContainersLatest"
    WindowsServer2008R2SP1Japanese64BitSQL2012SP4Standard = "WindowsServer2008R2SP1Japanese64BitSQL2012SP4Standard"
    WindowsServer2012R2RTMEnglish64BitCore = "WindowsServer2012R2RTMEnglish64BitCore"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP2Web = "WindowsServer2012R2RTMEnglish64BitSQL2014SP2Web"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP3Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2014SP3Enterprise"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP2Standard = "WindowsServer2012R2RTMJapanese64BitSQL2016SP2Standard"
    WindowsServer2012RTMEnglish64BitSQL2014SP3Web = "WindowsServer2012RTMEnglish64BitSQL2014SP3Web"
    WindowsServer2012RTMSwedish64BitBase = "WindowsServer2012RTMSwedish64BitBase"
    WindowsServer2016ChineseSimplifiedFullBase = "WindowsServer2016ChineseSimplifiedFullBase"
    WindowsServer2019PolishFullBase = "WindowsServer2019PolishFullBase"
    WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Web = "WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Web"
    WindowsServer2008R2SP1PortugueseBrazil64BitBase = "WindowsServer2008R2SP1PortugueseBrazil64BitBase"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP1Enterprise = "WindowsServer2012R2RTMJapanese64BitSQL2016SP1Enterprise"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP2Express = "WindowsServer2012R2RTMJapanese64BitSQL2016SP2Express"
    WindowsServer2012RTMEnglish64BitSQL2014SP3Express = "WindowsServer2012RTMEnglish64BitSQL2014SP3Express"
    WindowsServer2012RTMJapanese64BitSQL2014SP2Standard = "WindowsServer2012RTMJapanese64BitSQL2014SP2Standard"
    WindowsServer2016EnglishCoreBase = "WindowsServer2016EnglishCoreBase"
    WindowsServer2016EnglishFullBase = "WindowsServer2016EnglishFullBase"
    WindowsServer2016EnglishFullSQL2017Web = "WindowsServer2016EnglishFullSQL2017Web"
    WindowsServer2019GermanFullBase = "WindowsServer2019GermanFullBase"
    WindowsServer2003R2SP2English64BitSQL2005SP4Standard = "WindowsServer2003R2SP2English64BitSQL2005SP4Standard"
    WindowsServer2008R2SP1English64BitSQL2012SP4Enterprise = "WindowsServer2008R2SP1English64BitSQL2012SP4Enterprise"
    WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Express = "WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Express"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP1Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2016SP1Enterprise"
    WindowsServer2012RTMEnglish64BitSQL2014SP2Web = "WindowsServer2012RTMEnglish64BitSQL2014SP2Web"
    WindowsServer2012RTMJapanese64BitSQL2008R2SP3Express = "WindowsServer2012RTMJapanese64BitSQL2008R2SP3Express"
    WindowsServer2016FrenchFullBase = "WindowsServer2016FrenchFullBase"
    WindowsServer2016JapaneseFullSQL2016SP2Enterprise = "WindowsServer2016JapaneseFullSQL2016SP2Enterprise"
    WindowsServer2019CzechFullBase = "WindowsServer2019CzechFullBase"
    WindowsServer1809EnglishCoreBase = "WindowsServer1809EnglishCoreBase"
    WindowsServer1809EnglishCoreContainersLatest = "WindowsServer1809EnglishCoreContainersLatest"
    WindowsServer2003R2SP2LanguagePacks64BitSQL2005SP4Express = "WindowsServer2003R2SP2LanguagePacks64BitSQL2005SP4Express"
    WindowsServer2012R2RTMTurkish64BitBase = "WindowsServer2012R2RTMTurkish64BitBase"
    WindowsServer2012RTMJapanese64BitSQL2012SP4Web = "WindowsServer2012RTMJapanese64BitSQL2012SP4Web"
    WindowsServer2012RTMPolish64BitBase = "WindowsServer2012RTMPolish64BitBase"
    WindowsServer2012RTMSpanish64BitBase = "WindowsServer2012RTMSpanish64BitBase"
    WindowsServer2016EnglishFullSQL2016SP1Enterprise = "WindowsServer2016EnglishFullSQL2016SP1Enterprise"
    WindowsServer2016JapaneseFullSQL2016SP2Express = "WindowsServer2016JapaneseFullSQL2016SP2Express"
    WindowsServer2019EnglishFullSQL2016SP2Enterprise = "WindowsServer2019EnglishFullSQL2016SP2Enterprise"
    WindowsServer1709EnglishCoreBase = "WindowsServer1709EnglishCoreBase"
    WindowsServer2008R2SP1English64BitSQL2012RTMSP2Enterprise = "WindowsServer2008R2SP1English64BitSQL2012RTMSP2Enterprise"
    WindowsServer2008R2SP1English64BitSQL2012SP4Standard = "WindowsServer2008R2SP1English64BitSQL2012SP4Standard"
    WindowsServer2008SP2PortugueseBrazil32BitBase = "WindowsServer2008SP2PortugueseBrazil32BitBase"
    WindowsServer2012R2RTMJapanese64BitSQL2014SP2Standard = "WindowsServer2012R2RTMJapanese64BitSQL2014SP2Standard"
    WindowsServer2012RTMJapanese64BitSQL2012SP4Express = "WindowsServer2012RTMJapanese64BitSQL2012SP4Express"
    WindowsServer2012RTMPortuguesePortugal64BitBase = "WindowsServer2012RTMPortuguesePortugal64BitBase"
    WindowsServer2016CzechFullBase = "WindowsServer2016CzechFullBase"
    WindowsServer2016JapaneseFullSQL2016SP1Standard = "WindowsServer2016JapaneseFullSQL2016SP1Standard"
    WindowsServer2019DutchFullBase = "WindowsServer2019DutchFullBase"
    WindowsServer2008R2SP1English64BitCore = "WindowsServer2008R2SP1English64BitCore"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP2Web = "WindowsServer2012R2RTMEnglish64BitSQL2016SP2Web"
    WindowsServer2012R2RTMKorean64BitBase = "WindowsServer2012R2RTMKorean64BitBase"
    WindowsServer2012RTMDutch64BitBase = "WindowsServer2012RTMDutch64BitBase"
    WindowsServer2016English64BitSQL2012SP4Enterprise = "WindowsServer2016English64BitSQL2012SP4Enterprise"
    WindowsServer2016EnglishCoreSQL2016SP1Standard = "WindowsServer2016EnglishCoreSQL2016SP1Standard"
    WindowsServer2016EnglishCoreSQL2016SP2Express = "WindowsServer2016EnglishCoreSQL2016SP2Express"
    WindowsServer2016EnglishCoreSQL2016SP2Web = "WindowsServer2016EnglishCoreSQL2016SP2Web"
    WindowsServer2016EnglishFullSQL2017Standard = "WindowsServer2016EnglishFullSQL2017Standard"
    WindowsServer2019PortugueseBrazilFullBase = "WindowsServer2019PortugueseBrazilFullBase"
    WindowsServer2008R2SP1English64BitSQL2008R2SP3Standard = "WindowsServer2008R2SP1English64BitSQL2008R2SP3Standard"
    WindowsServer2008R2SP1English64BitSharePoint2010SP2Foundation = "WindowsServer2008R2SP1English64BitSharePoint2010SP2Foundation"
    WindowsServer2012R2RTMEnglishP3 = "WindowsServer2012R2RTMEnglishP3"
    WindowsServer2012R2RTMJapanese64BitSQL2014SP3Standard = "WindowsServer2012R2RTMJapanese64BitSQL2014SP3Standard"
    WindowsServer2012R2RTMSpanish64BitBase = "WindowsServer2012R2RTMSpanish64BitBase"
    WindowsServer2012RTMJapanese64BitSQL2014SP3Express = "WindowsServer2012RTMJapanese64BitSQL2014SP3Express"
    WindowsServer2016EnglishCoreSQL2016SP2Standard = "WindowsServer2016EnglishCoreSQL2016SP2Standard"
    WindowsServer2016JapaneseFullSQL2016SP2Standard = "WindowsServer2016JapaneseFullSQL2016SP2Standard"
    WindowsServer2019PortuguesePortugalFullBase = "WindowsServer2019PortuguesePortugalFullBase"
    WindowsServer2019SwedishFullBase = "WindowsServer2019SwedishFullBase"
    WindowsServer2012R2RTMEnglish64BitHyperV = "WindowsServer2012R2RTMEnglish64BitHyperV"
    WindowsServer2012RTMKorean64BitBase = "WindowsServer2012RTMKorean64BitBase"
    WindowsServer2012RTMRussian64BitBase = "WindowsServer2012RTMRussian64BitBase"
    WindowsServer2016ChineseTraditionalFullBase = "WindowsServer2016ChineseTraditionalFullBase"
    WindowsServer2016EnglishFullSQL2016SP2Web = "WindowsServer2016EnglishFullSQL2016SP2Web"
    WindowsServer2016EnglishFullSQL2017Express = "WindowsServer2016EnglishFullSQL2017Express"

__all__ = ["AllTraffic", "AmazonLinuxEdition", "AmazonLinuxGeneration", "AmazonLinuxImage", "AmazonLinuxImageProps", "AmazonLinuxStorage", "AmazonLinuxVirt", "AnyIPv4", "AnyIPv6", "CfnCustomerGateway", "CfnCustomerGatewayProps", "CfnDHCPOptions", "CfnDHCPOptionsProps", "CfnEC2Fleet", "CfnEC2FleetProps", "CfnEIP", "CfnEIPAssociation", "CfnEIPAssociationProps", "CfnEIPProps", "CfnEgressOnlyInternetGateway", "CfnEgressOnlyInternetGatewayProps", "CfnFlowLog", "CfnFlowLogProps", "CfnHost", "CfnHostProps", "CfnInstance", "CfnInstanceProps", "CfnInternetGateway", "CfnInternetGatewayProps", "CfnLaunchTemplate", "CfnLaunchTemplateProps", "CfnNatGateway", "CfnNatGatewayProps", "CfnNetworkAcl", "CfnNetworkAclEntry", "CfnNetworkAclEntryProps", "CfnNetworkAclProps", "CfnNetworkInterface", "CfnNetworkInterfaceAttachment", "CfnNetworkInterfaceAttachmentProps", "CfnNetworkInterfacePermission", "CfnNetworkInterfacePermissionProps", "CfnNetworkInterfaceProps", "CfnPlacementGroup", "CfnPlacementGroupProps", "CfnRoute", "CfnRouteProps", "CfnRouteTable", "CfnRouteTableProps", "CfnSecurityGroup", "CfnSecurityGroupEgress", "CfnSecurityGroupEgressProps", "CfnSecurityGroupIngress", "CfnSecurityGroupIngressProps", "CfnSecurityGroupProps", "CfnSpotFleet", "CfnSpotFleetProps", "CfnSubnet", "CfnSubnetCidrBlock", "CfnSubnetCidrBlockProps", "CfnSubnetNetworkAclAssociation", "CfnSubnetNetworkAclAssociationProps", "CfnSubnetProps", "CfnSubnetRouteTableAssociation", "CfnSubnetRouteTableAssociationProps", "CfnTransitGateway", "CfnTransitGatewayAttachment", "CfnTransitGatewayAttachmentProps", "CfnTransitGatewayProps", "CfnTransitGatewayRoute", "CfnTransitGatewayRouteProps", "CfnTransitGatewayRouteTable", "CfnTransitGatewayRouteTableAssociation", "CfnTransitGatewayRouteTableAssociationProps", "CfnTransitGatewayRouteTablePropagation", "CfnTransitGatewayRouteTablePropagationProps", "CfnTransitGatewayRouteTableProps", "CfnTrunkInterfaceAssociation", "CfnTrunkInterfaceAssociationProps", "CfnVPC", "CfnVPCCidrBlock", "CfnVPCCidrBlockProps", "CfnVPCDHCPOptionsAssociation", "CfnVPCDHCPOptionsAssociationProps", "CfnVPCEndpoint", "CfnVPCEndpointConnectionNotification", "CfnVPCEndpointConnectionNotificationProps", "CfnVPCEndpointProps", "CfnVPCEndpointService", "CfnVPCEndpointServicePermissions", "CfnVPCEndpointServicePermissionsProps", "CfnVPCEndpointServiceProps", "CfnVPCGatewayAttachment", "CfnVPCGatewayAttachmentProps", "CfnVPCPeeringConnection", "CfnVPCPeeringConnectionProps", "CfnVPCProps", "CfnVPNConnection", "CfnVPNConnectionProps", "CfnVPNConnectionRoute", "CfnVPNConnectionRouteProps", "CfnVPNGateway", "CfnVPNGatewayProps", "CfnVPNGatewayRoutePropagation", "CfnVPNGatewayRoutePropagationProps", "CfnVolume", "CfnVolumeAttachment", "CfnVolumeAttachmentProps", "CfnVolumeProps", "CidrIPv4", "CidrIPv6", "ConnectionRule", "Connections", "ConnectionsProps", "DefaultInstanceTenancy", "GenericLinuxImage", "IConnectable", "IMachineImageSource", "IPortRange", "ISecurityGroup", "ISecurityGroupRule", "IVpcNetwork", "IVpcSubnet", "IVpnConnection", "IcmpAllTypeCodes", "IcmpAllTypesAndCodes", "IcmpPing", "IcmpTypeAndCode", "InstanceClass", "InstanceSize", "InstanceType", "InstanceTypePair", "LinuxOS", "MachineImage", "OperatingSystem", "OperatingSystemType", "PrefixList", "Protocol", "SecurityGroup", "SecurityGroupBase", "SecurityGroupImportProps", "SecurityGroupProps", "SubnetConfiguration", "SubnetSelection", "SubnetType", "TcpAllPorts", "TcpPort", "TcpPortFromAttribute", "TcpPortRange", "UdpAllPorts", "UdpPort", "UdpPortFromAttribute", "UdpPortRange", "VpcNetwork", "VpcNetworkBase", "VpcNetworkImportProps", "VpcNetworkProps", "VpcNetworkProvider", "VpcNetworkProviderProps", "VpcPrivateSubnet", "VpcPublicSubnet", "VpcSubnet", "VpcSubnetImportProps", "VpcSubnetProps", "VpnConnection", "VpnConnectionOptions", "VpnConnectionProps", "VpnConnectionType", "VpnTunnelOption", "WindowsImage", "WindowsOS", "WindowsVersion", "__jsii_assembly__"]

publication.publish()
