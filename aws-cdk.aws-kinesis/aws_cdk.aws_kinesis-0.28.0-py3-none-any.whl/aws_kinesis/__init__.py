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
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-kinesis", "0.28.0", __name__, "aws-kinesis@0.28.0.jsii.tgz")
class CfnStream(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesis.CfnStream"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, shard_count: typing.Union[jsii.Number, aws_cdk.cdk.Token], name: typing.Optional[str]=None, retention_period_hours: typing.Optional[typing.Union[jsii.Number, aws_cdk.cdk.Token]]=None, stream_encryption: typing.Optional[typing.Union[aws_cdk.cdk.Token, "StreamEncryptionProperty"]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        props: CfnStreamProps = {"shardCount": shard_count}

        if name is not None:
            props["name"] = name

        if retention_period_hours is not None:
            props["retentionPeriodHours"] = retention_period_hours

        if stream_encryption is not None:
            props["streamEncryption"] = stream_encryption

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnStream, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStreamProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        return jsii.get(self, "streamArn")

    @property
    @jsii.member(jsii_name="streamId")
    def stream_id(self) -> str:
        return jsii.get(self, "streamId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.CfnStream.StreamEncryptionProperty")
    class StreamEncryptionProperty(jsii.compat.TypedDict):
        encryptionType: str
        keyId: str


class CfnStreamConsumer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesis.CfnStreamConsumer"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, consumer_name: str, stream_arn: str) -> None:
        props: CfnStreamConsumerProps = {"consumerName": consumer_name, "streamArn": stream_arn}

        jsii.create(CfnStreamConsumer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStreamConsumerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="streamConsumerArn")
    def stream_consumer_arn(self) -> str:
        return jsii.get(self, "streamConsumerArn")

    @property
    @jsii.member(jsii_name="streamConsumerConsumerArn")
    def stream_consumer_consumer_arn(self) -> str:
        return jsii.get(self, "streamConsumerConsumerArn")

    @property
    @jsii.member(jsii_name="streamConsumerConsumerCreationTimestamp")
    def stream_consumer_consumer_creation_timestamp(self) -> str:
        return jsii.get(self, "streamConsumerConsumerCreationTimestamp")

    @property
    @jsii.member(jsii_name="streamConsumerConsumerName")
    def stream_consumer_consumer_name(self) -> str:
        return jsii.get(self, "streamConsumerConsumerName")

    @property
    @jsii.member(jsii_name="streamConsumerConsumerStatus")
    def stream_consumer_consumer_status(self) -> str:
        return jsii.get(self, "streamConsumerConsumerStatus")

    @property
    @jsii.member(jsii_name="streamConsumerStreamArn")
    def stream_consumer_stream_arn(self) -> str:
        return jsii.get(self, "streamConsumerStreamArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.CfnStreamConsumerProps")
class CfnStreamConsumerProps(jsii.compat.TypedDict):
    consumerName: str
    streamArn: str

class _CfnStreamProps(jsii.compat.TypedDict, total=False):
    name: str
    retentionPeriodHours: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    streamEncryption: typing.Union[aws_cdk.cdk.Token, "CfnStream.StreamEncryptionProperty"]
    tags: typing.List[aws_cdk.cdk.CfnTag]

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.CfnStreamProps")
class CfnStreamProps(_CfnStreamProps):
    shardCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]

@jsii.interface(jsii_type="@aws-cdk/aws-kinesis.IStream")
class IStream(aws_cdk.cdk.IConstruct, aws_cdk.aws_logs.ILogSubscriptionDestination, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IStreamProxy

    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "StreamImportProps":
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        ...


class _IStreamProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct), jsii.proxy_for(aws_cdk.aws_logs.ILogSubscriptionDestination)):
    __jsii_type__ = "@aws-cdk/aws-kinesis.IStream"
    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        return jsii.get(self, "streamArn")

    @property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> str:
        return jsii.get(self, "streamName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")

    @jsii.member(jsii_name="export")
    def export(self) -> "StreamImportProps":
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantReadWrite", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [grantee])


@jsii.implements(IStream)
class StreamBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-kinesis.StreamBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _StreamBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        jsii.create(StreamBase, self, [scope, id])

    @jsii.member(jsii_name="export")
    @abc.abstractmethod
    def export(self) -> "StreamImportProps":
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantReadWrite", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="logSubscriptionDestination")
    def log_subscription_destination(self, source_log_group: aws_cdk.aws_logs.ILogGroup) -> aws_cdk.aws_logs.LogSubscriptionDestination:
        return jsii.invoke(self, "logSubscriptionDestination", [source_log_group])

    @property
    @jsii.member(jsii_name="streamArn")
    @abc.abstractmethod
    def stream_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="streamName")
    @abc.abstractmethod
    def stream_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="encryptionKey")
    @abc.abstractmethod
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        ...


class _StreamBaseProxy(StreamBase):
    @jsii.member(jsii_name="export")
    def export(self) -> "StreamImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        return jsii.get(self, "streamArn")

    @property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> str:
        return jsii.get(self, "streamName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")


class Stream(StreamBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesis.Stream"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, encryption: typing.Optional["StreamEncryption"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IEncryptionKey]=None, retention_period_hours: typing.Optional[jsii.Number]=None, shard_count: typing.Optional[jsii.Number]=None, stream_name: typing.Optional[str]=None) -> None:
        props: StreamProps = {}

        if encryption is not None:
            props["encryption"] = encryption

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if retention_period_hours is not None:
            props["retentionPeriodHours"] = retention_period_hours

        if shard_count is not None:
            props["shardCount"] = shard_count

        if stream_name is not None:
            props["streamName"] = stream_name

        jsii.create(Stream, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, stream_arn: str, encryption_key: typing.Optional[aws_cdk.aws_kms.EncryptionKeyImportProps]=None) -> "IStream":
        props: StreamImportProps = {"streamArn": stream_arn}

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="export")
    def export(self) -> "StreamImportProps":
        return jsii.invoke(self, "export", [])

    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        return jsii.get(self, "streamArn")

    @property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> str:
        return jsii.get(self, "streamName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IEncryptionKey]:
        return jsii.get(self, "encryptionKey")


@jsii.enum(jsii_type="@aws-cdk/aws-kinesis.StreamEncryption")
class StreamEncryption(enum.Enum):
    Unencrypted = "Unencrypted"
    Kms = "Kms"

class _StreamImportProps(jsii.compat.TypedDict, total=False):
    encryptionKey: aws_cdk.aws_kms.EncryptionKeyImportProps

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.StreamImportProps")
class StreamImportProps(_StreamImportProps):
    streamArn: str

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.StreamProps")
class StreamProps(jsii.compat.TypedDict, total=False):
    encryption: "StreamEncryption"
    encryptionKey: aws_cdk.aws_kms.IEncryptionKey
    retentionPeriodHours: jsii.Number
    shardCount: jsii.Number
    streamName: str

__all__ = ["CfnStream", "CfnStreamConsumer", "CfnStreamConsumerProps", "CfnStreamProps", "IStream", "Stream", "StreamBase", "StreamEncryption", "StreamImportProps", "StreamProps", "__jsii_assembly__"]

publication.publish()
