import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticache", "0.28.0", __name__, "aws-elasticache@0.28.0.jsii.tgz")
class CfnCacheCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticache.CfnCacheCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cache_node_type: str, engine: str, num_cache_nodes: typing.Union[jsii.Number, aws_cdk.cdk.Token], auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, az_mode: typing.Optional[str]=None, cache_parameter_group_name: typing.Optional[str]=None, cache_security_group_names: typing.Optional[typing.List[str]]=None, cache_subnet_group_name: typing.Optional[str]=None, cluster_name: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, notification_topic_arn: typing.Optional[str]=None, port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, preferred_availability_zone: typing.Optional[str]=None, preferred_availability_zones: typing.Optional[typing.List[str]]=None, preferred_maintenance_window: typing.Optional[str]=None, snapshot_arns: typing.Optional[typing.List[str]]=None, snapshot_name: typing.Optional[str]=None, snapshot_retention_limit: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, snapshot_window: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnCacheClusterProps = {"cacheNodeType": cache_node_type, "engine": engine, "numCacheNodes": num_cache_nodes}

        if auto_minor_version_upgrade is not None:
            props["autoMinorVersionUpgrade"] = auto_minor_version_upgrade

        if az_mode is not None:
            props["azMode"] = az_mode

        if cache_parameter_group_name is not None:
            props["cacheParameterGroupName"] = cache_parameter_group_name

        if cache_security_group_names is not None:
            props["cacheSecurityGroupNames"] = cache_security_group_names

        if cache_subnet_group_name is not None:
            props["cacheSubnetGroupName"] = cache_subnet_group_name

        if cluster_name is not None:
            props["clusterName"] = cluster_name

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if notification_topic_arn is not None:
            props["notificationTopicArn"] = notification_topic_arn

        if port is not None:
            props["port"] = port

        if preferred_availability_zone is not None:
            props["preferredAvailabilityZone"] = preferred_availability_zone

        if preferred_availability_zones is not None:
            props["preferredAvailabilityZones"] = preferred_availability_zones

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if snapshot_arns is not None:
            props["snapshotArns"] = snapshot_arns

        if snapshot_name is not None:
            props["snapshotName"] = snapshot_name

        if snapshot_retention_limit is not None:
            props["snapshotRetentionLimit"] = snapshot_retention_limit

        if snapshot_window is not None:
            props["snapshotWindow"] = snapshot_window

        if tags is not None:
            props["tags"] = tags

        if vpc_security_group_ids is not None:
            props["vpcSecurityGroupIds"] = vpc_security_group_ids

        jsii.create(CfnCacheCluster, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="cacheClusterConfigurationEndpointAddress")
    def cache_cluster_configuration_endpoint_address(self) -> str:
        return jsii.get(self, "cacheClusterConfigurationEndpointAddress")

    @property
    @jsii.member(jsii_name="cacheClusterConfigurationEndpointPort")
    def cache_cluster_configuration_endpoint_port(self) -> str:
        return jsii.get(self, "cacheClusterConfigurationEndpointPort")

    @property
    @jsii.member(jsii_name="cacheClusterName")
    def cache_cluster_name(self) -> str:
        return jsii.get(self, "cacheClusterName")

    @property
    @jsii.member(jsii_name="cacheClusterRedisEndpointAddress")
    def cache_cluster_redis_endpoint_address(self) -> str:
        return jsii.get(self, "cacheClusterRedisEndpointAddress")

    @property
    @jsii.member(jsii_name="cacheClusterRedisEndpointPort")
    def cache_cluster_redis_endpoint_port(self) -> str:
        return jsii.get(self, "cacheClusterRedisEndpointPort")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCacheClusterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnCacheClusterProps(jsii.compat.TypedDict, total=False):
    autoMinorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    azMode: str
    cacheParameterGroupName: str
    cacheSecurityGroupNames: typing.List[str]
    cacheSubnetGroupName: str
    clusterName: str
    engineVersion: str
    notificationTopicArn: str
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    preferredAvailabilityZone: str
    preferredAvailabilityZones: typing.List[str]
    preferredMaintenanceWindow: str
    snapshotArns: typing.List[str]
    snapshotName: str
    snapshotRetentionLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    snapshotWindow: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcSecurityGroupIds: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticache.CfnCacheClusterProps")
class CfnCacheClusterProps(_CfnCacheClusterProps):
    cacheNodeType: str
    engine: str
    numCacheNodes: typing.Union[jsii.Number, aws_cdk.cdk.Token]

class CfnParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticache.CfnParameterGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cache_parameter_group_family: str, description: str, properties: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None) -> None:
        props: CfnParameterGroupProps = {"cacheParameterGroupFamily": cache_parameter_group_family, "description": description}

        if properties is not None:
            props["properties"] = properties

        jsii.create(CfnParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        return jsii.get(self, "parameterGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnParameterGroupProps":
        return jsii.get(self, "propertyOverrides")


class _CfnParameterGroupProps(jsii.compat.TypedDict, total=False):
    properties: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticache.CfnParameterGroupProps")
class CfnParameterGroupProps(_CfnParameterGroupProps):
    cacheParameterGroupFamily: str
    description: str

class CfnReplicationGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticache.CfnReplicationGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, replication_group_description: str, at_rest_encryption_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, auth_token: typing.Optional[str]=None, automatic_failover_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, cache_node_type: typing.Optional[str]=None, cache_parameter_group_name: typing.Optional[str]=None, cache_security_group_names: typing.Optional[typing.List[str]]=None, cache_subnet_group_name: typing.Optional[str]=None, engine: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, node_group_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "NodeGroupConfigurationProperty"]]]]=None, notification_topic_arn: typing.Optional[str]=None, num_cache_clusters: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, num_node_groups: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, preferred_cache_cluster_a_zs: typing.Optional[typing.List[str]]=None, preferred_maintenance_window: typing.Optional[str]=None, primary_cluster_id: typing.Optional[str]=None, replicas_per_node_group: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, replication_group_id: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, snapshot_arns: typing.Optional[typing.List[str]]=None, snapshot_name: typing.Optional[str]=None, snapshot_retention_limit: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, snapshotting_cluster_id: typing.Optional[str]=None, snapshot_window: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, transit_encryption_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnReplicationGroupProps = {"replicationGroupDescription": replication_group_description}

        if at_rest_encryption_enabled is not None:
            props["atRestEncryptionEnabled"] = at_rest_encryption_enabled

        if auth_token is not None:
            props["authToken"] = auth_token

        if automatic_failover_enabled is not None:
            props["automaticFailoverEnabled"] = automatic_failover_enabled

        if auto_minor_version_upgrade is not None:
            props["autoMinorVersionUpgrade"] = auto_minor_version_upgrade

        if cache_node_type is not None:
            props["cacheNodeType"] = cache_node_type

        if cache_parameter_group_name is not None:
            props["cacheParameterGroupName"] = cache_parameter_group_name

        if cache_security_group_names is not None:
            props["cacheSecurityGroupNames"] = cache_security_group_names

        if cache_subnet_group_name is not None:
            props["cacheSubnetGroupName"] = cache_subnet_group_name

        if engine is not None:
            props["engine"] = engine

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if node_group_configuration is not None:
            props["nodeGroupConfiguration"] = node_group_configuration

        if notification_topic_arn is not None:
            props["notificationTopicArn"] = notification_topic_arn

        if num_cache_clusters is not None:
            props["numCacheClusters"] = num_cache_clusters

        if num_node_groups is not None:
            props["numNodeGroups"] = num_node_groups

        if port is not None:
            props["port"] = port

        if preferred_cache_cluster_a_zs is not None:
            props["preferredCacheClusterAZs"] = preferred_cache_cluster_a_zs

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if primary_cluster_id is not None:
            props["primaryClusterId"] = primary_cluster_id

        if replicas_per_node_group is not None:
            props["replicasPerNodeGroup"] = replicas_per_node_group

        if replication_group_id is not None:
            props["replicationGroupId"] = replication_group_id

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if snapshot_arns is not None:
            props["snapshotArns"] = snapshot_arns

        if snapshot_name is not None:
            props["snapshotName"] = snapshot_name

        if snapshot_retention_limit is not None:
            props["snapshotRetentionLimit"] = snapshot_retention_limit

        if snapshotting_cluster_id is not None:
            props["snapshottingClusterId"] = snapshotting_cluster_id

        if snapshot_window is not None:
            props["snapshotWindow"] = snapshot_window

        if tags is not None:
            props["tags"] = tags

        if transit_encryption_enabled is not None:
            props["transitEncryptionEnabled"] = transit_encryption_enabled

        jsii.create(CfnReplicationGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnReplicationGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="replicationGroupConfigurationEndPointAddress")
    def replication_group_configuration_end_point_address(self) -> str:
        return jsii.get(self, "replicationGroupConfigurationEndPointAddress")

    @property
    @jsii.member(jsii_name="replicationGroupConfigurationEndPointPort")
    def replication_group_configuration_end_point_port(self) -> str:
        return jsii.get(self, "replicationGroupConfigurationEndPointPort")

    @property
    @jsii.member(jsii_name="replicationGroupName")
    def replication_group_name(self) -> str:
        return jsii.get(self, "replicationGroupName")

    @property
    @jsii.member(jsii_name="replicationGroupPrimaryEndPointAddress")
    def replication_group_primary_end_point_address(self) -> str:
        return jsii.get(self, "replicationGroupPrimaryEndPointAddress")

    @property
    @jsii.member(jsii_name="replicationGroupPrimaryEndPointPort")
    def replication_group_primary_end_point_port(self) -> str:
        return jsii.get(self, "replicationGroupPrimaryEndPointPort")

    @property
    @jsii.member(jsii_name="replicationGroupReadEndPointAddresses")
    def replication_group_read_end_point_addresses(self) -> str:
        return jsii.get(self, "replicationGroupReadEndPointAddresses")

    @property
    @jsii.member(jsii_name="replicationGroupReadEndPointAddressesList")
    def replication_group_read_end_point_addresses_list(self) -> typing.List[str]:
        return jsii.get(self, "replicationGroupReadEndPointAddressesList")

    @property
    @jsii.member(jsii_name="replicationGroupReadEndPointPorts")
    def replication_group_read_end_point_ports(self) -> str:
        return jsii.get(self, "replicationGroupReadEndPointPorts")

    @property
    @jsii.member(jsii_name="replicationGroupReadEndPointPortsList")
    def replication_group_read_end_point_ports_list(self) -> typing.List[str]:
        return jsii.get(self, "replicationGroupReadEndPointPortsList")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticache.CfnReplicationGroup.NodeGroupConfigurationProperty")
    class NodeGroupConfigurationProperty(jsii.compat.TypedDict, total=False):
        nodeGroupId: str
        primaryAvailabilityZone: str
        replicaAvailabilityZones: typing.List[str]
        replicaCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        slots: str


class _CfnReplicationGroupProps(jsii.compat.TypedDict, total=False):
    atRestEncryptionEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    authToken: str
    automaticFailoverEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    autoMinorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    cacheNodeType: str
    cacheParameterGroupName: str
    cacheSecurityGroupNames: typing.List[str]
    cacheSubnetGroupName: str
    engine: str
    engineVersion: str
    nodeGroupConfiguration: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnReplicationGroup.NodeGroupConfigurationProperty"]]]
    notificationTopicArn: str
    numCacheClusters: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    numNodeGroups: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    preferredCacheClusterAZs: typing.List[str]
    preferredMaintenanceWindow: str
    primaryClusterId: str
    replicasPerNodeGroup: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    replicationGroupId: str
    securityGroupIds: typing.List[str]
    snapshotArns: typing.List[str]
    snapshotName: str
    snapshotRetentionLimit: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    snapshottingClusterId: str
    snapshotWindow: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    transitEncryptionEnabled: typing.Union[bool, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticache.CfnReplicationGroupProps")
class CfnReplicationGroupProps(_CfnReplicationGroupProps):
    replicationGroupDescription: str

class CfnSecurityGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticache.CfnSecurityGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str) -> None:
        props: CfnSecurityGroupProps = {"description": description}

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
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> str:
        return jsii.get(self, "securityGroupName")


class CfnSecurityGroupIngress(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticache.CfnSecurityGroupIngress"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cache_security_group_name: str, ec2_security_group_name: str, ec2_security_group_owner_id: typing.Optional[str]=None) -> None:
        props: CfnSecurityGroupIngressProps = {"cacheSecurityGroupName": cache_security_group_name, "ec2SecurityGroupName": ec2_security_group_name}

        if ec2_security_group_owner_id is not None:
            props["ec2SecurityGroupOwnerId"] = ec2_security_group_owner_id

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
    ec2SecurityGroupOwnerId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticache.CfnSecurityGroupIngressProps")
class CfnSecurityGroupIngressProps(_CfnSecurityGroupIngressProps):
    cacheSecurityGroupName: str
    ec2SecurityGroupName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticache.CfnSecurityGroupProps")
class CfnSecurityGroupProps(jsii.compat.TypedDict):
    description: str

class CfnSubnetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticache.CfnSubnetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, subnet_ids: typing.List[str], cache_subnet_group_name: typing.Optional[str]=None) -> None:
        props: CfnSubnetGroupProps = {"description": description, "subnetIds": subnet_ids}

        if cache_subnet_group_name is not None:
            props["cacheSubnetGroupName"] = cache_subnet_group_name

        jsii.create(CfnSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubnetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> str:
        return jsii.get(self, "subnetGroupName")


class _CfnSubnetGroupProps(jsii.compat.TypedDict, total=False):
    cacheSubnetGroupName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticache.CfnSubnetGroupProps")
class CfnSubnetGroupProps(_CfnSubnetGroupProps):
    description: str
    subnetIds: typing.List[str]

__all__ = ["CfnCacheCluster", "CfnCacheClusterProps", "CfnParameterGroup", "CfnParameterGroupProps", "CfnReplicationGroup", "CfnReplicationGroupProps", "CfnSecurityGroup", "CfnSecurityGroupIngress", "CfnSecurityGroupIngressProps", "CfnSecurityGroupProps", "CfnSubnetGroup", "CfnSubnetGroupProps", "__jsii_assembly__"]

publication.publish()
