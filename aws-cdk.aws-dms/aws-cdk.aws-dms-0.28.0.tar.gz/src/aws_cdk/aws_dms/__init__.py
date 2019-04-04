import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-dms", "0.28.0", __name__, "aws-dms@0.28.0.jsii.tgz")
class CfnCertificate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dms.CfnCertificate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, certificate_identifier: typing.Optional[str]=None, certificate_pem: typing.Optional[str]=None, certificate_wallet: typing.Optional[str]=None) -> None:
        props: CfnCertificateProps = {}

        if certificate_identifier is not None:
            props["certificateIdentifier"] = certificate_identifier

        if certificate_pem is not None:
            props["certificatePem"] = certificate_pem

        if certificate_wallet is not None:
            props["certificateWallet"] = certificate_wallet

        jsii.create(CfnCertificate, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        return jsii.get(self, "certificateArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCertificateProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnCertificateProps")
class CfnCertificateProps(jsii.compat.TypedDict, total=False):
    certificateIdentifier: str
    certificatePem: str
    certificateWallet: str

class CfnEndpoint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dms.CfnEndpoint"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, endpoint_type: str, engine_name: str, certificate_arn: typing.Optional[str]=None, database_name: typing.Optional[str]=None, dynamo_db_settings: typing.Optional[typing.Union["DynamoDbSettingsProperty", aws_cdk.cdk.Token]]=None, elasticsearch_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ElasticsearchSettingsProperty"]]=None, endpoint_identifier: typing.Optional[str]=None, extra_connection_attributes: typing.Optional[str]=None, kinesis_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "KinesisSettingsProperty"]]=None, kms_key_id: typing.Optional[str]=None, mongo_db_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "MongoDbSettingsProperty"]]=None, password: typing.Optional[str]=None, port: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, s3_settings: typing.Optional[typing.Union[aws_cdk.cdk.Token, "S3SettingsProperty"]]=None, server_name: typing.Optional[str]=None, ssl_mode: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, username: typing.Optional[str]=None) -> None:
        props: CfnEndpointProps = {"endpointType": endpoint_type, "engineName": engine_name}

        if certificate_arn is not None:
            props["certificateArn"] = certificate_arn

        if database_name is not None:
            props["databaseName"] = database_name

        if dynamo_db_settings is not None:
            props["dynamoDbSettings"] = dynamo_db_settings

        if elasticsearch_settings is not None:
            props["elasticsearchSettings"] = elasticsearch_settings

        if endpoint_identifier is not None:
            props["endpointIdentifier"] = endpoint_identifier

        if extra_connection_attributes is not None:
            props["extraConnectionAttributes"] = extra_connection_attributes

        if kinesis_settings is not None:
            props["kinesisSettings"] = kinesis_settings

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if mongo_db_settings is not None:
            props["mongoDbSettings"] = mongo_db_settings

        if password is not None:
            props["password"] = password

        if port is not None:
            props["port"] = port

        if s3_settings is not None:
            props["s3Settings"] = s3_settings

        if server_name is not None:
            props["serverName"] = server_name

        if ssl_mode is not None:
            props["sslMode"] = ssl_mode

        if tags is not None:
            props["tags"] = tags

        if username is not None:
            props["username"] = username

        jsii.create(CfnEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="endpointArn")
    def endpoint_arn(self) -> str:
        return jsii.get(self, "endpointArn")

    @property
    @jsii.member(jsii_name="endpointExternalId")
    def endpoint_external_id(self) -> str:
        return jsii.get(self, "endpointExternalId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEndpointProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnEndpoint.DynamoDbSettingsProperty")
    class DynamoDbSettingsProperty(jsii.compat.TypedDict, total=False):
        serviceAccessRoleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnEndpoint.ElasticsearchSettingsProperty")
    class ElasticsearchSettingsProperty(jsii.compat.TypedDict, total=False):
        endpointUri: str
        errorRetryDuration: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        fullLoadErrorPercentage: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        serviceAccessRoleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnEndpoint.KinesisSettingsProperty")
    class KinesisSettingsProperty(jsii.compat.TypedDict, total=False):
        messageFormat: str
        serviceAccessRoleArn: str
        streamArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnEndpoint.MongoDbSettingsProperty")
    class MongoDbSettingsProperty(jsii.compat.TypedDict, total=False):
        authMechanism: str
        authSource: str
        authType: str
        databaseName: str
        docsToInvestigate: str
        extractDocId: str
        nestingLevel: str
        password: str
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        serverName: str
        username: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnEndpoint.S3SettingsProperty")
    class S3SettingsProperty(jsii.compat.TypedDict, total=False):
        bucketFolder: str
        bucketName: str
        compressionType: str
        csvDelimiter: str
        csvRowDelimiter: str
        externalTableDefinition: str
        serviceAccessRoleArn: str


class _CfnEndpointProps(jsii.compat.TypedDict, total=False):
    certificateArn: str
    databaseName: str
    dynamoDbSettings: typing.Union["CfnEndpoint.DynamoDbSettingsProperty", aws_cdk.cdk.Token]
    elasticsearchSettings: typing.Union[aws_cdk.cdk.Token, "CfnEndpoint.ElasticsearchSettingsProperty"]
    endpointIdentifier: str
    extraConnectionAttributes: str
    kinesisSettings: typing.Union[aws_cdk.cdk.Token, "CfnEndpoint.KinesisSettingsProperty"]
    kmsKeyId: str
    mongoDbSettings: typing.Union[aws_cdk.cdk.Token, "CfnEndpoint.MongoDbSettingsProperty"]
    password: str
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    s3Settings: typing.Union[aws_cdk.cdk.Token, "CfnEndpoint.S3SettingsProperty"]
    serverName: str
    sslMode: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    username: str

@jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnEndpointProps")
class CfnEndpointProps(_CfnEndpointProps):
    endpointType: str
    engineName: str

class CfnEventSubscription(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dms.CfnEventSubscription"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, sns_topic_arn: str, enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, event_categories: typing.Optional[typing.List[str]]=None, source_ids: typing.Optional[typing.List[str]]=None, source_type: typing.Optional[str]=None, subscription_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnEventSubscriptionProps = {"snsTopicArn": sns_topic_arn}

        if enabled is not None:
            props["enabled"] = enabled

        if event_categories is not None:
            props["eventCategories"] = event_categories

        if source_ids is not None:
            props["sourceIds"] = source_ids

        if source_type is not None:
            props["sourceType"] = source_type

        if subscription_name is not None:
            props["subscriptionName"] = subscription_name

        if tags is not None:
            props["tags"] = tags

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

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnEventSubscriptionProps(jsii.compat.TypedDict, total=False):
    enabled: typing.Union[bool, aws_cdk.cdk.Token]
    eventCategories: typing.List[str]
    sourceIds: typing.List[str]
    sourceType: str
    subscriptionName: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnEventSubscriptionProps")
class CfnEventSubscriptionProps(_CfnEventSubscriptionProps):
    snsTopicArn: str

class CfnReplicationInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dms.CfnReplicationInstance"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, replication_instance_class: str, allocated_storage: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, allow_major_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, auto_minor_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, availability_zone: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, multi_az: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, preferred_maintenance_window: typing.Optional[str]=None, publicly_accessible: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, replication_instance_identifier: typing.Optional[str]=None, replication_subnet_group_identifier: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        props: CfnReplicationInstanceProps = {"replicationInstanceClass": replication_instance_class}

        if allocated_storage is not None:
            props["allocatedStorage"] = allocated_storage

        if allow_major_version_upgrade is not None:
            props["allowMajorVersionUpgrade"] = allow_major_version_upgrade

        if auto_minor_version_upgrade is not None:
            props["autoMinorVersionUpgrade"] = auto_minor_version_upgrade

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if multi_az is not None:
            props["multiAz"] = multi_az

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if publicly_accessible is not None:
            props["publiclyAccessible"] = publicly_accessible

        if replication_instance_identifier is not None:
            props["replicationInstanceIdentifier"] = replication_instance_identifier

        if replication_subnet_group_identifier is not None:
            props["replicationSubnetGroupIdentifier"] = replication_subnet_group_identifier

        if tags is not None:
            props["tags"] = tags

        if vpc_security_group_ids is not None:
            props["vpcSecurityGroupIds"] = vpc_security_group_ids

        jsii.create(CfnReplicationInstance, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnReplicationInstanceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="replicationInstanceArn")
    def replication_instance_arn(self) -> str:
        return jsii.get(self, "replicationInstanceArn")

    @property
    @jsii.member(jsii_name="replicationInstancePrivateIpAddresses")
    def replication_instance_private_ip_addresses(self) -> typing.List[str]:
        return jsii.get(self, "replicationInstancePrivateIpAddresses")

    @property
    @jsii.member(jsii_name="replicationInstancePublicIpAddresses")
    def replication_instance_public_ip_addresses(self) -> typing.List[str]:
        return jsii.get(self, "replicationInstancePublicIpAddresses")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnReplicationInstanceProps(jsii.compat.TypedDict, total=False):
    allocatedStorage: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    allowMajorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    autoMinorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    availabilityZone: str
    engineVersion: str
    kmsKeyId: str
    multiAz: typing.Union[bool, aws_cdk.cdk.Token]
    preferredMaintenanceWindow: str
    publiclyAccessible: typing.Union[bool, aws_cdk.cdk.Token]
    replicationInstanceIdentifier: str
    replicationSubnetGroupIdentifier: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    vpcSecurityGroupIds: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnReplicationInstanceProps")
class CfnReplicationInstanceProps(_CfnReplicationInstanceProps):
    replicationInstanceClass: str

class CfnReplicationSubnetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dms.CfnReplicationSubnetGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, replication_subnet_group_description: str, subnet_ids: typing.List[str], replication_subnet_group_identifier: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnReplicationSubnetGroupProps = {"replicationSubnetGroupDescription": replication_subnet_group_description, "subnetIds": subnet_ids}

        if replication_subnet_group_identifier is not None:
            props["replicationSubnetGroupIdentifier"] = replication_subnet_group_identifier

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnReplicationSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnReplicationSubnetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="replicationSubnetGroupName")
    def replication_subnet_group_name(self) -> str:
        return jsii.get(self, "replicationSubnetGroupName")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnReplicationSubnetGroupProps(jsii.compat.TypedDict, total=False):
    replicationSubnetGroupIdentifier: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnReplicationSubnetGroupProps")
class CfnReplicationSubnetGroupProps(_CfnReplicationSubnetGroupProps):
    replicationSubnetGroupDescription: str
    subnetIds: typing.List[str]

class CfnReplicationTask(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dms.CfnReplicationTask"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, migration_type: str, replication_instance_arn: str, source_endpoint_arn: str, table_mappings: str, target_endpoint_arn: str, cdc_start_time: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, replication_task_identifier: typing.Optional[str]=None, replication_task_settings: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnReplicationTaskProps = {"migrationType": migration_type, "replicationInstanceArn": replication_instance_arn, "sourceEndpointArn": source_endpoint_arn, "tableMappings": table_mappings, "targetEndpointArn": target_endpoint_arn}

        if cdc_start_time is not None:
            props["cdcStartTime"] = cdc_start_time

        if replication_task_identifier is not None:
            props["replicationTaskIdentifier"] = replication_task_identifier

        if replication_task_settings is not None:
            props["replicationTaskSettings"] = replication_task_settings

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnReplicationTask, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnReplicationTaskProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="replicationTaskArn")
    def replication_task_arn(self) -> str:
        return jsii.get(self, "replicationTaskArn")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class _CfnReplicationTaskProps(jsii.compat.TypedDict, total=False):
    cdcStartTime: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    replicationTaskIdentifier: str
    replicationTaskSettings: str
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-dms.CfnReplicationTaskProps")
class CfnReplicationTaskProps(_CfnReplicationTaskProps):
    migrationType: str
    replicationInstanceArn: str
    sourceEndpointArn: str
    tableMappings: str
    targetEndpointArn: str

__all__ = ["CfnCertificate", "CfnCertificateProps", "CfnEndpoint", "CfnEndpointProps", "CfnEventSubscription", "CfnEventSubscriptionProps", "CfnReplicationInstance", "CfnReplicationInstanceProps", "CfnReplicationSubnetGroup", "CfnReplicationSubnetGroupProps", "CfnReplicationTask", "CfnReplicationTaskProps", "__jsii_assembly__"]

publication.publish()
