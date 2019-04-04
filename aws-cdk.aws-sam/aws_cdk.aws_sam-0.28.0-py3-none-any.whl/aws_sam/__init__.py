import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sam", "0.28.0", __name__, "aws-sam@0.28.0.jsii.tgz")
class CfnApi(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sam.CfnApi"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, stage_name: str, auth: typing.Optional[typing.Union["AuthProperty", aws_cdk.cdk.Token]]=None, binary_media_types: typing.Optional[typing.List[str]]=None, cache_cluster_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, cache_cluster_size: typing.Optional[str]=None, cors: typing.Optional[str]=None, definition_body: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, definition_uri: typing.Optional[typing.Union[str, aws_cdk.cdk.Token, "S3LocationProperty"]]=None, endpoint_configuration: typing.Optional[str]=None, method_settings: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, name: typing.Optional[str]=None, tracing_enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, variables: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None) -> None:
        props: CfnApiProps = {"stageName": stage_name}

        if auth is not None:
            props["auth"] = auth

        if binary_media_types is not None:
            props["binaryMediaTypes"] = binary_media_types

        if cache_cluster_enabled is not None:
            props["cacheClusterEnabled"] = cache_cluster_enabled

        if cache_cluster_size is not None:
            props["cacheClusterSize"] = cache_cluster_size

        if cors is not None:
            props["cors"] = cors

        if definition_body is not None:
            props["definitionBody"] = definition_body

        if definition_uri is not None:
            props["definitionUri"] = definition_uri

        if endpoint_configuration is not None:
            props["endpointConfiguration"] = endpoint_configuration

        if method_settings is not None:
            props["methodSettings"] = method_settings

        if name is not None:
            props["name"] = name

        if tracing_enabled is not None:
            props["tracingEnabled"] = tracing_enabled

        if variables is not None:
            props["variables"] = variables

        jsii.create(CfnApi, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="requiredTransform")
    def REQUIRED_TRANSFORM(cls) -> str:
        return jsii.sget(cls, "requiredTransform")

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="apiName")
    def api_name(self) -> str:
        return jsii.get(self, "apiName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApiProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnApi.AuthProperty")
    class AuthProperty(jsii.compat.TypedDict, total=False):
        authorizers: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        defaultAuthorizer: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnApi.S3LocationProperty")
    class S3LocationProperty(jsii.compat.TypedDict):
        bucket: str
        key: str
        version: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnApiProps(jsii.compat.TypedDict, total=False):
    auth: typing.Union["CfnApi.AuthProperty", aws_cdk.cdk.Token]
    binaryMediaTypes: typing.List[str]
    cacheClusterEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    cacheClusterSize: str
    cors: str
    definitionBody: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    definitionUri: typing.Union[str, aws_cdk.cdk.Token, "CfnApi.S3LocationProperty"]
    endpointConfiguration: str
    methodSettings: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    name: str
    tracingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    variables: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]

@jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnApiProps")
class CfnApiProps(_CfnApiProps):
    stageName: str

class CfnApplication(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sam.CfnApplication"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, location: typing.Union[str, aws_cdk.cdk.Token, "ApplicationLocationProperty"], notification_arns: typing.Optional[typing.List[str]]=None, parameters: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]]=None, tags: typing.Optional[typing.Mapping[str,str]]=None, timeout_in_minutes: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnApplicationProps = {"location": location}

        if notification_arns is not None:
            props["notificationArns"] = notification_arns

        if parameters is not None:
            props["parameters"] = parameters

        if tags is not None:
            props["tags"] = tags

        if timeout_in_minutes is not None:
            props["timeoutInMinutes"] = timeout_in_minutes

        jsii.create(CfnApplication, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="requiredTransform")
    def REQUIRED_TRANSFORM(cls) -> str:
        return jsii.sget(cls, "requiredTransform")

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnApplication.ApplicationLocationProperty")
    class ApplicationLocationProperty(jsii.compat.TypedDict):
        applicationId: str
        semanticVersion: str


class _CfnApplicationProps(jsii.compat.TypedDict, total=False):
    notificationArns: typing.List[str]
    parameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    tags: typing.Mapping[str,str]
    timeoutInMinutes: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnApplicationProps")
class CfnApplicationProps(_CfnApplicationProps):
    location: typing.Union[str, aws_cdk.cdk.Token, "CfnApplication.ApplicationLocationProperty"]

class CfnFunction(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sam.CfnFunction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, code_uri: typing.Union[str, aws_cdk.cdk.Token, "S3LocationProperty"], handler: str, runtime: str, auto_publish_alias: typing.Optional[str]=None, dead_letter_queue: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DeadLetterQueueProperty"]]=None, deployment_preference: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DeploymentPreferenceProperty"]]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Union[aws_cdk.cdk.Token, "FunctionEnvironmentProperty"]]=None, events: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[aws_cdk.cdk.Token, "EventSourceProperty"]]]]=None, function_name: typing.Optional[str]=None, kms_key_arn: typing.Optional[str]=None, layers: typing.Optional[typing.List[str]]=None, memory_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, permissions_boundary: typing.Optional[str]=None, policies: typing.Optional[typing.Union[str, aws_cdk.cdk.Token, "IAMPolicyDocumentProperty", typing.List[typing.Union[str, aws_cdk.cdk.Token, "IAMPolicyDocumentProperty"]]]]=None, reserved_concurrent_executions: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, role: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str,str]]=None, timeout: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, tracing: typing.Optional[str]=None, vpc_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "VpcConfigProperty"]]=None) -> None:
        props: CfnFunctionProps = {"codeUri": code_uri, "handler": handler, "runtime": runtime}

        if auto_publish_alias is not None:
            props["autoPublishAlias"] = auto_publish_alias

        if dead_letter_queue is not None:
            props["deadLetterQueue"] = dead_letter_queue

        if deployment_preference is not None:
            props["deploymentPreference"] = deployment_preference

        if description is not None:
            props["description"] = description

        if environment is not None:
            props["environment"] = environment

        if events is not None:
            props["events"] = events

        if function_name is not None:
            props["functionName"] = function_name

        if kms_key_arn is not None:
            props["kmsKeyArn"] = kms_key_arn

        if layers is not None:
            props["layers"] = layers

        if memory_size is not None:
            props["memorySize"] = memory_size

        if permissions_boundary is not None:
            props["permissionsBoundary"] = permissions_boundary

        if policies is not None:
            props["policies"] = policies

        if reserved_concurrent_executions is not None:
            props["reservedConcurrentExecutions"] = reserved_concurrent_executions

        if role is not None:
            props["role"] = role

        if tags is not None:
            props["tags"] = tags

        if timeout is not None:
            props["timeout"] = timeout

        if tracing is not None:
            props["tracing"] = tracing

        if vpc_config is not None:
            props["vpcConfig"] = vpc_config

        jsii.create(CfnFunction, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="requiredTransform")
    def REQUIRED_TRANSFORM(cls) -> str:
        return jsii.sget(cls, "requiredTransform")

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        return jsii.get(self, "functionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFunctionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.AlexaSkillEventProperty")
    class AlexaSkillEventProperty(jsii.compat.TypedDict, total=False):
        variables: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]

    class _ApiEventProperty(jsii.compat.TypedDict, total=False):
        restApiId: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.ApiEventProperty")
    class ApiEventProperty(_ApiEventProperty):
        method: str
        path: str

    class _CloudWatchEventEventProperty(jsii.compat.TypedDict, total=False):
        input: str
        inputPath: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.CloudWatchEventEventProperty")
    class CloudWatchEventEventProperty(_CloudWatchEventEventProperty):
        pattern: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.DeadLetterQueueProperty")
    class DeadLetterQueueProperty(jsii.compat.TypedDict):
        targetArn: str
        type: str

    class _DeploymentPreferenceProperty(jsii.compat.TypedDict, total=False):
        alarms: typing.List[str]
        hooks: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.DeploymentPreferenceProperty")
    class DeploymentPreferenceProperty(_DeploymentPreferenceProperty):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        type: str

    class _DynamoDBEventProperty(jsii.compat.TypedDict, total=False):
        batchSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.DynamoDBEventProperty")
    class DynamoDBEventProperty(_DynamoDBEventProperty):
        startingPosition: str
        stream: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.EventSourceProperty")
    class EventSourceProperty(jsii.compat.TypedDict):
        properties: typing.Union[aws_cdk.cdk.Token, "CfnFunction.AlexaSkillEventProperty", "CfnFunction.ApiEventProperty", "CfnFunction.CloudWatchEventEventProperty", "CfnFunction.DynamoDBEventProperty", "CfnFunction.S3EventProperty", "CfnFunction.SNSEventProperty", "CfnFunction.SQSEventProperty", "CfnFunction.KinesisEventProperty", "CfnFunction.ScheduleEventProperty", "CfnFunction.IoTRuleEventProperty"]
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.FunctionEnvironmentProperty")
    class FunctionEnvironmentProperty(jsii.compat.TypedDict):
        variables: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]

    @jsii.interface(jsii_type="@aws-cdk/aws-sam.CfnFunction.IAMPolicyDocumentProperty")
    class IAMPolicyDocumentProperty(jsii.compat.Protocol):
        @staticmethod
        def __jsii_proxy_class__():
            return _IAMPolicyDocumentPropertyProxy

        @property
        @jsii.member(jsii_name="statement")
        def statement(self) -> typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]:
            ...


    class _IAMPolicyDocumentPropertyProxy():
        __jsii_type__ = "@aws-cdk/aws-sam.CfnFunction.IAMPolicyDocumentProperty"
        @property
        @jsii.member(jsii_name="statement")
        def statement(self) -> typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]:
            return jsii.get(self, "statement")


    class _IoTRuleEventProperty(jsii.compat.TypedDict, total=False):
        awsIotSqlVersion: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.IoTRuleEventProperty")
    class IoTRuleEventProperty(_IoTRuleEventProperty):
        sql: str

    class _KinesisEventProperty(jsii.compat.TypedDict, total=False):
        batchSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.KinesisEventProperty")
    class KinesisEventProperty(_KinesisEventProperty):
        startingPosition: str
        stream: str

    class _S3EventProperty(jsii.compat.TypedDict, total=False):
        filter: typing.Union[aws_cdk.cdk.Token, "CfnFunction.S3NotificationFilterProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.S3EventProperty")
    class S3EventProperty(_S3EventProperty):
        bucket: str
        events: typing.Union[str, aws_cdk.cdk.Token, typing.List[str]]

    class _S3LocationProperty(jsii.compat.TypedDict, total=False):
        version: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.S3LocationProperty")
    class S3LocationProperty(_S3LocationProperty):
        bucket: str
        key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.S3NotificationFilterProperty")
    class S3NotificationFilterProperty(jsii.compat.TypedDict):
        s3Key: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.SNSEventProperty")
    class SNSEventProperty(jsii.compat.TypedDict):
        topic: str

    class _SQSEventProperty(jsii.compat.TypedDict, total=False):
        batchSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        enabled: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.SQSEventProperty")
    class SQSEventProperty(_SQSEventProperty):
        queue: str

    class _ScheduleEventProperty(jsii.compat.TypedDict, total=False):
        input: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.ScheduleEventProperty")
    class ScheduleEventProperty(_ScheduleEventProperty):
        schedule: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunction.VpcConfigProperty")
    class VpcConfigProperty(jsii.compat.TypedDict):
        securityGroupIds: typing.List[str]
        subnetIds: typing.List[str]


class _CfnFunctionProps(jsii.compat.TypedDict, total=False):
    autoPublishAlias: str
    deadLetterQueue: typing.Union[aws_cdk.cdk.Token, "CfnFunction.DeadLetterQueueProperty"]
    deploymentPreference: typing.Union[aws_cdk.cdk.Token, "CfnFunction.DeploymentPreferenceProperty"]
    description: str
    environment: typing.Union[aws_cdk.cdk.Token, "CfnFunction.FunctionEnvironmentProperty"]
    events: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,typing.Union[aws_cdk.cdk.Token, "CfnFunction.EventSourceProperty"]]]
    functionName: str
    kmsKeyArn: str
    layers: typing.List[str]
    memorySize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    permissionsBoundary: str
    policies: typing.Union[str, aws_cdk.cdk.Token, "CfnFunction.IAMPolicyDocumentProperty", typing.List[typing.Union[str, aws_cdk.cdk.Token, "CfnFunction.IAMPolicyDocumentProperty"]]]
    reservedConcurrentExecutions: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    role: str
    tags: typing.Mapping[str,str]
    timeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    tracing: str
    vpcConfig: typing.Union[aws_cdk.cdk.Token, "CfnFunction.VpcConfigProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnFunctionProps")
class CfnFunctionProps(_CfnFunctionProps):
    codeUri: typing.Union[str, aws_cdk.cdk.Token, "CfnFunction.S3LocationProperty"]
    handler: str
    runtime: str

class CfnLayerVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sam.CfnLayerVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, compatible_runtimes: typing.Optional[typing.List[str]]=None, content_uri: typing.Optional[str]=None, description: typing.Optional[str]=None, layer_name: typing.Optional[str]=None, license_info: typing.Optional[str]=None, retention_policy: typing.Optional[str]=None) -> None:
        props: CfnLayerVersionProps = {}

        if compatible_runtimes is not None:
            props["compatibleRuntimes"] = compatible_runtimes

        if content_uri is not None:
            props["contentUri"] = content_uri

        if description is not None:
            props["description"] = description

        if layer_name is not None:
            props["layerName"] = layer_name

        if license_info is not None:
            props["licenseInfo"] = license_info

        if retention_policy is not None:
            props["retentionPolicy"] = retention_policy

        jsii.create(CfnLayerVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="requiredTransform")
    def REQUIRED_TRANSFORM(cls) -> str:
        return jsii.sget(cls, "requiredTransform")

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        return jsii.get(self, "layerVersionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLayerVersionProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnLayerVersionProps")
class CfnLayerVersionProps(jsii.compat.TypedDict, total=False):
    compatibleRuntimes: typing.List[str]
    contentUri: str
    description: str
    layerName: str
    licenseInfo: str
    retentionPolicy: str

class CfnSimpleTable(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sam.CfnSimpleTable"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, primary_key: typing.Optional[typing.Union[aws_cdk.cdk.Token, "PrimaryKeyProperty"]]=None, provisioned_throughput: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ProvisionedThroughputProperty"]]=None, sse_specification: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SSESpecificationProperty"]]=None, table_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        props: CfnSimpleTableProps = {}

        if primary_key is not None:
            props["primaryKey"] = primary_key

        if provisioned_throughput is not None:
            props["provisionedThroughput"] = provisioned_throughput

        if sse_specification is not None:
            props["sseSpecification"] = sse_specification

        if table_name is not None:
            props["tableName"] = table_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnSimpleTable, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="requiredTransform")
    def REQUIRED_TRANSFORM(cls) -> str:
        return jsii.sget(cls, "requiredTransform")

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSimpleTableProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="simpleTableName")
    def simple_table_name(self) -> str:
        return jsii.get(self, "simpleTableName")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    class _PrimaryKeyProperty(jsii.compat.TypedDict, total=False):
        name: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnSimpleTable.PrimaryKeyProperty")
    class PrimaryKeyProperty(_PrimaryKeyProperty):
        type: str

    class _ProvisionedThroughputProperty(jsii.compat.TypedDict, total=False):
        readCapacityUnits: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnSimpleTable.ProvisionedThroughputProperty")
    class ProvisionedThroughputProperty(_ProvisionedThroughputProperty):
        writeCapacityUnits: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnSimpleTable.SSESpecificationProperty")
    class SSESpecificationProperty(jsii.compat.TypedDict, total=False):
        sseEnabled: typing.Union[bool, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-sam.CfnSimpleTableProps")
class CfnSimpleTableProps(jsii.compat.TypedDict, total=False):
    primaryKey: typing.Union[aws_cdk.cdk.Token, "CfnSimpleTable.PrimaryKeyProperty"]
    provisionedThroughput: typing.Union[aws_cdk.cdk.Token, "CfnSimpleTable.ProvisionedThroughputProperty"]
    sseSpecification: typing.Union[aws_cdk.cdk.Token, "CfnSimpleTable.SSESpecificationProperty"]
    tableName: str
    tags: typing.Mapping[str,str]

__all__ = ["CfnApi", "CfnApiProps", "CfnApplication", "CfnApplicationProps", "CfnFunction", "CfnFunctionProps", "CfnLayerVersion", "CfnLayerVersionProps", "CfnSimpleTable", "CfnSimpleTableProps", "__jsii_assembly__"]

publication.publish()
