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
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3_notifications
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sqs", "0.28.0", __name__, "aws-sqs@0.28.0.jsii.tgz")
class CfnQueue(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sqs.CfnQueue"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, content_based_deduplication: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, delay_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, fifo_queue: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, kms_data_key_reuse_period_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, kms_master_key_id: typing.Optional[str]=None, maximum_message_size: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, message_retention_period: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, queue_name: typing.Optional[str]=None, receive_message_wait_time_seconds: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, redrive_policy: typing.Optional[typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, visibility_timeout: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None) -> None:
        props: CfnQueueProps = {}

        if content_based_deduplication is not None:
            props["contentBasedDeduplication"] = content_based_deduplication

        if delay_seconds is not None:
            props["delaySeconds"] = delay_seconds

        if fifo_queue is not None:
            props["fifoQueue"] = fifo_queue

        if kms_data_key_reuse_period_seconds is not None:
            props["kmsDataKeyReusePeriodSeconds"] = kms_data_key_reuse_period_seconds

        if kms_master_key_id is not None:
            props["kmsMasterKeyId"] = kms_master_key_id

        if maximum_message_size is not None:
            props["maximumMessageSize"] = maximum_message_size

        if message_retention_period is not None:
            props["messageRetentionPeriod"] = message_retention_period

        if queue_name is not None:
            props["queueName"] = queue_name

        if receive_message_wait_time_seconds is not None:
            props["receiveMessageWaitTimeSeconds"] = receive_message_wait_time_seconds

        if redrive_policy is not None:
            props["redrivePolicy"] = redrive_policy

        if tags is not None:
            props["tags"] = tags

        if visibility_timeout is not None:
            props["visibilityTimeout"] = visibility_timeout

        jsii.create(CfnQueue, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnQueueProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        return jsii.get(self, "queueArn")

    @property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        return jsii.get(self, "queueName")

    @property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        return jsii.get(self, "queueUrl")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")


class CfnQueuePolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sqs.CfnQueuePolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], queues: typing.List[str]) -> None:
        props: CfnQueuePolicyProps = {"policyDocument": policy_document, "queues": queues}

        jsii.create(CfnQueuePolicy, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnQueuePolicyProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.CfnQueuePolicyProps")
class CfnQueuePolicyProps(jsii.compat.TypedDict):
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    queues: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.CfnQueueProps")
class CfnQueueProps(jsii.compat.TypedDict, total=False):
    contentBasedDeduplication: typing.Union[bool, aws_cdk.cdk.Token]
    delaySeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    fifoQueue: typing.Union[bool, aws_cdk.cdk.Token]
    kmsDataKeyReusePeriodSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    kmsMasterKeyId: str
    maximumMessageSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    messageRetentionPeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    queueName: str
    receiveMessageWaitTimeSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    redrivePolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    tags: typing.List[aws_cdk.cdk.CfnTag]
    visibilityTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.DeadLetterQueue")
class DeadLetterQueue(jsii.compat.TypedDict):
    maxReceiveCount: jsii.Number
    queue: "IQueue"

@jsii.interface(jsii_type="@aws-cdk/aws-sqs.IQueue")
class IQueue(aws_cdk.cdk.IConstruct, aws_cdk.aws_s3_notifications.IBucketNotificationDestination, aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IQueueProxy

    @property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "QueueImportProps":
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *queue_actions: str) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        ...


class _IQueueProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_s3_notifications.IBucketNotificationDestination), jsii.proxy_for(aws_cdk.aws_autoscaling_api.ILifecycleHookTarget)):
    __jsii_type__ = "@aws-cdk/aws-sqs.IQueue"
    @property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        return jsii.get(self, "queueArn")

    @property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        return jsii.get(self, "queueName")

    @property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        return jsii.get(self, "queueUrl")

    @property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionMasterKey")

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="export")
    def export(self) -> "QueueImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *queue_actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, queue_actions])

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantConsumeMessages", [grantee])

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPurge", [grantee])

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantSendMessages", [grantee])

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

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricApproximateAgeOfOldestMessage", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricApproximateNumberOfMessagesDelayed", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricApproximateNumberOfMessagesNotVisible", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricApproximateNumberOfMessagesVisible", [props])

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfEmptyReceives", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfMessagesDeleted", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfMessagesReceived", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfMessagesSent", [props])

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSentMessageSize", [props])


@jsii.implements(IQueue)
class QueueBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-sqs.QueueBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _QueueBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(QueueBase, self, [scope, id])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="asBucketNotificationDestination")
    def as_bucket_notification_destination(self, bucket_arn: str, bucket_id: str) -> aws_cdk.aws_s3_notifications.BucketNotificationDestinationProps:
        return jsii.invoke(self, "asBucketNotificationDestination", [bucket_arn, bucket_id])

    @jsii.member(jsii_name="asLifecycleHookTarget")
    def as_lifecycle_hook_target(self, lifecycle_hook: aws_cdk.aws_autoscaling_api.ILifecycleHook) -> aws_cdk.aws_autoscaling_api.LifecycleHookTargetProps:
        return jsii.invoke(self, "asLifecycleHookTarget", [lifecycle_hook])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "QueueImportProps":
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantConsumeMessages")
    def grant_consume_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantConsumeMessages", [grantee])

    @jsii.member(jsii_name="grantPurge")
    def grant_purge(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantPurge", [grantee])

    @jsii.member(jsii_name="grantSendMessages")
    def grant_send_messages(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantSendMessages", [grantee])

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

    @jsii.member(jsii_name="metricApproximateAgeOfOldestMessage")
    def metric_approximate_age_of_oldest_message(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricApproximateAgeOfOldestMessage", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesDelayed")
    def metric_approximate_number_of_messages_delayed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricApproximateNumberOfMessagesDelayed", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesNotVisible")
    def metric_approximate_number_of_messages_not_visible(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricApproximateNumberOfMessagesNotVisible", [props])

    @jsii.member(jsii_name="metricApproximateNumberOfMessagesVisible")
    def metric_approximate_number_of_messages_visible(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricApproximateNumberOfMessagesVisible", [props])

    @jsii.member(jsii_name="metricNumberOfEmptyReceives")
    def metric_number_of_empty_receives(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfEmptyReceives", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesDeleted")
    def metric_number_of_messages_deleted(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfMessagesDeleted", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesReceived")
    def metric_number_of_messages_received(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfMessagesReceived", [props])

    @jsii.member(jsii_name="metricNumberOfMessagesSent")
    def metric_number_of_messages_sent(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricNumberOfMessagesSent", [props])

    @jsii.member(jsii_name="metricSentMessageSize")
    def metric_sent_message_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
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

        return jsii.invoke(self, "metricSentMessageSize", [props])

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> bool:
        ...

    @property
    @jsii.member(jsii_name="queueArn")
    @abc.abstractmethod
    def queue_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="queueName")
    @abc.abstractmethod
    def queue_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="queueUrl")
    @abc.abstractmethod
    def queue_url(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="encryptionMasterKey")
    @abc.abstractmethod
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        ...


class _QueueBaseProxy(QueueBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "QueueImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        return jsii.get(self, "autoCreatePolicy")

    @property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        return jsii.get(self, "queueArn")

    @property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        return jsii.get(self, "queueName")

    @property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        return jsii.get(self, "queueUrl")

    @property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionMasterKey")


class Queue(QueueBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sqs.Queue"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, content_based_deduplication: typing.Optional[bool]=None, data_key_reuse_sec: typing.Optional[jsii.Number]=None, dead_letter_queue: typing.Optional["DeadLetterQueue"]=None, delivery_delay_sec: typing.Optional[jsii.Number]=None, encryption: typing.Optional["QueueEncryption"]=None, encryption_master_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, fifo: typing.Optional[bool]=None, max_message_size_bytes: typing.Optional[jsii.Number]=None, queue_name: typing.Optional[str]=None, receive_message_wait_time_sec: typing.Optional[jsii.Number]=None, retention_period_sec: typing.Optional[jsii.Number]=None, visibility_timeout_sec: typing.Optional[jsii.Number]=None) -> None:
        props: QueueProps = {}

        if content_based_deduplication is not None:
            props["contentBasedDeduplication"] = content_based_deduplication

        if data_key_reuse_sec is not None:
            props["dataKeyReuseSec"] = data_key_reuse_sec

        if dead_letter_queue is not None:
            props["deadLetterQueue"] = dead_letter_queue

        if delivery_delay_sec is not None:
            props["deliveryDelaySec"] = delivery_delay_sec

        if encryption is not None:
            props["encryption"] = encryption

        if encryption_master_key is not None:
            props["encryptionMasterKey"] = encryption_master_key

        if fifo is not None:
            props["fifo"] = fifo

        if max_message_size_bytes is not None:
            props["maxMessageSizeBytes"] = max_message_size_bytes

        if queue_name is not None:
            props["queueName"] = queue_name

        if receive_message_wait_time_sec is not None:
            props["receiveMessageWaitTimeSec"] = receive_message_wait_time_sec

        if retention_period_sec is not None:
            props["retentionPeriodSec"] = retention_period_sec

        if visibility_timeout_sec is not None:
            props["visibilityTimeoutSec"] = visibility_timeout_sec

        jsii.create(Queue, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, queue_arn: str, queue_url: str, key_arn: typing.Optional[str]=None, queue_name: typing.Optional[str]=None) -> "IQueue":
        props: QueueImportProps = {"queueArn": queue_arn, "queueUrl": queue_url}

        if key_arn is not None:
            props["keyArn"] = key_arn

        if queue_name is not None:
            props["queueName"] = queue_name

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "QueueImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        return jsii.get(self, "autoCreatePolicy")

    @property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        return jsii.get(self, "queueArn")

    @property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        return jsii.get(self, "queueName")

    @property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        return jsii.get(self, "queueUrl")

    @property
    @jsii.member(jsii_name="encryptionMasterKey")
    def encryption_master_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionMasterKey")


@jsii.enum(jsii_type="@aws-cdk/aws-sqs.QueueEncryption")
class QueueEncryption(enum.Enum):
    Unencrypted = "Unencrypted"
    KmsManaged = "KmsManaged"
    Kms = "Kms"

class _QueueImportProps(jsii.compat.TypedDict, total=False):
    keyArn: str
    queueName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.QueueImportProps")
class QueueImportProps(_QueueImportProps):
    queueArn: str
    queueUrl: str

class QueuePolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sqs.QueuePolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, queues: typing.List["IQueue"]) -> None:
        props: QueuePolicyProps = {"queues": queues}

        jsii.create(QueuePolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="document")
    def document(self) -> aws_cdk.aws_iam.PolicyDocument:
        return jsii.get(self, "document")


@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.QueuePolicyProps")
class QueuePolicyProps(jsii.compat.TypedDict):
    queues: typing.List["IQueue"]

@jsii.data_type(jsii_type="@aws-cdk/aws-sqs.QueueProps")
class QueueProps(jsii.compat.TypedDict, total=False):
    contentBasedDeduplication: bool
    dataKeyReuseSec: jsii.Number
    deadLetterQueue: "DeadLetterQueue"
    deliveryDelaySec: jsii.Number
    encryption: "QueueEncryption"
    encryptionMasterKey: aws_cdk.aws_kms.IEncryptionKey
    fifo: bool
    maxMessageSizeBytes: jsii.Number
    queueName: str
    receiveMessageWaitTimeSec: jsii.Number
    retentionPeriodSec: jsii.Number
    visibilityTimeoutSec: jsii.Number

__all__ = ["CfnQueue", "CfnQueuePolicy", "CfnQueuePolicyProps", "CfnQueueProps", "DeadLetterQueue", "IQueue", "Queue", "QueueBase", "QueueEncryption", "QueueImportProps", "QueuePolicy", "QueuePolicyProps", "QueueProps", "__jsii_assembly__"]

publication.publish()
