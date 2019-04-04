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
import aws_cdk.aws_logs
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloudtrail", "0.28.0", __name__, "aws-cloudtrail@0.28.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-cloudtrail.AddS3EventSelectorOptions")
class AddS3EventSelectorOptions(jsii.compat.TypedDict, total=False):
    includeManagementEvents: bool
    readWriteType: "ReadWriteType"

class CfnTrail(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudtrail.CfnTrail"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, is_logging: typing.Union[bool, aws_cdk.cdk.Token], s3_bucket_name: str, cloud_watch_logs_log_group_arn: typing.Optional[str]=None, cloud_watch_logs_role_arn: typing.Optional[str]=None, enable_log_file_validation: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, event_selectors: typing.Optional[typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "EventSelectorProperty"]]]]=None, include_global_service_events: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, is_multi_region_trail: typing.Optional[typing.Union[bool, aws_cdk.cdk.Token]]=None, kms_key_id: typing.Optional[str]=None, s3_key_prefix: typing.Optional[str]=None, sns_topic_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, trail_name: typing.Optional[str]=None) -> None:
        props: CfnTrailProps = {"isLogging": is_logging, "s3BucketName": s3_bucket_name}

        if cloud_watch_logs_log_group_arn is not None:
            props["cloudWatchLogsLogGroupArn"] = cloud_watch_logs_log_group_arn

        if cloud_watch_logs_role_arn is not None:
            props["cloudWatchLogsRoleArn"] = cloud_watch_logs_role_arn

        if enable_log_file_validation is not None:
            props["enableLogFileValidation"] = enable_log_file_validation

        if event_selectors is not None:
            props["eventSelectors"] = event_selectors

        if include_global_service_events is not None:
            props["includeGlobalServiceEvents"] = include_global_service_events

        if is_multi_region_trail is not None:
            props["isMultiRegionTrail"] = is_multi_region_trail

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if s3_key_prefix is not None:
            props["s3KeyPrefix"] = s3_key_prefix

        if sns_topic_name is not None:
            props["snsTopicName"] = sns_topic_name

        if tags is not None:
            props["tags"] = tags

        if trail_name is not None:
            props["trailName"] = trail_name

        jsii.create(CfnTrail, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnTrailProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="trailArn")
    def trail_arn(self) -> str:
        return jsii.get(self, "trailArn")

    @property
    @jsii.member(jsii_name="trailName")
    def trail_name(self) -> str:
        return jsii.get(self, "trailName")

    @property
    @jsii.member(jsii_name="trailSnsTopicArn")
    def trail_sns_topic_arn(self) -> str:
        return jsii.get(self, "trailSnsTopicArn")

    class _DataResourceProperty(jsii.compat.TypedDict, total=False):
        values: typing.List[str]

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudtrail.CfnTrail.DataResourceProperty")
    class DataResourceProperty(_DataResourceProperty):
        type: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudtrail.CfnTrail.EventSelectorProperty")
    class EventSelectorProperty(jsii.compat.TypedDict, total=False):
        dataResources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTrail.DataResourceProperty"]]]
        includeManagementEvents: typing.Union[bool, aws_cdk.cdk.Token]
        readWriteType: str


class _CfnTrailProps(jsii.compat.TypedDict, total=False):
    cloudWatchLogsLogGroupArn: str
    cloudWatchLogsRoleArn: str
    enableLogFileValidation: typing.Union[bool, aws_cdk.cdk.Token]
    eventSelectors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTrail.EventSelectorProperty"]]]
    includeGlobalServiceEvents: typing.Union[bool, aws_cdk.cdk.Token]
    isMultiRegionTrail: typing.Union[bool, aws_cdk.cdk.Token]
    kmsKeyId: str
    s3KeyPrefix: str
    snsTopicName: str
    tags: typing.List[aws_cdk.cdk.CfnTag]
    trailName: str

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudtrail.CfnTrailProps")
class CfnTrailProps(_CfnTrailProps):
    isLogging: typing.Union[bool, aws_cdk.cdk.Token]
    s3BucketName: str

class CloudTrail(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudtrail.CloudTrail"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cloud_watch_logs_retention_time_days: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, enable_file_validation: typing.Optional[bool]=None, include_global_service_events: typing.Optional[bool]=None, is_multi_region_trail: typing.Optional[bool]=None, kms_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, management_events: typing.Optional["ReadWriteType"]=None, s3_key_prefix: typing.Optional[str]=None, send_to_cloud_watch_logs: typing.Optional[bool]=None, sns_topic: typing.Optional[str]=None, trail_name: typing.Optional[str]=None) -> None:
        props: CloudTrailProps = {}

        if cloud_watch_logs_retention_time_days is not None:
            props["cloudWatchLogsRetentionTimeDays"] = cloud_watch_logs_retention_time_days

        if enable_file_validation is not None:
            props["enableFileValidation"] = enable_file_validation

        if include_global_service_events is not None:
            props["includeGlobalServiceEvents"] = include_global_service_events

        if is_multi_region_trail is not None:
            props["isMultiRegionTrail"] = is_multi_region_trail

        if kms_key is not None:
            props["kmsKey"] = kms_key

        if management_events is not None:
            props["managementEvents"] = management_events

        if s3_key_prefix is not None:
            props["s3KeyPrefix"] = s3_key_prefix

        if send_to_cloud_watch_logs is not None:
            props["sendToCloudWatchLogs"] = send_to_cloud_watch_logs

        if sns_topic is not None:
            props["snsTopic"] = sns_topic

        if trail_name is not None:
            props["trailName"] = trail_name

        jsii.create(CloudTrail, self, [scope, id, props])

    @jsii.member(jsii_name="addS3EventSelector")
    def add_s3_event_selector(self, prefixes: typing.List[str], *, include_management_events: typing.Optional[bool]=None, read_write_type: typing.Optional["ReadWriteType"]=None) -> None:
        options: AddS3EventSelectorOptions = {}

        if include_management_events is not None:
            options["includeManagementEvents"] = include_management_events

        if read_write_type is not None:
            options["readWriteType"] = read_write_type

        return jsii.invoke(self, "addS3EventSelector", [prefixes, options])

    @property
    @jsii.member(jsii_name="cloudTrailArn")
    def cloud_trail_arn(self) -> str:
        return jsii.get(self, "cloudTrailArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudtrail.CloudTrailProps")
class CloudTrailProps(jsii.compat.TypedDict, total=False):
    cloudWatchLogsRetentionTimeDays: aws_cdk.aws_logs.RetentionDays
    enableFileValidation: bool
    includeGlobalServiceEvents: bool
    isMultiRegionTrail: bool
    kmsKey: aws_cdk.aws_kms.IEncryptionKey
    managementEvents: "ReadWriteType"
    s3KeyPrefix: str
    sendToCloudWatchLogs: bool
    snsTopic: str
    trailName: str

@jsii.enum(jsii_type="@aws-cdk/aws-cloudtrail.ReadWriteType")
class ReadWriteType(enum.Enum):
    ReadOnly = "ReadOnly"
    WriteOnly = "WriteOnly"
    All = "All"

__all__ = ["AddS3EventSelectorOptions", "CfnTrail", "CfnTrailProps", "CloudTrail", "CloudTrailProps", "ReadWriteType", "__jsii_assembly__"]

publication.publish()
