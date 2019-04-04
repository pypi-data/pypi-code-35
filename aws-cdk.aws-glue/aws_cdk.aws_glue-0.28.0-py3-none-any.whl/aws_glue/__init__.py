import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-glue", "0.28.0", __name__, "aws-glue@0.28.0.jsii.tgz")
class CfnClassifier(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnClassifier"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, grok_classifier: typing.Optional[typing.Union["GrokClassifierProperty", aws_cdk.cdk.Token]]=None, json_classifier: typing.Optional[typing.Union[aws_cdk.cdk.Token, "JsonClassifierProperty"]]=None, xml_classifier: typing.Optional[typing.Union[aws_cdk.cdk.Token, "XMLClassifierProperty"]]=None) -> None:
        props: CfnClassifierProps = {}

        if grok_classifier is not None:
            props["grokClassifier"] = grok_classifier

        if json_classifier is not None:
            props["jsonClassifier"] = json_classifier

        if xml_classifier is not None:
            props["xmlClassifier"] = xml_classifier

        jsii.create(CfnClassifier, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="classifierName")
    def classifier_name(self) -> str:
        return jsii.get(self, "classifierName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClassifierProps":
        return jsii.get(self, "propertyOverrides")

    class _GrokClassifierProperty(jsii.compat.TypedDict, total=False):
        customPatterns: str
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifier.GrokClassifierProperty")
    class GrokClassifierProperty(_GrokClassifierProperty):
        classification: str
        grokPattern: str

    class _JsonClassifierProperty(jsii.compat.TypedDict, total=False):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifier.JsonClassifierProperty")
    class JsonClassifierProperty(_JsonClassifierProperty):
        jsonPath: str

    class _XMLClassifierProperty(jsii.compat.TypedDict, total=False):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifier.XMLClassifierProperty")
    class XMLClassifierProperty(_XMLClassifierProperty):
        classification: str
        rowTag: str


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifierProps")
class CfnClassifierProps(jsii.compat.TypedDict, total=False):
    grokClassifier: typing.Union["CfnClassifier.GrokClassifierProperty", aws_cdk.cdk.Token]
    jsonClassifier: typing.Union[aws_cdk.cdk.Token, "CfnClassifier.JsonClassifierProperty"]
    xmlClassifier: typing.Union[aws_cdk.cdk.Token, "CfnClassifier.XMLClassifierProperty"]

class CfnConnection(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnConnection"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, catalog_id: str, connection_input: typing.Union[aws_cdk.cdk.Token, "ConnectionInputProperty"]) -> None:
        props: CfnConnectionProps = {"catalogId": catalog_id, "connectionInput": connection_input}

        jsii.create(CfnConnection, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> str:
        return jsii.get(self, "connectionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConnectionProps":
        return jsii.get(self, "propertyOverrides")

    class _ConnectionInputProperty(jsii.compat.TypedDict, total=False):
        description: str
        matchCriteria: typing.List[str]
        name: str
        physicalConnectionRequirements: typing.Union[aws_cdk.cdk.Token, "CfnConnection.PhysicalConnectionRequirementsProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnConnection.ConnectionInputProperty")
    class ConnectionInputProperty(_ConnectionInputProperty):
        connectionProperties: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        connectionType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnConnection.PhysicalConnectionRequirementsProperty")
    class PhysicalConnectionRequirementsProperty(jsii.compat.TypedDict, total=False):
        availabilityZone: str
        securityGroupIdList: typing.List[str]
        subnetId: str


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnConnectionProps")
class CfnConnectionProps(jsii.compat.TypedDict):
    catalogId: str
    connectionInput: typing.Union[aws_cdk.cdk.Token, "CfnConnection.ConnectionInputProperty"]

class CfnCrawler(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnCrawler"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, database_name: str, role: str, targets: typing.Union[aws_cdk.cdk.Token, "TargetsProperty"], classifiers: typing.Optional[typing.List[str]]=None, configuration: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, schedule: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ScheduleProperty"]]=None, schema_change_policy: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SchemaChangePolicyProperty"]]=None, table_prefix: typing.Optional[str]=None) -> None:
        props: CfnCrawlerProps = {"databaseName": database_name, "role": role, "targets": targets}

        if classifiers is not None:
            props["classifiers"] = classifiers

        if configuration is not None:
            props["configuration"] = configuration

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        if schedule is not None:
            props["schedule"] = schedule

        if schema_change_policy is not None:
            props["schemaChangePolicy"] = schema_change_policy

        if table_prefix is not None:
            props["tablePrefix"] = table_prefix

        jsii.create(CfnCrawler, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="crawlerName")
    def crawler_name(self) -> str:
        return jsii.get(self, "crawlerName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCrawlerProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.JdbcTargetProperty")
    class JdbcTargetProperty(jsii.compat.TypedDict, total=False):
        connectionName: str
        exclusions: typing.List[str]
        path: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.S3TargetProperty")
    class S3TargetProperty(jsii.compat.TypedDict, total=False):
        exclusions: typing.List[str]
        path: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.ScheduleProperty")
    class ScheduleProperty(jsii.compat.TypedDict, total=False):
        scheduleExpression: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.SchemaChangePolicyProperty")
    class SchemaChangePolicyProperty(jsii.compat.TypedDict, total=False):
        deleteBehavior: str
        updateBehavior: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.TargetsProperty")
    class TargetsProperty(jsii.compat.TypedDict, total=False):
        jdbcTargets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCrawler.JdbcTargetProperty"]]]
        s3Targets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCrawler.S3TargetProperty"]]]


class _CfnCrawlerProps(jsii.compat.TypedDict, total=False):
    classifiers: typing.List[str]
    configuration: str
    description: str
    name: str
    schedule: typing.Union[aws_cdk.cdk.Token, "CfnCrawler.ScheduleProperty"]
    schemaChangePolicy: typing.Union[aws_cdk.cdk.Token, "CfnCrawler.SchemaChangePolicyProperty"]
    tablePrefix: str

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawlerProps")
class CfnCrawlerProps(_CfnCrawlerProps):
    databaseName: str
    role: str
    targets: typing.Union[aws_cdk.cdk.Token, "CfnCrawler.TargetsProperty"]

class CfnDatabase(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnDatabase"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, catalog_id: str, database_input: typing.Union[aws_cdk.cdk.Token, "DatabaseInputProperty"]) -> None:
        props: CfnDatabaseProps = {"catalogId": catalog_id, "databaseInput": database_input}

        jsii.create(CfnDatabase, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        return jsii.get(self, "databaseName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDatabaseProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDatabase.DatabaseInputProperty")
    class DatabaseInputProperty(jsii.compat.TypedDict, total=False):
        description: str
        locationUri: str
        name: str
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDatabaseProps")
class CfnDatabaseProps(jsii.compat.TypedDict):
    catalogId: str
    databaseInput: typing.Union[aws_cdk.cdk.Token, "CfnDatabase.DatabaseInputProperty"]

class CfnDevEndpoint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnDevEndpoint"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, public_key: str, role_arn: str, endpoint_name: typing.Optional[str]=None, extra_jars_s3_path: typing.Optional[str]=None, extra_python_libs_s3_path: typing.Optional[str]=None, number_of_nodes: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_id: typing.Optional[str]=None) -> None:
        props: CfnDevEndpointProps = {"publicKey": public_key, "roleArn": role_arn}

        if endpoint_name is not None:
            props["endpointName"] = endpoint_name

        if extra_jars_s3_path is not None:
            props["extraJarsS3Path"] = extra_jars_s3_path

        if extra_python_libs_s3_path is not None:
            props["extraPythonLibsS3Path"] = extra_python_libs_s3_path

        if number_of_nodes is not None:
            props["numberOfNodes"] = number_of_nodes

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if subnet_id is not None:
            props["subnetId"] = subnet_id

        jsii.create(CfnDevEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="devEndpointId")
    def dev_endpoint_id(self) -> str:
        return jsii.get(self, "devEndpointId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDevEndpointProps":
        return jsii.get(self, "propertyOverrides")


class _CfnDevEndpointProps(jsii.compat.TypedDict, total=False):
    endpointName: str
    extraJarsS3Path: str
    extraPythonLibsS3Path: str
    numberOfNodes: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    securityGroupIds: typing.List[str]
    subnetId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDevEndpointProps")
class CfnDevEndpointProps(_CfnDevEndpointProps):
    publicKey: str
    roleArn: str

class CfnJob(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnJob"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, command: typing.Union[aws_cdk.cdk.Token, "JobCommandProperty"], role: str, allocated_capacity: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, connections: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ConnectionsListProperty"]]=None, default_arguments: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, description: typing.Optional[str]=None, execution_property: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ExecutionPropertyProperty"]]=None, log_uri: typing.Optional[str]=None, max_retries: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, name: typing.Optional[str]=None) -> None:
        props: CfnJobProps = {"command": command, "role": role}

        if allocated_capacity is not None:
            props["allocatedCapacity"] = allocated_capacity

        if connections is not None:
            props["connections"] = connections

        if default_arguments is not None:
            props["defaultArguments"] = default_arguments

        if description is not None:
            props["description"] = description

        if execution_property is not None:
            props["executionProperty"] = execution_property

        if log_uri is not None:
            props["logUri"] = log_uri

        if max_retries is not None:
            props["maxRetries"] = max_retries

        if name is not None:
            props["name"] = name

        jsii.create(CfnJob, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> str:
        return jsii.get(self, "jobName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnJobProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJob.ConnectionsListProperty")
    class ConnectionsListProperty(jsii.compat.TypedDict, total=False):
        connections: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJob.ExecutionPropertyProperty")
    class ExecutionPropertyProperty(jsii.compat.TypedDict, total=False):
        maxConcurrentRuns: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJob.JobCommandProperty")
    class JobCommandProperty(jsii.compat.TypedDict, total=False):
        name: str
        scriptLocation: str


class _CfnJobProps(jsii.compat.TypedDict, total=False):
    allocatedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    connections: typing.Union[aws_cdk.cdk.Token, "CfnJob.ConnectionsListProperty"]
    defaultArguments: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    description: str
    executionProperty: typing.Union[aws_cdk.cdk.Token, "CfnJob.ExecutionPropertyProperty"]
    logUri: str
    maxRetries: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJobProps")
class CfnJobProps(_CfnJobProps):
    command: typing.Union[aws_cdk.cdk.Token, "CfnJob.JobCommandProperty"]
    role: str

class CfnPartition(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnPartition"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, catalog_id: str, database_name: str, partition_input: typing.Union[aws_cdk.cdk.Token, "PartitionInputProperty"], table_name: str) -> None:
        props: CfnPartitionProps = {"catalogId": catalog_id, "databaseName": database_name, "partitionInput": partition_input, "tableName": table_name}

        jsii.create(CfnPartition, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="partitionId")
    def partition_id(self) -> str:
        return jsii.get(self, "partitionId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPartitionProps":
        return jsii.get(self, "propertyOverrides")

    class _ColumnProperty(jsii.compat.TypedDict, total=False):
        comment: str
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.ColumnProperty")
    class ColumnProperty(_ColumnProperty):
        name: str

    class _OrderProperty(jsii.compat.TypedDict, total=False):
        sortOrder: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.OrderProperty")
    class OrderProperty(_OrderProperty):
        column: str

    class _PartitionInputProperty(jsii.compat.TypedDict, total=False):
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        storageDescriptor: typing.Union[aws_cdk.cdk.Token, "CfnPartition.StorageDescriptorProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.PartitionInputProperty")
    class PartitionInputProperty(_PartitionInputProperty):
        values: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.SerdeInfoProperty")
    class SerdeInfoProperty(jsii.compat.TypedDict, total=False):
        name: str
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        serializationLibrary: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.SkewedInfoProperty")
    class SkewedInfoProperty(jsii.compat.TypedDict, total=False):
        skewedColumnNames: typing.List[str]
        skewedColumnValueLocationMaps: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        skewedColumnValues: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.StorageDescriptorProperty")
    class StorageDescriptorProperty(jsii.compat.TypedDict, total=False):
        bucketColumns: typing.List[str]
        columns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPartition.ColumnProperty"]]]
        compressed: typing.Union[bool, aws_cdk.cdk.Token]
        inputFormat: str
        location: str
        numberOfBuckets: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        outputFormat: str
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        serdeInfo: typing.Union[aws_cdk.cdk.Token, "CfnPartition.SerdeInfoProperty"]
        skewedInfo: typing.Union[aws_cdk.cdk.Token, "CfnPartition.SkewedInfoProperty"]
        sortColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPartition.OrderProperty"]]]
        storedAsSubDirectories: typing.Union[bool, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartitionProps")
class CfnPartitionProps(jsii.compat.TypedDict):
    catalogId: str
    databaseName: str
    partitionInput: typing.Union[aws_cdk.cdk.Token, "CfnPartition.PartitionInputProperty"]
    tableName: str

class CfnTable(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnTable"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, catalog_id: str, database_name: str, table_input: typing.Union[aws_cdk.cdk.Token, "TableInputProperty"]) -> None:
        props: CfnTableProps = {"catalogId": catalog_id, "databaseName": database_name, "tableInput": table_input}

        jsii.create(CfnTable, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTableProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        return jsii.get(self, "tableName")

    class _ColumnProperty(jsii.compat.TypedDict, total=False):
        comment: str
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.ColumnProperty")
    class ColumnProperty(_ColumnProperty):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.OrderProperty")
    class OrderProperty(jsii.compat.TypedDict):
        column: str
        sortOrder: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.SerdeInfoProperty")
    class SerdeInfoProperty(jsii.compat.TypedDict, total=False):
        name: str
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        serializationLibrary: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.SkewedInfoProperty")
    class SkewedInfoProperty(jsii.compat.TypedDict, total=False):
        skewedColumnNames: typing.List[str]
        skewedColumnValueLocationMaps: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        skewedColumnValues: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.StorageDescriptorProperty")
    class StorageDescriptorProperty(jsii.compat.TypedDict, total=False):
        bucketColumns: typing.List[str]
        columns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTable.ColumnProperty"]]]
        compressed: typing.Union[bool, aws_cdk.cdk.Token]
        inputFormat: str
        location: str
        numberOfBuckets: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        outputFormat: str
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        serdeInfo: typing.Union[aws_cdk.cdk.Token, "CfnTable.SerdeInfoProperty"]
        skewedInfo: typing.Union[aws_cdk.cdk.Token, "CfnTable.SkewedInfoProperty"]
        sortColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTable.OrderProperty"]]]
        storedAsSubDirectories: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.TableInputProperty")
    class TableInputProperty(jsii.compat.TypedDict, total=False):
        description: str
        name: str
        owner: str
        parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        partitionKeys: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTable.ColumnProperty"]]]
        retention: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        storageDescriptor: typing.Union[aws_cdk.cdk.Token, "CfnTable.StorageDescriptorProperty"]
        tableType: str
        viewExpandedText: str
        viewOriginalText: str


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTableProps")
class CfnTableProps(jsii.compat.TypedDict):
    catalogId: str
    databaseName: str
    tableInput: typing.Union[aws_cdk.cdk.Token, "CfnTable.TableInputProperty"]

class CfnTrigger(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnTrigger"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ActionProperty"]]], type: str, description: typing.Optional[str]=None, name: typing.Optional[str]=None, predicate: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PredicateProperty"]]=None, schedule: typing.Optional[str]=None) -> None:
        props: CfnTriggerProps = {"actions": actions, "type": type}

        if description is not None:
            props["description"] = description

        if name is not None:
            props["name"] = name

        if predicate is not None:
            props["predicate"] = predicate

        if schedule is not None:
            props["schedule"] = schedule

        jsii.create(CfnTrigger, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTriggerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="triggerName")
    def trigger_name(self) -> str:
        return jsii.get(self, "triggerName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTrigger.ActionProperty")
    class ActionProperty(jsii.compat.TypedDict, total=False):
        arguments: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        jobName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTrigger.ConditionProperty")
    class ConditionProperty(jsii.compat.TypedDict, total=False):
        jobName: str
        logicalOperator: str
        state: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTrigger.PredicateProperty")
    class PredicateProperty(jsii.compat.TypedDict, total=False):
        conditions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTrigger.ConditionProperty"]]]
        logical: str


class _CfnTriggerProps(jsii.compat.TypedDict, total=False):
    description: str
    name: str
    predicate: typing.Union[aws_cdk.cdk.Token, "CfnTrigger.PredicateProperty"]
    schedule: str

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTriggerProps")
class CfnTriggerProps(_CfnTriggerProps):
    actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTrigger.ActionProperty"]]]
    type: str

class _Column(jsii.compat.TypedDict, total=False):
    comment: str

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.Column")
class Column(_Column):
    name: str
    type: "Type"

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.DataFormat")
class DataFormat(jsii.compat.TypedDict):
    inputFormat: "InputFormat"
    outputFormat: "OutputFormat"
    serializationLibrary: "SerializationLibrary"

class Database(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.Database"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, database_name: str, location_uri: typing.Optional[str]=None) -> None:
        props: DatabaseProps = {"databaseName": database_name}

        if location_uri is not None:
            props["locationUri"] = location_uri

        jsii.create(Database, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, catalog_arn: str, catalog_id: str, database_arn: str, database_name: str, location_uri: str) -> "IDatabase":
        props: DatabaseImportProps = {"catalogArn": catalog_arn, "catalogId": catalog_id, "databaseArn": database_arn, "databaseName": database_name, "locationUri": location_uri}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "DatabaseImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> str:
        return jsii.get(self, "catalogArn")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        return jsii.get(self, "catalogId")

    @property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> str:
        return jsii.get(self, "databaseArn")

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        return jsii.get(self, "databaseName")

    @property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> str:
        return jsii.get(self, "locationUri")


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.DatabaseImportProps")
class DatabaseImportProps(jsii.compat.TypedDict):
    catalogArn: str
    catalogId: str
    databaseArn: str
    databaseName: str
    locationUri: str

class _DatabaseProps(jsii.compat.TypedDict, total=False):
    locationUri: str

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.DatabaseProps")
class DatabaseProps(_DatabaseProps):
    databaseName: str

@jsii.interface(jsii_type="@aws-cdk/aws-glue.IDatabase")
class IDatabase(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseProxy

    @property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "DatabaseImportProps":
        ...


class _IDatabaseProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-glue.IDatabase"
    @property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> str:
        return jsii.get(self, "catalogArn")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        return jsii.get(self, "catalogId")

    @property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> str:
        return jsii.get(self, "databaseArn")

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        return jsii.get(self, "databaseName")

    @property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> str:
        return jsii.get(self, "locationUri")

    @jsii.member(jsii_name="export")
    def export(self) -> "DatabaseImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-glue.ITable")
class ITable(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ITableProxy

    @property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "TableImportProps":
        ...


class _ITableProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-glue.ITable"
    @property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        return jsii.get(self, "tableArn")

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        return jsii.get(self, "tableName")

    @jsii.member(jsii_name="export")
    def export(self) -> "TableImportProps":
        return jsii.invoke(self, "export", [])


class InputFormat(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.InputFormat"):
    def __init__(self, class_name: str) -> None:
        jsii.create(InputFormat, self, [class_name])

    @classproperty
    @jsii.member(jsii_name="TextInputFormat")
    def TEXT_INPUT_FORMAT(cls) -> "InputFormat":
        return jsii.sget(cls, "TextInputFormat")

    @property
    @jsii.member(jsii_name="className")
    def class_name(self) -> str:
        return jsii.get(self, "className")


class OutputFormat(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.OutputFormat"):
    def __init__(self, class_name: str) -> None:
        jsii.create(OutputFormat, self, [class_name])

    @classproperty
    @jsii.member(jsii_name="HiveIgnoreKeyTextOutputFormat")
    def HIVE_IGNORE_KEY_TEXT_OUTPUT_FORMAT(cls) -> "OutputFormat":
        return jsii.sget(cls, "HiveIgnoreKeyTextOutputFormat")

    @property
    @jsii.member(jsii_name="className")
    def class_name(self) -> str:
        return jsii.get(self, "className")


class Schema(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.Schema"):
    def __init__(self) -> None:
        jsii.create(Schema, self, [])

    @jsii.member(jsii_name="array")
    @classmethod
    def array(cls, *, input_string: str, is_primitive: bool) -> "Type":
        item_type: Type = {"inputString": input_string, "isPrimitive": is_primitive}

        return jsii.sinvoke(cls, "array", [item_type])

    @jsii.member(jsii_name="char")
    @classmethod
    def char(cls, length: jsii.Number) -> "Type":
        return jsii.sinvoke(cls, "char", [length])

    @jsii.member(jsii_name="decimal")
    @classmethod
    def decimal(cls, precision: jsii.Number, scale: typing.Optional[jsii.Number]=None) -> "Type":
        return jsii.sinvoke(cls, "decimal", [precision, scale])

    @jsii.member(jsii_name="map")
    @classmethod
    def map(cls, key_type: "Type", *, input_string: str, is_primitive: bool) -> "Type":
        value_type: Type = {"inputString": input_string, "isPrimitive": is_primitive}

        return jsii.sinvoke(cls, "map", [key_type, value_type])

    @jsii.member(jsii_name="struct")
    @classmethod
    def struct(cls, columns: typing.List["Column"]) -> "Type":
        return jsii.sinvoke(cls, "struct", [columns])

    @jsii.member(jsii_name="varchar")
    @classmethod
    def varchar(cls, length: jsii.Number) -> "Type":
        return jsii.sinvoke(cls, "varchar", [length])

    @classproperty
    @jsii.member(jsii_name="bigint")
    def BIGINT(cls) -> "Type":
        return jsii.sget(cls, "bigint")

    @classproperty
    @jsii.member(jsii_name="binary")
    def BINARY(cls) -> "Type":
        return jsii.sget(cls, "binary")

    @classproperty
    @jsii.member(jsii_name="boolean")
    def BOOLEAN(cls) -> "Type":
        return jsii.sget(cls, "boolean")

    @classproperty
    @jsii.member(jsii_name="date")
    def DATE(cls) -> "Type":
        return jsii.sget(cls, "date")

    @classproperty
    @jsii.member(jsii_name="double")
    def DOUBLE(cls) -> "Type":
        return jsii.sget(cls, "double")

    @classproperty
    @jsii.member(jsii_name="float")
    def FLOAT(cls) -> "Type":
        return jsii.sget(cls, "float")

    @classproperty
    @jsii.member(jsii_name="integer")
    def INTEGER(cls) -> "Type":
        return jsii.sget(cls, "integer")

    @classproperty
    @jsii.member(jsii_name="smallint")
    def SMALLINT(cls) -> "Type":
        return jsii.sget(cls, "smallint")

    @classproperty
    @jsii.member(jsii_name="string")
    def STRING(cls) -> "Type":
        return jsii.sget(cls, "string")

    @classproperty
    @jsii.member(jsii_name="timestamp")
    def TIMESTAMP(cls) -> "Type":
        return jsii.sget(cls, "timestamp")

    @classproperty
    @jsii.member(jsii_name="tinyint")
    def TINYINT(cls) -> "Type":
        return jsii.sget(cls, "tinyint")


class SerializationLibrary(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.SerializationLibrary"):
    def __init__(self, class_name: str) -> None:
        jsii.create(SerializationLibrary, self, [class_name])

    @classproperty
    @jsii.member(jsii_name="HiveJson")
    def HIVE_JSON(cls) -> "SerializationLibrary":
        return jsii.sget(cls, "HiveJson")

    @classproperty
    @jsii.member(jsii_name="OpenXJson")
    def OPEN_X_JSON(cls) -> "SerializationLibrary":
        return jsii.sget(cls, "OpenXJson")

    @property
    @jsii.member(jsii_name="className")
    def class_name(self) -> str:
        return jsii.get(self, "className")


@jsii.implements(ITable)
class Table(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.Table"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, columns: typing.List["Column"], database: "IDatabase", data_format: "DataFormat", table_name: str, bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, compressed: typing.Optional[bool]=None, description: typing.Optional[str]=None, encryption: typing.Optional["TableEncryption"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, partition_keys: typing.Optional[typing.List["Column"]]=None, s3_prefix: typing.Optional[str]=None, stored_as_sub_directories: typing.Optional[bool]=None) -> None:
        props: TableProps = {"columns": columns, "database": database, "dataFormat": data_format, "tableName": table_name}

        if bucket is not None:
            props["bucket"] = bucket

        if compressed is not None:
            props["compressed"] = compressed

        if description is not None:
            props["description"] = description

        if encryption is not None:
            props["encryption"] = encryption

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if partition_keys is not None:
            props["partitionKeys"] = partition_keys

        if s3_prefix is not None:
            props["s3Prefix"] = s3_prefix

        if stored_as_sub_directories is not None:
            props["storedAsSubDirectories"] = stored_as_sub_directories

        jsii.create(Table, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, table_arn: str, table_name: str) -> "ITable":
        props: TableImportProps = {"tableArn": table_arn, "tableName": table_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "TableImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantReadWrite", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [grantee])

    @property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        return jsii.get(self, "bucket")

    @property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List["Column"]:
        return jsii.get(self, "columns")

    @property
    @jsii.member(jsii_name="database")
    def database(self) -> "IDatabase":
        return jsii.get(self, "database")

    @property
    @jsii.member(jsii_name="dataFormat")
    def data_format(self) -> "DataFormat":
        return jsii.get(self, "dataFormat")

    @property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> "TableEncryption":
        return jsii.get(self, "encryption")

    @property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> str:
        return jsii.get(self, "s3Prefix")

    @property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        return jsii.get(self, "tableArn")

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        return jsii.get(self, "tableName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")

    @property
    @jsii.member(jsii_name="partitionKeys")
    def partition_keys(self) -> typing.Optional[typing.List["Column"]]:
        return jsii.get(self, "partitionKeys")


@jsii.enum(jsii_type="@aws-cdk/aws-glue.TableEncryption")
class TableEncryption(enum.Enum):
    Unencrypted = "Unencrypted"
    S3Managed = "S3Managed"
    Kms = "Kms"
    KmsManaged = "KmsManaged"
    ClientSideKms = "ClientSideKms"

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.TableImportProps")
class TableImportProps(jsii.compat.TypedDict):
    tableArn: str
    tableName: str

class _TableProps(jsii.compat.TypedDict, total=False):
    bucket: aws_cdk.aws_s3.IBucket
    compressed: bool
    description: str
    encryption: "TableEncryption"
    encryptionKey: aws_cdk.aws_kms.IEncryptionKey
    partitionKeys: typing.List["Column"]
    s3Prefix: str
    storedAsSubDirectories: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.TableProps")
class TableProps(_TableProps):
    columns: typing.List["Column"]
    database: "IDatabase"
    dataFormat: "DataFormat"
    tableName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.Type")
class Type(jsii.compat.TypedDict):
    inputString: str
    isPrimitive: bool

__all__ = ["CfnClassifier", "CfnClassifierProps", "CfnConnection", "CfnConnectionProps", "CfnCrawler", "CfnCrawlerProps", "CfnDatabase", "CfnDatabaseProps", "CfnDevEndpoint", "CfnDevEndpointProps", "CfnJob", "CfnJobProps", "CfnPartition", "CfnPartitionProps", "CfnTable", "CfnTableProps", "CfnTrigger", "CfnTriggerProps", "Column", "DataFormat", "Database", "DatabaseImportProps", "DatabaseProps", "IDatabase", "ITable", "InputFormat", "OutputFormat", "Schema", "SerializationLibrary", "Table", "TableEncryption", "TableImportProps", "TableProps", "Type", "__jsii_assembly__"]

publication.publish()
