import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/cdk", "0.28.0", __name__, "cdk@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/cdk.AppProps")
class AppProps(jsii.compat.TypedDict, total=False):
    autoRun: bool
    context: typing.Mapping[str,str]

class _ArnComponents(jsii.compat.TypedDict, total=False):
    account: str
    partition: str
    region: str
    resourceName: str
    sep: str

@jsii.data_type(jsii_type="@aws-cdk/cdk.ArnComponents")
class ArnComponents(_ArnComponents):
    resource: str
    service: str

@jsii.data_type(jsii_type="@aws-cdk/cdk.AutoScalingCreationPolicy")
class AutoScalingCreationPolicy(jsii.compat.TypedDict, total=False):
    minSuccessfulInstancesPercent: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/cdk.AutoScalingReplacingUpdate")
class AutoScalingReplacingUpdate(jsii.compat.TypedDict, total=False):
    willReplace: bool

@jsii.data_type(jsii_type="@aws-cdk/cdk.AutoScalingRollingUpdate")
class AutoScalingRollingUpdate(jsii.compat.TypedDict, total=False):
    maxBatchSize: jsii.Number
    minInstancesInService: jsii.Number
    minSuccessfulInstancesPercent: jsii.Number
    pauseTime: str
    suspendProcesses: typing.List[str]
    waitOnResourceSignals: bool

@jsii.data_type(jsii_type="@aws-cdk/cdk.AutoScalingScheduledAction")
class AutoScalingScheduledAction(jsii.compat.TypedDict, total=False):
    ignoreUnmodifiedGroupSizeProperties: bool

class AvailabilityZoneProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.AvailabilityZoneProvider"):
    def __init__(self, context: "Construct") -> None:
        jsii.create(AvailabilityZoneProvider, self, [context])

    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        return jsii.get(self, "availabilityZones")


class Aws(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Aws"):
    @classproperty
    @jsii.member(jsii_name="accountId")
    def account_id(cls) -> str:
        return jsii.sget(cls, "accountId")

    @classproperty
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(cls) -> typing.List[str]:
        return jsii.sget(cls, "notificationArns")

    @classproperty
    @jsii.member(jsii_name="noValue")
    def no_value(cls) -> str:
        return jsii.sget(cls, "noValue")

    @classproperty
    @jsii.member(jsii_name="partition")
    def partition(cls) -> str:
        return jsii.sget(cls, "partition")

    @classproperty
    @jsii.member(jsii_name="region")
    def region(cls) -> str:
        return jsii.sget(cls, "region")

    @classproperty
    @jsii.member(jsii_name="stackId")
    def stack_id(cls) -> str:
        return jsii.sget(cls, "stackId")

    @classproperty
    @jsii.member(jsii_name="stackName")
    def stack_name(cls) -> str:
        return jsii.sget(cls, "stackName")

    @classproperty
    @jsii.member(jsii_name="urlSuffix")
    def url_suffix(cls) -> str:
        return jsii.sget(cls, "urlSuffix")


@jsii.data_type(jsii_type="@aws-cdk/cdk.CfnConditionProps")
class CfnConditionProps(jsii.compat.TypedDict, total=False):
    expression: "ICfnConditionExpression"

@jsii.enum(jsii_type="@aws-cdk/cdk.CfnDynamicReferenceService")
class CfnDynamicReferenceService(enum.Enum):
    Ssm = "Ssm"
    SsmSecure = "SsmSecure"
    SecretsManager = "SecretsManager"

@jsii.data_type(jsii_type="@aws-cdk/cdk.CfnMappingProps")
class CfnMappingProps(jsii.compat.TypedDict, total=False):
    mapping: typing.Mapping[str,typing.Mapping[str,typing.Any]]

@jsii.data_type(jsii_type="@aws-cdk/cdk.CfnOutputProps")
class CfnOutputProps(jsii.compat.TypedDict, total=False):
    condition: "CfnCondition"
    description: str
    disableExport: bool
    export: str
    value: typing.Any

class _CfnParameterProps(jsii.compat.TypedDict, total=False):
    allowedPattern: str
    allowedValues: typing.List[str]
    constraintDescription: str
    default: typing.Any
    description: str
    maxLength: jsii.Number
    maxValue: jsii.Number
    minLength: jsii.Number
    minValue: jsii.Number
    noEcho: bool

@jsii.data_type(jsii_type="@aws-cdk/cdk.CfnParameterProps")
class CfnParameterProps(_CfnParameterProps):
    type: str

class _CfnResourceProps(jsii.compat.TypedDict, total=False):
    properties: typing.Any

@jsii.data_type(jsii_type="@aws-cdk/cdk.CfnResourceProps")
class CfnResourceProps(_CfnResourceProps):
    type: str

@jsii.data_type(jsii_type="@aws-cdk/cdk.CfnRuleProps")
class CfnRuleProps(jsii.compat.TypedDict, total=False):
    assertions: typing.List["RuleAssertion"]
    ruleCondition: "ICfnConditionExpression"

@jsii.data_type(jsii_type="@aws-cdk/cdk.CfnTag")
class CfnTag(jsii.compat.TypedDict):
    key: str
    value: str

class CloudFormationJSON(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CloudFormationJSON"):
    def __init__(self) -> None:
        jsii.create(CloudFormationJSON, self, [])

    @jsii.member(jsii_name="stringify")
    @classmethod
    def stringify(cls, obj: typing.Any, context: "IConstruct") -> str:
        return jsii.sinvoke(cls, "stringify", [obj, context])


class _CodeDeployLambdaAliasUpdate(jsii.compat.TypedDict, total=False):
    afterAllowTrafficHook: str
    beforeAllowTrafficHook: str

@jsii.data_type(jsii_type="@aws-cdk/cdk.CodeDeployLambdaAliasUpdate")
class CodeDeployLambdaAliasUpdate(_CodeDeployLambdaAliasUpdate):
    applicationName: str
    deploymentGroupName: str

class ConstructNode(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.ConstructNode"):
    def __init__(self, host: "Construct", scope: "IConstruct", id: str) -> None:
        jsii.create(ConstructNode, self, [host, scope, id])

    @jsii.member(jsii_name="addChild")
    def add_child(self, child: "IConstruct", child_name: str) -> None:
        return jsii.invoke(self, "addChild", [child, child_name])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *dependencies: "IDependable") -> None:
        return jsii.invoke(self, "addDependency", [dependencies])

    @jsii.member(jsii_name="addError")
    def add_error(self, message: str) -> None:
        return jsii.invoke(self, "addError", [message])

    @jsii.member(jsii_name="addInfo")
    def add_info(self, message: str) -> None:
        return jsii.invoke(self, "addInfo", [message])

    @jsii.member(jsii_name="addMetadata")
    def add_metadata(self, type: str, data: typing.Any, from_: typing.Any=None) -> None:
        return jsii.invoke(self, "addMetadata", [type, data, from_])

    @jsii.member(jsii_name="addWarning")
    def add_warning(self, message: str) -> None:
        return jsii.invoke(self, "addWarning", [message])

    @jsii.member(jsii_name="ancestors")
    def ancestors(self, up_to: typing.Optional["Construct"]=None) -> typing.List["IConstruct"]:
        return jsii.invoke(self, "ancestors", [up_to])

    @jsii.member(jsii_name="apply")
    def apply(self, aspect: "IAspect") -> None:
        return jsii.invoke(self, "apply", [aspect])

    @jsii.member(jsii_name="findAll")
    def find_all(self, order: typing.Optional["ConstructOrder"]=None) -> typing.List["IConstruct"]:
        return jsii.invoke(self, "findAll", [order])

    @jsii.member(jsii_name="findChild")
    def find_child(self, path: str) -> "IConstruct":
        return jsii.invoke(self, "findChild", [path])

    @jsii.member(jsii_name="findDependencies")
    def find_dependencies(self) -> typing.List["Dependency"]:
        return jsii.invoke(self, "findDependencies", [])

    @jsii.member(jsii_name="findReferences")
    def find_references(self) -> typing.List["OutgoingReference"]:
        return jsii.invoke(self, "findReferences", [])

    @jsii.member(jsii_name="getContext")
    def get_context(self, key: str) -> typing.Any:
        return jsii.invoke(self, "getContext", [key])

    @jsii.member(jsii_name="lock")
    def lock(self) -> None:
        return jsii.invoke(self, "lock", [])

    @jsii.member(jsii_name="prepareTree")
    def prepare_tree(self) -> None:
        return jsii.invoke(self, "prepareTree", [])

    @jsii.member(jsii_name="recordReference")
    def record_reference(self, *refs: "Token") -> None:
        return jsii.invoke(self, "recordReference", [refs])

    @jsii.member(jsii_name="requireContext")
    def require_context(self, key: str) -> typing.Any:
        return jsii.invoke(self, "requireContext", [key])

    @jsii.member(jsii_name="required")
    def required(self, props: typing.Any, name: str) -> typing.Any:
        return jsii.invoke(self, "required", [props, name])

    @jsii.member(jsii_name="resolve")
    def resolve(self, obj: typing.Any) -> typing.Any:
        return jsii.invoke(self, "resolve", [obj])

    @jsii.member(jsii_name="setContext")
    def set_context(self, key: str, value: typing.Any) -> None:
        return jsii.invoke(self, "setContext", [key, value])

    @jsii.member(jsii_name="stringifyJson")
    def stringify_json(self, obj: typing.Any) -> str:
        return jsii.invoke(self, "stringifyJson", [obj])

    @jsii.member(jsii_name="toTreeString")
    def to_tree_string(self, depth: typing.Optional[jsii.Number]=None) -> str:
        return jsii.invoke(self, "toTreeString", [depth])

    @jsii.member(jsii_name="tryFindChild")
    def try_find_child(self, path: str) -> typing.Optional["IConstruct"]:
        return jsii.invoke(self, "tryFindChild", [path])

    @jsii.member(jsii_name="unlock")
    def unlock(self) -> None:
        return jsii.invoke(self, "unlock", [])

    @jsii.member(jsii_name="validateTree")
    def validate_tree(self) -> typing.List["ValidationError"]:
        return jsii.invoke(self, "validateTree", [])

    @property
    @jsii.member(jsii_name="aspects")
    def aspects(self) -> typing.List["IAspect"]:
        return jsii.get(self, "aspects")

    @property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List["IConstruct"]:
        return jsii.get(self, "children")

    @property
    @jsii.member(jsii_name="host")
    def host(self) -> "Construct":
        return jsii.get(self, "host")

    @property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        return jsii.get(self, "id")

    @property
    @jsii.member(jsii_name="locked")
    def locked(self) -> bool:
        return jsii.get(self, "locked")

    @property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.List["MetadataEntry"]:
        return jsii.get(self, "metadata")

    @property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        return jsii.get(self, "path")

    @property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "Stack":
        return jsii.get(self, "stack")

    @property
    @jsii.member(jsii_name="typename")
    def typename(self) -> str:
        return jsii.get(self, "typename")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        return jsii.get(self, "uniqueId")

    @property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional["IConstruct"]:
        return jsii.get(self, "scope")


@jsii.enum(jsii_type="@aws-cdk/cdk.ConstructOrder")
class ConstructOrder(enum.Enum):
    PreOrder = "PreOrder"
    PostOrder = "PostOrder"

class ContextProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.ContextProvider"):
    def __init__(self, context: "Construct", provider: str, props: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        jsii.create(ContextProvider, self, [context, provider, props])

    @jsii.member(jsii_name="getStringListValue")
    def get_string_list_value(self, default_value: typing.List[str]) -> typing.List[str]:
        return jsii.invoke(self, "getStringListValue", [default_value])

    @jsii.member(jsii_name="getStringValue")
    def get_string_value(self, default_value: str) -> str:
        return jsii.invoke(self, "getStringValue", [default_value])

    @jsii.member(jsii_name="getValue")
    def get_value(self, default_value: typing.Any) -> typing.Any:
        return jsii.invoke(self, "getValue", [default_value])

    @property
    @jsii.member(jsii_name="context")
    def context(self) -> "Construct":
        return jsii.get(self, "context")

    @property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        return jsii.get(self, "key")

    @property
    @jsii.member(jsii_name="provider")
    def provider(self) -> str:
        return jsii.get(self, "provider")


@jsii.data_type(jsii_type="@aws-cdk/cdk.CreationPolicy")
class CreationPolicy(jsii.compat.TypedDict, total=False):
    autoScalingCreationPolicy: "AutoScalingCreationPolicy"
    resourceSignal: "ResourceSignal"

@jsii.enum(jsii_type="@aws-cdk/cdk.DeletionPolicy")
class DeletionPolicy(enum.Enum):
    Delete = "Delete"
    Retain = "Retain"
    Snapshot = "Snapshot"

@jsii.data_type(jsii_type="@aws-cdk/cdk.Dependency")
class Dependency(jsii.compat.TypedDict):
    source: "IConstruct"
    target: "IConstruct"

@jsii.data_type(jsii_type="@aws-cdk/cdk.DynamicReferenceProps")
class DynamicReferenceProps(jsii.compat.TypedDict):
    referenceKey: str
    service: "CfnDynamicReferenceService"

@jsii.data_type(jsii_type="@aws-cdk/cdk.Environment")
class Environment(jsii.compat.TypedDict, total=False):
    account: str
    region: str

@jsii.data_type(jsii_type="@aws-cdk/cdk.FileSystemStoreOptions")
class FileSystemStoreOptions(jsii.compat.TypedDict):
    outdir: str

class Fn(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Fn"):
    def __init__(self) -> None:
        jsii.create(Fn, self, [])

    @jsii.member(jsii_name="base64")
    @classmethod
    def base64(cls, data: str) -> str:
        return jsii.sinvoke(cls, "base64", [data])

    @jsii.member(jsii_name="cidr")
    @classmethod
    def cidr(cls, ip_block: str, count: jsii.Number, size_mask: typing.Optional[str]=None) -> str:
        return jsii.sinvoke(cls, "cidr", [ip_block, count, size_mask])

    @jsii.member(jsii_name="conditionAnd")
    @classmethod
    def condition_and(cls, *conditions: "ICfnConditionExpression") -> "ICfnConditionExpression":
        return jsii.sinvoke(cls, "conditionAnd", [conditions])

    @jsii.member(jsii_name="conditionContains")
    @classmethod
    def condition_contains(cls, list_of_strings: typing.List[str], value: str) -> "ICfnConditionExpression":
        return jsii.sinvoke(cls, "conditionContains", [list_of_strings, value])

    @jsii.member(jsii_name="conditionEquals")
    @classmethod
    def condition_equals(cls, lhs: typing.Any, rhs: typing.Any) -> "ICfnConditionExpression":
        return jsii.sinvoke(cls, "conditionEquals", [lhs, rhs])

    @jsii.member(jsii_name="conditionIf")
    @classmethod
    def condition_if(cls, condition_id: str, value_if_true: typing.Any, value_if_false: typing.Any) -> "ICfnConditionExpression":
        return jsii.sinvoke(cls, "conditionIf", [condition_id, value_if_true, value_if_false])

    @jsii.member(jsii_name="conditionNot")
    @classmethod
    def condition_not(cls, condition: "ICfnConditionExpression") -> "ICfnConditionExpression":
        return jsii.sinvoke(cls, "conditionNot", [condition])

    @jsii.member(jsii_name="conditionOr")
    @classmethod
    def condition_or(cls, *conditions: "ICfnConditionExpression") -> "ICfnConditionExpression":
        return jsii.sinvoke(cls, "conditionOr", [conditions])

    @jsii.member(jsii_name="findInMap")
    @classmethod
    def find_in_map(cls, map_name: str, top_level_key: str, second_level_key: str) -> str:
        return jsii.sinvoke(cls, "findInMap", [map_name, top_level_key, second_level_key])

    @jsii.member(jsii_name="getAtt")
    @classmethod
    def get_att(cls, logical_name_of_resource: str, attribute_name: str) -> "Token":
        return jsii.sinvoke(cls, "getAtt", [logical_name_of_resource, attribute_name])

    @jsii.member(jsii_name="getAZs")
    @classmethod
    def get_a_zs(cls, region: typing.Optional[str]=None) -> typing.List[str]:
        return jsii.sinvoke(cls, "getAZs", [region])

    @jsii.member(jsii_name="importValue")
    @classmethod
    def import_value(cls, shared_value_to_import: str) -> str:
        return jsii.sinvoke(cls, "importValue", [shared_value_to_import])

    @jsii.member(jsii_name="join")
    @classmethod
    def join(cls, delimiter: str, list_of_values: typing.List[str]) -> str:
        return jsii.sinvoke(cls, "join", [delimiter, list_of_values])

    @jsii.member(jsii_name="select")
    @classmethod
    def select(cls, index: jsii.Number, array: typing.List[str]) -> str:
        return jsii.sinvoke(cls, "select", [index, array])

    @jsii.member(jsii_name="split")
    @classmethod
    def split(cls, delimiter: str, source: str) -> typing.List[str]:
        return jsii.sinvoke(cls, "split", [delimiter, source])

    @jsii.member(jsii_name="sub")
    @classmethod
    def sub(cls, body: str, variables: typing.Optional[typing.Mapping[str,str]]=None) -> str:
        return jsii.sinvoke(cls, "sub", [body, variables])

    @jsii.member(jsii_name="conditionEachMemberEquals")
    def condition_each_member_equals(self, list_of_strings: typing.List[str], value: str) -> "ICfnConditionExpression":
        return jsii.invoke(self, "conditionEachMemberEquals", [list_of_strings, value])

    @jsii.member(jsii_name="conditionEachMemberIn")
    def condition_each_member_in(self, strings_to_check: typing.List[str], strings_to_match: str) -> "ICfnConditionExpression":
        return jsii.invoke(self, "conditionEachMemberIn", [strings_to_check, strings_to_match])

    @jsii.member(jsii_name="refAll")
    def ref_all(self, parameter_type: str) -> typing.List[str]:
        return jsii.invoke(self, "refAll", [parameter_type])

    @jsii.member(jsii_name="valueOf")
    def value_of(self, parameter_or_logical_id: str, attribute: str) -> str:
        return jsii.invoke(self, "valueOf", [parameter_or_logical_id, attribute])

    @jsii.member(jsii_name="valueOfAll")
    def value_of_all(self, parameter_type: str, attribute: str) -> typing.List[str]:
        return jsii.invoke(self, "valueOfAll", [parameter_type, attribute])


@jsii.interface(jsii_type="@aws-cdk/cdk.IAddressingScheme")
class IAddressingScheme(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IAddressingSchemeProxy

    @jsii.member(jsii_name="allocateAddress")
    def allocate_address(self, address_components: typing.List[str]) -> str:
        ...


class _IAddressingSchemeProxy():
    __jsii_type__ = "@aws-cdk/cdk.IAddressingScheme"
    @jsii.member(jsii_name="allocateAddress")
    def allocate_address(self, address_components: typing.List[str]) -> str:
        return jsii.invoke(self, "allocateAddress", [address_components])


@jsii.implements(IAddressingScheme)
class HashedAddressingScheme(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.HashedAddressingScheme"):
    def __init__(self) -> None:
        jsii.create(HashedAddressingScheme, self, [])

    @jsii.member(jsii_name="allocateAddress")
    def allocate_address(self, address_components: typing.List[str]) -> str:
        return jsii.invoke(self, "allocateAddress", [address_components])


@jsii.interface(jsii_type="@aws-cdk/cdk.IAspect")
class IAspect(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IAspectProxy

    @jsii.member(jsii_name="visit")
    def visit(self, node: "IConstruct") -> None:
        ...


class _IAspectProxy():
    __jsii_type__ = "@aws-cdk/cdk.IAspect"
    @jsii.member(jsii_name="visit")
    def visit(self, node: "IConstruct") -> None:
        return jsii.invoke(self, "visit", [node])


@jsii.interface(jsii_type="@aws-cdk/cdk.ICfnConditionExpression")
class ICfnConditionExpression(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ICfnConditionExpressionProxy

    @jsii.member(jsii_name="resolve")
    def resolve(self, *, prefix: typing.List[str], scope: "IConstruct") -> typing.Any:
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        ...


class _ICfnConditionExpressionProxy():
    __jsii_type__ = "@aws-cdk/cdk.ICfnConditionExpression"
    @jsii.member(jsii_name="resolve")
    def resolve(self, *, prefix: typing.List[str], scope: "IConstruct") -> typing.Any:
        context: ResolveContext = {"prefix": prefix, "scope": scope}

        return jsii.invoke(self, "resolve", [context])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])


@jsii.interface(jsii_type="@aws-cdk/cdk.IDependable")
class IDependable(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IDependableProxy

    @property
    @jsii.member(jsii_name="dependencyRoots")
    def dependency_roots(self) -> typing.List["IConstruct"]:
        ...


class _IDependableProxy():
    __jsii_type__ = "@aws-cdk/cdk.IDependable"
    @property
    @jsii.member(jsii_name="dependencyRoots")
    def dependency_roots(self) -> typing.List["IConstruct"]:
        return jsii.get(self, "dependencyRoots")


@jsii.implements(IDependable)
class ConcreteDependable(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.ConcreteDependable"):
    def __init__(self) -> None:
        jsii.create(ConcreteDependable, self, [])

    @jsii.member(jsii_name="add")
    def add(self, construct: "IConstruct") -> None:
        return jsii.invoke(self, "add", [construct])

    @property
    @jsii.member(jsii_name="dependencyRoots")
    def dependency_roots(self) -> typing.List["IConstruct"]:
        return jsii.get(self, "dependencyRoots")


@jsii.interface(jsii_type="@aws-cdk/cdk.IConstruct")
class IConstruct(IDependable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IConstructProxy

    @property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        ...


class _IConstructProxy(jsii.proxy_for(IDependable)):
    __jsii_type__ = "@aws-cdk/cdk.IConstruct"
    @property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        return jsii.get(self, "node")


@jsii.implements(IConstruct)
class Construct(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Construct"):
    def __init__(self, scope: "Construct", id: str) -> None:
        jsii.create(Construct, self, [scope, id])

    @jsii.member(jsii_name="isConstruct")
    @classmethod
    def is_construct(cls, x: "IConstruct") -> bool:
        return jsii.sinvoke(cls, "isConstruct", [x])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        return jsii.invoke(self, "prepare", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="dependencyRoots")
    def dependency_roots(self) -> typing.List["IConstruct"]:
        return jsii.get(self, "dependencyRoots")

    @property
    @jsii.member(jsii_name="node")
    def node(self) -> "ConstructNode":
        return jsii.get(self, "node")


class CfnElement(Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/cdk.CfnElement"):
    @staticmethod
    def __jsii_proxy_class__():
        return _CfnElementProxy

    def __init__(self, scope: "Construct", id: str) -> None:
        jsii.create(CfnElement, self, [scope, id])

    @jsii.member(jsii_name="isCfnElement")
    @classmethod
    def is_cfn_element(cls, construct: "IConstruct") -> bool:
        return jsii.sinvoke(cls, "isCfnElement", [construct])

    @jsii.member(jsii_name="overrideLogicalId")
    def override_logical_id(self, new_logical_id: str) -> None:
        return jsii.invoke(self, "overrideLogicalId", [new_logical_id])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        return jsii.invoke(self, "prepare", [])

    @property
    @jsii.member(jsii_name="creationStackTrace")
    def creation_stack_trace(self) -> typing.List[str]:
        return jsii.get(self, "creationStackTrace")

    @property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> str:
        return jsii.get(self, "logicalId")

    @property
    @jsii.member(jsii_name="stackPath")
    def stack_path(self) -> str:
        return jsii.get(self, "stackPath")


class _CfnElementProxy(CfnElement):
    pass

class CfnOutput(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CfnOutput"):
    def __init__(self, scope: "Construct", id: str, *, condition: typing.Optional["CfnCondition"]=None, description: typing.Optional[str]=None, disable_export: typing.Optional[bool]=None, export: typing.Optional[str]=None, value: typing.Any=None) -> None:
        props: CfnOutputProps = {}

        if condition is not None:
            props["condition"] = condition

        if description is not None:
            props["description"] = description

        if disable_export is not None:
            props["disableExport"] = disable_export

        if export is not None:
            props["export"] = export

        if value is not None:
            props["value"] = value

        jsii.create(CfnOutput, self, [scope, id, props])

    @jsii.member(jsii_name="makeImportValue")
    def make_import_value(self) -> typing.Any:
        return jsii.invoke(self, "makeImportValue", [])

    @jsii.member(jsii_name="obtainExportName")
    def obtain_export_name(self) -> str:
        return jsii.invoke(self, "obtainExportName", [])

    @property
    @jsii.member(jsii_name="ref")
    def ref(self) -> str:
        return jsii.get(self, "ref")

    @property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        return jsii.get(self, "value")

    @property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional["CfnCondition"]:
        return jsii.get(self, "condition")

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        return jsii.get(self, "description")

    @property
    @jsii.member(jsii_name="export")
    def export(self) -> typing.Optional[str]:
        return jsii.get(self, "export")

    @export.setter
    def export(self, value: typing.Optional[str]):
        return jsii.set(self, "export", value)


class CfnRefElement(CfnElement, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/cdk.CfnRefElement"):
    @staticmethod
    def __jsii_proxy_class__():
        return _CfnRefElementProxy

    def __init__(self, scope: "Construct", id: str) -> None:
        jsii.create(CfnRefElement, self, [scope, id])

    @property
    @jsii.member(jsii_name="ref")
    def ref(self) -> str:
        return jsii.get(self, "ref")

    @property
    @jsii.member(jsii_name="referenceToken")
    def _reference_token(self) -> "Token":
        return jsii.get(self, "referenceToken")


class _CfnRefElementProxy(CfnRefElement, jsii.proxy_for(CfnElement)):
    pass

@jsii.implements(ICfnConditionExpression)
class CfnCondition(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CfnCondition"):
    def __init__(self, scope: "Construct", id: str, *, expression: typing.Optional["ICfnConditionExpression"]=None) -> None:
        props: CfnConditionProps = {}

        if expression is not None:
            props["expression"] = expression

        jsii.create(CfnCondition, self, [scope, id, props])

    @jsii.member(jsii_name="resolve")
    def resolve(self, *, prefix: typing.List[str], scope: "IConstruct") -> typing.Any:
        _context: ResolveContext = {"prefix": prefix, "scope": scope}

        return jsii.invoke(self, "resolve", [_context])

    @property
    @jsii.member(jsii_name="expression")
    def expression(self) -> typing.Optional["ICfnConditionExpression"]:
        return jsii.get(self, "expression")

    @expression.setter
    def expression(self, value: typing.Optional["ICfnConditionExpression"]):
        return jsii.set(self, "expression", value)


class CfnMapping(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CfnMapping"):
    def __init__(self, scope: "Construct", id: str, *, mapping: typing.Optional[typing.Mapping[str,typing.Mapping[str,typing.Any]]]=None) -> None:
        props: CfnMappingProps = {}

        if mapping is not None:
            props["mapping"] = mapping

        jsii.create(CfnMapping, self, [scope, id, props])

    @jsii.member(jsii_name="findInMap")
    def find_in_map(self, key1: str, key2: str) -> str:
        return jsii.invoke(self, "findInMap", [key1, key2])

    @jsii.member(jsii_name="setValue")
    def set_value(self, key1: str, key2: str, value: typing.Any) -> None:
        return jsii.invoke(self, "setValue", [key1, key2, value])


class CfnParameter(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CfnParameter"):
    def __init__(self, scope: "Construct", id: str, *, type: str, allowed_pattern: typing.Optional[str]=None, allowed_values: typing.Optional[typing.List[str]]=None, constraint_description: typing.Optional[str]=None, default: typing.Any=None, description: typing.Optional[str]=None, max_length: typing.Optional[jsii.Number]=None, max_value: typing.Optional[jsii.Number]=None, min_length: typing.Optional[jsii.Number]=None, min_value: typing.Optional[jsii.Number]=None, no_echo: typing.Optional[bool]=None) -> None:
        props: CfnParameterProps = {"type": type}

        if allowed_pattern is not None:
            props["allowedPattern"] = allowed_pattern

        if allowed_values is not None:
            props["allowedValues"] = allowed_values

        if constraint_description is not None:
            props["constraintDescription"] = constraint_description

        if default is not None:
            props["default"] = default

        if description is not None:
            props["description"] = description

        if max_length is not None:
            props["maxLength"] = max_length

        if max_value is not None:
            props["maxValue"] = max_value

        if min_length is not None:
            props["minLength"] = min_length

        if min_value is not None:
            props["minValue"] = min_value

        if no_echo is not None:
            props["noEcho"] = no_echo

        jsii.create(CfnParameter, self, [scope, id, props])

    @jsii.member(jsii_name="resolve")
    def resolve(self) -> typing.Any:
        return jsii.invoke(self, "resolve", [])

    @property
    @jsii.member(jsii_name="noEcho")
    def no_echo(self) -> bool:
        return jsii.get(self, "noEcho")

    @property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[str]:
        return jsii.get(self, "stringListValue")

    @string_list_value.setter
    def string_list_value(self, value: typing.List[str]):
        return jsii.set(self, "stringListValue", value)

    @property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> str:
        return jsii.get(self, "stringValue")

    @string_value.setter
    def string_value(self, value: str):
        return jsii.set(self, "stringValue", value)

    @property
    @jsii.member(jsii_name="value")
    def value(self) -> "Token":
        return jsii.get(self, "value")

    @value.setter
    def value(self, value: "Token"):
        return jsii.set(self, "value", value)


class CfnResource(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CfnResource"):
    def __init__(self, scope: "Construct", id: str, *, type: str, properties: typing.Any=None) -> None:
        props: CfnResourceProps = {"type": type}

        if properties is not None:
            props["properties"] = properties

        jsii.create(CfnResource, self, [scope, id, props])

    @jsii.member(jsii_name="attribute")
    @classmethod
    def attribute(cls, custom_name: typing.Optional[str]=None) -> typing.Any:
        return jsii.sinvoke(cls, "attribute", [custom_name])

    @jsii.member(jsii_name="isCfnResource")
    @classmethod
    def is_cfn_resource(cls, construct: "IConstruct") -> bool:
        return jsii.sinvoke(cls, "isCfnResource", [construct])

    @jsii.member(jsii_name="isTaggable")
    @classmethod
    def is_taggable(cls, construct: typing.Any) -> bool:
        return jsii.sinvoke(cls, "isTaggable", [construct])

    @jsii.member(jsii_name="addDeletionOverride")
    def add_deletion_override(self, path: str) -> None:
        return jsii.invoke(self, "addDeletionOverride", [path])

    @jsii.member(jsii_name="addDependsOn")
    def add_depends_on(self, resource: "CfnResource") -> None:
        return jsii.invoke(self, "addDependsOn", [resource])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="addPropertyDeletionOverride")
    def add_property_deletion_override(self, property_path: str) -> None:
        return jsii.invoke(self, "addPropertyDeletionOverride", [property_path])

    @jsii.member(jsii_name="addPropertyOverride")
    def add_property_override(self, property_path: str, value: typing.Any) -> None:
        return jsii.invoke(self, "addPropertyOverride", [property_path, value])

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: str) -> "CfnReference":
        return jsii.invoke(self, "getAtt", [attribute_name])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @property
    @jsii.member(jsii_name="options")
    def options(self) -> "IResourceOptions":
        return jsii.get(self, "options")

    @property
    @jsii.member(jsii_name="properties")
    def _properties(self) -> typing.Any:
        return jsii.get(self, "properties")

    @property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> str:
        return jsii.get(self, "resourceType")

    @property
    @jsii.member(jsii_name="untypedPropertyOverrides")
    def _untyped_property_overrides(self) -> typing.Any:
        return jsii.get(self, "untypedPropertyOverrides")


class CfnRule(CfnRefElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CfnRule"):
    def __init__(self, scope: "Construct", id: str, *, assertions: typing.Optional[typing.List["RuleAssertion"]]=None, rule_condition: typing.Optional["ICfnConditionExpression"]=None) -> None:
        props: CfnRuleProps = {}

        if assertions is not None:
            props["assertions"] = assertions

        if rule_condition is not None:
            props["ruleCondition"] = rule_condition

        jsii.create(CfnRule, self, [scope, id, props])

    @jsii.member(jsii_name="addAssertion")
    def add_assertion(self, condition: "ICfnConditionExpression", description: str) -> None:
        return jsii.invoke(self, "addAssertion", [condition, description])

    @property
    @jsii.member(jsii_name="assertions")
    def assertions(self) -> typing.Optional[typing.List["RuleAssertion"]]:
        return jsii.get(self, "assertions")

    @assertions.setter
    def assertions(self, value: typing.Optional[typing.List["RuleAssertion"]]):
        return jsii.set(self, "assertions", value)

    @property
    @jsii.member(jsii_name="ruleCondition")
    def rule_condition(self) -> typing.Optional["ICfnConditionExpression"]:
        return jsii.get(self, "ruleCondition")

    @rule_condition.setter
    def rule_condition(self, value: typing.Optional["ICfnConditionExpression"]):
        return jsii.set(self, "ruleCondition", value)


@jsii.interface(jsii_type="@aws-cdk/cdk.IResolvedValuePostProcessor")
class IResolvedValuePostProcessor(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IResolvedValuePostProcessorProxy

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, *, prefix: typing.List[str], scope: "IConstruct") -> typing.Any:
        ...


class _IResolvedValuePostProcessorProxy():
    __jsii_type__ = "@aws-cdk/cdk.IResolvedValuePostProcessor"
    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, *, prefix: typing.List[str], scope: "IConstruct") -> typing.Any:
        context: ResolveContext = {"prefix": prefix, "scope": scope}

        return jsii.invoke(self, "postProcess", [input, context])


@jsii.interface(jsii_type="@aws-cdk/cdk.IResourceOptions")
class IResourceOptions(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IResourceOptionsProxy

    @property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional["CfnCondition"]:
        ...

    @condition.setter
    def condition(self, value: typing.Optional["CfnCondition"]):
        ...

    @property
    @jsii.member(jsii_name="creationPolicy")
    def creation_policy(self) -> typing.Optional["CreationPolicy"]:
        ...

    @creation_policy.setter
    def creation_policy(self, value: typing.Optional["CreationPolicy"]):
        ...

    @property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> typing.Optional["DeletionPolicy"]:
        ...

    @deletion_policy.setter
    def deletion_policy(self, value: typing.Optional["DeletionPolicy"]):
        ...

    @property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        ...

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str,typing.Any]]):
        ...

    @property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> typing.Optional["UpdatePolicy"]:
        ...

    @update_policy.setter
    def update_policy(self, value: typing.Optional["UpdatePolicy"]):
        ...

    @property
    @jsii.member(jsii_name="updateReplacePolicy")
    def update_replace_policy(self) -> typing.Optional["DeletionPolicy"]:
        ...

    @update_replace_policy.setter
    def update_replace_policy(self, value: typing.Optional["DeletionPolicy"]):
        ...


class _IResourceOptionsProxy():
    __jsii_type__ = "@aws-cdk/cdk.IResourceOptions"
    @property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional["CfnCondition"]:
        return jsii.get(self, "condition")

    @condition.setter
    def condition(self, value: typing.Optional["CfnCondition"]):
        return jsii.set(self, "condition", value)

    @property
    @jsii.member(jsii_name="creationPolicy")
    def creation_policy(self) -> typing.Optional["CreationPolicy"]:
        return jsii.get(self, "creationPolicy")

    @creation_policy.setter
    def creation_policy(self, value: typing.Optional["CreationPolicy"]):
        return jsii.set(self, "creationPolicy", value)

    @property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> typing.Optional["DeletionPolicy"]:
        return jsii.get(self, "deletionPolicy")

    @deletion_policy.setter
    def deletion_policy(self, value: typing.Optional["DeletionPolicy"]):
        return jsii.set(self, "deletionPolicy", value)

    @property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        return jsii.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str,typing.Any]]):
        return jsii.set(self, "metadata", value)

    @property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(self) -> typing.Optional["UpdatePolicy"]:
        return jsii.get(self, "updatePolicy")

    @update_policy.setter
    def update_policy(self, value: typing.Optional["UpdatePolicy"]):
        return jsii.set(self, "updatePolicy", value)

    @property
    @jsii.member(jsii_name="updateReplacePolicy")
    def update_replace_policy(self) -> typing.Optional["DeletionPolicy"]:
        return jsii.get(self, "updateReplacePolicy")

    @update_replace_policy.setter
    def update_replace_policy(self, value: typing.Optional["DeletionPolicy"]):
        return jsii.set(self, "updateReplacePolicy", value)


@jsii.interface(jsii_type="@aws-cdk/cdk.ISessionStore")
class ISessionStore(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISessionStoreProxy

    @jsii.member(jsii_name="exists")
    def exists(self, name: str) -> bool:
        ...

    @jsii.member(jsii_name="list")
    def list(self) -> typing.List[str]:
        ...

    @jsii.member(jsii_name="lock")
    def lock(self) -> None:
        ...

    @jsii.member(jsii_name="mkdir")
    def mkdir(self, directory_name: str) -> str:
        ...

    @jsii.member(jsii_name="readdir")
    def readdir(self, directory_name: str) -> typing.List[str]:
        ...

    @jsii.member(jsii_name="readFile")
    def read_file(self, file_name: str) -> typing.Any:
        ...

    @jsii.member(jsii_name="readJson")
    def read_json(self, file_name: str) -> typing.Any:
        ...

    @jsii.member(jsii_name="writeFile")
    def write_file(self, artifact_name: str, data: typing.Any) -> None:
        ...

    @jsii.member(jsii_name="writeJson")
    def write_json(self, artifact_name: str, json: typing.Any) -> None:
        ...


class _ISessionStoreProxy():
    __jsii_type__ = "@aws-cdk/cdk.ISessionStore"
    @jsii.member(jsii_name="exists")
    def exists(self, name: str) -> bool:
        return jsii.invoke(self, "exists", [name])

    @jsii.member(jsii_name="list")
    def list(self) -> typing.List[str]:
        return jsii.invoke(self, "list", [])

    @jsii.member(jsii_name="lock")
    def lock(self) -> None:
        return jsii.invoke(self, "lock", [])

    @jsii.member(jsii_name="mkdir")
    def mkdir(self, directory_name: str) -> str:
        return jsii.invoke(self, "mkdir", [directory_name])

    @jsii.member(jsii_name="readdir")
    def readdir(self, directory_name: str) -> typing.List[str]:
        return jsii.invoke(self, "readdir", [directory_name])

    @jsii.member(jsii_name="readFile")
    def read_file(self, file_name: str) -> typing.Any:
        return jsii.invoke(self, "readFile", [file_name])

    @jsii.member(jsii_name="readJson")
    def read_json(self, file_name: str) -> typing.Any:
        return jsii.invoke(self, "readJson", [file_name])

    @jsii.member(jsii_name="writeFile")
    def write_file(self, artifact_name: str, data: typing.Any) -> None:
        return jsii.invoke(self, "writeFile", [artifact_name, data])

    @jsii.member(jsii_name="writeJson")
    def write_json(self, artifact_name: str, json: typing.Any) -> None:
        return jsii.invoke(self, "writeJson", [artifact_name, json])


@jsii.implements(ISessionStore)
class FileSystemStore(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.FileSystemStore"):
    def __init__(self, *, outdir: str) -> None:
        options: FileSystemStoreOptions = {"outdir": outdir}

        jsii.create(FileSystemStore, self, [options])

    @jsii.member(jsii_name="exists")
    def exists(self, name: str) -> bool:
        return jsii.invoke(self, "exists", [name])

    @jsii.member(jsii_name="list")
    def list(self) -> typing.List[str]:
        return jsii.invoke(self, "list", [])

    @jsii.member(jsii_name="lock")
    def lock(self) -> None:
        return jsii.invoke(self, "lock", [])

    @jsii.member(jsii_name="mkdir")
    def mkdir(self, directory_name: str) -> str:
        return jsii.invoke(self, "mkdir", [directory_name])

    @jsii.member(jsii_name="readdir")
    def readdir(self, directory_name: str) -> typing.List[str]:
        return jsii.invoke(self, "readdir", [directory_name])

    @jsii.member(jsii_name="readFile")
    def read_file(self, file_name: str) -> typing.Any:
        return jsii.invoke(self, "readFile", [file_name])

    @jsii.member(jsii_name="readJson")
    def read_json(self, file_name: str) -> typing.Any:
        return jsii.invoke(self, "readJson", [file_name])

    @jsii.member(jsii_name="writeFile")
    def write_file(self, file_name: str, data: typing.Any) -> None:
        return jsii.invoke(self, "writeFile", [file_name, data])

    @jsii.member(jsii_name="writeJson")
    def write_json(self, file_name: str, json: typing.Any) -> None:
        return jsii.invoke(self, "writeJson", [file_name, json])


@jsii.interface(jsii_type="@aws-cdk/cdk.ISynthesisSession")
class ISynthesisSession(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISynthesisSessionProxy

    @property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> aws_cdk.cx_api.AssemblyManifest:
        ...

    @property
    @jsii.member(jsii_name="store")
    def store(self) -> "ISessionStore":
        ...

    @jsii.member(jsii_name="addArtifact")
    def add_artifact(self, id: str, *, environment: str, type: aws_cdk.cx_api.ArtifactType, auto_deploy: typing.Optional[bool]=None, dependencies: typing.Optional[typing.List[str]]=None, metadata: typing.Optional[typing.Mapping[str,typing.Any]]=None, missing: typing.Optional[typing.Mapping[str,typing.Any]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        ...

    @jsii.member(jsii_name="addBuildStep")
    def add_build_step(self, id: str, *, parameters: typing.Mapping[str,typing.Any], type: str, depends: typing.Optional[typing.List[str]]=None) -> None:
        ...

    @jsii.member(jsii_name="getArtifact")
    def get_artifact(self, id: str) -> aws_cdk.cx_api.Artifact:
        ...

    @jsii.member(jsii_name="tryGetArtifact")
    def try_get_artifact(self, id: str) -> typing.Optional[aws_cdk.cx_api.Artifact]:
        ...


class _ISynthesisSessionProxy():
    __jsii_type__ = "@aws-cdk/cdk.ISynthesisSession"
    @property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> aws_cdk.cx_api.AssemblyManifest:
        return jsii.get(self, "manifest")

    @property
    @jsii.member(jsii_name="store")
    def store(self) -> "ISessionStore":
        return jsii.get(self, "store")

    @jsii.member(jsii_name="addArtifact")
    def add_artifact(self, id: str, *, environment: str, type: aws_cdk.cx_api.ArtifactType, auto_deploy: typing.Optional[bool]=None, dependencies: typing.Optional[typing.List[str]]=None, metadata: typing.Optional[typing.Mapping[str,typing.Any]]=None, missing: typing.Optional[typing.Mapping[str,typing.Any]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        droplet: aws_cdk.cx_api.Artifact = {"environment": environment, "type": type}

        if auto_deploy is not None:
            droplet["autoDeploy"] = auto_deploy

        if dependencies is not None:
            droplet["dependencies"] = dependencies

        if metadata is not None:
            droplet["metadata"] = metadata

        if missing is not None:
            droplet["missing"] = missing

        if properties is not None:
            droplet["properties"] = properties

        return jsii.invoke(self, "addArtifact", [id, droplet])

    @jsii.member(jsii_name="addBuildStep")
    def add_build_step(self, id: str, *, parameters: typing.Mapping[str,typing.Any], type: str, depends: typing.Optional[typing.List[str]]=None) -> None:
        step: aws_cdk.cx_api.BuildStep = {"parameters": parameters, "type": type}

        if depends is not None:
            step["depends"] = depends

        return jsii.invoke(self, "addBuildStep", [id, step])

    @jsii.member(jsii_name="getArtifact")
    def get_artifact(self, id: str) -> aws_cdk.cx_api.Artifact:
        return jsii.invoke(self, "getArtifact", [id])

    @jsii.member(jsii_name="tryGetArtifact")
    def try_get_artifact(self, id: str) -> typing.Optional[aws_cdk.cx_api.Artifact]:
        return jsii.invoke(self, "tryGetArtifact", [id])


@jsii.interface(jsii_type="@aws-cdk/cdk.ISynthesizable")
class ISynthesizable(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISynthesizableProxy

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: "ISynthesisSession") -> None:
        ...


class _ISynthesizableProxy():
    __jsii_type__ = "@aws-cdk/cdk.ISynthesizable"
    @jsii.member(jsii_name="synthesize")
    def synthesize(self, session: "ISynthesisSession") -> None:
        return jsii.invoke(self, "synthesize", [session])


@jsii.interface(jsii_type="@aws-cdk/cdk.ITaggable")
class ITaggable(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ITaggableProxy

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TagManager":
        ...


class _ITaggableProxy():
    __jsii_type__ = "@aws-cdk/cdk.ITaggable"
    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "TagManager":
        return jsii.get(self, "tags")


@jsii.interface(jsii_type="@aws-cdk/cdk.ITemplateOptions")
class ITemplateOptions(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ITemplateOptionsProxy

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        ...

    @description.setter
    def description(self, value: typing.Optional[str]):
        ...

    @property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        ...

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str,typing.Any]]):
        ...

    @property
    @jsii.member(jsii_name="templateFormatVersion")
    def template_format_version(self) -> typing.Optional[str]:
        ...

    @template_format_version.setter
    def template_format_version(self, value: typing.Optional[str]):
        ...

    @property
    @jsii.member(jsii_name="transform")
    def transform(self) -> typing.Optional[str]:
        ...

    @transform.setter
    def transform(self, value: typing.Optional[str]):
        ...


class _ITemplateOptionsProxy():
    __jsii_type__ = "@aws-cdk/cdk.ITemplateOptions"
    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        return jsii.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: typing.Optional[typing.Mapping[str,typing.Any]]):
        return jsii.set(self, "metadata", value)

    @property
    @jsii.member(jsii_name="templateFormatVersion")
    def template_format_version(self) -> typing.Optional[str]:
        return jsii.get(self, "templateFormatVersion")

    @template_format_version.setter
    def template_format_version(self, value: typing.Optional[str]):
        return jsii.set(self, "templateFormatVersion", value)

    @property
    @jsii.member(jsii_name="transform")
    def transform(self) -> typing.Optional[str]:
        return jsii.get(self, "transform")

    @transform.setter
    def transform(self, value: typing.Optional[str]):
        return jsii.set(self, "transform", value)


@jsii.implements(ISessionStore)
class InMemoryStore(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.InMemoryStore"):
    def __init__(self) -> None:
        jsii.create(InMemoryStore, self, [])

    @jsii.member(jsii_name="exists")
    def exists(self, name: str) -> bool:
        return jsii.invoke(self, "exists", [name])

    @jsii.member(jsii_name="list")
    def list(self) -> typing.List[str]:
        return jsii.invoke(self, "list", [])

    @jsii.member(jsii_name="lock")
    def lock(self) -> None:
        return jsii.invoke(self, "lock", [])

    @jsii.member(jsii_name="mkdir")
    def mkdir(self, directory_name: str) -> str:
        return jsii.invoke(self, "mkdir", [directory_name])

    @jsii.member(jsii_name="readdir")
    def readdir(self, directory_name: str) -> typing.List[str]:
        return jsii.invoke(self, "readdir", [directory_name])

    @jsii.member(jsii_name="readFile")
    def read_file(self, file_name: str) -> typing.Any:
        return jsii.invoke(self, "readFile", [file_name])

    @jsii.member(jsii_name="readJson")
    def read_json(self, file_name: str) -> typing.Any:
        return jsii.invoke(self, "readJson", [file_name])

    @jsii.member(jsii_name="writeFile")
    def write_file(self, file_name: str, data: typing.Any) -> None:
        return jsii.invoke(self, "writeFile", [file_name, data])

    @jsii.member(jsii_name="writeJson")
    def write_json(self, file_name: str, json: typing.Any) -> None:
        return jsii.invoke(self, "writeJson", [file_name, json])


class Include(CfnElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Include"):
    def __init__(self, scope: "Construct", id: str, *, template: typing.Mapping[typing.Any, typing.Any]) -> None:
        props: IncludeProps = {"template": template}

        jsii.create(Include, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="template")
    def template(self) -> typing.Mapping[typing.Any, typing.Any]:
        return jsii.get(self, "template")


@jsii.data_type(jsii_type="@aws-cdk/cdk.IncludeProps")
class IncludeProps(jsii.compat.TypedDict):
    template: typing.Mapping[typing.Any, typing.Any]

class LogicalIDs(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.LogicalIDs"):
    def __init__(self, naming_scheme: "IAddressingScheme") -> None:
        jsii.create(LogicalIDs, self, [naming_scheme])

    @jsii.member(jsii_name="assertAllRenamesApplied")
    def assert_all_renames_applied(self) -> None:
        return jsii.invoke(self, "assertAllRenamesApplied", [])

    @jsii.member(jsii_name="getLogicalId")
    def get_logical_id(self, cfn_element: "CfnElement") -> str:
        return jsii.invoke(self, "getLogicalId", [cfn_element])

    @jsii.member(jsii_name="renameLogical")
    def rename_logical(self, old_id: str, new_id: str) -> None:
        return jsii.invoke(self, "renameLogical", [old_id, new_id])

    @property
    @jsii.member(jsii_name="namingScheme")
    def naming_scheme(self) -> "IAddressingScheme":
        return jsii.get(self, "namingScheme")


@jsii.data_type(jsii_type="@aws-cdk/cdk.ManifestOptions")
class ManifestOptions(jsii.compat.TypedDict, total=False):
    legacyManifest: bool
    runtimeInformation: bool

class _MetadataEntry(jsii.compat.TypedDict, total=False):
    data: typing.Any

@jsii.data_type(jsii_type="@aws-cdk/cdk.MetadataEntry")
class MetadataEntry(_MetadataEntry):
    trace: typing.List[str]
    type: str

@jsii.data_type(jsii_type="@aws-cdk/cdk.OutgoingReference")
class OutgoingReference(jsii.compat.TypedDict):
    reference: "Reference"
    source: "IConstruct"

@jsii.enum(jsii_type="@aws-cdk/cdk.RemovalPolicy")
class RemovalPolicy(enum.Enum):
    Destroy = "Destroy"
    Orphan = "Orphan"
    Forbid = "Forbid"

@jsii.data_type(jsii_type="@aws-cdk/cdk.ResolveContext")
class ResolveContext(jsii.compat.TypedDict):
    prefix: typing.List[str]
    scope: "IConstruct"

@jsii.data_type(jsii_type="@aws-cdk/cdk.ResourceSignal")
class ResourceSignal(jsii.compat.TypedDict, total=False):
    count: jsii.Number
    timeout: str

class Root(Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Root"):
    def __init__(self) -> None:
        jsii.create(Root, self, [])


class App(Root, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.App"):
    def __init__(self, *, auto_run: typing.Optional[bool]=None, context: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        props: AppProps = {}

        if auto_run is not None:
            props["autoRun"] = auto_run

        if context is not None:
            props["context"] = context

        jsii.create(App, self, [props])

    @jsii.member(jsii_name="run")
    def run(self) -> "ISynthesisSession":
        return jsii.invoke(self, "run", [])

    @jsii.member(jsii_name="synthesizeStack")
    def synthesize_stack(self, stack_name: str) -> aws_cdk.cx_api.SynthesizedStack:
        return jsii.invoke(self, "synthesizeStack", [stack_name])

    @jsii.member(jsii_name="synthesizeStacks")
    def synthesize_stacks(self, stack_names: typing.List[str]) -> typing.List[aws_cdk.cx_api.SynthesizedStack]:
        return jsii.invoke(self, "synthesizeStacks", [stack_names])


@jsii.data_type(jsii_type="@aws-cdk/cdk.RuleAssertion")
class RuleAssertion(jsii.compat.TypedDict):
    assert_: "ICfnConditionExpression"
    assertDescription: str

class SSMParameterProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.SSMParameterProvider"):
    def __init__(self, context: "Construct", *, parameter_name: str) -> None:
        props: SSMParameterProviderProps = {"parameterName": parameter_name}

        jsii.create(SSMParameterProvider, self, [context, props])

    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self, default_value: typing.Optional[str]=None) -> typing.Any:
        return jsii.invoke(self, "parameterValue", [default_value])


@jsii.data_type(jsii_type="@aws-cdk/cdk.SSMParameterProviderProps")
class SSMParameterProviderProps(jsii.compat.TypedDict):
    parameterName: str

class ScopedAws(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.ScopedAws"):
    def __init__(self, scope: "Construct") -> None:
        jsii.create(ScopedAws, self, [scope])

    @property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> str:
        return jsii.get(self, "accountId")

    @property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.List[str]:
        return jsii.get(self, "notificationArns")

    @property
    @jsii.member(jsii_name="partition")
    def partition(self) -> str:
        return jsii.get(self, "partition")

    @property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        return jsii.get(self, "region")

    @property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "Construct":
        return jsii.get(self, "scope")

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        return jsii.get(self, "stackId")

    @property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        return jsii.get(self, "stackName")

    @property
    @jsii.member(jsii_name="urlSuffix")
    def url_suffix(self) -> str:
        return jsii.get(self, "urlSuffix")


@jsii.data_type(jsii_type="@aws-cdk/cdk.SecretsManagerSecretOptions")
class SecretsManagerSecretOptions(jsii.compat.TypedDict, total=False):
    jsonField: str
    versionId: str
    versionStage: str

class Stack(Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Stack"):
    def __init__(self, scope: typing.Optional["Construct"]=None, name: typing.Optional[str]=None, *, auto_deploy: typing.Optional[bool]=None, env: typing.Optional["Environment"]=None, naming_scheme: typing.Optional["IAddressingScheme"]=None, stack_name: typing.Optional[str]=None) -> None:
        props: StackProps = {}

        if auto_deploy is not None:
            props["autoDeploy"] = auto_deploy

        if env is not None:
            props["env"] = env

        if naming_scheme is not None:
            props["namingScheme"] = naming_scheme

        if stack_name is not None:
            props["stackName"] = stack_name

        jsii.create(Stack, self, [scope, name, props])

    @jsii.member(jsii_name="annotatePhysicalName")
    @classmethod
    def annotate_physical_name(cls, construct: "Construct", physical_name: typing.Optional[str]=None) -> None:
        return jsii.sinvoke(cls, "annotatePhysicalName", [construct, physical_name])

    @jsii.member(jsii_name="isStack")
    @classmethod
    def is_stack(cls, x: typing.Any) -> bool:
        return jsii.sinvoke(cls, "isStack", [x])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, stack: "Stack", reason: typing.Optional[str]=None) -> None:
        return jsii.invoke(self, "addDependency", [stack, reason])

    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Stack"]:
        return jsii.invoke(self, "dependencies", [])

    @jsii.member(jsii_name="findResource")
    def find_resource(self, path: str) -> typing.Optional["CfnResource"]:
        return jsii.invoke(self, "findResource", [path])

    @jsii.member(jsii_name="formatArn")
    def format_arn(self, *, resource: str, service: str, account: typing.Optional[str]=None, partition: typing.Optional[str]=None, region: typing.Optional[str]=None, resource_name: typing.Optional[str]=None, sep: typing.Optional[str]=None) -> str:
        components: ArnComponents = {"resource": resource, "service": service}

        if account is not None:
            components["account"] = account

        if partition is not None:
            components["partition"] = partition

        if region is not None:
            components["region"] = region

        if resource_name is not None:
            components["resourceName"] = resource_name

        if sep is not None:
            components["sep"] = sep

        return jsii.invoke(self, "formatArn", [components])

    @jsii.member(jsii_name="parentApp")
    def parent_app(self) -> typing.Optional["App"]:
        return jsii.invoke(self, "parentApp", [])

    @jsii.member(jsii_name="parseArn")
    def parse_arn(self, arn: str, sep_if_token: typing.Optional[str]=None, has_name: typing.Optional[bool]=None) -> "ArnComponents":
        return jsii.invoke(self, "parseArn", [arn, sep_if_token, has_name])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        return jsii.invoke(self, "prepare", [])

    @jsii.member(jsii_name="renameLogical")
    def rename_logical(self, old_id: str, new_id: str) -> None:
        return jsii.invoke(self, "renameLogical", [old_id, new_id])

    @jsii.member(jsii_name="reportMissingContext")
    def report_missing_context(self, key: str, *, props: typing.Mapping[str,typing.Any], provider: str) -> None:
        details: aws_cdk.cx_api.MissingContext = {"props": props, "provider": provider}

        return jsii.invoke(self, "reportMissingContext", [key, details])

    @jsii.member(jsii_name="requireAccountId")
    def require_account_id(self, why: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "requireAccountId", [why])

    @jsii.member(jsii_name="requireRegion")
    def require_region(self, why: typing.Optional[str]=None) -> str:
        return jsii.invoke(self, "requireRegion", [why])

    @jsii.member(jsii_name="setParameterValue")
    def set_parameter_value(self, parameter: "CfnParameter", value: str) -> None:
        return jsii.invoke(self, "setParameterValue", [parameter, value])

    @jsii.member(jsii_name="synthesize")
    def _synthesize(self, session: "ISynthesisSession") -> None:
        return jsii.invoke(self, "synthesize", [session])

    @property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> str:
        return jsii.get(self, "accountId")

    @property
    @jsii.member(jsii_name="autoDeploy")
    def auto_deploy(self) -> bool:
        return jsii.get(self, "autoDeploy")

    @property
    @jsii.member(jsii_name="env")
    def env(self) -> "Environment":
        return jsii.get(self, "env")

    @property
    @jsii.member(jsii_name="environment")
    def environment(self) -> str:
        return jsii.get(self, "environment")

    @property
    @jsii.member(jsii_name="logicalIds")
    def logical_ids(self) -> "LogicalIDs":
        return jsii.get(self, "logicalIds")

    @property
    @jsii.member(jsii_name="missingContext")
    def missing_context(self) -> typing.Mapping[str,aws_cdk.cx_api.MissingContext]:
        return jsii.get(self, "missingContext")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.List[str]:
        return jsii.get(self, "notificationArns")

    @property
    @jsii.member(jsii_name="partition")
    def partition(self) -> str:
        return jsii.get(self, "partition")

    @property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        return jsii.get(self, "region")

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        return jsii.get(self, "stackId")

    @property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        return jsii.get(self, "stackName")

    @property
    @jsii.member(jsii_name="templateOptions")
    def template_options(self) -> "ITemplateOptions":
        return jsii.get(self, "templateOptions")

    @property
    @jsii.member(jsii_name="urlSuffix")
    def url_suffix(self) -> str:
        return jsii.get(self, "urlSuffix")


@jsii.data_type(jsii_type="@aws-cdk/cdk.StackProps")
class StackProps(jsii.compat.TypedDict, total=False):
    autoDeploy: bool
    env: "Environment"
    namingScheme: "IAddressingScheme"
    stackName: str

class StringListCfnOutput(Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.StringListCfnOutput"):
    def __init__(self, scope: "Construct", id: str, *, values: typing.List[typing.Any], condition: typing.Optional["CfnCondition"]=None, description: typing.Optional[str]=None, disable_export: typing.Optional[bool]=None, export: typing.Optional[str]=None, separator: typing.Optional[str]=None) -> None:
        props: StringListCfnOutputProps = {"values": values}

        if condition is not None:
            props["condition"] = condition

        if description is not None:
            props["description"] = description

        if disable_export is not None:
            props["disableExport"] = disable_export

        if export is not None:
            props["export"] = export

        if separator is not None:
            props["separator"] = separator

        jsii.create(StringListCfnOutput, self, [scope, id, props])

    @jsii.member(jsii_name="makeImportValues")
    def make_import_values(self) -> typing.List[str]:
        return jsii.invoke(self, "makeImportValues", [])

    @property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return jsii.get(self, "length")


class _StringListCfnOutputProps(jsii.compat.TypedDict, total=False):
    condition: "CfnCondition"
    description: str
    disableExport: bool
    export: str
    separator: str

@jsii.data_type(jsii_type="@aws-cdk/cdk.StringListCfnOutputProps")
class StringListCfnOutputProps(_StringListCfnOutputProps):
    values: typing.List[typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/cdk.SynthesisOptions")
class SynthesisOptions(ManifestOptions, jsii.compat.TypedDict, total=False):
    skipValidation: bool
    store: "ISessionStore"

@jsii.implements(ISynthesisSession)
class SynthesisSession(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.SynthesisSession"):
    def __init__(self, *, skip_validation: typing.Optional[bool]=None, store: typing.Optional["ISessionStore"]=None, legacy_manifest: typing.Optional[bool]=None, runtime_information: typing.Optional[bool]=None) -> None:
        options: SynthesisOptions = {}

        if skip_validation is not None:
            options["skipValidation"] = skip_validation

        if store is not None:
            options["store"] = store

        if legacy_manifest is not None:
            options["legacyManifest"] = legacy_manifest

        if runtime_information is not None:
            options["runtimeInformation"] = runtime_information

        jsii.create(SynthesisSession, self, [options])

    @jsii.member(jsii_name="isSynthesizable")
    @classmethod
    def is_synthesizable(cls, obj: typing.Any) -> bool:
        return jsii.sinvoke(cls, "isSynthesizable", [obj])

    @jsii.member(jsii_name="addArtifact")
    def add_artifact(self, id: str, *, environment: str, type: aws_cdk.cx_api.ArtifactType, auto_deploy: typing.Optional[bool]=None, dependencies: typing.Optional[typing.List[str]]=None, metadata: typing.Optional[typing.Mapping[str,typing.Any]]=None, missing: typing.Optional[typing.Mapping[str,typing.Any]]=None, properties: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        artifact: aws_cdk.cx_api.Artifact = {"environment": environment, "type": type}

        if auto_deploy is not None:
            artifact["autoDeploy"] = auto_deploy

        if dependencies is not None:
            artifact["dependencies"] = dependencies

        if metadata is not None:
            artifact["metadata"] = metadata

        if missing is not None:
            artifact["missing"] = missing

        if properties is not None:
            artifact["properties"] = properties

        return jsii.invoke(self, "addArtifact", [id, artifact])

    @jsii.member(jsii_name="addBuildStep")
    def add_build_step(self, id: str, *, parameters: typing.Mapping[str,typing.Any], type: str, depends: typing.Optional[typing.List[str]]=None) -> None:
        step: aws_cdk.cx_api.BuildStep = {"parameters": parameters, "type": type}

        if depends is not None:
            step["depends"] = depends

        return jsii.invoke(self, "addBuildStep", [id, step])

    @jsii.member(jsii_name="close")
    def close(self, *, legacy_manifest: typing.Optional[bool]=None, runtime_information: typing.Optional[bool]=None) -> aws_cdk.cx_api.AssemblyManifest:
        options: ManifestOptions = {}

        if legacy_manifest is not None:
            options["legacyManifest"] = legacy_manifest

        if runtime_information is not None:
            options["runtimeInformation"] = runtime_information

        return jsii.invoke(self, "close", [options])

    @jsii.member(jsii_name="getArtifact")
    def get_artifact(self, id: str) -> aws_cdk.cx_api.Artifact:
        return jsii.invoke(self, "getArtifact", [id])

    @jsii.member(jsii_name="tryGetArtifact")
    def try_get_artifact(self, id: str) -> typing.Optional[aws_cdk.cx_api.Artifact]:
        return jsii.invoke(self, "tryGetArtifact", [id])

    @property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> aws_cdk.cx_api.AssemblyManifest:
        return jsii.get(self, "manifest")

    @property
    @jsii.member(jsii_name="store")
    def store(self) -> "ISessionStore":
        return jsii.get(self, "store")


class Synthesizer(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Synthesizer"):
    def __init__(self) -> None:
        jsii.create(Synthesizer, self, [])

    @jsii.member(jsii_name="synthesize")
    def synthesize(self, root: "IConstruct", *, skip_validation: typing.Optional[bool]=None, store: typing.Optional["ISessionStore"]=None, legacy_manifest: typing.Optional[bool]=None, runtime_information: typing.Optional[bool]=None) -> "ISynthesisSession":
        options: SynthesisOptions = {}

        if skip_validation is not None:
            options["skipValidation"] = skip_validation

        if store is not None:
            options["store"] = store

        if legacy_manifest is not None:
            options["legacyManifest"] = legacy_manifest

        if runtime_information is not None:
            options["runtimeInformation"] = runtime_information

        return jsii.invoke(self, "synthesize", [root, options])


@jsii.implements(IAspect)
class TagBase(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/cdk.TagBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _TagBaseProxy

    def __init__(self, key: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        props: TagProps = {}

        if apply_to_launched_instances is not None:
            props["applyToLaunchedInstances"] = apply_to_launched_instances

        if exclude_resource_types is not None:
            props["excludeResourceTypes"] = exclude_resource_types

        if include_resource_types is not None:
            props["includeResourceTypes"] = include_resource_types

        if priority is not None:
            props["priority"] = priority

        jsii.create(TagBase, self, [key, props])

    @jsii.member(jsii_name="applyTag")
    @abc.abstractmethod
    def _apply_tag(self, resource: "ITaggable") -> None:
        ...

    @jsii.member(jsii_name="visit")
    def visit(self, construct: "IConstruct") -> None:
        return jsii.invoke(self, "visit", [construct])

    @property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        return jsii.get(self, "key")

    @property
    @jsii.member(jsii_name="props")
    def _props(self) -> "TagProps":
        return jsii.get(self, "props")


class _TagBaseProxy(TagBase):
    @jsii.member(jsii_name="applyTag")
    def _apply_tag(self, resource: "ITaggable") -> None:
        return jsii.invoke(self, "applyTag", [resource])


class RemoveTag(TagBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.RemoveTag"):
    def __init__(self, key: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        props: TagProps = {}

        if apply_to_launched_instances is not None:
            props["applyToLaunchedInstances"] = apply_to_launched_instances

        if exclude_resource_types is not None:
            props["excludeResourceTypes"] = exclude_resource_types

        if include_resource_types is not None:
            props["includeResourceTypes"] = include_resource_types

        if priority is not None:
            props["priority"] = priority

        jsii.create(RemoveTag, self, [key, props])

    @jsii.member(jsii_name="applyTag")
    def _apply_tag(self, resource: "ITaggable") -> None:
        return jsii.invoke(self, "applyTag", [resource])


class Tag(TagBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Tag"):
    def __init__(self, key: str, value: str, *, apply_to_launched_instances: typing.Optional[bool]=None, exclude_resource_types: typing.Optional[typing.List[str]]=None, include_resource_types: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        props: TagProps = {}

        if apply_to_launched_instances is not None:
            props["applyToLaunchedInstances"] = apply_to_launched_instances

        if exclude_resource_types is not None:
            props["excludeResourceTypes"] = exclude_resource_types

        if include_resource_types is not None:
            props["includeResourceTypes"] = include_resource_types

        if priority is not None:
            props["priority"] = priority

        jsii.create(Tag, self, [key, value, props])

    @jsii.member(jsii_name="applyTag")
    def _apply_tag(self, resource: "ITaggable") -> None:
        return jsii.invoke(self, "applyTag", [resource])

    @property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        return jsii.get(self, "value")


class TagManager(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.TagManager"):
    def __init__(self, tag_type: "TagType", resource_type_name: str, tag_structure: typing.Any=None) -> None:
        jsii.create(TagManager, self, [tag_type, resource_type_name, tag_structure])

    @jsii.member(jsii_name="applyTagAspectHere")
    def apply_tag_aspect_here(self, include: typing.Optional[typing.List[str]]=None, exclude: typing.Optional[typing.List[str]]=None) -> bool:
        return jsii.invoke(self, "applyTagAspectHere", [include, exclude])

    @jsii.member(jsii_name="removeTag")
    def remove_tag(self, key: str, priority: jsii.Number) -> None:
        return jsii.invoke(self, "removeTag", [key, priority])

    @jsii.member(jsii_name="renderTags")
    def render_tags(self) -> typing.Any:
        return jsii.invoke(self, "renderTags", [])

    @jsii.member(jsii_name="setTag")
    def set_tag(self, key: str, value: str, priority: typing.Optional[jsii.Number]=None, apply_to_launched_instances: typing.Optional[bool]=None) -> None:
        return jsii.invoke(self, "setTag", [key, value, priority, apply_to_launched_instances])


@jsii.data_type(jsii_type="@aws-cdk/cdk.TagProps")
class TagProps(jsii.compat.TypedDict, total=False):
    applyToLaunchedInstances: bool
    excludeResourceTypes: typing.List[str]
    includeResourceTypes: typing.List[str]
    priority: jsii.Number

@jsii.enum(jsii_type="@aws-cdk/cdk.TagType")
class TagType(enum.Enum):
    Standard = "Standard"
    AutoScalingGroup = "AutoScalingGroup"
    Map = "Map"
    NotTaggable = "NotTaggable"

class Token(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Token"):
    def __init__(self, value_or_function: typing.Any=None, display_name: typing.Optional[str]=None) -> None:
        jsii.create(Token, self, [value_or_function, display_name])

    @jsii.member(jsii_name="unresolved")
    @classmethod
    def unresolved(cls, obj: typing.Any) -> bool:
        return jsii.sinvoke(cls, "unresolved", [obj])

    @jsii.member(jsii_name="resolve")
    def resolve(self, *, prefix: typing.List[str], scope: "IConstruct") -> typing.Any:
        _context: ResolveContext = {"prefix": prefix, "scope": scope}

        return jsii.invoke(self, "resolve", [_context])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toList")
    def to_list(self) -> typing.List[str]:
        return jsii.invoke(self, "toList", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[str]:
        return jsii.get(self, "displayName")

    @property
    @jsii.member(jsii_name="valueOrFunction")
    def value_or_function(self) -> typing.Any:
        return jsii.get(self, "valueOrFunction")


class CfnDynamicReference(Token, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CfnDynamicReference"):
    def __init__(self, service: "CfnDynamicReferenceService", key: str) -> None:
        jsii.create(CfnDynamicReference, self, [service, key])


class Reference(Token, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.Reference"):
    def __init__(self, value: typing.Any, display_name: str, target: "Construct") -> None:
        jsii.create(Reference, self, [value, display_name, target])

    @jsii.member(jsii_name="isReference")
    @classmethod
    def is_reference(cls, x: "Token") -> bool:
        return jsii.sinvoke(cls, "isReference", [x])

    @property
    @jsii.member(jsii_name="target")
    def target(self) -> "Construct":
        return jsii.get(self, "target")


class CfnReference(Reference, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.CfnReference"):
    def __init__(self, value: typing.Any, display_name: str, target: "Construct") -> None:
        jsii.create(CfnReference, self, [value, display_name, target])

    @jsii.member(jsii_name="isCfnReference")
    @classmethod
    def is_cfn_reference(cls, x: "Token") -> bool:
        return jsii.sinvoke(cls, "isCfnReference", [x])

    @jsii.member(jsii_name="consumeFromStack")
    def consume_from_stack(self, consuming_stack: "Stack", consuming_construct: "IConstruct") -> None:
        return jsii.invoke(self, "consumeFromStack", [consuming_stack, consuming_construct])

    @jsii.member(jsii_name="resolve")
    def resolve(self, *, prefix: typing.List[str], scope: "IConstruct") -> typing.Any:
        context: ResolveContext = {"prefix": prefix, "scope": scope}

        return jsii.invoke(self, "resolve", [context])


class SecretValue(Token, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.SecretValue"):
    def __init__(self, value_or_function: typing.Any=None, display_name: typing.Optional[str]=None) -> None:
        jsii.create(SecretValue, self, [value_or_function, display_name])

    @jsii.member(jsii_name="cfnDynamicReference")
    @classmethod
    def cfn_dynamic_reference(cls, ref: "CfnDynamicReference") -> "SecretValue":
        return jsii.sinvoke(cls, "cfnDynamicReference", [ref])

    @jsii.member(jsii_name="cfnParameter")
    @classmethod
    def cfn_parameter(cls, param: "CfnParameter") -> "SecretValue":
        return jsii.sinvoke(cls, "cfnParameter", [param])

    @jsii.member(jsii_name="plainText")
    @classmethod
    def plain_text(cls, secret: str) -> "SecretValue":
        return jsii.sinvoke(cls, "plainText", [secret])

    @jsii.member(jsii_name="secretsManager")
    @classmethod
    def secrets_manager(cls, secret_id: str, *, json_field: typing.Optional[str]=None, version_id: typing.Optional[str]=None, version_stage: typing.Optional[str]=None) -> "SecretValue":
        options: SecretsManagerSecretOptions = {}

        if json_field is not None:
            options["jsonField"] = json_field

        if version_id is not None:
            options["versionId"] = version_id

        if version_stage is not None:
            options["versionStage"] = version_stage

        return jsii.sinvoke(cls, "secretsManager", [secret_id, options])

    @jsii.member(jsii_name="ssmSecure")
    @classmethod
    def ssm_secure(cls, parameter_name: str, version: str) -> "SecretValue":
        return jsii.sinvoke(cls, "ssmSecure", [parameter_name, version])


@jsii.data_type(jsii_type="@aws-cdk/cdk.UpdatePolicy")
class UpdatePolicy(jsii.compat.TypedDict, total=False):
    autoScalingReplacingUpdate: "AutoScalingReplacingUpdate"
    autoScalingRollingUpdate: "AutoScalingRollingUpdate"
    autoScalingScheduledAction: "AutoScalingScheduledAction"
    codeDeployLambdaAliasUpdate: "CodeDeployLambdaAliasUpdate"
    useOnlineResharding: bool

class ValidationError(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.ValidationError"):
    def __init__(self, source: "IConstruct", message: str) -> None:
        jsii.create(ValidationError, self, [source, message])

    @property
    @jsii.member(jsii_name="message")
    def message(self) -> str:
        return jsii.get(self, "message")

    @property
    @jsii.member(jsii_name="source")
    def source(self) -> "IConstruct":
        return jsii.get(self, "source")


class ValidationResult(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.ValidationResult"):
    def __init__(self, error_message: typing.Optional[str]=None, results: typing.Optional["ValidationResults"]=None) -> None:
        jsii.create(ValidationResult, self, [error_message, results])

    @jsii.member(jsii_name="assertSuccess")
    def assert_success(self) -> None:
        return jsii.invoke(self, "assertSuccess", [])

    @jsii.member(jsii_name="errorTree")
    def error_tree(self) -> str:
        return jsii.invoke(self, "errorTree", [])

    @jsii.member(jsii_name="prefix")
    def prefix(self, message: str) -> "ValidationResult":
        return jsii.invoke(self, "prefix", [message])

    @property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> str:
        return jsii.get(self, "errorMessage")

    @property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> bool:
        return jsii.get(self, "isSuccess")

    @property
    @jsii.member(jsii_name="results")
    def results(self) -> "ValidationResults":
        return jsii.get(self, "results")


class ValidationResults(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cdk.ValidationResults"):
    def __init__(self, results: typing.Optional[typing.List["ValidationResult"]]=None) -> None:
        jsii.create(ValidationResults, self, [results])

    @jsii.member(jsii_name="collect")
    def collect(self, result: "ValidationResult") -> None:
        return jsii.invoke(self, "collect", [result])

    @jsii.member(jsii_name="errorTreeList")
    def error_tree_list(self) -> str:
        return jsii.invoke(self, "errorTreeList", [])

    @jsii.member(jsii_name="wrap")
    def wrap(self, message: str) -> "ValidationResult":
        return jsii.invoke(self, "wrap", [message])

    @property
    @jsii.member(jsii_name="isSuccess")
    def is_success(self) -> bool:
        return jsii.get(self, "isSuccess")

    @property
    @jsii.member(jsii_name="results")
    def results(self) -> typing.List["ValidationResult"]:
        return jsii.get(self, "results")

    @results.setter
    def results(self, value: typing.List["ValidationResult"]):
        return jsii.set(self, "results", value)


__all__ = ["App", "AppProps", "ArnComponents", "AutoScalingCreationPolicy", "AutoScalingReplacingUpdate", "AutoScalingRollingUpdate", "AutoScalingScheduledAction", "AvailabilityZoneProvider", "Aws", "CfnCondition", "CfnConditionProps", "CfnDynamicReference", "CfnDynamicReferenceService", "CfnElement", "CfnMapping", "CfnMappingProps", "CfnOutput", "CfnOutputProps", "CfnParameter", "CfnParameterProps", "CfnRefElement", "CfnReference", "CfnResource", "CfnResourceProps", "CfnRule", "CfnRuleProps", "CfnTag", "CloudFormationJSON", "CodeDeployLambdaAliasUpdate", "ConcreteDependable", "Construct", "ConstructNode", "ConstructOrder", "ContextProvider", "CreationPolicy", "DeletionPolicy", "Dependency", "DynamicReferenceProps", "Environment", "FileSystemStore", "FileSystemStoreOptions", "Fn", "HashedAddressingScheme", "IAddressingScheme", "IAspect", "ICfnConditionExpression", "IConstruct", "IDependable", "IResolvedValuePostProcessor", "IResourceOptions", "ISessionStore", "ISynthesisSession", "ISynthesizable", "ITaggable", "ITemplateOptions", "InMemoryStore", "Include", "IncludeProps", "LogicalIDs", "ManifestOptions", "MetadataEntry", "OutgoingReference", "Reference", "RemovalPolicy", "RemoveTag", "ResolveContext", "ResourceSignal", "Root", "RuleAssertion", "SSMParameterProvider", "SSMParameterProviderProps", "ScopedAws", "SecretValue", "SecretsManagerSecretOptions", "Stack", "StackProps", "StringListCfnOutput", "StringListCfnOutputProps", "SynthesisOptions", "SynthesisSession", "Synthesizer", "Tag", "TagBase", "TagManager", "TagProps", "TagType", "Token", "UpdatePolicy", "ValidationError", "ValidationResult", "ValidationResults", "__jsii_assembly__"]

publication.publish()
