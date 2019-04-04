import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-dynamodb", "0.28.0", __name__, "aws-dynamodb@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.Attribute")
class Attribute(jsii.compat.TypedDict):
    name: str
    type: "AttributeType"

@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.AttributeType")
class AttributeType(enum.Enum):
    Binary = "Binary"
    Number = "Number"
    String = "String"

@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.BillingMode")
class BillingMode(enum.Enum):
    PayPerRequest = "PayPerRequest"
    Provisioned = "Provisioned"

class CfnTable(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dynamodb.CfnTable"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, key_schema: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["KeySchemaProperty", aws_cdk.cdk.Token]]], attribute_definitions: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "AttributeDefinitionProperty"]]]]=None, billing_mode: typing.Optional[str]=None, global_secondary_indexes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "GlobalSecondaryIndexProperty"]]]]=None, local_secondary_indexes: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "LocalSecondaryIndexProperty"]]]]=None, point_in_time_recovery_specification: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PointInTimeRecoverySpecificationProperty"]]=None, provisioned_throughput: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ProvisionedThroughputProperty"]]=None, sse_specification: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SSESpecificationProperty"]]=None, stream_specification: typing.Optional[typing.Union[aws_cdk.cdk.Token, "StreamSpecificationProperty"]]=None, table_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, time_to_live_specification: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TimeToLiveSpecificationProperty"]]=None) -> None:
        props: CfnTableProps = {"keySchema": key_schema}

        if attribute_definitions is not None:
            props["attributeDefinitions"] = attribute_definitions

        if billing_mode is not None:
            props["billingMode"] = billing_mode

        if global_secondary_indexes is not None:
            props["globalSecondaryIndexes"] = global_secondary_indexes

        if local_secondary_indexes is not None:
            props["localSecondaryIndexes"] = local_secondary_indexes

        if point_in_time_recovery_specification is not None:
            props["pointInTimeRecoverySpecification"] = point_in_time_recovery_specification

        if provisioned_throughput is not None:
            props["provisionedThroughput"] = provisioned_throughput

        if sse_specification is not None:
            props["sseSpecification"] = sse_specification

        if stream_specification is not None:
            props["streamSpecification"] = stream_specification

        if table_name is not None:
            props["tableName"] = table_name

        if tags is not None:
            props["tags"] = tags

        if time_to_live_specification is not None:
            props["timeToLiveSpecification"] = time_to_live_specification

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
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        return jsii.get(self, "tableArn")

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        return jsii.get(self, "tableName")

    @property
    @jsii.member(jsii_name="tableStreamArn")
    def table_stream_arn(self) -> str:
        return jsii.get(self, "tableStreamArn")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.AttributeDefinitionProperty")
    class AttributeDefinitionProperty(jsii.compat.TypedDict):
        attributeName: str
        attributeType: str

    class _GlobalSecondaryIndexProperty(jsii.compat.TypedDict, total=False):
        provisionedThroughput: typing.Union[aws_cdk.cdk.Token, "CfnTable.ProvisionedThroughputProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.GlobalSecondaryIndexProperty")
    class GlobalSecondaryIndexProperty(_GlobalSecondaryIndexProperty):
        indexName: str
        keySchema: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnTable.KeySchemaProperty", aws_cdk.cdk.Token]]]
        projection: typing.Union[aws_cdk.cdk.Token, "CfnTable.ProjectionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.KeySchemaProperty")
    class KeySchemaProperty(jsii.compat.TypedDict):
        attributeName: str
        keyType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.LocalSecondaryIndexProperty")
    class LocalSecondaryIndexProperty(jsii.compat.TypedDict):
        indexName: str
        keySchema: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnTable.KeySchemaProperty", aws_cdk.cdk.Token]]]
        projection: typing.Union[aws_cdk.cdk.Token, "CfnTable.ProjectionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.PointInTimeRecoverySpecificationProperty")
    class PointInTimeRecoverySpecificationProperty(jsii.compat.TypedDict, total=False):
        pointInTimeRecoveryEnabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.ProjectionProperty")
    class ProjectionProperty(jsii.compat.TypedDict, total=False):
        nonKeyAttributes: typing.List[str]
        projectionType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.ProvisionedThroughputProperty")
    class ProvisionedThroughputProperty(jsii.compat.TypedDict):
        readCapacityUnits: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        writeCapacityUnits: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.SSESpecificationProperty")
    class SSESpecificationProperty(jsii.compat.TypedDict):
        sseEnabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.StreamSpecificationProperty")
    class StreamSpecificationProperty(jsii.compat.TypedDict):
        streamViewType: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTable.TimeToLiveSpecificationProperty")
    class TimeToLiveSpecificationProperty(jsii.compat.TypedDict):
        attributeName: str
        enabled: typing.Union[bool, aws_cdk.cdk.Token]


class _CfnTableProps(jsii.compat.TypedDict, total=False):
    attributeDefinitions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTable.AttributeDefinitionProperty"]]]
    billingMode: str
    globalSecondaryIndexes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTable.GlobalSecondaryIndexProperty"]]]
    localSecondaryIndexes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTable.LocalSecondaryIndexProperty"]]]
    pointInTimeRecoverySpecification: typing.Union[aws_cdk.cdk.Token, "CfnTable.PointInTimeRecoverySpecificationProperty"]
    provisionedThroughput: typing.Union[aws_cdk.cdk.Token, "CfnTable.ProvisionedThroughputProperty"]
    sseSpecification: typing.Union[aws_cdk.cdk.Token, "CfnTable.SSESpecificationProperty"]
    streamSpecification: typing.Union[aws_cdk.cdk.Token, "CfnTable.StreamSpecificationProperty"]
    tableName: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    timeToLiveSpecification: typing.Union[aws_cdk.cdk.Token, "CfnTable.TimeToLiveSpecificationProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.CfnTableProps")
class CfnTableProps(_CfnTableProps):
    keySchema: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnTable.KeySchemaProperty", aws_cdk.cdk.Token]]]

@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.EnableScalingProps")
class EnableScalingProps(jsii.compat.TypedDict):
    maxCapacity: jsii.Number
    minCapacity: jsii.Number

@jsii.interface(jsii_type="@aws-cdk/aws-dynamodb.IScalableTableAttribute")
class IScalableTableAttribute(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IScalableTableAttributeProxy

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        ...

    @jsii.member(jsii_name="scaleOnUtilization")
    def scale_on_utilization(self, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        ...


class _IScalableTableAttributeProxy():
    __jsii_type__ = "@aws-cdk/aws-dynamodb.IScalableTableAttribute"
    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        actions: aws_cdk.aws_applicationautoscaling.ScalingSchedule = {"schedule": schedule}

        if end_time is not None:
            actions["endTime"] = end_time

        if max_capacity is not None:
            actions["maxCapacity"] = max_capacity

        if min_capacity is not None:
            actions["minCapacity"] = min_capacity

        if start_time is not None:
            actions["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, actions])

    @jsii.member(jsii_name="scaleOnUtilization")
    def scale_on_utilization(self, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        props: UtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "scaleOnUtilization", [props])


@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.ProjectionType")
class ProjectionType(enum.Enum):
    KeysOnly = "KeysOnly"
    Include = "Include"
    All = "All"

class _SecondaryIndexProps(jsii.compat.TypedDict, total=False):
    nonKeyAttributes: typing.List[str]
    projectionType: "ProjectionType"

@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.SecondaryIndexProps")
class SecondaryIndexProps(_SecondaryIndexProps):
    indexName: str

class _GlobalSecondaryIndexProps(SecondaryIndexProps, jsii.compat.TypedDict, total=False):
    readCapacity: jsii.Number
    sortKey: "Attribute"
    writeCapacity: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.GlobalSecondaryIndexProps")
class GlobalSecondaryIndexProps(_GlobalSecondaryIndexProps):
    partitionKey: "Attribute"

@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.LocalSecondaryIndexProps")
class LocalSecondaryIndexProps(SecondaryIndexProps, jsii.compat.TypedDict):
    sortKey: "Attribute"

@jsii.enum(jsii_type="@aws-cdk/aws-dynamodb.StreamViewType")
class StreamViewType(enum.Enum):
    NewImage = "NewImage"
    OldImage = "OldImage"
    NewAndOldImages = "NewAndOldImages"
    KeysOnly = "KeysOnly"

class Table(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dynamodb.Table"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, partition_key: "Attribute", billing_mode: typing.Optional["BillingMode"]=None, pitr_enabled: typing.Optional[bool]=None, read_capacity: typing.Optional[jsii.Number]=None, sort_key: typing.Optional["Attribute"]=None, sse_enabled: typing.Optional[bool]=None, stream_specification: typing.Optional["StreamViewType"]=None, table_name: typing.Optional[str]=None, ttl_attribute_name: typing.Optional[str]=None, write_capacity: typing.Optional[jsii.Number]=None) -> None:
        props: TableProps = {"partitionKey": partition_key}

        if billing_mode is not None:
            props["billingMode"] = billing_mode

        if pitr_enabled is not None:
            props["pitrEnabled"] = pitr_enabled

        if read_capacity is not None:
            props["readCapacity"] = read_capacity

        if sort_key is not None:
            props["sortKey"] = sort_key

        if sse_enabled is not None:
            props["sseEnabled"] = sse_enabled

        if stream_specification is not None:
            props["streamSpecification"] = stream_specification

        if table_name is not None:
            props["tableName"] = table_name

        if ttl_attribute_name is not None:
            props["ttlAttributeName"] = ttl_attribute_name

        if write_capacity is not None:
            props["writeCapacity"] = write_capacity

        jsii.create(Table, self, [scope, id, props])

    @jsii.member(jsii_name="grantListStreams")
    @classmethod
    def grant_list_streams(cls, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.sinvoke(cls, "grantListStreams", [grantee])

    @jsii.member(jsii_name="addGlobalSecondaryIndex")
    def add_global_secondary_index(self, *, partition_key: "Attribute", read_capacity: typing.Optional[jsii.Number]=None, sort_key: typing.Optional["Attribute"]=None, write_capacity: typing.Optional[jsii.Number]=None, index_name: str, non_key_attributes: typing.Optional[typing.List[str]]=None, projection_type: typing.Optional["ProjectionType"]=None) -> None:
        props: GlobalSecondaryIndexProps = {"partitionKey": partition_key, "indexName": index_name}

        if read_capacity is not None:
            props["readCapacity"] = read_capacity

        if sort_key is not None:
            props["sortKey"] = sort_key

        if write_capacity is not None:
            props["writeCapacity"] = write_capacity

        if non_key_attributes is not None:
            props["nonKeyAttributes"] = non_key_attributes

        if projection_type is not None:
            props["projectionType"] = projection_type

        return jsii.invoke(self, "addGlobalSecondaryIndex", [props])

    @jsii.member(jsii_name="addLocalSecondaryIndex")
    def add_local_secondary_index(self, *, sort_key: "Attribute", index_name: str, non_key_attributes: typing.Optional[typing.List[str]]=None, projection_type: typing.Optional["ProjectionType"]=None) -> None:
        props: LocalSecondaryIndexProps = {"sortKey": sort_key, "indexName": index_name}

        if non_key_attributes is not None:
            props["nonKeyAttributes"] = non_key_attributes

        if projection_type is not None:
            props["projectionType"] = projection_type

        return jsii.invoke(self, "addLocalSecondaryIndex", [props])

    @jsii.member(jsii_name="autoScaleGlobalSecondaryIndexReadCapacity")
    def auto_scale_global_secondary_index_read_capacity(self, index_name: str, *, max_capacity: jsii.Number, min_capacity: jsii.Number) -> "IScalableTableAttribute":
        props: EnableScalingProps = {"maxCapacity": max_capacity, "minCapacity": min_capacity}

        return jsii.invoke(self, "autoScaleGlobalSecondaryIndexReadCapacity", [index_name, props])

    @jsii.member(jsii_name="autoScaleGlobalSecondaryIndexWriteCapacity")
    def auto_scale_global_secondary_index_write_capacity(self, index_name: str, *, max_capacity: jsii.Number, min_capacity: jsii.Number) -> "IScalableTableAttribute":
        props: EnableScalingProps = {"maxCapacity": max_capacity, "minCapacity": min_capacity}

        return jsii.invoke(self, "autoScaleGlobalSecondaryIndexWriteCapacity", [index_name, props])

    @jsii.member(jsii_name="autoScaleReadCapacity")
    def auto_scale_read_capacity(self, *, max_capacity: jsii.Number, min_capacity: jsii.Number) -> "IScalableTableAttribute":
        props: EnableScalingProps = {"maxCapacity": max_capacity, "minCapacity": min_capacity}

        return jsii.invoke(self, "autoScaleReadCapacity", [props])

    @jsii.member(jsii_name="autoScaleWriteCapacity")
    def auto_scale_write_capacity(self, *, max_capacity: jsii.Number, min_capacity: jsii.Number) -> "IScalableTableAttribute":
        props: EnableScalingProps = {"maxCapacity": max_capacity, "minCapacity": min_capacity}

        return jsii.invoke(self, "autoScaleWriteCapacity", [props])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantFullAccess")
    def grant_full_access(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantFullAccess", [grantee])

    @jsii.member(jsii_name="grantReadData")
    def grant_read_data(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantReadData", [grantee])

    @jsii.member(jsii_name="grantReadWriteData")
    def grant_read_write_data(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantReadWriteData", [grantee])

    @jsii.member(jsii_name="grantStream")
    def grant_stream(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantStream", [grantee, actions])

    @jsii.member(jsii_name="grantStreamRead")
    def grant_stream_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantStreamRead", [grantee])

    @jsii.member(jsii_name="grantWriteData")
    def grant_write_data(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWriteData", [grantee])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        return jsii.get(self, "tableArn")

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        return jsii.get(self, "tableName")

    @property
    @jsii.member(jsii_name="tableStreamArn")
    def table_stream_arn(self) -> str:
        return jsii.get(self, "tableStreamArn")


class _TableProps(jsii.compat.TypedDict, total=False):
    billingMode: "BillingMode"
    pitrEnabled: bool
    readCapacity: jsii.Number
    sortKey: "Attribute"
    sseEnabled: bool
    streamSpecification: "StreamViewType"
    tableName: str
    ttlAttributeName: str
    writeCapacity: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.TableProps")
class TableProps(_TableProps):
    partitionKey: "Attribute"

@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb.UtilizationScalingProps")
class UtilizationScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    targetUtilizationPercent: jsii.Number

__all__ = ["Attribute", "AttributeType", "BillingMode", "CfnTable", "CfnTableProps", "EnableScalingProps", "GlobalSecondaryIndexProps", "IScalableTableAttribute", "LocalSecondaryIndexProps", "ProjectionType", "SecondaryIndexProps", "StreamViewType", "Table", "TableProps", "UtilizationScalingProps", "__jsii_assembly__"]

publication.publish()
