import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-iot", "0.28.0", __name__, "aws-iot@0.28.0.jsii.tgz")
class CfnCertificate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnCertificate"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, certificate_signing_request: str, status: str) -> None:
        props: CfnCertificateProps = {"certificateSigningRequest": certificate_signing_request, "status": status}

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
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> str:
        return jsii.get(self, "certificateId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCertificateProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnCertificateProps")
class CfnCertificateProps(jsii.compat.TypedDict):
    certificateSigningRequest: str
    status: str

class CfnPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], policy_name: typing.Optional[str]=None) -> None:
        props: CfnPolicyProps = {"policyDocument": policy_document}

        if policy_name is not None:
            props["policyName"] = policy_name

        jsii.create(CfnPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="policyArn")
    def policy_arn(self) -> str:
        return jsii.get(self, "policyArn")

    @property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        return jsii.get(self, "policyName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPolicyProps":
        return jsii.get(self, "propertyOverrides")


class CfnPolicyPrincipalAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnPolicyPrincipalAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_name: str, principal: str) -> None:
        props: CfnPolicyPrincipalAttachmentProps = {"policyName": policy_name, "principal": principal}

        jsii.create(CfnPolicyPrincipalAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPolicyPrincipalAttachmentProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnPolicyPrincipalAttachmentProps")
class CfnPolicyPrincipalAttachmentProps(jsii.compat.TypedDict):
    policyName: str
    principal: str

class _CfnPolicyProps(jsii.compat.TypedDict, total=False):
    policyName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnPolicyProps")
class CfnPolicyProps(_CfnPolicyProps):
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]

class CfnThing(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnThing"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, attribute_payload: typing.Optional[typing.Union[aws_cdk.cdk.Token, "AttributePayloadProperty"]]=None, thing_name: typing.Optional[str]=None) -> None:
        props: CfnThingProps = {}

        if attribute_payload is not None:
            props["attributePayload"] = attribute_payload

        if thing_name is not None:
            props["thingName"] = thing_name

        jsii.create(CfnThing, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnThingProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="thingName")
    def thing_name(self) -> str:
        return jsii.get(self, "thingName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThing.AttributePayloadProperty")
    class AttributePayloadProperty(jsii.compat.TypedDict, total=False):
        attributes: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]


class CfnThingPrincipalAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnThingPrincipalAttachment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, principal: str, thing_name: str) -> None:
        props: CfnThingPrincipalAttachmentProps = {"principal": principal, "thingName": thing_name}

        jsii.create(CfnThingPrincipalAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnThingPrincipalAttachmentProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThingPrincipalAttachmentProps")
class CfnThingPrincipalAttachmentProps(jsii.compat.TypedDict):
    principal: str
    thingName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThingProps")
class CfnThingProps(jsii.compat.TypedDict, total=False):
    attributePayload: typing.Union[aws_cdk.cdk.Token, "CfnThing.AttributePayloadProperty"]
    thingName: str

class CfnTopicRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnTopicRule"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, topic_rule_payload: typing.Union[aws_cdk.cdk.Token, "TopicRulePayloadProperty"], rule_name: typing.Optional[str]=None) -> None:
        props: CfnTopicRuleProps = {"topicRulePayload": topic_rule_payload}

        if rule_name is not None:
            props["ruleName"] = rule_name

        jsii.create(CfnTopicRule, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTopicRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="topicRuleArn")
    def topic_rule_arn(self) -> str:
        return jsii.get(self, "topicRuleArn")

    @property
    @jsii.member(jsii_name="topicRuleName")
    def topic_rule_name(self) -> str:
        return jsii.get(self, "topicRuleName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.ActionProperty")
    class ActionProperty(jsii.compat.TypedDict, total=False):
        cloudwatchAlarm: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.CloudwatchAlarmActionProperty"]
        cloudwatchMetric: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.CloudwatchMetricActionProperty"]
        dynamoDb: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.DynamoDBActionProperty"]
        dynamoDBv2: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.DynamoDBv2ActionProperty"]
        elasticsearch: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.ElasticsearchActionProperty"]
        firehose: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.FirehoseActionProperty"]
        iotAnalytics: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.IotAnalyticsActionProperty"]
        kinesis: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.KinesisActionProperty"]
        lambda_: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.LambdaActionProperty"]
        republish: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.RepublishActionProperty"]
        s3: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.S3ActionProperty"]
        sns: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.SnsActionProperty"]
        sqs: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.SqsActionProperty"]
        stepFunctions: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.StepFunctionsActionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.CloudwatchAlarmActionProperty")
    class CloudwatchAlarmActionProperty(jsii.compat.TypedDict):
        alarmName: str
        roleArn: str
        stateReason: str
        stateValue: str

    class _CloudwatchMetricActionProperty(jsii.compat.TypedDict, total=False):
        metricTimestamp: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.CloudwatchMetricActionProperty")
    class CloudwatchMetricActionProperty(_CloudwatchMetricActionProperty):
        metricName: str
        metricNamespace: str
        metricUnit: str
        metricValue: str
        roleArn: str

    class _DynamoDBActionProperty(jsii.compat.TypedDict, total=False):
        hashKeyType: str
        payloadField: str
        rangeKeyField: str
        rangeKeyType: str
        rangeKeyValue: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.DynamoDBActionProperty")
    class DynamoDBActionProperty(_DynamoDBActionProperty):
        hashKeyField: str
        hashKeyValue: str
        roleArn: str
        tableName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.DynamoDBv2ActionProperty")
    class DynamoDBv2ActionProperty(jsii.compat.TypedDict, total=False):
        putItem: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.PutItemInputProperty"]
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.ElasticsearchActionProperty")
    class ElasticsearchActionProperty(jsii.compat.TypedDict):
        endpoint: str
        id: str
        index: str
        roleArn: str
        type: str

    class _FirehoseActionProperty(jsii.compat.TypedDict, total=False):
        separator: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.FirehoseActionProperty")
    class FirehoseActionProperty(_FirehoseActionProperty):
        deliveryStreamName: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.IotAnalyticsActionProperty")
    class IotAnalyticsActionProperty(jsii.compat.TypedDict):
        channelName: str
        roleArn: str

    class _KinesisActionProperty(jsii.compat.TypedDict, total=False):
        partitionKey: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.KinesisActionProperty")
    class KinesisActionProperty(_KinesisActionProperty):
        roleArn: str
        streamName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.LambdaActionProperty")
    class LambdaActionProperty(jsii.compat.TypedDict, total=False):
        functionArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.PutItemInputProperty")
    class PutItemInputProperty(jsii.compat.TypedDict):
        tableName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.RepublishActionProperty")
    class RepublishActionProperty(jsii.compat.TypedDict):
        roleArn: str
        topic: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.S3ActionProperty")
    class S3ActionProperty(jsii.compat.TypedDict):
        bucketName: str
        key: str
        roleArn: str

    class _SnsActionProperty(jsii.compat.TypedDict, total=False):
        messageFormat: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.SnsActionProperty")
    class SnsActionProperty(_SnsActionProperty):
        roleArn: str
        targetArn: str

    class _SqsActionProperty(jsii.compat.TypedDict, total=False):
        useBase64: typing.Union[bool, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.SqsActionProperty")
    class SqsActionProperty(_SqsActionProperty):
        queueUrl: str
        roleArn: str

    class _StepFunctionsActionProperty(jsii.compat.TypedDict, total=False):
        executionNamePrefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.StepFunctionsActionProperty")
    class StepFunctionsActionProperty(_StepFunctionsActionProperty):
        roleArn: str
        stateMachineName: str

    class _TopicRulePayloadProperty(jsii.compat.TypedDict, total=False):
        awsIotSqlVersion: str
        description: str
        errorAction: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.ActionProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.TopicRulePayloadProperty")
    class TopicRulePayloadProperty(_TopicRulePayloadProperty):
        actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.ActionProperty"]]]
        ruleDisabled: typing.Union[bool, aws_cdk.cdk.Token]
        sql: str


class _CfnTopicRuleProps(jsii.compat.TypedDict, total=False):
    ruleName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRuleProps")
class CfnTopicRuleProps(_CfnTopicRuleProps):
    topicRulePayload: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.TopicRulePayloadProperty"]

__all__ = ["CfnCertificate", "CfnCertificateProps", "CfnPolicy", "CfnPolicyPrincipalAttachment", "CfnPolicyPrincipalAttachmentProps", "CfnPolicyProps", "CfnThing", "CfnThingPrincipalAttachment", "CfnThingPrincipalAttachmentProps", "CfnThingProps", "CfnTopicRule", "CfnTopicRuleProps", "__jsii_assembly__"]

publication.publish()
