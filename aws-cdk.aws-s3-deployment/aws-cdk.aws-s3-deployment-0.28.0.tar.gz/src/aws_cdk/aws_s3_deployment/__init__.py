import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.assets
import aws_cdk.aws_cloudformation
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-s3-deployment", "0.28.0", __name__, "aws-s3-deployment@0.28.0.jsii.tgz")
class BucketDeployment(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.BucketDeployment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, destination_bucket: aws_cdk.aws_s3.IBucket, source: "ISource", destination_key_prefix: typing.Optional[str]=None, retain_on_delete: typing.Optional[bool]=None) -> None:
        props: BucketDeploymentProps = {"destinationBucket": destination_bucket, "source": source}

        if destination_key_prefix is not None:
            props["destinationKeyPrefix"] = destination_key_prefix

        if retain_on_delete is not None:
            props["retainOnDelete"] = retain_on_delete

        jsii.create(BucketDeployment, self, [scope, id, props])


class _BucketDeploymentProps(jsii.compat.TypedDict, total=False):
    destinationKeyPrefix: str
    retainOnDelete: bool

@jsii.data_type(jsii_type="@aws-cdk/aws-s3-deployment.BucketDeploymentProps")
class BucketDeploymentProps(_BucketDeploymentProps):
    destinationBucket: aws_cdk.aws_s3.IBucket
    source: "ISource"

@jsii.interface(jsii_type="@aws-cdk/aws-s3-deployment.ISource")
class ISource(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISourceProxy

    @jsii.member(jsii_name="bind")
    def bind(self, context: aws_cdk.cdk.Construct) -> "SourceProps":
        ...


class _ISourceProxy():
    __jsii_type__ = "@aws-cdk/aws-s3-deployment.ISource"
    @jsii.member(jsii_name="bind")
    def bind(self, context: aws_cdk.cdk.Construct) -> "SourceProps":
        return jsii.invoke(self, "bind", [context])


class Source(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.Source"):
    @jsii.member(jsii_name="asset")
    @classmethod
    def asset(cls, path: str) -> "ISource":
        return jsii.sinvoke(cls, "asset", [path])

    @jsii.member(jsii_name="bucket")
    @classmethod
    def bucket(cls, bucket: aws_cdk.aws_s3.IBucket, zip_object_key: str) -> "ISource":
        return jsii.sinvoke(cls, "bucket", [bucket, zip_object_key])


@jsii.data_type(jsii_type="@aws-cdk/aws-s3-deployment.SourceProps")
class SourceProps(jsii.compat.TypedDict):
    bucket: aws_cdk.aws_s3.IBucket
    zipObjectKey: str

__all__ = ["BucketDeployment", "BucketDeploymentProps", "ISource", "Source", "SourceProps", "__jsii_assembly__"]

publication.publish()
