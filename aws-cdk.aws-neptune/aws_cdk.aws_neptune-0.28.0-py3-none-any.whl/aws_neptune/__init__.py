import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-neptune", "0.28.0", __name__, "aws-neptune@0.28.0.jsii.tgz")
class CfnDBCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zones: typing.Optional[typing.List[str]]=None, backup_retention_period: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, db_cluster_identifier: typing.Optional[str]=None, db_cluster_parameter_group_name: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, iam_auth_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, kms_key_id: typing.Optional[str]=None, port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, snapshot_identifier: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnDBClusterProps = {}

        if availability_zones is not None:
            props["availabilityZones"] = availability_zones

        if backup_retention_period is not None:
            props["backupRetentionPeriod"] = backup_retention_period

        if db_cluster_identifier is not None:
            props["dbClusterIdentifier"] = db_cluster_identifier

        if db_cluster_parameter_group_name is not None:
            props["dbClusterParameterGroupName"] = db_cluster_parameter_group_name

        if db_subnet_group_name is not None:
            props["dbSubnetGroupName"] = db_subnet_group_name

        if iam_auth_enabled is not None:
            props["iamAuthEnabled"] = iam_auth_enabled

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if port is not None:
            props["port"] = port

        if preferred_backup_window is not None:
            props["preferredBackupWindow"] = preferred_backup_window

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if snapshot_identifier is not None:
            props["snapshotIdentifier"] = snapshot_identifier

        if storage_encrypted is not None:
            props["storageEncrypted"] = storage_encrypted

        if tags is not None:
            props["tags"] = tags

        if vpc_security_group_ids is not None:
            props["vpcSecurityGroupIds"] = vpc_security_group_ids

        jsii.create(CfnDBCluster, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dbClusterClusterResourceId")
    def db_cluster_cluster_resource_id(self) -> str:
        return jsii.get(self, "dbClusterClusterResourceId")

    @property
    @jsii.member(jsii_name="dbClusterEndpoint")
    def db_cluster_endpoint(self) -> str:
        return jsii.get(self, "dbClusterEndpoint")

    @property
    @jsii.member(jsii_name="dbClusterName")
    def db_cluster_name(self) -> str:
        return jsii.get(self, "dbClusterName")

    @property
    @jsii.member(jsii_name="dbClusterPort")
    def db_cluster_port(self) -> str:
        return jsii.get(self, "dbClusterPort")

    @property
    @jsii.member(jsii_name="dbClusterReadEndpoint")
    def db_cluster_read_endpoint(self) -> str:
        return jsii.get(self, "dbClusterReadEndpoint")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBClusterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnDBClusterParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBClusterParameterGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, family: str, parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDBClusterParameterGroupProps = {"description": description, "family": family, "parameters": parameters}

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dbClusterParameterGroupName")
    def db_cluster_parameter_group_name(self) -> str:
        return jsii.get(self, "dbClusterParameterGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBClusterParameterGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnDBClusterParameterGroupProps(jsii.compat.TypedDict, total=False):
    name: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBClusterParameterGroupProps")
class CfnDBClusterParameterGroupProps(_CfnDBClusterParameterGroupProps):
    description: str
    family: str
    parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBClusterProps")
class CfnDBClusterProps(jsii.compat.TypedDict, total=False):
    availabilityZones: typing.List[str]
    backupRetentionPeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    dbClusterIdentifier: str
    dbClusterParameterGroupName: str
    dbSubnetGroupName: str
    iamAuthEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    kmsKeyId: str
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    preferredBackupWindow: str
    preferredMaintenanceWindow: str
    snapshotIdentifier: str
    storageEncrypted: typing.Union[bool, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcSecurityGroupIds: typing.List[str]

class CfnDBInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_instance_class: str, allow_major_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, availability_zone: typing.Optional[str]=None, db_cluster_identifier: typing.Optional[str]=None, db_instance_identifier: typing.Optional[str]=None, db_parameter_group_name: typing.Optional[str]=None, db_snapshot_identifier: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDBInstanceProps = {"dbInstanceClass": db_instance_class}

        if allow_major_version_upgrade is not None:
            props["allowMajorVersionUpgrade"] = allow_major_version_upgrade

        if auto_minor_version_upgrade is not None:
            props["autoMinorVersionUpgrade"] = auto_minor_version_upgrade

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if db_cluster_identifier is not None:
            props["dbClusterIdentifier"] = db_cluster_identifier

        if db_instance_identifier is not None:
            props["dbInstanceIdentifier"] = db_instance_identifier

        if db_parameter_group_name is not None:
            props["dbParameterGroupName"] = db_parameter_group_name

        if db_snapshot_identifier is not None:
            props["dbSnapshotIdentifier"] = db_snapshot_identifier

        if db_subnet_group_name is not None:
            props["dbSubnetGroupName"] = db_subnet_group_name

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBInstance, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dbInstanceEndpoint")
    def db_instance_endpoint(self) -> str:
        return jsii.get(self, "dbInstanceEndpoint")

    @property
    @jsii.member(jsii_name="dbInstanceId")
    def db_instance_id(self) -> str:
        return jsii.get(self, "dbInstanceId")

    @property
    @jsii.member(jsii_name="dbInstancePort")
    def db_instance_port(self) -> str:
        return jsii.get(self, "dbInstancePort")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBInstanceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnDBInstanceProps(jsii.compat.TypedDict, total=False):
    allowMajorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    autoMinorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    availabilityZone: str
    dbClusterIdentifier: str
    dbInstanceIdentifier: str
    dbParameterGroupName: str
    dbSnapshotIdentifier: str
    dbSubnetGroupName: str
    preferredMaintenanceWindow: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBInstanceProps")
class CfnDBInstanceProps(_CfnDBInstanceProps):
    dbInstanceClass: str

class CfnDBParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBParameterGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, family: str, parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDBParameterGroupProps = {"description": description, "family": family, "parameters": parameters}

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dbParameterGroupName")
    def db_parameter_group_name(self) -> str:
        return jsii.get(self, "dbParameterGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBParameterGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnDBParameterGroupProps(jsii.compat.TypedDict, total=False):
    name: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBParameterGroupProps")
class CfnDBParameterGroupProps(_CfnDBParameterGroupProps):
    description: str
    family: str
    parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnDBSubnetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBSubnetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_subnet_group_description: str, subnet_ids: typing.List[str], db_subnet_group_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDBSubnetGroupProps = {"dbSubnetGroupDescription": db_subnet_group_description, "subnetIds": subnet_ids}

        if db_subnet_group_name is not None:
            props["dbSubnetGroupName"] = db_subnet_group_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> str:
        return jsii.get(self, "dbSubnetGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBSubnetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnDBSubnetGroupProps(jsii.compat.TypedDict, total=False):
    dbSubnetGroupName: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBSubnetGroupProps")
class CfnDBSubnetGroupProps(_CfnDBSubnetGroupProps):
    dbSubnetGroupDescription: str
    subnetIds: typing.List[str]

__all__ = ["CfnDBCluster", "CfnDBClusterParameterGroup", "CfnDBClusterParameterGroupProps", "CfnDBClusterProps", "CfnDBInstance", "CfnDBInstanceProps", "CfnDBParameterGroup", "CfnDBParameterGroupProps", "CfnDBSubnetGroup", "CfnDBSubnetGroupProps", "__jsii_assembly__"]

publication.publish()
