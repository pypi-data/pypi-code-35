import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.assets
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_logs
import aws_cdk.aws_s3
import aws_cdk.aws_s3_notifications
import aws_cdk.aws_sqs
import aws_cdk.aws_stepfunctions
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-lambda", "0.28.0", __name__, "aws-lambda@0.28.0.jsii.tgz")
class _AliasProps(jsii.compat.TypedDict, total=False):
    additionalVersions: typing.List["VersionWeight"]
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.AliasProps")
class AliasProps(_AliasProps):
    aliasName: str
    version: "Version"

class CfnAlias(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.CfnAlias"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, function_name: str, function_version: str, name: str, description: typing.Optional[str]=None, routing_config: typing.Optional[typing.Union["AliasRoutingConfigurationProperty", aws_cdk.cdk.Token]]=None) -> None:
        props: CfnAliasProps = {"functionName": function_name, "functionVersion": function_version, "name": name}

        if description is not None:
            props["description"] = description

        if routing_config is not None:
            props["routingConfig"] = routing_config

        jsii.create(CfnAlias, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> str:
        return jsii.get(self, "aliasArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAliasProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnAlias.AliasRoutingConfigurationProperty")
    class AliasRoutingConfigurationProperty(jsii.compat.TypedDict):
        additionalVersionWeights: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAlias.VersionWeightProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnAlias.VersionWeightProperty")
    class VersionWeightProperty(jsii.compat.TypedDict):
        functionVersion: str
        functionWeight: typing.Union[jsii.Number, aws_cdk.cdk.Token]


class _CfnAliasProps(jsii.compat.TypedDict, total=False):
    description: str
    routingConfig: typing.Union["CfnAlias.AliasRoutingConfigurationProperty", aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnAliasProps")
class CfnAliasProps(_CfnAliasProps):
    functionName: str
    functionVersion: str
    name: str

class CfnEventSourceMapping(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.CfnEventSourceMapping"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, event_source_arn: str, function_name: str, batch_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, enabled: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, starting_position: typing.Optional[str]=None) -> None:
        props: CfnEventSourceMappingProps = {"eventSourceArn": event_source_arn, "functionName": function_name}

        if batch_size is not None:
            props["batchSize"] = batch_size

        if enabled is not None:
            props["enabled"] = enabled

        if starting_position is not None:
            props["startingPosition"] = starting_position

        jsii.create(CfnEventSourceMapping, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="eventSourceMappingName")
    def event_source_mapping_name(self) -> str:
        return jsii.get(self, "eventSourceMappingName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEventSourceMappingProps":
        return jsii.get(self, "propertyOverrides")


class _CfnEventSourceMappingProps(jsii.compat.TypedDict, total=False):
    batchSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    enabled: typing.Union[bool, aws_cdk.cdk.Token]
    startingPosition: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnEventSourceMappingProps")
class CfnEventSourceMappingProps(_CfnEventSourceMappingProps):
    eventSourceArn: str
    functionName: str

class CfnFunction(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.CfnFunction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, code: typing.Union[aws_cdk.cdk.Token, "CodeProperty"], handler: str, role: str, runtime: str, dead_letter_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "DeadLetterConfigProperty"]]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Union[aws_cdk.cdk.Token, "EnvironmentProperty"]]=None, function_name: typing.Optional[str]=None, kms_key_arn: typing.Optional[str]=None, layers: typing.Optional[typing.List[str]]=None, memory_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, reserved_concurrent_executions: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, timeout: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, tracing_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "TracingConfigProperty"]]=None, vpc_config: typing.Optional[typing.Union[aws_cdk.cdk.Token, "VpcConfigProperty"]]=None) -> None:
        props: CfnFunctionProps = {"code": code, "handler": handler, "role": role, "runtime": runtime}

        if dead_letter_config is not None:
            props["deadLetterConfig"] = dead_letter_config

        if description is not None:
            props["description"] = description

        if environment is not None:
            props["environment"] = environment

        if function_name is not None:
            props["functionName"] = function_name

        if kms_key_arn is not None:
            props["kmsKeyArn"] = kms_key_arn

        if layers is not None:
            props["layers"] = layers

        if memory_size is not None:
            props["memorySize"] = memory_size

        if reserved_concurrent_executions is not None:
            props["reservedConcurrentExecutions"] = reserved_concurrent_executions

        if tags is not None:
            props["tags"] = tags

        if timeout is not None:
            props["timeout"] = timeout

        if tracing_config is not None:
            props["tracingConfig"] = tracing_config

        if vpc_config is not None:
            props["vpcConfig"] = vpc_config

        jsii.create(CfnFunction, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        return jsii.get(self, "functionArn")

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

    @jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnFunction.CodeProperty")
    class CodeProperty(jsii.compat.TypedDict, total=False):
        s3Bucket: str
        s3Key: str
        s3ObjectVersion: str
        zipFile: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnFunction.DeadLetterConfigProperty")
    class DeadLetterConfigProperty(jsii.compat.TypedDict, total=False):
        targetArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnFunction.EnvironmentProperty")
    class EnvironmentProperty(jsii.compat.TypedDict, total=False):
        variables: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnFunction.TracingConfigProperty")
    class TracingConfigProperty(jsii.compat.TypedDict, total=False):
        mode: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnFunction.VpcConfigProperty")
    class VpcConfigProperty(jsii.compat.TypedDict):
        securityGroupIds: typing.List[str]
        subnetIds: typing.List[str]


class _CfnFunctionProps(jsii.compat.TypedDict, total=False):
    deadLetterConfig: typing.Union[aws_cdk.cdk.Token, "CfnFunction.DeadLetterConfigProperty"]
    description: str
    environment: typing.Union[aws_cdk.cdk.Token, "CfnFunction.EnvironmentProperty"]
    functionName: str
    kmsKeyArn: str
    layers: typing.List[str]
    memorySize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    reservedConcurrentExecutions: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    timeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    tracingConfig: typing.Union[aws_cdk.cdk.Token, "CfnFunction.TracingConfigProperty"]
    vpcConfig: typing.Union[aws_cdk.cdk.Token, "CfnFunction.VpcConfigProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnFunctionProps")
class CfnFunctionProps(_CfnFunctionProps):
    code: typing.Union[aws_cdk.cdk.Token, "CfnFunction.CodeProperty"]
    handler: str
    role: str
    runtime: str

class CfnLayerVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.CfnLayerVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, content: typing.Union[aws_cdk.cdk.Token, "ContentProperty"], compatible_runtimes: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, layer_name: typing.Optional[str]=None, license_info: typing.Optional[str]=None) -> None:
        props: CfnLayerVersionProps = {"content": content}

        if compatible_runtimes is not None:
            props["compatibleRuntimes"] = compatible_runtimes

        if description is not None:
            props["description"] = description

        if layer_name is not None:
            props["layerName"] = layer_name

        if license_info is not None:
            props["licenseInfo"] = license_info

        jsii.create(CfnLayerVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

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

    class _ContentProperty(jsii.compat.TypedDict, total=False):
        s3ObjectVersion: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnLayerVersion.ContentProperty")
    class ContentProperty(_ContentProperty):
        s3Bucket: str
        s3Key: str


class CfnLayerVersionPermission(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.CfnLayerVersionPermission"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, action: str, layer_version_arn: str, principal: str, organization_id: typing.Optional[str]=None) -> None:
        props: CfnLayerVersionPermissionProps = {"action": action, "layerVersionArn": layer_version_arn, "principal": principal}

        if organization_id is not None:
            props["organizationId"] = organization_id

        jsii.create(CfnLayerVersionPermission, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="layerVersionPermissionArn")
    def layer_version_permission_arn(self) -> str:
        return jsii.get(self, "layerVersionPermissionArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLayerVersionPermissionProps":
        return jsii.get(self, "propertyOverrides")


class _CfnLayerVersionPermissionProps(jsii.compat.TypedDict, total=False):
    organizationId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnLayerVersionPermissionProps")
class CfnLayerVersionPermissionProps(_CfnLayerVersionPermissionProps):
    action: str
    layerVersionArn: str
    principal: str

class _CfnLayerVersionProps(jsii.compat.TypedDict, total=False):
    compatibleRuntimes: typing.List[str]
    description: str
    layerName: str
    licenseInfo: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnLayerVersionProps")
class CfnLayerVersionProps(_CfnLayerVersionProps):
    content: typing.Union[aws_cdk.cdk.Token, "CfnLayerVersion.ContentProperty"]

class CfnPermission(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.CfnPermission"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, action: str, function_name: str, principal: str, event_source_token: typing.Optional[str]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        props: CfnPermissionProps = {"action": action, "functionName": function_name, "principal": principal}

        if event_source_token is not None:
            props["eventSourceToken"] = event_source_token

        if source_account is not None:
            props["sourceAccount"] = source_account

        if source_arn is not None:
            props["sourceArn"] = source_arn

        jsii.create(CfnPermission, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPermissionProps":
        return jsii.get(self, "propertyOverrides")


class _CfnPermissionProps(jsii.compat.TypedDict, total=False):
    eventSourceToken: str
    sourceAccount: str
    sourceArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnPermissionProps")
class CfnPermissionProps(_CfnPermissionProps):
    action: str
    functionName: str
    principal: str

class CfnVersion(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.CfnVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, function_name: str, code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        props: CfnVersionProps = {"functionName": function_name}

        if code_sha256 is not None:
            props["codeSha256"] = code_sha256

        if description is not None:
            props["description"] = description

        jsii.create(CfnVersion, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnVersionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        return jsii.get(self, "version")

    @property
    @jsii.member(jsii_name="versionArn")
    def version_arn(self) -> str:
        return jsii.get(self, "versionArn")


class _CfnVersionProps(jsii.compat.TypedDict, total=False):
    codeSha256: str
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.CfnVersionProps")
class CfnVersionProps(_CfnVersionProps):
    functionName: str

class Code(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-lambda.Code"):
    @staticmethod
    def __jsii_proxy_class__():
        return _CodeProxy

    def __init__(self) -> None:
        jsii.create(Code, self, [])

    @jsii.member(jsii_name="asset")
    @classmethod
    def asset(cls, path: str) -> "AssetCode":
        return jsii.sinvoke(cls, "asset", [path])

    @jsii.member(jsii_name="bucket")
    @classmethod
    def bucket(cls, bucket: aws_cdk.aws_s3.IBucket, key: str, object_version: typing.Optional[str]=None) -> "S3Code":
        return jsii.sinvoke(cls, "bucket", [bucket, key, object_version])

    @jsii.member(jsii_name="directory")
    @classmethod
    def directory(cls, directory_to_zip: str) -> "AssetCode":
        return jsii.sinvoke(cls, "directory", [directory_to_zip])

    @jsii.member(jsii_name="file")
    @classmethod
    def file(cls, file_path: str) -> "AssetCode":
        return jsii.sinvoke(cls, "file", [file_path])

    @jsii.member(jsii_name="inline")
    @classmethod
    def inline(cls, code: str) -> "InlineCode":
        return jsii.sinvoke(cls, "inline", [code])

    @jsii.member(jsii_name="bind")
    def bind(self, _construct: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [_construct])

    @property
    @jsii.member(jsii_name="isInline")
    @abc.abstractmethod
    def is_inline(self) -> bool:
        ...


class _CodeProxy(Code):
    @property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        return jsii.get(self, "isInline")


class AssetCode(Code, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.AssetCode"):
    def __init__(self, path: str, packaging: typing.Optional[aws_cdk.assets.AssetPackaging]=None) -> None:
        jsii.create(AssetCode, self, [path, packaging])

    @jsii.member(jsii_name="bind")
    def bind(self, construct: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [construct])

    @property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        return jsii.get(self, "isInline")

    @property
    @jsii.member(jsii_name="packaging")
    def packaging(self) -> aws_cdk.assets.AssetPackaging:
        return jsii.get(self, "packaging")

    @property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        return jsii.get(self, "path")


class EventSourceMapping(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.EventSourceMapping"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, event_source_arn: str, target: "IFunction", batch_size: typing.Optional[jsii.Number]=None, enabled: typing.Optional[bool]=None, starting_position: typing.Optional["StartingPosition"]=None) -> None:
        props: EventSourceMappingProps = {"eventSourceArn": event_source_arn, "target": target}

        if batch_size is not None:
            props["batchSize"] = batch_size

        if enabled is not None:
            props["enabled"] = enabled

        if starting_position is not None:
            props["startingPosition"] = starting_position

        jsii.create(EventSourceMapping, self, [scope, id, props])


class _EventSourceMappingProps(jsii.compat.TypedDict, total=False):
    batchSize: jsii.Number
    enabled: bool
    startingPosition: "StartingPosition"

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.EventSourceMappingProps")
class EventSourceMappingProps(_EventSourceMappingProps):
    eventSourceArn: str
    target: "IFunction"

class _FunctionImportProps(jsii.compat.TypedDict, total=False):
    role: aws_cdk.aws_iam.IRole
    securityGroupId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.FunctionImportProps")
class FunctionImportProps(_FunctionImportProps):
    functionArn: str

class _FunctionProps(jsii.compat.TypedDict, total=False):
    allowAllOutbound: bool
    deadLetterQueue: aws_cdk.aws_sqs.IQueue
    deadLetterQueueEnabled: bool
    description: str
    environment: typing.Mapping[str,typing.Any]
    events: typing.List["IEventSource"]
    functionName: str
    initialPolicy: typing.List[aws_cdk.aws_iam.PolicyStatement]
    layers: typing.List["ILayerVersion"]
    logRetentionDays: aws_cdk.aws_logs.RetentionDays
    memorySize: jsii.Number
    reservedConcurrentExecutions: jsii.Number
    role: aws_cdk.aws_iam.IRole
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    timeout: jsii.Number
    tracing: "Tracing"
    vpc: aws_cdk.aws_ec2.IVpcNetwork
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.FunctionProps")
class FunctionProps(_FunctionProps):
    code: "Code"
    handler: str
    runtime: "Runtime"

@jsii.interface(jsii_type="@aws-cdk/aws-lambda.IEventSource")
class IEventSource(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IEventSourceProxy

    @jsii.member(jsii_name="bind")
    def bind(self, target: "FunctionBase") -> None:
        ...


class _IEventSourceProxy():
    __jsii_type__ = "@aws-cdk/aws-lambda.IEventSource"
    @jsii.member(jsii_name="bind")
    def bind(self, target: "FunctionBase") -> None:
        return jsii.invoke(self, "bind", [target])


@jsii.interface(jsii_type="@aws-cdk/aws-lambda.IFunction")
class IFunction(aws_cdk.cdk.IConstruct, aws_cdk.aws_events.IEventRuleTarget, aws_cdk.aws_logs.ILogSubscriptionDestination, aws_cdk.aws_s3_notifications.IBucketNotificationDestination, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_stepfunctions.IStepFunctionsTaskResource, aws_cdk.aws_iam.IGrantable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IFunctionProxy

    @property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="isBoundToVpc")
    def is_bound_to_vpc(self) -> bool:
        ...

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        ...

    @jsii.member(jsii_name="addEventSource")
    def add_event_source(self, source: "IEventSource") -> None:
        ...

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, principal: aws_cdk.aws_iam.IPrincipal, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        ...

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "FunctionImportProps":
        ...

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricErrors")
    def metric_errors(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricThrottles")
    def metric_throttles(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...


class _IFunctionProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_events.IEventRuleTarget), jsii.proxy_for(aws_cdk.aws_logs.ILogSubscriptionDestination), jsii.proxy_for(aws_cdk.aws_s3_notifications.IBucketNotificationDestination), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), jsii.proxy_for(aws_cdk.aws_stepfunctions.IStepFunctionsTaskResource), jsii.proxy_for(aws_cdk.aws_iam.IGrantable)):
    __jsii_type__ = "@aws-cdk/aws-lambda.IFunction"
    @property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        return jsii.get(self, "functionArn")

    @property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        return jsii.get(self, "functionName")

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        return jsii.get(self, "id")

    @property
    @jsii.member(jsii_name="isBoundToVpc")
    def is_bound_to_vpc(self) -> bool:
        return jsii.get(self, "isBoundToVpc")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")

    @jsii.member(jsii_name="addEventSource")
    def add_event_source(self, source: "IEventSource") -> None:
        return jsii.invoke(self, "addEventSource", [source])

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, principal: aws_cdk.aws_iam.IPrincipal, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        permission: Permission = {"principal": principal}

        if action is not None:
            permission["action"] = action

        if event_source_token is not None:
            permission["eventSourceToken"] = event_source_token

        if source_account is not None:
            permission["sourceAccount"] = source_account

        if source_arn is not None:
            permission["sourceArn"] = source_arn

        return jsii.invoke(self, "addPermission", [id, permission])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="export")
    def export(self) -> "FunctionImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantInvoke", [identity])

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

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricErrors")
    def metric_errors(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricErrors", [props])

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricInvocations", [props])

    @jsii.member(jsii_name="metricThrottles")
    def metric_throttles(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricThrottles", [props])


@jsii.implements(IFunction)
class FunctionBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-lambda.FunctionBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _FunctionBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(FunctionBase, self, [scope, id])

    @jsii.member(jsii_name="addEventSource")
    def add_event_source(self, source: "IEventSource") -> None:
        return jsii.invoke(self, "addEventSource", [source])

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, principal: aws_cdk.aws_iam.IPrincipal, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        permission: Permission = {"principal": principal}

        if action is not None:
            permission["action"] = action

        if event_source_token is not None:
            permission["eventSourceToken"] = event_source_token

        if source_account is not None:
            permission["sourceAccount"] = source_account

        if source_arn is not None:
            permission["sourceArn"] = source_arn

        return jsii.invoke(self, "addPermission", [id, permission])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="asBucketNotificationDestination")
    def as_bucket_notification_destination(self, bucket_arn: str, bucket_id: str) -> aws_cdk.aws_s3_notifications.BucketNotificationDestinationProps:
        return jsii.invoke(self, "asBucketNotificationDestination", [bucket_arn, bucket_id])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, rule_arn: str, rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [rule_arn, rule_id])

    @jsii.member(jsii_name="asStepFunctionsTaskResource")
    def as_step_functions_task_resource(self, _calling_task: aws_cdk.aws_stepfunctions.Task) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskResourceProps:
        return jsii.invoke(self, "asStepFunctionsTaskResource", [_calling_task])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "FunctionImportProps":
        ...

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantInvoke", [grantee])

    @jsii.member(jsii_name="logSubscriptionDestination")
    def log_subscription_destination(self, source_log_group: aws_cdk.aws_logs.ILogGroup) -> aws_cdk.aws_logs.LogSubscriptionDestination:
        return jsii.invoke(self, "logSubscriptionDestination", [source_log_group])

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

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricErrors")
    def metric_errors(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricErrors", [props])

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricInvocations", [props])

    @jsii.member(jsii_name="metricThrottles")
    def metric_throttles(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricThrottles", [props])

    @property
    @jsii.member(jsii_name="canCreatePermissions")
    @abc.abstractmethod
    def _can_create_permissions(self) -> bool:
        ...

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="functionArn")
    @abc.abstractmethod
    def function_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="functionName")
    @abc.abstractmethod
    def function_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="grantPrincipal")
    @abc.abstractmethod
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        ...

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        return jsii.get(self, "id")

    @property
    @jsii.member(jsii_name="isBoundToVpc")
    def is_bound_to_vpc(self) -> bool:
        return jsii.get(self, "isBoundToVpc")

    @property
    @jsii.member(jsii_name="role")
    @abc.abstractmethod
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        ...


class _FunctionBaseProxy(FunctionBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "FunctionImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        return jsii.get(self, "canCreatePermissions")

    @property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        return jsii.get(self, "functionArn")

    @property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        return jsii.get(self, "functionName")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


class Alias(FunctionBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.Alias"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, alias_name: str, version: "Version", additional_versions: typing.Optional[typing.List["VersionWeight"]]=None, description: typing.Optional[str]=None) -> None:
        props: AliasProps = {"aliasName": alias_name, "version": version}

        if additional_versions is not None:
            props["additionalVersions"] = additional_versions

        if description is not None:
            props["description"] = description

        jsii.create(Alias, self, [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "FunctionImportProps":
        return jsii.invoke(self, "export", [])

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

    @property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        return jsii.get(self, "canCreatePermissions")

    @property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        return jsii.get(self, "functionArn")

    @property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        return jsii.get(self, "functionName")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


class Function(FunctionBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.Function"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, code: "Code", handler: str, runtime: "Runtime", allow_all_outbound: typing.Optional[bool]=None, dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str,typing.Any]]=None, events: typing.Optional[typing.List["IEventSource"]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, layers: typing.Optional[typing.List["ILayerVersion"]]=None, log_retention_days: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, timeout: typing.Optional[jsii.Number]=None, tracing: typing.Optional["Tracing"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        props: FunctionProps = {"code": code, "handler": handler, "runtime": runtime}

        if allow_all_outbound is not None:
            props["allowAllOutbound"] = allow_all_outbound

        if dead_letter_queue is not None:
            props["deadLetterQueue"] = dead_letter_queue

        if dead_letter_queue_enabled is not None:
            props["deadLetterQueueEnabled"] = dead_letter_queue_enabled

        if description is not None:
            props["description"] = description

        if environment is not None:
            props["environment"] = environment

        if events is not None:
            props["events"] = events

        if function_name is not None:
            props["functionName"] = function_name

        if initial_policy is not None:
            props["initialPolicy"] = initial_policy

        if layers is not None:
            props["layers"] = layers

        if log_retention_days is not None:
            props["logRetentionDays"] = log_retention_days

        if memory_size is not None:
            props["memorySize"] = memory_size

        if reserved_concurrent_executions is not None:
            props["reservedConcurrentExecutions"] = reserved_concurrent_executions

        if role is not None:
            props["role"] = role

        if security_group is not None:
            props["securityGroup"] = security_group

        if timeout is not None:
            props["timeout"] = timeout

        if tracing is not None:
            props["tracing"] = tracing

        if vpc is not None:
            props["vpc"] = vpc

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(Function, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, function_arn: str, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group_id: typing.Optional[str]=None) -> "IFunction":
        props: FunctionImportProps = {"functionArn": function_arn}

        if role is not None:
            props["role"] = role

        if security_group_id is not None:
            props["securityGroupId"] = security_group_id

        return jsii.sinvoke(cls, "import", [scope, id, props])

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

    @jsii.member(jsii_name="metricAllConcurrentExecutions")
    @classmethod
    def metric_all_concurrent_executions(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllConcurrentExecutions", [props])

    @jsii.member(jsii_name="metricAllDuration")
    @classmethod
    def metric_all_duration(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllDuration", [props])

    @jsii.member(jsii_name="metricAllErrors")
    @classmethod
    def metric_all_errors(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllErrors", [props])

    @jsii.member(jsii_name="metricAllInvocations")
    @classmethod
    def metric_all_invocations(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllInvocations", [props])

    @jsii.member(jsii_name="metricAllThrottles")
    @classmethod
    def metric_all_throttles(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllThrottles", [props])

    @jsii.member(jsii_name="metricAllUnreservedConcurrentExecutions")
    @classmethod
    def metric_all_unreserved_concurrent_executions(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.sinvoke(cls, "metricAllUnreservedConcurrentExecutions", [props])

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, key: str, value: typing.Any) -> "Function":
        return jsii.invoke(self, "addEnvironment", [key, value])

    @jsii.member(jsii_name="addLayer")
    def add_layer(self, layer: "ILayerVersion") -> "Function":
        return jsii.invoke(self, "addLayer", [layer])

    @jsii.member(jsii_name="addVersion")
    def add_version(self, name: str, code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None) -> "Version":
        return jsii.invoke(self, "addVersion", [name, code_sha256, description])

    @jsii.member(jsii_name="export")
    def export(self) -> "FunctionImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="newVersion")
    def new_version(self) -> "Version":
        return jsii.invoke(self, "newVersion", [])

    @property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        return jsii.get(self, "canCreatePermissions")

    @property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        return jsii.get(self, "functionArn")

    @property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        return jsii.get(self, "functionName")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="handler")
    def handler(self) -> str:
        return jsii.get(self, "handler")

    @property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> "Runtime":
        return jsii.get(self, "runtime")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


@jsii.interface(jsii_type="@aws-cdk/aws-lambda.ILayerVersion")
class ILayerVersion(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILayerVersionProxy

    @property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "LayerVersionImportProps":
        ...

    @jsii.member(jsii_name="grantUsage")
    def grant_usage(self, id: str, *, account_id: str, organization_id: typing.Optional[str]=None) -> "ILayerVersion":
        ...


class _ILayerVersionProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-lambda.ILayerVersion"
    @property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        return jsii.get(self, "layerVersionArn")

    @property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        return jsii.get(self, "compatibleRuntimes")

    @jsii.member(jsii_name="export")
    def export(self) -> "LayerVersionImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantUsage")
    def grant_usage(self, id: str, *, account_id: str, organization_id: typing.Optional[str]=None) -> "ILayerVersion":
        grantee: LayerVersionUsageGrantee = {"accountId": account_id}

        if organization_id is not None:
            grantee["organizationId"] = organization_id

        return jsii.invoke(self, "grantUsage", [id, grantee])


class ImportedFunction(FunctionBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.ImportedFunction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, function_arn: str, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group_id: typing.Optional[str]=None) -> None:
        props: FunctionImportProps = {"functionArn": function_arn}

        if role is not None:
            props["role"] = role

        if security_group_id is not None:
            props["securityGroupId"] = security_group_id

        jsii.create(ImportedFunction, self, [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "FunctionImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        return jsii.get(self, "canCreatePermissions")

    @property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        return jsii.get(self, "functionArn")

    @property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        return jsii.get(self, "functionName")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "FunctionImportProps":
        return jsii.get(self, "props")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


class InlineCode(Code, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.InlineCode"):
    def __init__(self, code: str) -> None:
        jsii.create(InlineCode, self, [code])

    @jsii.member(jsii_name="bind")
    def bind(self, construct: aws_cdk.cdk.Construct) -> None:
        return jsii.invoke(self, "bind", [construct])

    @property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        return jsii.get(self, "isInline")

    @property
    @jsii.member(jsii_name="code")
    def code(self) -> str:
        return jsii.get(self, "code")

    @code.setter
    def code(self, value: str):
        return jsii.set(self, "code", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.LambdaRuntimeProps")
class LambdaRuntimeProps(jsii.compat.TypedDict, total=False):
    supportsInlineCode: bool

@jsii.implements(ILayerVersion)
class LayerVersionBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-lambda.LayerVersionBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _LayerVersionBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(LayerVersionBase, self, [scope, id])

    @jsii.member(jsii_name="export")
    def export(self) -> "LayerVersionImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantUsage")
    def grant_usage(self, id: str, *, account_id: str, organization_id: typing.Optional[str]=None) -> "ILayerVersion":
        grantee: LayerVersionUsageGrantee = {"accountId": account_id}

        if organization_id is not None:
            grantee["organizationId"] = organization_id

        return jsii.invoke(self, "grantUsage", [id, grantee])

    @property
    @jsii.member(jsii_name="layerVersionArn")
    @abc.abstractmethod
    def layer_version_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="compatibleRuntimes")
    @abc.abstractmethod
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        ...


class _LayerVersionBaseProxy(LayerVersionBase):
    @property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        return jsii.get(self, "layerVersionArn")

    @property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        return jsii.get(self, "compatibleRuntimes")


class LayerVersion(LayerVersionBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.LayerVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, code: "Code", compatible_runtimes: typing.Optional[typing.List["Runtime"]]=None, description: typing.Optional[str]=None, license: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: LayerVersionProps = {"code": code}

        if compatible_runtimes is not None:
            props["compatibleRuntimes"] = compatible_runtimes

        if description is not None:
            props["description"] = description

        if license is not None:
            props["license"] = license

        if name is not None:
            props["name"] = name

        jsii.create(LayerVersion, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, layer_version_arn: str, compatible_runtimes: typing.Optional[typing.List["Runtime"]]=None) -> "ILayerVersion":
        props: LayerVersionImportProps = {"layerVersionArn": layer_version_arn}

        if compatible_runtimes is not None:
            props["compatibleRuntimes"] = compatible_runtimes

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        return jsii.get(self, "layerVersionArn")

    @property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        return jsii.get(self, "compatibleRuntimes")


class _LayerVersionImportProps(jsii.compat.TypedDict, total=False):
    compatibleRuntimes: typing.List["Runtime"]

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.LayerVersionImportProps")
class LayerVersionImportProps(_LayerVersionImportProps):
    layerVersionArn: str

class _LayerVersionProps(jsii.compat.TypedDict, total=False):
    compatibleRuntimes: typing.List["Runtime"]
    description: str
    license: str
    name: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.LayerVersionProps")
class LayerVersionProps(_LayerVersionProps):
    code: "Code"

class _LayerVersionUsageGrantee(jsii.compat.TypedDict, total=False):
    organizationId: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.LayerVersionUsageGrantee")
class LayerVersionUsageGrantee(_LayerVersionUsageGrantee):
    accountId: str

class LogRetention(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.LogRetention"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, log_group_name: str, retention_days: aws_cdk.aws_logs.RetentionDays) -> None:
        props: LogRetentionProps = {"logGroupName": log_group_name, "retentionDays": retention_days}

        jsii.create(LogRetention, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.LogRetentionProps")
class LogRetentionProps(jsii.compat.TypedDict):
    logGroupName: str
    retentionDays: aws_cdk.aws_logs.RetentionDays

class _Permission(jsii.compat.TypedDict, total=False):
    action: str
    eventSourceToken: str
    sourceAccount: str
    sourceArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.Permission")
class Permission(_Permission):
    principal: aws_cdk.aws_iam.IPrincipal

class Runtime(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.Runtime"):
    def __init__(self, name: str, family: typing.Optional["RuntimeFamily"]=None, *, supports_inline_code: typing.Optional[bool]=None) -> None:
        props: LambdaRuntimeProps = {}

        if supports_inline_code is not None:
            props["supportsInlineCode"] = supports_inline_code

        jsii.create(Runtime, self, [name, family, props])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @classproperty
    @jsii.member(jsii_name="All")
    def ALL(cls) -> typing.List["Runtime"]:
        return jsii.sget(cls, "All")

    @classproperty
    @jsii.member(jsii_name="DotNetCore1")
    def DOT_NET_CORE1(cls) -> "Runtime":
        return jsii.sget(cls, "DotNetCore1")

    @classproperty
    @jsii.member(jsii_name="DotNetCore2")
    def DOT_NET_CORE2(cls) -> "Runtime":
        return jsii.sget(cls, "DotNetCore2")

    @classproperty
    @jsii.member(jsii_name="DotNetCore21")
    def DOT_NET_CORE21(cls) -> "Runtime":
        return jsii.sget(cls, "DotNetCore21")

    @classproperty
    @jsii.member(jsii_name="Go1x")
    def GO1X(cls) -> "Runtime":
        return jsii.sget(cls, "Go1x")

    @classproperty
    @jsii.member(jsii_name="Java8")
    def JAVA8(cls) -> "Runtime":
        return jsii.sget(cls, "Java8")

    @classproperty
    @jsii.member(jsii_name="NodeJS")
    def NODE_JS(cls) -> "Runtime":
        return jsii.sget(cls, "NodeJS")

    @classproperty
    @jsii.member(jsii_name="NodeJS43")
    def NODE_J_S43(cls) -> "Runtime":
        return jsii.sget(cls, "NodeJS43")

    @classproperty
    @jsii.member(jsii_name="NodeJS610")
    def NODE_J_S610(cls) -> "Runtime":
        return jsii.sget(cls, "NodeJS610")

    @classproperty
    @jsii.member(jsii_name="NodeJS810")
    def NODE_J_S810(cls) -> "Runtime":
        return jsii.sget(cls, "NodeJS810")

    @classproperty
    @jsii.member(jsii_name="Provided")
    def PROVIDED(cls) -> "Runtime":
        return jsii.sget(cls, "Provided")

    @classproperty
    @jsii.member(jsii_name="Python27")
    def PYTHON27(cls) -> "Runtime":
        return jsii.sget(cls, "Python27")

    @classproperty
    @jsii.member(jsii_name="Python36")
    def PYTHON36(cls) -> "Runtime":
        return jsii.sget(cls, "Python36")

    @classproperty
    @jsii.member(jsii_name="Python37")
    def PYTHON37(cls) -> "Runtime":
        return jsii.sget(cls, "Python37")

    @classproperty
    @jsii.member(jsii_name="Ruby25")
    def RUBY25(cls) -> "Runtime":
        return jsii.sget(cls, "Ruby25")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @property
    @jsii.member(jsii_name="supportsInlineCode")
    def supports_inline_code(self) -> bool:
        return jsii.get(self, "supportsInlineCode")

    @property
    @jsii.member(jsii_name="family")
    def family(self) -> typing.Optional["RuntimeFamily"]:
        return jsii.get(self, "family")


@jsii.enum(jsii_type="@aws-cdk/aws-lambda.RuntimeFamily")
class RuntimeFamily(enum.Enum):
    NodeJS = "NodeJS"
    Java = "Java"
    Python = "Python"
    DotNetCore = "DotNetCore"
    Go = "Go"
    Ruby = "Ruby"
    Other = "Other"

class S3Code(Code, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.S3Code"):
    def __init__(self, bucket: aws_cdk.aws_s3.IBucket, key: str, object_version: typing.Optional[str]=None) -> None:
        jsii.create(S3Code, self, [bucket, key, object_version])

    @property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        return jsii.get(self, "isInline")

    @property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        return jsii.get(self, "key")

    @key.setter
    def key(self, value: str):
        return jsii.set(self, "key", value)

    @property
    @jsii.member(jsii_name="objectVersion")
    def object_version(self) -> typing.Optional[str]:
        return jsii.get(self, "objectVersion")

    @object_version.setter
    def object_version(self, value: typing.Optional[str]):
        return jsii.set(self, "objectVersion", value)


class SingletonFunction(FunctionBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.SingletonFunction"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, uuid: str, lambda_purpose: typing.Optional[str]=None, code: "Code", handler: str, runtime: "Runtime", allow_all_outbound: typing.Optional[bool]=None, dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str,typing.Any]]=None, events: typing.Optional[typing.List["IEventSource"]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, layers: typing.Optional[typing.List["ILayerVersion"]]=None, log_retention_days: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, timeout: typing.Optional[jsii.Number]=None, tracing: typing.Optional["Tracing"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpcNetwork]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        props: SingletonFunctionProps = {"uuid": uuid, "code": code, "handler": handler, "runtime": runtime}

        if lambda_purpose is not None:
            props["lambdaPurpose"] = lambda_purpose

        if allow_all_outbound is not None:
            props["allowAllOutbound"] = allow_all_outbound

        if dead_letter_queue is not None:
            props["deadLetterQueue"] = dead_letter_queue

        if dead_letter_queue_enabled is not None:
            props["deadLetterQueueEnabled"] = dead_letter_queue_enabled

        if description is not None:
            props["description"] = description

        if environment is not None:
            props["environment"] = environment

        if events is not None:
            props["events"] = events

        if function_name is not None:
            props["functionName"] = function_name

        if initial_policy is not None:
            props["initialPolicy"] = initial_policy

        if layers is not None:
            props["layers"] = layers

        if log_retention_days is not None:
            props["logRetentionDays"] = log_retention_days

        if memory_size is not None:
            props["memorySize"] = memory_size

        if reserved_concurrent_executions is not None:
            props["reservedConcurrentExecutions"] = reserved_concurrent_executions

        if role is not None:
            props["role"] = role

        if security_group is not None:
            props["securityGroup"] = security_group

        if timeout is not None:
            props["timeout"] = timeout

        if tracing is not None:
            props["tracing"] = tracing

        if vpc is not None:
            props["vpc"] = vpc

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(SingletonFunction, self, [scope, id, props])

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, name: str, *, principal: aws_cdk.aws_iam.IPrincipal, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        permission: Permission = {"principal": principal}

        if action is not None:
            permission["action"] = action

        if event_source_token is not None:
            permission["eventSourceToken"] = event_source_token

        if source_account is not None:
            permission["sourceAccount"] = source_account

        if source_arn is not None:
            permission["sourceArn"] = source_arn

        return jsii.invoke(self, "addPermission", [name, permission])

    @jsii.member(jsii_name="export")
    def export(self) -> "FunctionImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        return jsii.get(self, "canCreatePermissions")

    @property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        return jsii.get(self, "functionArn")

    @property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        return jsii.get(self, "functionName")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


class _SingletonFunctionProps(FunctionProps, jsii.compat.TypedDict, total=False):
    lambdaPurpose: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.SingletonFunctionProps")
class SingletonFunctionProps(_SingletonFunctionProps):
    uuid: str

@jsii.implements(ILayerVersion)
class SingletonLayerVersion(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.SingletonLayerVersion"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, uuid: str, code: "Code", compatible_runtimes: typing.Optional[typing.List["Runtime"]]=None, description: typing.Optional[str]=None, license: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        props: SingletonLayerVersionProps = {"uuid": uuid, "code": code}

        if compatible_runtimes is not None:
            props["compatibleRuntimes"] = compatible_runtimes

        if description is not None:
            props["description"] = description

        if license is not None:
            props["license"] = license

        if name is not None:
            props["name"] = name

        jsii.create(SingletonLayerVersion, self, [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "LayerVersionImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantUsage")
    def grant_usage(self, id: str, *, account_id: str, organization_id: typing.Optional[str]=None) -> "ILayerVersion":
        grantee: LayerVersionUsageGrantee = {"accountId": account_id}

        if organization_id is not None:
            grantee["organizationId"] = organization_id

        return jsii.invoke(self, "grantUsage", [id, grantee])

    @property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        return jsii.get(self, "layerVersionArn")

    @property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        return jsii.get(self, "compatibleRuntimes")


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.SingletonLayerVersionProps")
class SingletonLayerVersionProps(LayerVersionProps, jsii.compat.TypedDict):
    uuid: str

@jsii.enum(jsii_type="@aws-cdk/aws-lambda.StartingPosition")
class StartingPosition(enum.Enum):
    TrimHorizon = "TrimHorizon"
    Latest = "Latest"

@jsii.enum(jsii_type="@aws-cdk/aws-lambda.Tracing")
class Tracing(enum.Enum):
    Active = "Active"
    PassThrough = "PassThrough"
    Disabled = "Disabled"

class Version(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda.Version"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, lambda_: "IFunction", code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        props: VersionProps = {"lambda": lambda_}

        if code_sha256 is not None:
            props["codeSha256"] = code_sha256

        if description is not None:
            props["description"] = description

        jsii.create(Version, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="functionVersion")
    def function_version(self) -> str:
        return jsii.get(self, "functionVersion")

    @property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "IFunction":
        return jsii.get(self, "lambda")


class _VersionProps(jsii.compat.TypedDict, total=False):
    codeSha256: str
    description: str

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.VersionProps")
class VersionProps(_VersionProps):
    lambda_: "IFunction"

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda.VersionWeight")
class VersionWeight(jsii.compat.TypedDict):
    version: "Version"
    weight: jsii.Number

__all__ = ["Alias", "AliasProps", "AssetCode", "CfnAlias", "CfnAliasProps", "CfnEventSourceMapping", "CfnEventSourceMappingProps", "CfnFunction", "CfnFunctionProps", "CfnLayerVersion", "CfnLayerVersionPermission", "CfnLayerVersionPermissionProps", "CfnLayerVersionProps", "CfnPermission", "CfnPermissionProps", "CfnVersion", "CfnVersionProps", "Code", "EventSourceMapping", "EventSourceMappingProps", "Function", "FunctionBase", "FunctionImportProps", "FunctionProps", "IEventSource", "IFunction", "ILayerVersion", "ImportedFunction", "InlineCode", "LambdaRuntimeProps", "LayerVersion", "LayerVersionBase", "LayerVersionImportProps", "LayerVersionProps", "LayerVersionUsageGrantee", "LogRetention", "LogRetentionProps", "Permission", "Runtime", "RuntimeFamily", "S3Code", "SingletonFunction", "SingletonFunctionProps", "SingletonLayerVersion", "SingletonLayerVersionProps", "StartingPosition", "Tracing", "Version", "VersionProps", "VersionWeight", "__jsii_assembly__"]

publication.publish()
