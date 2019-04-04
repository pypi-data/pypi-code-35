import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-redshift", "0.28.0", __name__, "aws-redshift@0.28.0.jsii.tgz")
class CfnCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster_type: str, db_name: str, master_username: str, master_user_password: str, node_type: str, allow_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, automated_snapshot_retention_period: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, availability_zone: typing.Optional[str]=None, cluster_identifier: typing.Optional[str]=None, cluster_parameter_group_name: typing.Optional[str]=None, cluster_security_groups: typing.Optional[typing.List[str]]=None, cluster_subnet_group_name: typing.Optional[str]=None, cluster_version: typing.Optional[str]=None, elastic_ip: typing.Optional[str]=None, encrypted: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, hsm_client_certificate_identifier: typing.Optional[str]=None, hsm_configuration_identifier: typing.Optional[str]=None, iam_roles: typing.Optional[typing.List[str]]=None, kms_key_id: typing.Optional[str]=None, logging_properties: typing.Optional[typing.Union[aws_cdk.cdk.Token, "LoggingPropertiesProperty"]]=None, number_of_nodes: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, owner_account: typing.Optional[str]=None, port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, preferred_maintenance_window: typing.Optional[str]=None, publicly_accessible: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, snapshot_cluster_identifier: typing.Optional[str]=None, snapshot_identifier: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnClusterProps = {"clusterType": cluster_type, "dbName": db_name, "masterUsername": master_username, "masterUserPassword": master_user_password, "nodeType": node_type}

        if allow_version_upgrade is not None:
            props["allowVersionUpgrade"] = allow_version_upgrade

        if automated_snapshot_retention_period is not None:
            props["automatedSnapshotRetentionPeriod"] = automated_snapshot_retention_period

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if cluster_identifier is not None:
            props["clusterIdentifier"] = cluster_identifier

        if cluster_parameter_group_name is not None:
            props["clusterParameterGroupName"] = cluster_parameter_group_name

        if cluster_security_groups is not None:
            props["clusterSecurityGroups"] = cluster_security_groups

        if cluster_subnet_group_name is not None:
            props["clusterSubnetGroupName"] = cluster_subnet_group_name

        if cluster_version is not None:
            props["clusterVersion"] = cluster_version

        if elastic_ip is not None:
            props["elasticIp"] = elastic_ip

        if encrypted is not None:
            props["encrypted"] = encrypted

        if hsm_client_certificate_identifier is not None:
            props["hsmClientCertificateIdentifier"] = hsm_client_certificate_identifier

        if hsm_configuration_identifier is not None:
            props["hsmConfigurationIdentifier"] = hsm_configuration_identifier

        if iam_roles is not None:
            props["iamRoles"] = iam_roles

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if logging_properties is not None:
            props["loggingProperties"] = logging_properties

        if number_of_nodes is not None:
            props["numberOfNodes"] = number_of_nodes

        if owner_account is not None:
            props["ownerAccount"] = owner_account

        if port is not None:
            props["port"] = port

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if publicly_accessible is not None:
            props["publiclyAccessible"] = publicly_accessible

        if snapshot_cluster_identifier is not None:
            props["snapshotClusterIdentifier"] = snapshot_cluster_identifier

        if snapshot_identifier is not None:
            props["snapshotIdentifier"] = snapshot_identifier

        if tags is not None:
            props["tags"] = tags

        if vpc_security_group_ids is not None:
            props["vpcSecurityGroupIds"] = vpc_security_group_ids

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="clusterEndpointAddress")
    def cluster_endpoint_address(self) -> str:
        return jsii.get(self, "clusterEndpointAddress")

    @property
    @jsii.member(jsii_name="clusterEndpointPort")
    def cluster_endpoint_port(self) -> str:
        return jsii.get(self, "clusterEndpointPort")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _LoggingPropertiesProperty(jsii.compat.TypedDict, total=False):
        s3KeyPrefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnCluster.LoggingPropertiesProperty")
    class LoggingPropertiesProperty(_LoggingPropertiesProperty):
        bucketName: str


class CfnClusterParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnClusterParameterGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, parameter_group_family: str, parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ParameterProperty"]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnClusterParameterGroupProps = {"description": description, "parameterGroupFamily": parameter_group_family}

        if parameters is not None:
            props["parameters"] = parameters

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> str:
        return jsii.get(self, "clusterParameterGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterParameterGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterParameterGroup.ParameterProperty")
    class ParameterProperty(jsii.compat.TypedDict):
        parameterName: str
        parameterValue: str


class _CfnClusterParameterGroupProps(jsii.compat.TypedDict, total=False):
    parameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnClusterParameterGroup.ParameterProperty"]]]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterParameterGroupProps")
class CfnClusterParameterGroupProps(_CfnClusterParameterGroupProps):
    description: str
    parameterGroupFamily: str

class _CfnClusterProps(jsii.compat.TypedDict, total=False):
    allowVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    automatedSnapshotRetentionPeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    availabilityZone: str
    clusterIdentifier: str
    clusterParameterGroupName: str
    clusterSecurityGroups: typing.List[str]
    clusterSubnetGroupName: str
    clusterVersion: str
    elasticIp: str
    encrypted: typing.Union[bool, aws_cdk.cdk.Token]
    hsmClientCertificateIdentifier: str
    hsmConfigurationIdentifier: str
    iamRoles: typing.List[str]
    kmsKeyId: str
    loggingProperties: typing.Union[aws_cdk.cdk.Token, "CfnCluster.LoggingPropertiesProperty"]
    numberOfNodes: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    ownerAccount: str
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    preferredMaintenanceWindow: str
    publiclyAccessible: typing.Union[bool, aws_cdk.cdk.Token]
    snapshotClusterIdentifier: str
    snapshotIdentifier: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcSecurityGroupIds: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterProps")
class CfnClusterProps(_CfnClusterProps):
    clusterType: str
    dbName: str
    masterUsername: str
    masterUserPassword: str
    nodeType: str

class CfnClusterSecurityGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnClusterSecurityGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnClusterSecurityGroupProps = {"description": description}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnClusterSecurityGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="clusterSecurityGroupName")
    def cluster_security_group_name(self) -> str:
        return jsii.get(self, "clusterSecurityGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterSecurityGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnClusterSecurityGroupIngress(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnClusterSecurityGroupIngress"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster_security_group_name: str, cidrip: typing.Optional[str]=None, ec2_security_group_name: typing.Optional[str]=None, ec2_security_group_owner_id: typing.Optional[str]=None) -> None:
        props: CfnClusterSecurityGroupIngressProps = {"clusterSecurityGroupName": cluster_security_group_name}

        if cidrip is not None:
            props["cidrip"] = cidrip

        if ec2_security_group_name is not None:
            props["ec2SecurityGroupName"] = ec2_security_group_name

        if ec2_security_group_owner_id is not None:
            props["ec2SecurityGroupOwnerId"] = ec2_security_group_owner_id

        jsii.create(CfnClusterSecurityGroupIngress, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterSecurityGroupIngressProps":
        return jsii.get(self, "propertyOverrides")


class _CfnClusterSecurityGroupIngressProps(jsii.compat.TypedDict, total=False):
    cidrip: str
    ec2SecurityGroupName: str
    ec2SecurityGroupOwnerId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterSecurityGroupIngressProps")
class CfnClusterSecurityGroupIngressProps(_CfnClusterSecurityGroupIngressProps):
    clusterSecurityGroupName: str

class _CfnClusterSecurityGroupProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterSecurityGroupProps")
class CfnClusterSecurityGroupProps(_CfnClusterSecurityGroupProps):
    description: str

class CfnClusterSubnetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnClusterSubnetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, subnet_ids: typing.List[str], tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnClusterSubnetGroupProps = {"description": description, "subnetIds": subnet_ids}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnClusterSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="clusterSubnetGroupName")
    def cluster_subnet_group_name(self) -> str:
        return jsii.get(self, "clusterSubnetGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterSubnetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnClusterSubnetGroupProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterSubnetGroupProps")
class CfnClusterSubnetGroupProps(_CfnClusterSubnetGroupProps):
    description: str
    subnetIds: typing.List[str]

__all__ = ["CfnCluster", "CfnClusterParameterGroup", "CfnClusterParameterGroupProps", "CfnClusterProps", "CfnClusterSecurityGroup", "CfnClusterSecurityGroupIngress", "CfnClusterSecurityGroupIngressProps", "CfnClusterSecurityGroupProps", "CfnClusterSubnetGroup", "CfnClusterSubnetGroupProps", "__jsii_assembly__"]

publication.publish()
