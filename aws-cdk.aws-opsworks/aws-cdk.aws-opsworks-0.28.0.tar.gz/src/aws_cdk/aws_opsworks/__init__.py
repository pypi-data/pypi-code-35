import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-opsworks", "0.28.0", __name__, "aws-opsworks@0.28.0.jsii.tgz")
class CfnApp(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnApp"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, stack_id: str, type: str, app_source: typing.Optional[typing.Union["SourceProperty", aws_cdk.cdk.Token]]=None, attributes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, data_sources: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "DataSourceProperty"]]]]=None, description: typing.Optional[str]=None, domains: typing.Optional[typing.List[str]]=None, enable_ssl: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, environment: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "EnvironmentVariableProperty"]]]]=None, shortname: typing.Optional[str]=None, ssl_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SslConfigurationProperty"]]=None) -> None:
        props: CfnAppProps = {"name": name, "stackId": stack_id, "type": type}

        if app_source is not None:
            props["appSource"] = app_source

        if attributes is not None:
            props["attributes"] = attributes

        if data_sources is not None:
            props["dataSources"] = data_sources

        if description is not None:
            props["description"] = description

        if domains is not None:
            props["domains"] = domains

        if enable_ssl is not None:
            props["enableSsl"] = enable_ssl

        if environment is not None:
            props["environment"] = environment

        if shortname is not None:
            props["shortname"] = shortname

        if ssl_configuration is not None:
            props["sslConfiguration"] = ssl_configuration

        jsii.create(CfnApp, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> str:
        return jsii.get(self, "appId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAppProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.DataSourceProperty")
    class DataSourceProperty(jsii.compat.TypedDict, total=False):
        arn: str
        databaseName: str
        type: str

    class _EnvironmentVariableProperty(jsii.compat.TypedDict, total=False):
        secure: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.EnvironmentVariableProperty")
    class EnvironmentVariableProperty(_EnvironmentVariableProperty):
        key: str
        value: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.SourceProperty")
    class SourceProperty(jsii.compat.TypedDict, total=False):
        password: str
        revision: str
        sshKey: str
        type: str
        url: str
        username: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.SslConfigurationProperty")
    class SslConfigurationProperty(jsii.compat.TypedDict, total=False):
        certificate: str
        chain: str
        privateKey: str


class _CfnAppProps(jsii.compat.TypedDict, total=False):
    appSource: typing.Union["CfnApp.SourceProperty", aws_cdk.cdk.Token]
    attributes: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    dataSources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApp.DataSourceProperty"]]]
    description: str
    domains: typing.List[str]
    enableSsl: typing.Union[bool, aws_cdk.cdk.Token]
    environment: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApp.EnvironmentVariableProperty"]]]
    shortname: str
    sslConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApp.SslConfigurationProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnAppProps")
class CfnAppProps(_CfnAppProps):
    name: str
    stackId: str
    type: str

class CfnElasticLoadBalancerAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnElasticLoadBalancerAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, elastic_load_balancer_name: str, layer_id: str) -> None:
        props: CfnElasticLoadBalancerAttachmentProps = {"elasticLoadBalancerName": elastic_load_balancer_name, "layerId": layer_id}

        jsii.create(CfnElasticLoadBalancerAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnElasticLoadBalancerAttachmentProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnElasticLoadBalancerAttachmentProps")
class CfnElasticLoadBalancerAttachmentProps(jsii.compat.TypedDict):
    elasticLoadBalancerName: str
    layerId: str

class CfnInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_type: str, layer_ids: typing.List[str], stack_id: str, agent_version: typing.Optional[str]=None, ami_id: typing.Optional[str]=None, architecture: typing.Optional[str]=None, auto_scaling_type: typing.Optional[str]=None, availability_zone: typing.Optional[str]=None, block_device_mappings: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "BlockDeviceMappingProperty"]]]]=None, ebs_optimized: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, elastic_ips: typing.Optional[typing.List[str]]=None, hostname: typing.Optional[str]=None, install_updates_on_boot: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, os: typing.Optional[str]=None, root_device_type: typing.Optional[str]=None, ssh_key_name: typing.Optional[str]=None, subnet_id: typing.Optional[str]=None, tenancy: typing.Optional[str]=None, time_based_auto_scaling: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TimeBasedAutoScalingProperty"]]=None, virtualization_type: typing.Optional[str]=None, volumes: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnInstanceProps = {"instanceType": instance_type, "layerIds": layer_ids, "stackId": stack_id}

        if agent_version is not None:
            props["agentVersion"] = agent_version

        if ami_id is not None:
            props["amiId"] = ami_id

        if architecture is not None:
            props["architecture"] = architecture

        if auto_scaling_type is not None:
            props["autoScalingType"] = auto_scaling_type

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if block_device_mappings is not None:
            props["blockDeviceMappings"] = block_device_mappings

        if ebs_optimized is not None:
            props["ebsOptimized"] = ebs_optimized

        if elastic_ips is not None:
            props["elasticIps"] = elastic_ips

        if hostname is not None:
            props["hostname"] = hostname

        if install_updates_on_boot is not None:
            props["installUpdatesOnBoot"] = install_updates_on_boot

        if os is not None:
            props["os"] = os

        if root_device_type is not None:
            props["rootDeviceType"] = root_device_type

        if ssh_key_name is not None:
            props["sshKeyName"] = ssh_key_name

        if subnet_id is not None:
            props["subnetId"] = subnet_id

        if tenancy is not None:
            props["tenancy"] = tenancy

        if time_based_auto_scaling is not None:
            props["timeBasedAutoScaling"] = time_based_auto_scaling

        if virtualization_type is not None:
            props["virtualizationType"] = virtualization_type

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

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.BlockDeviceMappingProperty")
    class BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        deviceName: str
        ebs: typing.Union[aws_cdk.cdk.Token, "CfnInstance.EbsBlockDeviceProperty"]
        noDevice: str
        virtualName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.EbsBlockDeviceProperty")
    class EbsBlockDeviceProperty(jsii.compat.TypedDict, total=False):
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        snapshotId: str
        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.TimeBasedAutoScalingProperty")
    class TimeBasedAutoScalingProperty(jsii.compat.TypedDict, total=False):
        friday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        monday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        saturday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        sunday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        thursday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        tuesday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        wednesday: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]


class _CfnInstanceProps(jsii.compat.TypedDict, total=False):
    agentVersion: str
    amiId: str
    architecture: str
    autoScalingType: str
    availabilityZone: str
    blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.BlockDeviceMappingProperty"]]]
    ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
    elasticIps: typing.List[str]
    hostname: str
    installUpdatesOnBoot: typing.Union[bool, aws_cdk.cdk.Token]
    os: str
    rootDeviceType: str
    sshKeyName: str
    subnetId: str
    tenancy: str
    timeBasedAutoScaling: typing.Union[aws_cdk.cdk.Token, "CfnInstance.TimeBasedAutoScalingProperty"]
    virtualizationType: str
    volumes: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstanceProps")
class CfnInstanceProps(_CfnInstanceProps):
    instanceType: str
    layerIds: typing.List[str]
    stackId: str

class CfnLayer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnLayer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_assign_elastic_ips: typing.Union[bool, aws_cdk.cdk.Token], auto_assign_public_ips: typing.Union[bool, aws_cdk.cdk.Token], enable_auto_healing: typing.Union[bool, aws_cdk.cdk.Token], name: str, shortname: str, stack_id: str, type: str, attributes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, custom_instance_profile_arn: typing.Optional[str]=None, custom_json: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, custom_recipes: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RecipesProperty"]]=None, custom_security_group_ids: typing.Optional[typing.List[str]]=None, install_updates_on_boot: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, lifecycle_event_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LifecycleEventConfigurationProperty"]]=None, load_based_auto_scaling: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LoadBasedAutoScalingProperty"]]=None, packages: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, use_ebs_optimized_instances: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, volume_configurations: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "VolumeConfigurationProperty"]]]]=None) -> None:
        props: CfnLayerProps = {"autoAssignElasticIps": auto_assign_elastic_ips, "autoAssignPublicIps": auto_assign_public_ips, "enableAutoHealing": enable_auto_healing, "name": name, "shortname": shortname, "stackId": stack_id, "type": type}

        if attributes is not None:
            props["attributes"] = attributes

        if custom_instance_profile_arn is not None:
            props["customInstanceProfileArn"] = custom_instance_profile_arn

        if custom_json is not None:
            props["customJson"] = custom_json

        if custom_recipes is not None:
            props["customRecipes"] = custom_recipes

        if custom_security_group_ids is not None:
            props["customSecurityGroupIds"] = custom_security_group_ids

        if install_updates_on_boot is not None:
            props["installUpdatesOnBoot"] = install_updates_on_boot

        if lifecycle_event_configuration is not None:
            props["lifecycleEventConfiguration"] = lifecycle_event_configuration

        if load_based_auto_scaling is not None:
            props["loadBasedAutoScaling"] = load_based_auto_scaling

        if packages is not None:
            props["packages"] = packages

        if tags is not None:
            props["tags"] = tags

        if use_ebs_optimized_instances is not None:
            props["useEbsOptimizedInstances"] = use_ebs_optimized_instances

        if volume_configurations is not None:
            props["volumeConfigurations"] = volume_configurations

        jsii.create(CfnLayer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="layerId")
    def layer_id(self) -> str:
        return jsii.get(self, "layerId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLayerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.AutoScalingThresholdsProperty")
    class AutoScalingThresholdsProperty(jsii.compat.TypedDict, total=False):
        cpuThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        ignoreMetricsTime: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        instanceCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        loadThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        memoryThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        thresholdsWaitTime: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.LifecycleEventConfigurationProperty")
    class LifecycleEventConfigurationProperty(jsii.compat.TypedDict, total=False):
        shutdownEventConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnLayer.ShutdownEventConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.LoadBasedAutoScalingProperty")
    class LoadBasedAutoScalingProperty(jsii.compat.TypedDict, total=False):
        downScaling: typing.Union[aws_cdk.cdk.Token, "CfnLayer.AutoScalingThresholdsProperty"]
        enable: typing.Union[bool, aws_cdk.cdk.Token]
        upScaling: typing.Union[aws_cdk.cdk.Token, "CfnLayer.AutoScalingThresholdsProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.RecipesProperty")
    class RecipesProperty(jsii.compat.TypedDict, total=False):
        configure: typing.List[str]
        deploy: typing.List[str]
        setup: typing.List[str]
        shutdown: typing.List[str]
        undeploy: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.ShutdownEventConfigurationProperty")
    class ShutdownEventConfigurationProperty(jsii.compat.TypedDict, total=False):
        delayUntilElbConnectionsDrained: typing.Union[bool, aws_cdk.cdk.Token]
        executionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.VolumeConfigurationProperty")
    class VolumeConfigurationProperty(jsii.compat.TypedDict, total=False):
        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        mountPoint: str
        numberOfDisks: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        raidLevel: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        size: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        volumeType: str


class _CfnLayerProps(jsii.compat.TypedDict, total=False):
    attributes: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    customInstanceProfileArn: str
    customJson: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    customRecipes: typing.Union[aws_cdk.cdk.Token, "CfnLayer.RecipesProperty"]
    customSecurityGroupIds: typing.List[str]
    installUpdatesOnBoot: typing.Union[bool, aws_cdk.cdk.Token]
    lifecycleEventConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnLayer.LifecycleEventConfigurationProperty"]
    loadBasedAutoScaling: typing.Union[aws_cdk.cdk.Token, "CfnLayer.LoadBasedAutoScalingProperty"]
    packages: typing.List[str]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    useEbsOptimizedInstances: typing.Union[bool, aws_cdk.cdk.Token]
    volumeConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLayer.VolumeConfigurationProperty"]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayerProps")
class CfnLayerProps(_CfnLayerProps):
    autoAssignElasticIps: typing.Union[bool, aws_cdk.cdk.Token]
    autoAssignPublicIps: typing.Union[bool, aws_cdk.cdk.Token]
    enableAutoHealing: typing.Union[bool, aws_cdk.cdk.Token]
    name: str
    shortname: str
    stackId: str
    type: str

class CfnStack(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnStack"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, default_instance_profile_arn: str, name: str, service_role_arn: str, agent_version: typing.Optional[str]=None, attributes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, chef_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ChefConfigurationProperty"]]=None, clone_app_ids: typing.Optional[typing.List[str]]=None, clone_permissions: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, configuration_manager: typing.Optional[typing.Union[aws_cdk.cdk.Token, "StackConfigurationManagerProperty"]]=None, custom_cookbooks_source: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SourceProperty"]]=None, custom_json: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, default_availability_zone: typing.Optional[str]=None, default_os: typing.Optional[str]=None, default_root_device_type: typing.Optional[str]=None, default_ssh_key_name: typing.Optional[str]=None, default_subnet_id: typing.Optional[str]=None, ecs_cluster_arn: typing.Optional[str]=None, elastic_ips: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ElasticIpProperty"]]]]=None, hostname_theme: typing.Optional[str]=None, rds_db_instances: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "RdsDbInstanceProperty"]]]]=None, source_stack_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, use_custom_cookbooks: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, use_opsworks_security_groups: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, vpc_id: typing.Optional[str]=None) -> None:
        props: CfnStackProps = {"defaultInstanceProfileArn": default_instance_profile_arn, "name": name, "serviceRoleArn": service_role_arn}

        if agent_version is not None:
            props["agentVersion"] = agent_version

        if attributes is not None:
            props["attributes"] = attributes

        if chef_configuration is not None:
            props["chefConfiguration"] = chef_configuration

        if clone_app_ids is not None:
            props["cloneAppIds"] = clone_app_ids

        if clone_permissions is not None:
            props["clonePermissions"] = clone_permissions

        if configuration_manager is not None:
            props["configurationManager"] = configuration_manager

        if custom_cookbooks_source is not None:
            props["customCookbooksSource"] = custom_cookbooks_source

        if custom_json is not None:
            props["customJson"] = custom_json

        if default_availability_zone is not None:
            props["defaultAvailabilityZone"] = default_availability_zone

        if default_os is not None:
            props["defaultOs"] = default_os

        if default_root_device_type is not None:
            props["defaultRootDeviceType"] = default_root_device_type

        if default_ssh_key_name is not None:
            props["defaultSshKeyName"] = default_ssh_key_name

        if default_subnet_id is not None:
            props["defaultSubnetId"] = default_subnet_id

        if ecs_cluster_arn is not None:
            props["ecsClusterArn"] = ecs_cluster_arn

        if elastic_ips is not None:
            props["elasticIps"] = elastic_ips

        if hostname_theme is not None:
            props["hostnameTheme"] = hostname_theme

        if rds_db_instances is not None:
            props["rdsDbInstances"] = rds_db_instances

        if source_stack_id is not None:
            props["sourceStackId"] = source_stack_id

        if tags is not None:
            props["tags"] = tags

        if use_custom_cookbooks is not None:
            props["useCustomCookbooks"] = use_custom_cookbooks

        if use_opsworks_security_groups is not None:
            props["useOpsworksSecurityGroups"] = use_opsworks_security_groups

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(CfnStack, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStackProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        return jsii.get(self, "stackId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.ChefConfigurationProperty")
    class ChefConfigurationProperty(jsii.compat.TypedDict, total=False):
        berkshelfVersion: str
        manageBerkshelf: typing.Union[bool, aws_cdk.cdk.Token]

    class _ElasticIpProperty(jsii.compat.TypedDict, total=False):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.ElasticIpProperty")
    class ElasticIpProperty(_ElasticIpProperty):
        ip: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.RdsDbInstanceProperty")
    class RdsDbInstanceProperty(jsii.compat.TypedDict):
        dbPassword: str
        dbUser: str
        rdsDbInstanceArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.SourceProperty")
    class SourceProperty(jsii.compat.TypedDict, total=False):
        password: str
        revision: str
        sshKey: str
        type: str
        url: str
        username: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.StackConfigurationManagerProperty")
    class StackConfigurationManagerProperty(jsii.compat.TypedDict, total=False):
        name: str
        version: str


class _CfnStackProps(jsii.compat.TypedDict, total=False):
    agentVersion: str
    attributes: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    chefConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnStack.ChefConfigurationProperty"]
    cloneAppIds: typing.List[str]
    clonePermissions: typing.Union[bool, aws_cdk.cdk.Token]
    configurationManager: typing.Union[aws_cdk.cdk.Token, "CfnStack.StackConfigurationManagerProperty"]
    customCookbooksSource: typing.Union[aws_cdk.cdk.Token, "CfnStack.SourceProperty"]
    customJson: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    defaultAvailabilityZone: str
    defaultOs: str
    defaultRootDeviceType: str
    defaultSshKeyName: str
    defaultSubnetId: str
    ecsClusterArn: str
    elasticIps: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStack.ElasticIpProperty"]]]
    hostnameTheme: str
    rdsDbInstances: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStack.RdsDbInstanceProperty"]]]
    sourceStackId: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    useCustomCookbooks: typing.Union[bool, aws_cdk.cdk.Token]
    useOpsworksSecurityGroups: typing.Union[bool, aws_cdk.cdk.Token]
    vpcId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStackProps")
class CfnStackProps(_CfnStackProps):
    defaultInstanceProfileArn: str
    name: str
    serviceRoleArn: str

class CfnUserProfile(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnUserProfile"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, iam_user_arn: str, allow_self_management: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, ssh_public_key: typing.Optional[str]=None, ssh_username: typing.Optional[str]=None) -> None:
        props: CfnUserProfileProps = {"iamUserArn": iam_user_arn}

        if allow_self_management is not None:
            props["allowSelfManagement"] = allow_self_management

        if ssh_public_key is not None:
            props["sshPublicKey"] = ssh_public_key

        if ssh_username is not None:
            props["sshUsername"] = ssh_username

        jsii.create(CfnUserProfile, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnUserProfileProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="userProfileArn")
    def user_profile_arn(self) -> str:
        return jsii.get(self, "userProfileArn")

    @property
    @jsii.member(jsii_name="userProfileSshUsername")
    def user_profile_ssh_username(self) -> str:
        return jsii.get(self, "userProfileSshUsername")


class _CfnUserProfileProps(jsii.compat.TypedDict, total=False):
    allowSelfManagement: typing.Union[bool, aws_cdk.cdk.Token]
    sshPublicKey: str
    sshUsername: str

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnUserProfileProps")
class CfnUserProfileProps(_CfnUserProfileProps):
    iamUserArn: str

class CfnVolume(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnVolume"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ec2_volume_id: str, stack_id: str, mount_point: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: CfnVolumeProps = {"ec2VolumeId": ec2_volume_id, "stackId": stack_id}

        if mount_point is not None:
            props["mountPoint"] = mount_point

        if name is not None:
            props["name"] = name

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
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> str:
        return jsii.get(self, "volumeId")


class _CfnVolumeProps(jsii.compat.TypedDict, total=False):
    mountPoint: str
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnVolumeProps")
class CfnVolumeProps(_CfnVolumeProps):
    ec2VolumeId: str
    stackId: str

__all__ = ["CfnApp", "CfnAppProps", "CfnElasticLoadBalancerAttachment", "CfnElasticLoadBalancerAttachmentProps", "CfnInstance", "CfnInstanceProps", "CfnLayer", "CfnLayerProps", "CfnStack", "CfnStackProps", "CfnUserProfile", "CfnUserProfileProps", "CfnVolume", "CfnVolumeProps", "__jsii_assembly__"]

publication.publish()
