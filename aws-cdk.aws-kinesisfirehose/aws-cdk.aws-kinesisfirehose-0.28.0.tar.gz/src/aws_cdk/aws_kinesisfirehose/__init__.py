import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-kinesisfirehose", "0.28.0", __name__, "aws-kinesisfirehose@0.28.0.jsii.tgz")
class CfnDeliveryStream(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, delivery_stream_name: typing.Optional[str]=None, delivery_stream_type: typing.Optional[str]=None, elasticsearch_destination_configuration: typing.Optional[typing.Union["ElasticsearchDestinationConfigurationProperty", aws_cdk.cdk.Token]]=None, extended_s3_destination_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "ExtendedS3DestinationConfigurationProperty"]]=None, kinesis_stream_source_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "KinesisStreamSourceConfigurationProperty"]]=None, redshift_destination_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "RedshiftDestinationConfigurationProperty"]]=None, s3_destination_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "S3DestinationConfigurationProperty"]]=None, splunk_destination_configuration: typing.Optional[typing.Union[aws_cdk.cdk.Token, "SplunkDestinationConfigurationProperty"]]=None) -> None:
        props: CfnDeliveryStreamProps = {}

        if delivery_stream_name is not None:
            props["deliveryStreamName"] = delivery_stream_name

        if delivery_stream_type is not None:
            props["deliveryStreamType"] = delivery_stream_type

        if elasticsearch_destination_configuration is not None:
            props["elasticsearchDestinationConfiguration"] = elasticsearch_destination_configuration

        if extended_s3_destination_configuration is not None:
            props["extendedS3DestinationConfiguration"] = extended_s3_destination_configuration

        if kinesis_stream_source_configuration is not None:
            props["kinesisStreamSourceConfiguration"] = kinesis_stream_source_configuration

        if redshift_destination_configuration is not None:
            props["redshiftDestinationConfiguration"] = redshift_destination_configuration

        if s3_destination_configuration is not None:
            props["s3DestinationConfiguration"] = s3_destination_configuration

        if splunk_destination_configuration is not None:
            props["splunkDestinationConfiguration"] = splunk_destination_configuration

        jsii.create(CfnDeliveryStream, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> str:
        return jsii.get(self, "deliveryStreamArn")

    @property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> str:
        return jsii.get(self, "deliveryStreamName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeliveryStreamProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.BufferingHintsProperty")
    class BufferingHintsProperty(jsii.compat.TypedDict):
        intervalInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        sizeInMBs: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.CloudWatchLoggingOptionsProperty")
    class CloudWatchLoggingOptionsProperty(jsii.compat.TypedDict, total=False):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        logGroupName: str
        logStreamName: str

    class _CopyCommandProperty(jsii.compat.TypedDict, total=False):
        copyOptions: str
        dataTableColumns: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.CopyCommandProperty")
    class CopyCommandProperty(_CopyCommandProperty):
        dataTableName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchBufferingHintsProperty")
    class ElasticsearchBufferingHintsProperty(jsii.compat.TypedDict):
        intervalInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        sizeInMBs: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    class _ElasticsearchDestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        processingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessingConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty")
    class ElasticsearchDestinationConfigurationProperty(_ElasticsearchDestinationConfigurationProperty):
        bufferingHints: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ElasticsearchBufferingHintsProperty"]
        domainArn: str
        indexName: str
        indexRotationPeriod: str
        retryOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ElasticsearchRetryOptionsProperty"]
        roleArn: str
        s3BackupMode: str
        s3Configuration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
        typeName: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchRetryOptionsProperty")
    class ElasticsearchRetryOptionsProperty(jsii.compat.TypedDict):
        durationInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.EncryptionConfigurationProperty")
    class EncryptionConfigurationProperty(jsii.compat.TypedDict, total=False):
        kmsEncryptionConfig: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.KMSEncryptionConfigProperty"]
        noEncryptionConfig: str

    class _ExtendedS3DestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        encryptionConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.EncryptionConfigurationProperty"]
        processingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessingConfigurationProperty"]
        s3BackupConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
        s3BackupMode: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty")
    class ExtendedS3DestinationConfigurationProperty(_ExtendedS3DestinationConfigurationProperty):
        bucketArn: str
        bufferingHints: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.BufferingHintsProperty"]
        compressionFormat: str
        prefix: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.KMSEncryptionConfigProperty")
    class KMSEncryptionConfigProperty(jsii.compat.TypedDict):
        awskmsKeyArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty")
    class KinesisStreamSourceConfigurationProperty(jsii.compat.TypedDict):
        kinesisStreamArn: str
        roleArn: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty")
    class ProcessingConfigurationProperty(jsii.compat.TypedDict, total=False):
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        processors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessorProperty"]]]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessorParameterProperty")
    class ProcessorParameterProperty(jsii.compat.TypedDict):
        parameterName: str
        parameterValue: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessorProperty")
    class ProcessorProperty(jsii.compat.TypedDict):
        parameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessorParameterProperty"]]]
        type: str

    class _RedshiftDestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        processingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessingConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.RedshiftDestinationConfigurationProperty")
    class RedshiftDestinationConfigurationProperty(_RedshiftDestinationConfigurationProperty):
        clusterJdbcurl: str
        copyCommand: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CopyCommandProperty"]
        password: str
        roleArn: str
        s3Configuration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
        username: str

    class _S3DestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        encryptionConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.EncryptionConfigurationProperty"]
        prefix: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty")
    class S3DestinationConfigurationProperty(_S3DestinationConfigurationProperty):
        bucketArn: str
        bufferingHints: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.BufferingHintsProperty"]
        compressionFormat: str
        roleArn: str

    class _SplunkDestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        hecAcknowledgmentTimeoutInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        processingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessingConfigurationProperty"]
        retryOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.SplunkRetryOptionsProperty"]
        s3BackupMode: str

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.SplunkDestinationConfigurationProperty")
    class SplunkDestinationConfigurationProperty(_SplunkDestinationConfigurationProperty):
        hecEndpoint: str
        hecEndpointType: str
        hecToken: str
        s3Configuration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.SplunkRetryOptionsProperty")
    class SplunkRetryOptionsProperty(jsii.compat.TypedDict):
        durationInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStreamProps")
class CfnDeliveryStreamProps(jsii.compat.TypedDict, total=False):
    deliveryStreamName: str
    deliveryStreamType: str
    elasticsearchDestinationConfiguration: typing.Union["CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty", aws_cdk.cdk.Token]
    extendedS3DestinationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty"]
    kinesisStreamSourceConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.KinesisStreamSourceConfigurationProperty"]
    redshiftDestinationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.RedshiftDestinationConfigurationProperty"]
    s3DestinationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
    splunkDestinationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.SplunkDestinationConfigurationProperty"]

__all__ = ["CfnDeliveryStream", "CfnDeliveryStreamProps", "__jsii_assembly__"]

publication.publish()
