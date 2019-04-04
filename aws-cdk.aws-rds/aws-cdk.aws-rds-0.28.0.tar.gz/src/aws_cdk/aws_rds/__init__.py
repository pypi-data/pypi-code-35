import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_sam
import aws_cdk.aws_secretsmanager
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-rds", "0.28.0", __name__, "aws-rds@0.28.0.jsii.tgz")
class _BackupProps(jsii.compat.TypedDict, total=False):
    preferredWindow: str

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.BackupProps")
class BackupProps(_BackupProps):
    retentionDays: jsii.Number

class CfnDBCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, engine: str, availability_zones: typing.Optional[typing.List[str]]=None, backtrack_window: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, backup_retention_period: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, database_name: typing.Optional[str]=None, db_cluster_identifier: typing.Optional[str]=None, db_cluster_parameter_group_name: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, deletion_protection: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]]=None, enable_iam_database_authentication: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, engine_mode: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, master_username: typing.Optional[str]=None, master_user_password: typing.Optional[str]=None, port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, replication_source_identifier: typing.Optional[str]=None, scaling_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ScalingConfigurationProperty"]]=None, snapshot_identifier: typing.Optional[str]=None, source_region: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnDBClusterProps = {"engine": engine}

        if availability_zones is not None:
            props["availabilityZones"] = availability_zones

        if backtrack_window is not None:
            props["backtrackWindow"] = backtrack_window

        if backup_retention_period is not None:
            props["backupRetentionPeriod"] = backup_retention_period

        if database_name is not None:
            props["databaseName"] = database_name

        if db_cluster_identifier is not None:
            props["dbClusterIdentifier"] = db_cluster_identifier

        if db_cluster_parameter_group_name is not None:
            props["dbClusterParameterGroupName"] = db_cluster_parameter_group_name

        if db_subnet_group_name is not None:
            props["dbSubnetGroupName"] = db_subnet_group_name

        if deletion_protection is not None:
            props["deletionProtection"] = deletion_protection

        if enable_cloudwatch_logs_exports is not None:
            props["enableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports

        if enable_iam_database_authentication is not None:
            props["enableIamDatabaseAuthentication"] = enable_iam_database_authentication

        if engine_mode is not None:
            props["engineMode"] = engine_mode

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if master_username is not None:
            props["masterUsername"] = master_username

        if master_user_password is not None:
            props["masterUserPassword"] = master_user_password

        if port is not None:
            props["port"] = port

        if preferred_backup_window is not None:
            props["preferredBackupWindow"] = preferred_backup_window

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if replication_source_identifier is not None:
            props["replicationSourceIdentifier"] = replication_source_identifier

        if scaling_configuration is not None:
            props["scalingConfiguration"] = scaling_configuration

        if snapshot_identifier is not None:
            props["snapshotIdentifier"] = snapshot_identifier

        if source_region is not None:
            props["sourceRegion"] = source_region

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
    @jsii.member(jsii_name="dbClusterEndpointAddress")
    def db_cluster_endpoint_address(self) -> str:
        return jsii.get(self, "dbClusterEndpointAddress")

    @property
    @jsii.member(jsii_name="dbClusterEndpointPort")
    def db_cluster_endpoint_port(self) -> str:
        return jsii.get(self, "dbClusterEndpointPort")

    @property
    @jsii.member(jsii_name="dbClusterName")
    def db_cluster_name(self) -> str:
        return jsii.get(self, "dbClusterName")

    @property
    @jsii.member(jsii_name="dbClusterReadEndpointAddress")
    def db_cluster_read_endpoint_address(self) -> str:
        return jsii.get(self, "dbClusterReadEndpointAddress")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBClusterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBCluster.ScalingConfigurationProperty")
    class ScalingConfigurationProperty(jsii.compat.TypedDict, total=False):
        autoPause: typing.Union[bool, aws_cdk.cdk.Token]
        maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        secondsUntilAutoPause: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class CfnDBClusterParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBClusterParameterGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, family: str, parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDBClusterParameterGroupProps = {"description": description, "family": family, "parameters": parameters}

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
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBClusterParameterGroupProps")
class CfnDBClusterParameterGroupProps(_CfnDBClusterParameterGroupProps):
    description: str
    family: str
    parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class _CfnDBClusterProps(jsii.compat.TypedDict, total=False):
    availabilityZones: typing.List[str]
    backtrackWindow: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    backupRetentionPeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    databaseName: str
    dbClusterIdentifier: str
    dbClusterParameterGroupName: str
    dbSubnetGroupName: str
    deletionProtection: typing.Union[bool, aws_cdk.cdk.Token]
    enableCloudwatchLogsExports: typing.List[str]
    enableIamDatabaseAuthentication: typing.Union[bool, aws_cdk.cdk.Token]
    engineMode: str
    engineVersion: str
    kmsKeyId: str
    masterUsername: str
    masterUserPassword: str
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    preferredBackupWindow: str
    preferredMaintenanceWindow: str
    replicationSourceIdentifier: str
    scalingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDBCluster.ScalingConfigurationProperty"]
    snapshotIdentifier: str
    sourceRegion: str
    storageEncrypted: typing.Union[bool, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcSecurityGroupIds: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBClusterProps")
class CfnDBClusterProps(_CfnDBClusterProps):
    engine: str

class CfnDBInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_instance_class: str, allocated_storage: typing.Optional[str]=None, allow_major_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, availability_zone: typing.Optional[str]=None, backup_retention_period: typing.Optional[str]=None, character_set_name: typing.Optional[str]=None, copy_tags_to_snapshot: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, db_cluster_identifier: typing.Optional[str]=None, db_instance_identifier: typing.Optional[str]=None, db_name: typing.Optional[str]=None, db_parameter_group_name: typing.Optional[str]=None, db_security_groups: typing.Optional[typing.List[str]]=None, db_snapshot_identifier: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, delete_automated_backups: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, deletion_protection: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, domain: typing.Optional[str]=None, domain_iam_role_name: typing.Optional[str]=None, enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]]=None, enable_iam_database_authentication: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, enable_performance_insights: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, engine: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, iops: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, kms_key_id: typing.Optional[str]=None, license_model: typing.Optional[str]=None, master_username: typing.Optional[str]=None, master_user_password: typing.Optional[str]=None, monitoring_interval: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, monitoring_role_arn: typing.Optional[str]=None, multi_az: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, option_group_name: typing.Optional[str]=None, performance_insights_kms_key_id: typing.Optional[str]=None, performance_insights_retention_period: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, port: typing.Optional[str]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, processor_features: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ProcessorFeatureProperty"]]]]=None, promotion_tier: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, publicly_accessible: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, source_db_instance_identifier: typing.Optional[str]=None, source_region: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, storage_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, timezone: typing.Optional[str]=None, use_default_processor_features: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, vpc_security_groups: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnDBInstanceProps = {"dbInstanceClass": db_instance_class}

        if allocated_storage is not None:
            props["allocatedStorage"] = allocated_storage

        if allow_major_version_upgrade is not None:
            props["allowMajorVersionUpgrade"] = allow_major_version_upgrade

        if auto_minor_version_upgrade is not None:
            props["autoMinorVersionUpgrade"] = auto_minor_version_upgrade

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if backup_retention_period is not None:
            props["backupRetentionPeriod"] = backup_retention_period

        if character_set_name is not None:
            props["characterSetName"] = character_set_name

        if copy_tags_to_snapshot is not None:
            props["copyTagsToSnapshot"] = copy_tags_to_snapshot

        if db_cluster_identifier is not None:
            props["dbClusterIdentifier"] = db_cluster_identifier

        if db_instance_identifier is not None:
            props["dbInstanceIdentifier"] = db_instance_identifier

        if db_name is not None:
            props["dbName"] = db_name

        if db_parameter_group_name is not None:
            props["dbParameterGroupName"] = db_parameter_group_name

        if db_security_groups is not None:
            props["dbSecurityGroups"] = db_security_groups

        if db_snapshot_identifier is not None:
            props["dbSnapshotIdentifier"] = db_snapshot_identifier

        if db_subnet_group_name is not None:
            props["dbSubnetGroupName"] = db_subnet_group_name

        if delete_automated_backups is not None:
            props["deleteAutomatedBackups"] = delete_automated_backups

        if deletion_protection is not None:
            props["deletionProtection"] = deletion_protection

        if domain is not None:
            props["domain"] = domain

        if domain_iam_role_name is not None:
            props["domainIamRoleName"] = domain_iam_role_name

        if enable_cloudwatch_logs_exports is not None:
            props["enableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports

        if enable_iam_database_authentication is not None:
            props["enableIamDatabaseAuthentication"] = enable_iam_database_authentication

        if enable_performance_insights is not None:
            props["enablePerformanceInsights"] = enable_performance_insights

        if engine is not None:
            props["engine"] = engine

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if iops is not None:
            props["iops"] = iops

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if license_model is not None:
            props["licenseModel"] = license_model

        if master_username is not None:
            props["masterUsername"] = master_username

        if master_user_password is not None:
            props["masterUserPassword"] = master_user_password

        if monitoring_interval is not None:
            props["monitoringInterval"] = monitoring_interval

        if monitoring_role_arn is not None:
            props["monitoringRoleArn"] = monitoring_role_arn

        if multi_az is not None:
            props["multiAz"] = multi_az

        if option_group_name is not None:
            props["optionGroupName"] = option_group_name

        if performance_insights_kms_key_id is not None:
            props["performanceInsightsKmsKeyId"] = performance_insights_kms_key_id

        if performance_insights_retention_period is not None:
            props["performanceInsightsRetentionPeriod"] = performance_insights_retention_period

        if port is not None:
            props["port"] = port

        if preferred_backup_window is not None:
            props["preferredBackupWindow"] = preferred_backup_window

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if processor_features is not None:
            props["processorFeatures"] = processor_features

        if promotion_tier is not None:
            props["promotionTier"] = promotion_tier

        if publicly_accessible is not None:
            props["publiclyAccessible"] = publicly_accessible

        if source_db_instance_identifier is not None:
            props["sourceDbInstanceIdentifier"] = source_db_instance_identifier

        if source_region is not None:
            props["sourceRegion"] = source_region

        if storage_encrypted is not None:
            props["storageEncrypted"] = storage_encrypted

        if storage_type is not None:
            props["storageType"] = storage_type

        if tags is not None:
            props["tags"] = tags

        if timezone is not None:
            props["timezone"] = timezone

        if use_default_processor_features is not None:
            props["useDefaultProcessorFeatures"] = use_default_processor_features

        if vpc_security_groups is not None:
            props["vpcSecurityGroups"] = vpc_security_groups

        jsii.create(CfnDBInstance, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        return jsii.get(self, "dbInstanceEndpointAddress")

    @property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        return jsii.get(self, "dbInstanceEndpointPort")

    @property
    @jsii.member(jsii_name="dbInstanceId")
    def db_instance_id(self) -> str:
        return jsii.get(self, "dbInstanceId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBInstanceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBInstance.ProcessorFeatureProperty")
    class ProcessorFeatureProperty(jsii.compat.TypedDict, total=False):
        name: str
        value: str


class _CfnDBInstanceProps(jsii.compat.TypedDict, total=False):
    allocatedStorage: str
    allowMajorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    autoMinorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    availabilityZone: str
    backupRetentionPeriod: str
    characterSetName: str
    copyTagsToSnapshot: typing.Union[bool, aws_cdk.cdk.Token]
    dbClusterIdentifier: str
    dbInstanceIdentifier: str
    dbName: str
    dbParameterGroupName: str
    dbSecurityGroups: typing.List[str]
    dbSnapshotIdentifier: str
    dbSubnetGroupName: str
    deleteAutomatedBackups: typing.Union[bool, aws_cdk.cdk.Token]
    deletionProtection: typing.Union[bool, aws_cdk.cdk.Token]
    domain: str
    domainIamRoleName: str
    enableCloudwatchLogsExports: typing.List[str]
    enableIamDatabaseAuthentication: typing.Union[bool, aws_cdk.cdk.Token]
    enablePerformanceInsights: typing.Union[bool, aws_cdk.cdk.Token]
    engine: str
    engineVersion: str
    iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    kmsKeyId: str
    licenseModel: str
    masterUsername: str
    masterUserPassword: str
    monitoringInterval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    monitoringRoleArn: str
    multiAz: typing.Union[bool, aws_cdk.cdk.Token]
    optionGroupName: str
    performanceInsightsKmsKeyId: str
    performanceInsightsRetentionPeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    port: str
    preferredBackupWindow: str
    preferredMaintenanceWindow: str
    processorFeatures: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDBInstance.ProcessorFeatureProperty"]]]
    promotionTier: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    publiclyAccessible: typing.Union[bool, aws_cdk.cdk.Token]
    sourceDbInstanceIdentifier: str
    sourceRegion: str
    storageEncrypted: typing.Union[bool, aws_cdk.cdk.Token]
    storageType: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    timezone: str
    useDefaultProcessorFeatures: typing.Union[bool, aws_cdk.cdk.Token]
    vpcSecurityGroups: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBInstanceProps")
class CfnDBInstanceProps(_CfnDBInstanceProps):
    dbInstanceClass: str

class CfnDBParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBParameterGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, family: str, parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDBParameterGroupProps = {"description": description, "family": family}

        if parameters is not None:
            props["parameters"] = parameters

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
    parameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBParameterGroupProps")
class CfnDBParameterGroupProps(_CfnDBParameterGroupProps):
    description: str
    family: str

class CfnDBSecurityGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_security_group_ingress: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "IngressProperty"]]], group_description: str, ec2_vpc_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnDBSecurityGroupProps = {"dbSecurityGroupIngress": db_security_group_ingress, "groupDescription": group_description}

        if ec2_vpc_id is not None:
            props["ec2VpcId"] = ec2_vpc_id

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBSecurityGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dbSecurityGroupName")
    def db_security_group_name(self) -> str:
        return jsii.get(self, "dbSecurityGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBSecurityGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroup.IngressProperty")
    class IngressProperty(jsii.compat.TypedDict, total=False):
        cidrip: str
        ec2SecurityGroupId: str
        ec2SecurityGroupName: str
        ec2SecurityGroupOwnerId: str


class CfnDBSecurityGroupIngress(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroupIngress"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_security_group_name: str, cidrip: typing.Optional[str]=None, ec2_security_group_id: typing.Optional[str]=None, ec2_security_group_name: typing.Optional[str]=None, ec2_security_group_owner_id: typing.Optional[str]=None) -> None:
        props: CfnDBSecurityGroupIngressProps = {"dbSecurityGroupName": db_security_group_name}

        if cidrip is not None:
            props["cidrip"] = cidrip

        if ec2_security_group_id is not None:
            props["ec2SecurityGroupId"] = ec2_security_group_id

        if ec2_security_group_name is not None:
            props["ec2SecurityGroupName"] = ec2_security_group_name

        if ec2_security_group_owner_id is not None:
            props["ec2SecurityGroupOwnerId"] = ec2_security_group_owner_id

        jsii.create(CfnDBSecurityGroupIngress, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="dbSecurityGroupIngressName")
    def db_security_group_ingress_name(self) -> str:
        return jsii.get(self, "dbSecurityGroupIngressName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBSecurityGroupIngressProps":
        return jsii.get(self, "propertyOverrides")


class _CfnDBSecurityGroupIngressProps(jsii.compat.TypedDict, total=False):
    cidrip: str
    ec2SecurityGroupId: str
    ec2SecurityGroupName: str
    ec2SecurityGroupOwnerId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroupIngressProps")
class CfnDBSecurityGroupIngressProps(_CfnDBSecurityGroupIngressProps):
    dbSecurityGroupName: str

class _CfnDBSecurityGroupProps(jsii.compat.TypedDict, total=False):
    ec2VpcId: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroupProps")
class CfnDBSecurityGroupProps(_CfnDBSecurityGroupProps):
    dbSecurityGroupIngress: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDBSecurityGroup.IngressProperty"]]]
    groupDescription: str

class CfnDBSubnetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBSubnetGroup"):
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

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBSubnetGroupProps")
class CfnDBSubnetGroupProps(_CfnDBSubnetGroupProps):
    dbSubnetGroupDescription: str
    subnetIds: typing.List[str]

class CfnEventSubscription(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnEventSubscription"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, sns_topic_arn: str, enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, event_categories: typing.Optional[typing.List[str]]=None, source_ids: typing.Optional[typing.List[str]]=None, source_type: typing.Optional[str]=None) -> None:
        props: CfnEventSubscriptionProps = {"snsTopicArn": sns_topic_arn}

        if enabled is not None:
            props["enabled"] = enabled

        if event_categories is not None:
            props["eventCategories"] = event_categories

        if source_ids is not None:
            props["sourceIds"] = source_ids

        if source_type is not None:
            props["sourceType"] = source_type

        jsii.create(CfnEventSubscription, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="eventSubscriptionName")
    def event_subscription_name(self) -> str:
        return jsii.get(self, "eventSubscriptionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEventSubscriptionProps":
        return jsii.get(self, "propertyOverrides")


class _CfnEventSubscriptionProps(jsii.compat.TypedDict, total=False):
    enabled: typing.Union[bool, aws_cdk.cdk.Token]
    eventCategories: typing.List[str]
    sourceIds: typing.List[str]
    sourceType: str

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnEventSubscriptionProps")
class CfnEventSubscriptionProps(_CfnEventSubscriptionProps):
    snsTopicArn: str

class CfnOptionGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnOptionGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, engine_name: str, major_engine_version: str, option_configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "OptionConfigurationProperty"]]], option_group_description: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnOptionGroupProps = {"engineName": engine_name, "majorEngineVersion": major_engine_version, "optionConfigurations": option_configurations, "optionGroupDescription": option_group_description}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnOptionGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="optionGroupName")
    def option_group_name(self) -> str:
        return jsii.get(self, "optionGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnOptionGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _OptionConfigurationProperty(jsii.compat.TypedDict, total=False):
        dbSecurityGroupMemberships: typing.List[str]
        optionSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnOptionGroup.OptionSettingProperty"]]]
        optionVersion: str
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        vpcSecurityGroupMemberships: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnOptionGroup.OptionConfigurationProperty")
    class OptionConfigurationProperty(_OptionConfigurationProperty):
        optionName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnOptionGroup.OptionSettingProperty")
    class OptionSettingProperty(jsii.compat.TypedDict, total=False):
        name: str
        value: str


class _CfnOptionGroupProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnOptionGroupProps")
class CfnOptionGroupProps(_CfnOptionGroupProps):
    engineName: str
    majorEngineVersion: str
    optionConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnOptionGroup.OptionConfigurationProperty"]]]
    optionGroupDescription: str

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.ClusterParameterGroupImportProps")
class ClusterParameterGroupImportProps(jsii.compat.TypedDict):
    parameterGroupName: str

class _ClusterParameterGroupProps(jsii.compat.TypedDict, total=False):
    parameters: typing.Mapping[str,typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.ClusterParameterGroupProps")
class ClusterParameterGroupProps(_ClusterParameterGroupProps):
    description: str
    family: str

@jsii.enum(jsii_type="@aws-cdk/aws-rds.DatabaseClusterEngine")
class DatabaseClusterEngine(enum.Enum):
    Aurora = "Aurora"
    AuroraMysql = "AuroraMysql"
    AuroraPostgresql = "AuroraPostgresql"
    Neptune = "Neptune"

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.DatabaseClusterImportProps")
class DatabaseClusterImportProps(jsii.compat.TypedDict):
    clusterEndpointAddress: str
    clusterIdentifier: str
    instanceEndpointAddresses: typing.List[str]
    instanceIdentifiers: typing.List[str]
    port: str
    readerEndpointAddress: str
    securityGroupId: str

class _DatabaseClusterProps(jsii.compat.TypedDict, total=False):
    backup: "BackupProps"
    clusterIdentifier: str
    defaultDatabaseName: str
    deleteReplacePolicy: aws_cdk.cdk.DeletionPolicy
    instanceIdentifierBase: str
    instances: jsii.Number
    kmsKey: aws_cdk.aws_kms.IEncryptionKey
    parameterGroup: "IClusterParameterGroup"
    port: jsii.Number
    preferredMaintenanceWindow: str
    storageEncrypted: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.DatabaseClusterProps")
class DatabaseClusterProps(_DatabaseClusterProps):
    engine: "DatabaseClusterEngine"
    instanceProps: "InstanceProps"
    masterUser: "Login"

@jsii.enum(jsii_type="@aws-cdk/aws-rds.DatabaseEngine")
class DatabaseEngine(enum.Enum):
    MariaDb = "MariaDb"
    Mysql = "Mysql"
    Oracle = "Oracle"
    Postgres = "Postgres"
    SqlServer = "SqlServer"

class DatabaseSecret(aws_cdk.aws_secretsmanager.Secret, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.DatabaseSecret"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, username: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None) -> None:
        props: DatabaseSecretProps = {"username": username}

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        jsii.create(DatabaseSecret, self, [scope, id, props])


class _DatabaseSecretProps(jsii.compat.TypedDict, total=False):
    encryptionKey: aws_cdk.aws_kms.IEncryptionKey

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.DatabaseSecretProps")
class DatabaseSecretProps(_DatabaseSecretProps):
    username: str

class Endpoint(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.Endpoint"):
    def __init__(self, address: str, port: str) -> None:
        jsii.create(Endpoint, self, [address, port])

    @property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> str:
        return jsii.get(self, "hostname")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> str:
        return jsii.get(self, "port")

    @property
    @jsii.member(jsii_name="socketAddress")
    def socket_address(self) -> str:
        return jsii.get(self, "socketAddress")


@jsii.interface(jsii_type="@aws-cdk/aws-rds.IClusterParameterGroup")
class IClusterParameterGroup(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IClusterParameterGroupProxy

    @property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterParameterGroupImportProps":
        ...


class _IClusterParameterGroupProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-rds.IClusterParameterGroup"
    @property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        return jsii.get(self, "parameterGroupName")

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterParameterGroupImportProps":
        return jsii.invoke(self, "export", [])


@jsii.implements(IClusterParameterGroup)
class ClusterParameterGroup(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.ClusterParameterGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, family: str, parameters: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        props: ClusterParameterGroupProps = {"description": description, "family": family}

        if parameters is not None:
            props["parameters"] = parameters

        jsii.create(ClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, parameter_group_name: str) -> "IClusterParameterGroup":
        props: ClusterParameterGroupImportProps = {"parameterGroupName": parameter_group_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "ClusterParameterGroupImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="removeParameter")
    def remove_parameter(self, key: str) -> None:
        return jsii.invoke(self, "removeParameter", [key])

    @jsii.member(jsii_name="setParameter")
    def set_parameter(self, key: str, value: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "setParameter", [key, value])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        return jsii.get(self, "parameterGroupName")


@jsii.interface(jsii_type="@aws-cdk/aws-rds.IDatabaseCluster")
class IDatabaseCluster(aws_cdk.cdk.IConstruct, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_secretsmanager.ISecretAttachmentTarget, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseClusterProxy

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        ...

    @property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        ...

    @property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        ...

    @property
    @jsii.member(jsii_name="readerEndpoint")
    def reader_endpoint(self) -> "Endpoint":
        ...

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "DatabaseClusterImportProps":
        ...


class _IDatabaseClusterProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), jsii.proxy_for(aws_cdk.aws_secretsmanager.ISecretAttachmentTarget)):
    __jsii_type__ = "@aws-cdk/aws-rds.IDatabaseCluster"
    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        return jsii.get(self, "clusterIdentifier")

    @property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        return jsii.get(self, "instanceEndpoints")

    @property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        return jsii.get(self, "instanceIdentifiers")

    @property
    @jsii.member(jsii_name="readerEndpoint")
    def reader_endpoint(self) -> "Endpoint":
        return jsii.get(self, "readerEndpoint")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        return jsii.get(self, "securityGroupId")

    @jsii.member(jsii_name="export")
    def export(self) -> "DatabaseClusterImportProps":
        return jsii.invoke(self, "export", [])


@jsii.implements(IDatabaseCluster)
class DatabaseClusterBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-rds.DatabaseClusterBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _DatabaseClusterBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(DatabaseClusterBase, self, [scope, id])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, cluster_endpoint_address: str, cluster_identifier: str, instance_endpoint_addresses: typing.List[str], instance_identifiers: typing.List[str], port: str, reader_endpoint_address: str, security_group_id: str) -> "IDatabaseCluster":
        props: DatabaseClusterImportProps = {"clusterEndpointAddress": cluster_endpoint_address, "clusterIdentifier": cluster_identifier, "instanceEndpointAddresses": instance_endpoint_addresses, "instanceIdentifiers": instance_identifiers, "port": port, "readerEndpointAddress": reader_endpoint_address, "securityGroupId": security_group_id}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> aws_cdk.aws_secretsmanager.SecretAttachmentTargetProps:
        return jsii.invoke(self, "asSecretAttachmentTarget", [])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "DatabaseClusterImportProps":
        ...

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    @abc.abstractmethod
    def cluster_endpoint(self) -> "Endpoint":
        ...

    @property
    @jsii.member(jsii_name="clusterIdentifier")
    @abc.abstractmethod
    def cluster_identifier(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="connections")
    @abc.abstractmethod
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        ...

    @property
    @jsii.member(jsii_name="instanceEndpoints")
    @abc.abstractmethod
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        ...

    @property
    @jsii.member(jsii_name="instanceIdentifiers")
    @abc.abstractmethod
    def instance_identifiers(self) -> typing.List[str]:
        ...

    @property
    @jsii.member(jsii_name="readerEndpoint")
    @abc.abstractmethod
    def reader_endpoint(self) -> "Endpoint":
        ...

    @property
    @jsii.member(jsii_name="securityGroupId")
    @abc.abstractmethod
    def security_group_id(self) -> str:
        ...


class _DatabaseClusterBaseProxy(DatabaseClusterBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "DatabaseClusterImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        return jsii.get(self, "clusterIdentifier")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        return jsii.get(self, "instanceEndpoints")

    @property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        return jsii.get(self, "instanceIdentifiers")

    @property
    @jsii.member(jsii_name="readerEndpoint")
    def reader_endpoint(self) -> "Endpoint":
        return jsii.get(self, "readerEndpoint")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        return jsii.get(self, "securityGroupId")


@jsii.implements(IDatabaseCluster)
class DatabaseCluster(DatabaseClusterBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.DatabaseCluster"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, engine: "DatabaseClusterEngine", instance_props: "InstanceProps", master_user: "Login", backup: typing.Optional["BackupProps"]=None, cluster_identifier: typing.Optional[str]=None, default_database_name: typing.Optional[str]=None, delete_replace_policy: typing.Optional[aws_cdk.cdk.DeletionPolicy]=None, instance_identifier_base: typing.Optional[str]=None, instances: typing.Optional[jsii.Number]=None, kms_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, parameter_group: typing.Optional["IClusterParameterGroup"]=None, port: typing.Optional[jsii.Number]=None, preferred_maintenance_window: typing.Optional[str]=None, storage_encrypted: typing.Optional[bool]=None) -> None:
        props: DatabaseClusterProps = {"engine": engine, "instanceProps": instance_props, "masterUser": master_user}

        if backup is not None:
            props["backup"] = backup

        if cluster_identifier is not None:
            props["clusterIdentifier"] = cluster_identifier

        if default_database_name is not None:
            props["defaultDatabaseName"] = default_database_name

        if delete_replace_policy is not None:
            props["deleteReplacePolicy"] = delete_replace_policy

        if instance_identifier_base is not None:
            props["instanceIdentifierBase"] = instance_identifier_base

        if instances is not None:
            props["instances"] = instances

        if kms_key is not None:
            props["kmsKey"] = kms_key

        if parameter_group is not None:
            props["parameterGroup"] = parameter_group

        if port is not None:
            props["port"] = port

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if storage_encrypted is not None:
            props["storageEncrypted"] = storage_encrypted

        jsii.create(DatabaseCluster, self, [scope, id, props])

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(self, id: str, *, automatically_after_days: typing.Optional[jsii.Number]=None, serverless_application_location: typing.Optional["ServerlessApplicationLocation"]=None) -> "RotationSingleUser":
        options: RotationSingleUserOptions = {}

        if automatically_after_days is not None:
            options["automaticallyAfterDays"] = automatically_after_days

        if serverless_application_location is not None:
            options["serverlessApplicationLocation"] = serverless_application_location

        return jsii.invoke(self, "addRotationSingleUser", [id, options])

    @jsii.member(jsii_name="export")
    def export(self) -> "DatabaseClusterImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        return jsii.get(self, "clusterIdentifier")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="engine")
    def engine(self) -> "DatabaseClusterEngine":
        return jsii.get(self, "engine")

    @property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        return jsii.get(self, "instanceEndpoints")

    @property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        return jsii.get(self, "instanceIdentifiers")

    @property
    @jsii.member(jsii_name="readerEndpoint")
    def reader_endpoint(self) -> "Endpoint":
        return jsii.get(self, "readerEndpoint")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        return jsii.get(self, "securityGroupId")

    @property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        return jsii.get(self, "secret")


class _InstanceProps(jsii.compat.TypedDict, total=False):
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.InstanceProps")
class InstanceProps(_InstanceProps):
    instanceType: aws_cdk.aws_ec2.InstanceType
    vpc: aws_cdk.aws_ec2.IVpcNetwork

class _Login(jsii.compat.TypedDict, total=False):
    kmsKey: aws_cdk.aws_kms.IEncryptionKey
    password: aws_cdk.cdk.SecretValue

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.Login")
class Login(_Login):
    username: str

class RotationSingleUser(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.RotationSingleUser"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret: aws_cdk.aws_secretsmanager.ISecret, target: aws_cdk.aws_ec2.IConnectable, vpc: aws_cdk.aws_ec2.IVpcNetwork, engine: typing.Optional["DatabaseEngine"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, automatically_after_days: typing.Optional[jsii.Number]=None, serverless_application_location: typing.Optional["ServerlessApplicationLocation"]=None) -> None:
        props: RotationSingleUserProps = {"secret": secret, "target": target, "vpc": vpc}

        if engine is not None:
            props["engine"] = engine

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        if automatically_after_days is not None:
            props["automaticallyAfterDays"] = automatically_after_days

        if serverless_application_location is not None:
            props["serverlessApplicationLocation"] = serverless_application_location

        jsii.create(RotationSingleUser, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-rds.RotationSingleUserOptions")
class RotationSingleUserOptions(jsii.compat.TypedDict, total=False):
    automaticallyAfterDays: jsii.Number
    serverlessApplicationLocation: "ServerlessApplicationLocation"

class _RotationSingleUserProps(RotationSingleUserOptions, jsii.compat.TypedDict, total=False):
    engine: "DatabaseEngine"
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.RotationSingleUserProps")
class RotationSingleUserProps(_RotationSingleUserProps):
    secret: aws_cdk.aws_secretsmanager.ISecret
    target: aws_cdk.aws_ec2.IConnectable
    vpc: aws_cdk.aws_ec2.IVpcNetwork

class ServerlessApplicationLocation(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.ServerlessApplicationLocation"):
    def __init__(self, application_id: str, semantic_version: str) -> None:
        jsii.create(ServerlessApplicationLocation, self, [application_id, semantic_version])

    @classproperty
    @jsii.member(jsii_name="MariaDbRotationSingleUser")
    def MARIA_DB_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "MariaDbRotationSingleUser")

    @classproperty
    @jsii.member(jsii_name="MysqlRotationSingleUser")
    def MYSQL_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "MysqlRotationSingleUser")

    @classproperty
    @jsii.member(jsii_name="OracleRotationSingleUser")
    def ORACLE_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "OracleRotationSingleUser")

    @classproperty
    @jsii.member(jsii_name="PostgresRotationSingleUser")
    def POSTGRES_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "PostgresRotationSingleUser")

    @classproperty
    @jsii.member(jsii_name="SqlServerRotationSingleUser")
    def SQL_SERVER_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "SqlServerRotationSingleUser")

    @property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        return jsii.get(self, "applicationId")

    @property
    @jsii.member(jsii_name="semanticVersion")
    def semantic_version(self) -> str:
        return jsii.get(self, "semanticVersion")


__all__ = ["BackupProps", "CfnDBCluster", "CfnDBClusterParameterGroup", "CfnDBClusterParameterGroupProps", "CfnDBClusterProps", "CfnDBInstance", "CfnDBInstanceProps", "CfnDBParameterGroup", "CfnDBParameterGroupProps", "CfnDBSecurityGroup", "CfnDBSecurityGroupIngress", "CfnDBSecurityGroupIngressProps", "CfnDBSecurityGroupProps", "CfnDBSubnetGroup", "CfnDBSubnetGroupProps", "CfnEventSubscription", "CfnEventSubscriptionProps", "CfnOptionGroup", "CfnOptionGroupProps", "ClusterParameterGroup", "ClusterParameterGroupImportProps", "ClusterParameterGroupProps", "DatabaseCluster", "DatabaseClusterBase", "DatabaseClusterEngine", "DatabaseClusterImportProps", "DatabaseClusterProps", "DatabaseEngine", "DatabaseSecret", "DatabaseSecretProps", "Endpoint", "IClusterParameterGroup", "IDatabaseCluster", "InstanceProps", "Login", "RotationSingleUser", "RotationSingleUserOptions", "RotationSingleUserProps", "ServerlessApplicationLocation", "__jsii_assembly__"]

publication.publish()
