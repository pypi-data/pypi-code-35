import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-logs", "0.28.0", __name__, "aws-logs@0.28.0.jsii.tgz")
class CfnDestination(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnDestination"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, destination_name: str, destination_policy: str, role_arn: str, target_arn: str) -> None:
        props: CfnDestinationProps = {"destinationName": destination_name, "destinationPolicy": destination_policy, "roleArn": role_arn, "targetArn": target_arn}

        jsii.create(CfnDestination, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> str:
        return jsii.get(self, "destinationArn")

    @property
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> str:
        return jsii.get(self, "destinationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDestinationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnDestinationProps")
class CfnDestinationProps(jsii.compat.TypedDict):
    destinationName: str
    destinationPolicy: str
    roleArn: str
    targetArn: str

class CfnLogGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnLogGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, log_group_name: typing.Optional[str]=None, retention_in_days: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnLogGroupProps = {}

        if log_group_name is not None:
            props["logGroupName"] = log_group_name

        if retention_in_days is not None:
            props["retentionInDays"] = retention_in_days

        jsii.create(CfnLogGroup, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        return jsii.get(self, "logGroupArn")

    @property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        return jsii.get(self, "logGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLogGroupProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnLogGroupProps")
class CfnLogGroupProps(jsii.compat.TypedDict, total=False):
    logGroupName: str
    retentionInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]

class CfnLogStream(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnLogStream"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, log_group_name: str, log_stream_name: typing.Optional[str]=None) -> None:
        props: CfnLogStreamProps = {"logGroupName": log_group_name}

        if log_stream_name is not None:
            props["logStreamName"] = log_stream_name

        jsii.create(CfnLogStream, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        return jsii.get(self, "logStreamName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLogStreamProps":
        return jsii.get(self, "propertyOverrides")


class _CfnLogStreamProps(jsii.compat.TypedDict, total=False):
    logStreamName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnLogStreamProps")
class CfnLogStreamProps(_CfnLogStreamProps):
    logGroupName: str

class CfnMetricFilter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnMetricFilter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, filter_pattern: str, log_group_name: str, metric_transformations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "MetricTransformationProperty"]]]) -> None:
        props: CfnMetricFilterProps = {"filterPattern": filter_pattern, "logGroupName": log_group_name, "metricTransformations": metric_transformations}

        jsii.create(CfnMetricFilter, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="metricFilterName")
    def metric_filter_name(self) -> str:
        return jsii.get(self, "metricFilterName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMetricFilterProps":
        return jsii.get(self, "propertyOverrides")

    class _MetricTransformationProperty(jsii.compat.TypedDict, total=False):
        defaultValue: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnMetricFilter.MetricTransformationProperty")
    class MetricTransformationProperty(_MetricTransformationProperty):
        metricName: str
        metricNamespace: str
        metricValue: str


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnMetricFilterProps")
class CfnMetricFilterProps(jsii.compat.TypedDict):
    filterPattern: str
    logGroupName: str
    metricTransformations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnMetricFilter.MetricTransformationProperty"]]]

class CfnSubscriptionFilter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CfnSubscriptionFilter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, destination_arn: str, filter_pattern: str, log_group_name: str, role_arn: typing.Optional[str]=None) -> None:
        props: CfnSubscriptionFilterProps = {"destinationArn": destination_arn, "filterPattern": filter_pattern, "logGroupName": log_group_name}

        if role_arn is not None:
            props["roleArn"] = role_arn

        jsii.create(CfnSubscriptionFilter, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubscriptionFilterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subscriptionFilterName")
    def subscription_filter_name(self) -> str:
        return jsii.get(self, "subscriptionFilterName")


class _CfnSubscriptionFilterProps(jsii.compat.TypedDict, total=False):
    roleArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CfnSubscriptionFilterProps")
class CfnSubscriptionFilterProps(_CfnSubscriptionFilterProps):
    destinationArn: str
    filterPattern: str
    logGroupName: str

class _ColumnRestriction(jsii.compat.TypedDict, total=False):
    numberValue: jsii.Number
    stringValue: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.ColumnRestriction")
class ColumnRestriction(_ColumnRestriction):
    comparison: str

class _CrossAccountDestinationProps(jsii.compat.TypedDict, total=False):
    destinationName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.CrossAccountDestinationProps")
class CrossAccountDestinationProps(_CrossAccountDestinationProps):
    role: aws_cdk.aws_iam.Role
    targetArn: str

class FilterPattern(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.FilterPattern"):
    def __init__(self) -> None:
        jsii.create(FilterPattern, self, [])

    @jsii.member(jsii_name="all")
    @classmethod
    def all(cls, *patterns: "JSONPattern") -> "JSONPattern":
        return jsii.sinvoke(cls, "all", [patterns])

    @jsii.member(jsii_name="allEvents")
    @classmethod
    def all_events(cls) -> "IFilterPattern":
        return jsii.sinvoke(cls, "allEvents", [])

    @jsii.member(jsii_name="allTerms")
    @classmethod
    def all_terms(cls, *terms: str) -> "IFilterPattern":
        return jsii.sinvoke(cls, "allTerms", [terms])

    @jsii.member(jsii_name="any")
    @classmethod
    def any(cls, *patterns: "JSONPattern") -> "JSONPattern":
        return jsii.sinvoke(cls, "any", [patterns])

    @jsii.member(jsii_name="anyTerm")
    @classmethod
    def any_term(cls, *terms: str) -> "IFilterPattern":
        return jsii.sinvoke(cls, "anyTerm", [terms])

    @jsii.member(jsii_name="anyTermGroup")
    @classmethod
    def any_term_group(cls, *term_groups: typing.List[str]) -> "IFilterPattern":
        return jsii.sinvoke(cls, "anyTermGroup", [term_groups])

    @jsii.member(jsii_name="booleanValue")
    @classmethod
    def boolean_value(cls, json_field: str, value: bool) -> "JSONPattern":
        return jsii.sinvoke(cls, "booleanValue", [json_field, value])

    @jsii.member(jsii_name="exists")
    @classmethod
    def exists(cls, json_field: str) -> "JSONPattern":
        return jsii.sinvoke(cls, "exists", [json_field])

    @jsii.member(jsii_name="isNull")
    @classmethod
    def is_null(cls, json_field: str) -> "JSONPattern":
        return jsii.sinvoke(cls, "isNull", [json_field])

    @jsii.member(jsii_name="literal")
    @classmethod
    def literal(cls, log_pattern_string: str) -> "IFilterPattern":
        return jsii.sinvoke(cls, "literal", [log_pattern_string])

    @jsii.member(jsii_name="notExists")
    @classmethod
    def not_exists(cls, json_field: str) -> "JSONPattern":
        return jsii.sinvoke(cls, "notExists", [json_field])

    @jsii.member(jsii_name="numberValue")
    @classmethod
    def number_value(cls, json_field: str, comparison: str, value: jsii.Number) -> "JSONPattern":
        return jsii.sinvoke(cls, "numberValue", [json_field, comparison, value])

    @jsii.member(jsii_name="spaceDelimited")
    @classmethod
    def space_delimited(cls, *columns: str) -> "SpaceDelimitedTextPattern":
        return jsii.sinvoke(cls, "spaceDelimited", [columns])

    @jsii.member(jsii_name="stringValue")
    @classmethod
    def string_value(cls, json_field: str, comparison: str, value: str) -> "JSONPattern":
        return jsii.sinvoke(cls, "stringValue", [json_field, comparison, value])


@jsii.interface(jsii_type="@aws-cdk/aws-logs.IFilterPattern")
class IFilterPattern(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IFilterPatternProxy

    @property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        ...


class _IFilterPatternProxy():
    __jsii_type__ = "@aws-cdk/aws-logs.IFilterPattern"
    @property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        return jsii.get(self, "logPatternString")


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogGroup")
class ILogGroup(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILogGroupProxy

    @property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "LogGroupImportProps":
        ...

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="newMetricFilter")
    def new_metric_filter(self, scope: aws_cdk.cdk.Construct, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        ...

    @jsii.member(jsii_name="newStream")
    def new_stream(self, scope: aws_cdk.cdk.Construct, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        ...

    @jsii.member(jsii_name="newSubscriptionFilter")
    def new_subscription_filter(self, scope: aws_cdk.cdk.Construct, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        ...


class _ILogGroupProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-logs.ILogGroup"
    @property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        return jsii.get(self, "logGroupArn")

    @property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        return jsii.get(self, "logGroupName")

    @jsii.member(jsii_name="export")
    def export(self) -> "LogGroupImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> aws_cdk.aws_cloudwatch.Metric:
        return jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="newMetricFilter")
    def new_metric_filter(self, scope: aws_cdk.cdk.Construct, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        props: NewMetricFilterProps = {"filterPattern": filter_pattern, "metricName": metric_name, "metricNamespace": metric_namespace}

        if default_value is not None:
            props["defaultValue"] = default_value

        if metric_value is not None:
            props["metricValue"] = metric_value

        return jsii.invoke(self, "newMetricFilter", [scope, id, props])

    @jsii.member(jsii_name="newStream")
    def new_stream(self, scope: aws_cdk.cdk.Construct, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        props: NewLogStreamProps = {}

        if log_stream_name is not None:
            props["logStreamName"] = log_stream_name

        return jsii.invoke(self, "newStream", [scope, id, props])

    @jsii.member(jsii_name="newSubscriptionFilter")
    def new_subscription_filter(self, scope: aws_cdk.cdk.Construct, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        props: NewSubscriptionFilterProps = {"destination": destination, "filterPattern": filter_pattern}

        return jsii.invoke(self, "newSubscriptionFilter", [scope, id, props])


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogStream")
class ILogStream(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILogStreamProxy

    @property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "LogStreamImportProps":
        ...


class _ILogStreamProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-logs.ILogStream"
    @property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        return jsii.get(self, "logStreamName")

    @jsii.member(jsii_name="export")
    def export(self) -> "LogStreamImportProps":
        return jsii.invoke(self, "export", [])


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogSubscriptionDestination")
class ILogSubscriptionDestination(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILogSubscriptionDestinationProxy

    @jsii.member(jsii_name="logSubscriptionDestination")
    def log_subscription_destination(self, source_log_group: "ILogGroup") -> "LogSubscriptionDestination":
        ...


class _ILogSubscriptionDestinationProxy():
    __jsii_type__ = "@aws-cdk/aws-logs.ILogSubscriptionDestination"
    @jsii.member(jsii_name="logSubscriptionDestination")
    def log_subscription_destination(self, source_log_group: "ILogGroup") -> "LogSubscriptionDestination":
        return jsii.invoke(self, "logSubscriptionDestination", [source_log_group])


@jsii.implements(ILogSubscriptionDestination)
class CrossAccountDestination(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.CrossAccountDestination"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, role: aws_cdk.aws_iam.Role, target_arn: str, destination_name: typing.Optional[str]=None) -> None:
        props: CrossAccountDestinationProps = {"role": role, "targetArn": target_arn}

        if destination_name is not None:
            props["destinationName"] = destination_name

        jsii.create(CrossAccountDestination, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="logSubscriptionDestination")
    def log_subscription_destination(self, _source_log_group: "ILogGroup") -> "LogSubscriptionDestination":
        return jsii.invoke(self, "logSubscriptionDestination", [_source_log_group])

    @property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> str:
        return jsii.get(self, "destinationArn")

    @property
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> str:
        return jsii.get(self, "destinationName")

    @property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> aws_cdk.aws_iam.PolicyDocument:
        return jsii.get(self, "policyDocument")


@jsii.implements(IFilterPattern)
class JSONPattern(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-logs.JSONPattern"):
    @staticmethod
    def __jsii_proxy_class__():
        return _JSONPatternProxy

    def __init__(self, json_pattern_string: str) -> None:
        jsii.create(JSONPattern, self, [json_pattern_string])

    @property
    @jsii.member(jsii_name="jsonPatternString")
    def json_pattern_string(self) -> str:
        return jsii.get(self, "jsonPatternString")

    @property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        return jsii.get(self, "logPatternString")


class _JSONPatternProxy(JSONPattern):
    pass

@jsii.implements(ILogGroup)
class LogGroupBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-logs.LogGroupBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _LogGroupBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(LogGroupBase, self, [scope, id])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "LogGroupImportProps":
        ...

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> aws_cdk.aws_cloudwatch.Metric:
        return jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="newMetricFilter")
    def new_metric_filter(self, scope: aws_cdk.cdk.Construct, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        props: NewMetricFilterProps = {"filterPattern": filter_pattern, "metricName": metric_name, "metricNamespace": metric_namespace}

        if default_value is not None:
            props["defaultValue"] = default_value

        if metric_value is not None:
            props["metricValue"] = metric_value

        return jsii.invoke(self, "newMetricFilter", [scope, id, props])

    @jsii.member(jsii_name="newStream")
    def new_stream(self, scope: aws_cdk.cdk.Construct, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        props: NewLogStreamProps = {}

        if log_stream_name is not None:
            props["logStreamName"] = log_stream_name

        return jsii.invoke(self, "newStream", [scope, id, props])

    @jsii.member(jsii_name="newSubscriptionFilter")
    def new_subscription_filter(self, scope: aws_cdk.cdk.Construct, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        props: NewSubscriptionFilterProps = {"destination": destination, "filterPattern": filter_pattern}

        return jsii.invoke(self, "newSubscriptionFilter", [scope, id, props])

    @property
    @jsii.member(jsii_name="logGroupArn")
    @abc.abstractmethod
    def log_group_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="logGroupName")
    @abc.abstractmethod
    def log_group_name(self) -> str:
        ...


class _LogGroupBaseProxy(LogGroupBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "LogGroupImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        return jsii.get(self, "logGroupArn")

    @property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        return jsii.get(self, "logGroupName")


class LogGroup(LogGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.LogGroup"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, log_group_name: typing.Optional[str]=None, retain_log_group: typing.Optional[bool]=None, retention_days: typing.Optional["RetentionDays"]=None) -> None:
        props: LogGroupProps = {}

        if log_group_name is not None:
            props["logGroupName"] = log_group_name

        if retain_log_group is not None:
            props["retainLogGroup"] = retain_log_group

        if retention_days is not None:
            props["retentionDays"] = retention_days

        jsii.create(LogGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, log_group_arn: str) -> "ILogGroup":
        props: LogGroupImportProps = {"logGroupArn": log_group_arn}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "LogGroupImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        return jsii.get(self, "logGroupArn")

    @property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        return jsii.get(self, "logGroupName")


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.LogGroupImportProps")
class LogGroupImportProps(jsii.compat.TypedDict):
    logGroupArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.LogGroupProps")
class LogGroupProps(jsii.compat.TypedDict, total=False):
    logGroupName: str
    retainLogGroup: bool
    retentionDays: "RetentionDays"

@jsii.implements(ILogStream)
class LogStream(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.LogStream"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, log_group: "ILogGroup", log_stream_name: typing.Optional[str]=None, retain_log_stream: typing.Optional[bool]=None) -> None:
        props: LogStreamProps = {"logGroup": log_group}

        if log_stream_name is not None:
            props["logStreamName"] = log_stream_name

        if retain_log_stream is not None:
            props["retainLogStream"] = retain_log_stream

        jsii.create(LogStream, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, log_stream_name: str) -> "ILogStream":
        props: LogStreamImportProps = {"logStreamName": log_stream_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "LogStreamImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        return jsii.get(self, "logStreamName")


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.LogStreamImportProps")
class LogStreamImportProps(jsii.compat.TypedDict):
    logStreamName: str

class _LogStreamProps(jsii.compat.TypedDict, total=False):
    logStreamName: str
    retainLogStream: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.LogStreamProps")
class LogStreamProps(_LogStreamProps):
    logGroup: "ILogGroup"

class _LogSubscriptionDestination(jsii.compat.TypedDict, total=False):
    role: aws_cdk.aws_iam.Role

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.LogSubscriptionDestination")
class LogSubscriptionDestination(_LogSubscriptionDestination):
    arn: str

class MetricFilter(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.MetricFilter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, filter_pattern: "IFilterPattern", log_group: "ILogGroup", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> None:
        props: MetricFilterProps = {"filterPattern": filter_pattern, "logGroup": log_group, "metricName": metric_name, "metricNamespace": metric_namespace}

        if default_value is not None:
            props["defaultValue"] = default_value

        if metric_value is not None:
            props["metricValue"] = metric_value

        jsii.create(MetricFilter, self, [scope, id, props])


class _MetricFilterProps(jsii.compat.TypedDict, total=False):
    defaultValue: jsii.Number
    metricValue: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.MetricFilterProps")
class MetricFilterProps(_MetricFilterProps):
    filterPattern: "IFilterPattern"
    logGroup: "ILogGroup"
    metricName: str
    metricNamespace: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.NewLogStreamProps")
class NewLogStreamProps(jsii.compat.TypedDict, total=False):
    logStreamName: str

class _NewMetricFilterProps(jsii.compat.TypedDict, total=False):
    defaultValue: jsii.Number
    metricValue: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.NewMetricFilterProps")
class NewMetricFilterProps(_NewMetricFilterProps):
    filterPattern: "IFilterPattern"
    metricName: str
    metricNamespace: str

@jsii.data_type(jsii_type="@aws-cdk/aws-logs.NewSubscriptionFilterProps")
class NewSubscriptionFilterProps(jsii.compat.TypedDict):
    destination: "ILogSubscriptionDestination"
    filterPattern: "IFilterPattern"

@jsii.enum(jsii_type="@aws-cdk/aws-logs.RetentionDays")
class RetentionDays(enum.Enum):
    OneDay = "OneDay"
    ThreeDays = "ThreeDays"
    FiveDays = "FiveDays"
    OneWeek = "OneWeek"
    TwoWeeks = "TwoWeeks"
    OneMonth = "OneMonth"
    TwoMonths = "TwoMonths"
    ThreeMonths = "ThreeMonths"
    FourMonths = "FourMonths"
    FiveMonths = "FiveMonths"
    SixMonths = "SixMonths"
    OneYear = "OneYear"
    ThirteenMonths = "ThirteenMonths"
    EighteenMonths = "EighteenMonths"
    TwoYears = "TwoYears"
    FiveYears = "FiveYears"
    TenYears = "TenYears"

@jsii.implements(IFilterPattern)
class SpaceDelimitedTextPattern(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.SpaceDelimitedTextPattern"):
    def __init__(self, columns: typing.List[str], restrictions: typing.Mapping[str,typing.List["ColumnRestriction"]]) -> None:
        jsii.create(SpaceDelimitedTextPattern, self, [columns, restrictions])

    @jsii.member(jsii_name="construct")
    @classmethod
    def construct(cls, columns: typing.List[str]) -> "SpaceDelimitedTextPattern":
        return jsii.sinvoke(cls, "construct", [columns])

    @jsii.member(jsii_name="whereNumber")
    def where_number(self, column_name: str, comparison: str, value: jsii.Number) -> "SpaceDelimitedTextPattern":
        return jsii.invoke(self, "whereNumber", [column_name, comparison, value])

    @jsii.member(jsii_name="whereString")
    def where_string(self, column_name: str, comparison: str, value: str) -> "SpaceDelimitedTextPattern":
        return jsii.invoke(self, "whereString", [column_name, comparison, value])

    @property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[str]:
        return jsii.get(self, "columns")

    @property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        return jsii.get(self, "logPatternString")

    @property
    @jsii.member(jsii_name="restrictions")
    def restrictions(self) -> typing.Mapping[str,typing.List["ColumnRestriction"]]:
        return jsii.get(self, "restrictions")


class SubscriptionFilter(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.SubscriptionFilter"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern", log_group: "ILogGroup") -> None:
        props: SubscriptionFilterProps = {"destination": destination, "filterPattern": filter_pattern, "logGroup": log_group}

        jsii.create(SubscriptionFilter, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-logs.SubscriptionFilterProps")
class SubscriptionFilterProps(jsii.compat.TypedDict):
    destination: "ILogSubscriptionDestination"
    filterPattern: "IFilterPattern"
    logGroup: "ILogGroup"

__all__ = ["CfnDestination", "CfnDestinationProps", "CfnLogGroup", "CfnLogGroupProps", "CfnLogStream", "CfnLogStreamProps", "CfnMetricFilter", "CfnMetricFilterProps", "CfnSubscriptionFilter", "CfnSubscriptionFilterProps", "ColumnRestriction", "CrossAccountDestination", "CrossAccountDestinationProps", "FilterPattern", "IFilterPattern", "ILogGroup", "ILogStream", "ILogSubscriptionDestination", "JSONPattern", "LogGroup", "LogGroupBase", "LogGroupImportProps", "LogGroupProps", "LogStream", "LogStreamImportProps", "LogStreamProps", "LogSubscriptionDestination", "MetricFilter", "MetricFilterProps", "NewLogStreamProps", "NewMetricFilterProps", "NewSubscriptionFilterProps", "RetentionDays", "SpaceDelimitedTextPattern", "SubscriptionFilter", "SubscriptionFilterProps", "__jsii_assembly__"]

publication.publish()
