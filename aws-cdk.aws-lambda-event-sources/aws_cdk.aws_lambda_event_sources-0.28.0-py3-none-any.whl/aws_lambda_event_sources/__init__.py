import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_apigateway
import aws_cdk.aws_dynamodb
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kinesis
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-lambda-event-sources", "0.28.0", __name__, "aws-lambda-event-sources@0.28.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class ApiEventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.ApiEventSource"):
    def __init__(self, method: str, path: str, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional[aws_cdk.aws_apigateway.AuthorizationType]=None, authorizer_id: typing.Optional[str]=None, method_responses: typing.Optional[typing.List[aws_cdk.aws_apigateway.MethodResponse]]=None, operation_name: typing.Optional[str]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None) -> None:
        options: aws_cdk.aws_apigateway.MethodOptions = {}

        if api_key_required is not None:
            options["apiKeyRequired"] = api_key_required

        if authorization_type is not None:
            options["authorizationType"] = authorization_type

        if authorizer_id is not None:
            options["authorizerId"] = authorizer_id

        if method_responses is not None:
            options["methodResponses"] = method_responses

        if operation_name is not None:
            options["operationName"] = operation_name

        if request_parameters is not None:
            options["requestParameters"] = request_parameters

        jsii.create(ApiEventSource, self, [method, path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.FunctionBase) -> None:
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="method")
    def method(self) -> str:
        return jsii.get(self, "method")

    @property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        return jsii.get(self, "path")

    @property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Optional[aws_cdk.aws_apigateway.MethodOptions]:
        return jsii.get(self, "options")


@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class DynamoEventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.DynamoEventSource"):
    def __init__(self, table: aws_cdk.aws_dynamodb.Table, *, starting_position: aws_cdk.aws_lambda.StartingPosition, batch_size: typing.Optional[jsii.Number]=None) -> None:
        props: DynamoEventSourceProps = {"startingPosition": starting_position}

        if batch_size is not None:
            props["batchSize"] = batch_size

        jsii.create(DynamoEventSource, self, [table, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.FunctionBase) -> None:
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "DynamoEventSourceProps":
        return jsii.get(self, "props")

    @property
    @jsii.member(jsii_name="table")
    def table(self) -> aws_cdk.aws_dynamodb.Table:
        return jsii.get(self, "table")


class _DynamoEventSourceProps(jsii.compat.TypedDict, total=False):
    batchSize: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.DynamoEventSourceProps")
class DynamoEventSourceProps(_DynamoEventSourceProps):
    startingPosition: aws_cdk.aws_lambda.StartingPosition

@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class KinesisEventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.KinesisEventSource"):
    def __init__(self, stream: aws_cdk.aws_kinesis.IStream, *, starting_position: aws_cdk.aws_lambda.StartingPosition, batch_size: typing.Optional[jsii.Number]=None) -> None:
        props: KinesisEventSourceProps = {"startingPosition": starting_position}

        if batch_size is not None:
            props["batchSize"] = batch_size

        jsii.create(KinesisEventSource, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.FunctionBase) -> None:
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "KinesisEventSourceProps":
        return jsii.get(self, "props")

    @property
    @jsii.member(jsii_name="stream")
    def stream(self) -> aws_cdk.aws_kinesis.IStream:
        return jsii.get(self, "stream")


class _KinesisEventSourceProps(jsii.compat.TypedDict, total=False):
    batchSize: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.KinesisEventSourceProps")
class KinesisEventSourceProps(_KinesisEventSourceProps):
    startingPosition: aws_cdk.aws_lambda.StartingPosition

@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class S3EventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.S3EventSource"):
    def __init__(self, bucket: aws_cdk.aws_s3.Bucket, *, events: typing.List[aws_cdk.aws_s3.EventType], filters: typing.Optional[typing.List[aws_cdk.aws_s3.NotificationKeyFilter]]=None) -> None:
        props: S3EventSourceProps = {"events": events}

        if filters is not None:
            props["filters"] = filters

        jsii.create(S3EventSource, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.FunctionBase) -> None:
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.Bucket:
        return jsii.get(self, "bucket")

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "S3EventSourceProps":
        return jsii.get(self, "props")


class _S3EventSourceProps(jsii.compat.TypedDict, total=False):
    filters: typing.List[aws_cdk.aws_s3.NotificationKeyFilter]

@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.S3EventSourceProps")
class S3EventSourceProps(_S3EventSourceProps):
    events: typing.List[aws_cdk.aws_s3.EventType]

@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class SnsEventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.SnsEventSource"):
    def __init__(self, topic: aws_cdk.aws_sns.ITopic) -> None:
        jsii.create(SnsEventSource, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.FunctionBase) -> None:
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="topic")
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        return jsii.get(self, "topic")


@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class SqsEventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.SqsEventSource"):
    def __init__(self, queue: aws_cdk.aws_sqs.IQueue, *, batch_size: typing.Optional[jsii.Number]=None) -> None:
        props: SqsEventSourceProps = {}

        if batch_size is not None:
            props["batchSize"] = batch_size

        jsii.create(SqsEventSource, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.FunctionBase) -> None:
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "SqsEventSourceProps":
        return jsii.get(self, "props")

    @property
    @jsii.member(jsii_name="queue")
    def queue(self) -> aws_cdk.aws_sqs.IQueue:
        return jsii.get(self, "queue")


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.SqsEventSourceProps")
class SqsEventSourceProps(jsii.compat.TypedDict, total=False):
    batchSize: jsii.Number

__all__ = ["ApiEventSource", "DynamoEventSource", "DynamoEventSourceProps", "KinesisEventSource", "KinesisEventSourceProps", "S3EventSource", "S3EventSourceProps", "SnsEventSource", "SqsEventSource", "SqsEventSourceProps", "__jsii_assembly__"]

publication.publish()
