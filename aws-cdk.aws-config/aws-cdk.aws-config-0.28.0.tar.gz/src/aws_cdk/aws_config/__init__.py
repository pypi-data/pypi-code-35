import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-config", "0.28.0", __name__, "aws-config@0.28.0.jsii.tgz")
class CfnAggregationAuthorization(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnAggregationAuthorization"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authorized_account_id: str, authorized_aws_region: str) -> None:
        props: CfnAggregationAuthorizationProps = {"authorizedAccountId": authorized_account_id, "authorizedAwsRegion": authorized_aws_region}

        jsii.create(CfnAggregationAuthorization, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="aggregationAuthorizationArn")
    def aggregation_authorization_arn(self) -> str:
        return jsii.get(self, "aggregationAuthorizationArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAggregationAuthorizationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnAggregationAuthorizationProps")
class CfnAggregationAuthorizationProps(jsii.compat.TypedDict):
    authorizedAccountId: str
    authorizedAwsRegion: str

class CfnConfigRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnConfigRule"):
    def __init__(self, scope_: aws_cdk.cdk.Construct, id: str, *, source: typing.Union["SourceProperty", aws_cdk.cdk.Token], config_rule_name: typing.Optional[str]=None, description: typing.Optional[str]=None, input_parameters: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, maximum_execution_frequency: typing.Optional[str]=None, scope: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ScopeProperty"]]=None) -> None:
        props: CfnConfigRuleProps = {"source": source}

        if config_rule_name is not None:
            props["configRuleName"] = config_rule_name

        if description is not None:
            props["description"] = description

        if input_parameters is not None:
            props["inputParameters"] = input_parameters

        if maximum_execution_frequency is not None:
            props["maximumExecutionFrequency"] = maximum_execution_frequency

        if scope is not None:
            props["scope"] = scope

        jsii.create(CfnConfigRule, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="configRuleArn")
    def config_rule_arn(self) -> str:
        return jsii.get(self, "configRuleArn")

    @property
    @jsii.member(jsii_name="configRuleComplianceType")
    def config_rule_compliance_type(self) -> str:
        return jsii.get(self, "configRuleComplianceType")

    @property
    @jsii.member(jsii_name="configRuleId")
    def config_rule_id(self) -> str:
        return jsii.get(self, "configRuleId")

    @property
    @jsii.member(jsii_name="configRuleName")
    def config_rule_name(self) -> str:
        return jsii.get(self, "configRuleName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigRuleProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigRule.ScopeProperty")
    class ScopeProperty(jsii.compat.TypedDict, total=False):
        complianceResourceId: str
        complianceResourceTypes: typing.List[str]
        tagKey: str
        tagValue: str

    class _SourceDetailProperty(jsii.compat.TypedDict, total=False):
        maximumExecutionFrequency: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigRule.SourceDetailProperty")
    class SourceDetailProperty(_SourceDetailProperty):
        eventSource: str
        messageType: str

    class _SourceProperty(jsii.compat.TypedDict, total=False):
        sourceDetails: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigRule.SourceDetailProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigRule.SourceProperty")
    class SourceProperty(_SourceProperty):
        owner: str
        sourceIdentifier: str


class _CfnConfigRuleProps(jsii.compat.TypedDict, total=False):
    configRuleName: str
    description: str
    inputParameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    maximumExecutionFrequency: str
    scope: typing.Union[aws_cdk.cdk.Token, "CfnConfigRule.ScopeProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigRuleProps")
class CfnConfigRuleProps(_CfnConfigRuleProps):
    source: typing.Union["CfnConfigRule.SourceProperty", aws_cdk.cdk.Token]

class CfnConfigurationAggregator(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnConfigurationAggregator"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, configuration_aggregator_name: str, account_aggregation_sources: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "AccountAggregationSourceProperty"]]]]=None, organization_aggregation_source: typing.Optional[typing.Union[aws_cdk.cdk.Token, "OrganizationAggregationSourceProperty"]]=None) -> None:
        props: CfnConfigurationAggregatorProps = {"configurationAggregatorName": configuration_aggregator_name}

        if account_aggregation_sources is not None:
            props["accountAggregationSources"] = account_aggregation_sources

        if organization_aggregation_source is not None:
            props["organizationAggregationSource"] = organization_aggregation_source

        jsii.create(CfnConfigurationAggregator, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="configurationAggregatorName")
    def configuration_aggregator_name(self) -> str:
        return jsii.get(self, "configurationAggregatorName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationAggregatorProps":
        return jsii.get(self, "propertyOverrides")

    class _AccountAggregationSourceProperty(jsii.compat.TypedDict, total=False):
        allAwsRegions: typing.Union[bool, aws_cdk.cdk.Token]
        awsRegions: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationAggregator.AccountAggregationSourceProperty")
    class AccountAggregationSourceProperty(_AccountAggregationSourceProperty):
        accountIds: typing.List[str]

    class _OrganizationAggregationSourceProperty(jsii.compat.TypedDict, total=False):
        allAwsRegions: typing.Union[bool, aws_cdk.cdk.Token]
        awsRegions: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationAggregator.OrganizationAggregationSourceProperty")
    class OrganizationAggregationSourceProperty(_OrganizationAggregationSourceProperty):
        roleArn: str


class _CfnConfigurationAggregatorProps(jsii.compat.TypedDict, total=False):
    accountAggregationSources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigurationAggregator.AccountAggregationSourceProperty"]]]
    organizationAggregationSource: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationAggregator.OrganizationAggregationSourceProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationAggregatorProps")
class CfnConfigurationAggregatorProps(_CfnConfigurationAggregatorProps):
    configurationAggregatorName: str

class CfnConfigurationRecorder(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnConfigurationRecorder"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, role_arn: str, name: typing.Optional[str]=None, recording_group: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RecordingGroupProperty"]]=None) -> None:
        props: CfnConfigurationRecorderProps = {"roleArn": role_arn}

        if name is not None:
            props["name"] = name

        if recording_group is not None:
            props["recordingGroup"] = recording_group

        jsii.create(CfnConfigurationRecorder, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="configurationRecorderName")
    def configuration_recorder_name(self) -> str:
        return jsii.get(self, "configurationRecorderName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationRecorderProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationRecorder.RecordingGroupProperty")
    class RecordingGroupProperty(jsii.compat.TypedDict, total=False):
        allSupported: typing.Union[bool, aws_cdk.cdk.Token]
        includeGlobalResourceTypes: typing.Union[bool, aws_cdk.cdk.Token]
        resourceTypes: typing.List[str]


class _CfnConfigurationRecorderProps(jsii.compat.TypedDict, total=False):
    name: str
    recordingGroup: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationRecorder.RecordingGroupProperty"]

@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationRecorderProps")
class CfnConfigurationRecorderProps(_CfnConfigurationRecorderProps):
    roleArn: str

class CfnDeliveryChannel(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnDeliveryChannel"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, s3_bucket_name: str, config_snapshot_delivery_properties: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ConfigSnapshotDeliveryPropertiesProperty"]]=None, name: typing.Optional[str]=None, s3_key_prefix: typing.Optional[str]=None, sns_topic_arn: typing.Optional[str]=None) -> None:
        props: CfnDeliveryChannelProps = {"s3BucketName": s3_bucket_name}

        if config_snapshot_delivery_properties is not None:
            props["configSnapshotDeliveryProperties"] = config_snapshot_delivery_properties

        if name is not None:
            props["name"] = name

        if s3_key_prefix is not None:
            props["s3KeyPrefix"] = s3_key_prefix

        if sns_topic_arn is not None:
            props["snsTopicArn"] = sns_topic_arn

        jsii.create(CfnDeliveryChannel, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deliveryChannelName")
    def delivery_channel_name(self) -> str:
        return jsii.get(self, "deliveryChannelName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeliveryChannelProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty")
    class ConfigSnapshotDeliveryPropertiesProperty(jsii.compat.TypedDict, total=False):
        deliveryFrequency: str


class _CfnDeliveryChannelProps(jsii.compat.TypedDict, total=False):
    configSnapshotDeliveryProperties: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty"]
    name: str
    s3KeyPrefix: str
    snsTopicArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnDeliveryChannelProps")
class CfnDeliveryChannelProps(_CfnDeliveryChannelProps):
    s3BucketName: str

__all__ = ["CfnAggregationAuthorization", "CfnAggregationAuthorizationProps", "CfnConfigRule", "CfnConfigRuleProps", "CfnConfigurationAggregator", "CfnConfigurationAggregatorProps", "CfnConfigurationRecorder", "CfnConfigurationRecorderProps", "CfnDeliveryChannel", "CfnDeliveryChannelProps", "__jsii_assembly__"]

publication.publish()
