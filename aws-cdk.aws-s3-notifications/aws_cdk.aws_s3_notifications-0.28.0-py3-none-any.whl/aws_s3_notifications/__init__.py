import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-s3-notifications", "0.28.0", __name__, "aws-s3-notifications@0.28.0.jsii.tgz")
class _BucketNotificationDestinationProps(jsii.compat.TypedDict, total=False):
    dependencies: typing.List[aws_cdk.cdk.IDependable]

@jsii.data_type(jsii_type="@aws-cdk/aws-s3-notifications.BucketNotificationDestinationProps")
class BucketNotificationDestinationProps(_BucketNotificationDestinationProps):
    arn: str
    type: "BucketNotificationDestinationType"

@jsii.enum(jsii_type="@aws-cdk/aws-s3-notifications.BucketNotificationDestinationType")
class BucketNotificationDestinationType(enum.Enum):
    Lambda = "Lambda"
    Queue = "Queue"
    Topic = "Topic"

@jsii.interface(jsii_type="@aws-cdk/aws-s3-notifications.IBucketNotificationDestination")
class IBucketNotificationDestination(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IBucketNotificationDestinationProxy

    @jsii.member(jsii_name="asBucketNotificationDestination")
    def as_bucket_notification_destination(self, bucket_arn: str, bucket_id: str) -> "BucketNotificationDestinationProps":
        ...


class _IBucketNotificationDestinationProxy():
    __jsii_type__ = "@aws-cdk/aws-s3-notifications.IBucketNotificationDestination"
    @jsii.member(jsii_name="asBucketNotificationDestination")
    def as_bucket_notification_destination(self, bucket_arn: str, bucket_id: str) -> "BucketNotificationDestinationProps":
        return jsii.invoke(self, "asBucketNotificationDestination", [bucket_arn, bucket_id])


__all__ = ["BucketNotificationDestinationProps", "BucketNotificationDestinationType", "IBucketNotificationDestination", "__jsii_assembly__"]

publication.publish()
