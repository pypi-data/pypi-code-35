import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling_api
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3_notifications
import aws_cdk.aws_sqs
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sns", "0.28.0", __name__, "aws-sns@0.28.0.jsii.tgz")
class CfnSubscription(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnSubscription"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, protocol: str, topic_arn: str, delivery_policy: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, endpoint: typing.Optional[str]=None, filter_policy: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, raw_message_delivery: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, region: typing.Optional[str]=None) -> None:
        props: CfnSubscriptionProps = {"protocol": protocol, "topicArn": topic_arn}

        if delivery_policy is not None:
            props["deliveryPolicy"] = delivery_policy

        if endpoint is not None:
            props["endpoint"] = endpoint

        if filter_policy is not None:
            props["filterPolicy"] = filter_policy

        if raw_message_delivery is not None:
            props["rawMessageDelivery"] = raw_message_delivery

        if region is not None:
            props["region"] = region

        jsii.create(CfnSubscription, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubscriptionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subscriptionArn")
    def subscription_arn(self) -> str:
        return jsii.get(self, "subscriptionArn")


class _CfnSubscriptionProps(jsii.compat.TypedDict, total=False):
    deliveryPolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    endpoint: str
    filterPolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    rawMessageDelivery: typing.Union[bool, aws_cdk.cdk.Token]
    region: str

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnSubscriptionProps")
class CfnSubscriptionProps(_CfnSubscriptionProps):
    protocol: str
    topicArn: str

class CfnTopic(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnTopic"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, display_name: typing.Optional[str]=None, kms_master_key_id: typing.Optional[str]=None, subscription: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "SubscriptionProperty"]]]]=None, topic_name: typing.Optional[str]=None) -> None:
        props: CfnTopicProps = {}

        if display_name is not None:
            props["displayName"] = display_name

        if kms_master_key_id is not None:
            props["kmsMasterKeyId"] = kms_master_key_id

        if subscription is not None:
            props["subscription"] = subscription

        if topic_name is not None:
            props["topicName"] = topic_name

        jsii.create(CfnTopic, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTopicProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        return jsii.get(self, "topicName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopic.SubscriptionProperty")
    class SubscriptionProperty(jsii.compat.TypedDict):
        endpoint: str
        protocol: str


class CfnTopicPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnTopicPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], topics: typing.List[str]) -> None:
        props: CfnTopicPolicyProps = {"policyDocument": policy_document, "topics": topics}

        jsii.create(CfnTopicPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTopicPolicyProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopicPolicyProps")
class CfnTopicPolicyProps(jsii.compat.TypedDict):
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    topics: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopicProps")
class CfnTopicProps(jsii.compat.TypedDict, total=False):
    displayName: str
    kmsMasterKeyId: str
    subscription: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTopic.SubscriptionProperty"]]]
    topicName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.EmailSubscriptionOptions")
class EmailSubscriptionOptions(jsii.compat.TypedDict, total=False):
    json: bool

@jsii.interface(jsii_type="@aws-cdk/aws-sns.ITopic")
class ITopic(aws_cdk.cdk.IConstruct, aws_cdk.aws_events.IEventRuleTarget, aws_cdk.aws_cloudwatch.IAlarmAction, aws_cdk.aws_s3_notifications.IBucketNotificationDestination, aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ITopicProxy

    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "TopicImportProps":
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="subscribe")
    def subscribe(self, name: str, endpoint: str, protocol: "SubscriptionProtocol", raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        ...

    @jsii.member(jsii_name="subscribeEmail")
    def subscribe_email(self, name: str, email_address: str, *, json: typing.Optional[bool]=None) -> "Subscription":
        ...

    @jsii.member(jsii_name="subscribeLambda")
    def subscribe_lambda(self, lambda_function: aws_cdk.aws_lambda.IFunction) -> "Subscription":
        ...

    @jsii.member(jsii_name="subscribeQueue")
    def subscribe_queue(self, queue: aws_cdk.aws_sqs.IQueue, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        ...

    @jsii.member(jsii_name="subscribeUrl")
    def subscribe_url(self, name: str, url: str, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        ...


class _ITopicProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_events.IEventRuleTarget), jsii.proxy_for(aws_cdk.aws_cloudwatch.IAlarmAction), jsii.proxy_for(aws_cdk.aws_s3_notifications.IBucketNotificationDestination), jsii.proxy_for(aws_cdk.aws_autoscaling_api.ILifecycleHookTarget)):
    __jsii_type__ = "@aws-cdk/aws-sns.ITopic"
    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        return jsii.get(self, "topicName")

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="export")
    def export(self) -> "TopicImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPublish", [identity])

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

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfMessagesPublished", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsFailed", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props])

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricPublishSize", [props])

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props])

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSMSSuccessRate", [props])

    @jsii.member(jsii_name="subscribe")
    def subscribe(self, name: str, endpoint: str, protocol: "SubscriptionProtocol", raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        return jsii.invoke(self, "subscribe", [name, endpoint, protocol, raw_message_delivery])

    @jsii.member(jsii_name="subscribeEmail")
    def subscribe_email(self, name: str, email_address: str, *, json: typing.Optional[bool]=None) -> "Subscription":
        options: EmailSubscriptionOptions = {}

        if json is not None:
            options["json"] = json

        return jsii.invoke(self, "subscribeEmail", [name, email_address, options])

    @jsii.member(jsii_name="subscribeLambda")
    def subscribe_lambda(self, lambda_function: aws_cdk.aws_lambda.IFunction) -> "Subscription":
        return jsii.invoke(self, "subscribeLambda", [lambda_function])

    @jsii.member(jsii_name="subscribeQueue")
    def subscribe_queue(self, queue: aws_cdk.aws_sqs.IQueue, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        return jsii.invoke(self, "subscribeQueue", [queue, raw_message_delivery])

    @jsii.member(jsii_name="subscribeUrl")
    def subscribe_url(self, name: str, url: str, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        return jsii.invoke(self, "subscribeUrl", [name, url, raw_message_delivery])


class Subscription(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.Subscription"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, endpoint: typing.Any, protocol: "SubscriptionProtocol", topic: "ITopic", raw_message_delivery: typing.Optional[bool]=None) -> None:
        props: SubscriptionProps = {"endpoint": endpoint, "protocol": protocol, "topic": topic}

        if raw_message_delivery is not None:
            props["rawMessageDelivery"] = raw_message_delivery

        jsii.create(Subscription, self, [scope, id, props])


class _SubscriptionProps(jsii.compat.TypedDict, total=False):
    rawMessageDelivery: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.SubscriptionProps")
class SubscriptionProps(_SubscriptionProps):
    endpoint: typing.Any
    protocol: "SubscriptionProtocol"
    topic: "ITopic"

@jsii.enum(jsii_type="@aws-cdk/aws-sns.SubscriptionProtocol")
class SubscriptionProtocol(enum.Enum):
    Http = "Http"
    Https = "Https"
    Email = "Email"
    EmailJson = "EmailJson"
    Sms = "Sms"
    Sqs = "Sqs"
    Application = "Application"
    Lambda = "Lambda"

@jsii.implements(ITopic)
class TopicBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-sns.TopicBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _TopicBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(TopicBase, self, [scope, id])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="asBucketNotificationDestination")
    def as_bucket_notification_destination(self, bucket_arn: str, bucket_id: str) -> aws_cdk.aws_s3_notifications.BucketNotificationDestinationProps:
        return jsii.invoke(self, "asBucketNotificationDestination", [bucket_arn, bucket_id])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @jsii.member(jsii_name="asLifecycleHookTarget")
    def as_lifecycle_hook_target(self, lifecycle_hook: aws_cdk.aws_autoscaling_api.ILifecycleHook) -> aws_cdk.aws_autoscaling_api.LifecycleHookTargetProps:
        return jsii.invoke(self, "asLifecycleHookTarget", [lifecycle_hook])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "TopicImportProps":
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPublish", [grantee])

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

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfMessagesPublished", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsFailed", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props])

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricPublishSize", [props])

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props])

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSMSSuccessRate", [props])

    @jsii.member(jsii_name="subscribe")
    def subscribe(self, name: str, endpoint: str, protocol: "SubscriptionProtocol", raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        return jsii.invoke(self, "subscribe", [name, endpoint, protocol, raw_message_delivery])

    @jsii.member(jsii_name="subscribeEmail")
    def subscribe_email(self, name: str, email_address: str, *, json: typing.Optional[bool]=None) -> "Subscription":
        options: EmailSubscriptionOptions = {}

        if json is not None:
            options["json"] = json

        return jsii.invoke(self, "subscribeEmail", [name, email_address, options])

    @jsii.member(jsii_name="subscribeLambda")
    def subscribe_lambda(self, lambda_function: aws_cdk.aws_lambda.IFunction) -> "Subscription":
        return jsii.invoke(self, "subscribeLambda", [lambda_function])

    @jsii.member(jsii_name="subscribeQueue")
    def subscribe_queue(self, queue: aws_cdk.aws_sqs.IQueue, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        return jsii.invoke(self, "subscribeQueue", [queue, raw_message_delivery])

    @jsii.member(jsii_name="subscribeUrl")
    def subscribe_url(self, name: str, url: str, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        return jsii.invoke(self, "subscribeUrl", [name, url, raw_message_delivery])

    @property
    @jsii.member(jsii_name="alarmActionArn")
    def alarm_action_arn(self) -> str:
        return jsii.get(self, "alarmActionArn")

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> bool:
        ...

    @property
    @jsii.member(jsii_name="topicArn")
    @abc.abstractmethod
    def topic_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="topicName")
    @abc.abstractmethod
    def topic_name(self) -> str:
        ...


class _TopicBaseProxy(TopicBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "TopicImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        return jsii.get(self, "autoCreatePolicy")

    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        return jsii.get(self, "topicName")


class Topic(TopicBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.Topic"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, display_name: typing.Optional[str]=None, topic_name: typing.Optional[str]=None) -> None:
        props: TopicProps = {}

        if display_name is not None:
            props["displayName"] = display_name

        if topic_name is not None:
            props["topicName"] = topic_name

        jsii.create(Topic, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, topic_arn: str, topic_name: str) -> "ITopic":
        props: TopicImportProps = {"topicArn": topic_arn, "topicName": topic_name}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "TopicImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        return jsii.get(self, "autoCreatePolicy")

    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        return jsii.get(self, "topicName")


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.TopicImportProps")
class TopicImportProps(jsii.compat.TypedDict):
    topicArn: str
    topicName: str

class TopicPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.TopicPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, topics: typing.List["ITopic"]) -> None:
        props: TopicPolicyProps = {"topics": topics}

        jsii.create(TopicPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="document")
    def document(self) -> aws_cdk.aws_iam.PolicyDocument:
        return jsii.get(self, "document")


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.TopicPolicyProps")
class TopicPolicyProps(jsii.compat.TypedDict):
    topics: typing.List["ITopic"]

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.TopicProps")
class TopicProps(jsii.compat.TypedDict, total=False):
    displayName: str
    topicName: str

__all__ = ["CfnSubscription", "CfnSubscriptionProps", "CfnTopic", "CfnTopicPolicy", "CfnTopicPolicyProps", "CfnTopicProps", "EmailSubscriptionOptions", "ITopic", "Subscription", "SubscriptionProps", "SubscriptionProtocol", "Topic", "TopicBase", "TopicImportProps", "TopicPolicy", "TopicPolicyProps", "TopicProps", "__jsii_assembly__"]

publication.publish()
