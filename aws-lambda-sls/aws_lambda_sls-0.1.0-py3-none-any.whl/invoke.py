# coding:utf-8
import json
import base64
import logging
from botocore.config import Config
from aws_lambda_sls.compat import to_unicode, to_byte
from aws_lambda_sls.awsclient import AWSClient
from boto3.session import Session

logger = logging.getLogger(__name__)


class AwsServiceRequestError(Exception):
    pass


class ExpiredIteratorException(Exception):
    pass


def lambda_context(custom=None, env=None, client=None):
    if custom is not None:
        assert isinstance(custom, dict)
    if env is not None:
        assert isinstance(custom, dict)
    client_context = dict(
        custom=custom or {},
        env=env or {},
        client=client or {})
    json_context = to_byte(json.dumps(client_context))
    return to_unicode(base64.b64encode(json_context))


class FunctionInvoke(object):
    def __init__(self, lambda_service, function_name):
        self._lambda_service = lambda_service
        self._function_name = function_name
        self._custom = {}
        self._env = {}
        self._payload = {}

    def custom(self, **kwargs):
        self._custom.update(kwargs)
        return self

    def env(self, **kwargs):
        self._env.update(kwargs)
        return self

    def payload(self, **kwargs):
        self._payload.update(kwargs)
        return self

    def invoke(self, **payload):
        self._payload.update(payload)
        return self._lambda_service.invoke(
            self._function_name,
            payload=self._payload,
            custom=self._custom,
            env=self._env
        )


class AwsService(object):
    def __init__(self,
                 service_name,
                 aws_params=None,
                 profile=None,
                 connect_timeout=60,
                 read_timeout=60,
                 max_attempts=3,
                 **config_kwargs):
        """
        lambda service basic service.
        :param service_name: support the lambda service name to invoke,
                             it actually means a lambda function in aws.
        :param aws_params: AWS secret config
        :param profile: The name of the profile to use for this
            session.  Note that the profile can only be set when
            the session is created.
        :param read_timeout: invoke lambda function read timeout.
        :param max_attempts: invoke lambda function max attempts.
        """
        self.service_name = service_name
        self.aws_params = aws_params
        self.profile = profile
        self.config = Config(
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            retries=dict(max_attempts=max_attempts),
            **config_kwargs
        )
        self.session = Session(profile_name=profile, **aws_params or {})
        self.aws_client = self.create_aws_client()

    def create_aws_client(self):
        return AWSClient(self.session, config=self.config)


class LambdaService(AwsService):
    def __init__(self,
                 service_name,
                 aws_params=None,
                 profile=None,
                 lambda_url=None,
                 alias="$LATEST",
                 **kwargs):
        """
        lambda service basic service.
        :param service_name: support the lambda service name to invoke,
                             it actually means a lambda function in aws.
        :param alias: you want to invoke the service alias version.
        :param aws_params: AWS secret config
        :param lambda_url: local test lambda url, if you define this url, it means
                           service only visit local lambda service.
        :param profile: The name of the profile to use for this
            session.  Note that the profile can only be set when
            the session is created.
        :param read_timeout: invoke lambda function read timeout.
        :param max_attempts: invoke lambda function max attempts.
        """
        self.alias = alias
        self.lambda_url = lambda_url
        super(LambdaService, self).__init__(service_name, aws_params, profile, **kwargs)

    def create_aws_client(self):
        return AWSClient(self.session, config=self.config, endpoint_url=self.lambda_url)

    def invoke(self, function_name, payload=None, custom=None, env=None):
        """
        invoke your self defined lambda function method.
        :param function_name: your invoke function name
        :param payload: invoke params, dict type
        :param custom: context.client_context.custom params, dict type
        :param env: context.client_context.env params, dict type
        """
        payload = payload or {}
        payload["function_name"] = function_name
        client_context = lambda_context(custom=custom, env=env)
        resp = self.aws_client.invoke(
            self.service_name,
            payload=to_byte(json.dumps(payload)),
            client_context=client_context,
            alias=self.alias
        )
        return json.loads(resp["Payload"].read().decode("utf-8"))

    def __getattr__(self, name):
        return FunctionInvoke(self, name)


class KinesisService(AwsService):
    def __init__(self,
                 service_name,
                 aws_params=None,
                 profile=None,
                 **kwargs):
        """
        lambda service basic service.
        :param service_name: support the lambda service name to invoke,
                             it actually means a lambda function in aws.
        :param alias: you want to invoke the service alias version.
        :param aws_params: AWS secret config
        :param lambda_url: local test lambda url, if you define this url, it means
                           service only visit local lambda service.
        :param profile: The name of the profile to use for this
            session.  Note that the profile can only be set when
            the session is created.
        :param read_timeout: invoke lambda function read timeout.
        :param max_attempts: invoke lambda function max attempts.
        """
        super(KinesisService, self).__init__(service_name, aws_params, profile, **kwargs)

    def push_record(self, data, partition_key="partitionKey"):
        """
        Writes a single data record into an Amazon Kinesis data stream.
        :param data: The data blob to put into the record
        :param partition_key: the stream partition key
        """
        assert isinstance(data, dict)
        return self.aws_client.kinesis_push_record(
            self.service_name, json.dumps(data), partition_key
        )

    def push_records(self, data_records, partition_key="partitionKey"):
        """
        Writes a single data record into an Amazon Kinesis data stream.
        :param data_records: The data blob to put into the record list
        :param partition_key: the stream partition key
        """
        assert isinstance(data_records, (tuple, list))
        return self.aws_client.kinesis_push_records(self.service_name, [dict(
            Data=json.dumps(data),
            PartitionKey=partition_key
        ) for data in data_records])

    def list_shards(self):
        """
        Lists the shards in a stream.
        """
        result = self.aws_client.kinesis_list_shards(self.service_name)
        if result["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise AwsServiceRequestError
        return result["Shards"]

    def get_shard_iterator(self, shard_id, sequence_number=None):
        """
        Gets an Amazon Kinesis shard iterator.
        :param shard_id: The stream shard id
        :param sequence_number: shard sequence number
        """
        result = self.aws_client.kinesis_get_shard_iterator(self.service_name, shard_id, sequence_number)
        if result["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise AwsServiceRequestError
        return result["ShardIterator"]

    def get_records(self, shard_iterator, limit=10000):
        """
        Gets data records from a Kinesis data stream's shard.
        :param shard_iterator: The stream shard iterator
        :param limit: result limit
        """
        try:
            result = self.aws_client.kinesis_get_records(shard_iterator, limit)
            if result["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise AwsServiceRequestError
            return result["NextShardIterator"], result["Records"]
        except Exception as ex:
            if "ExpiredIteratorException" in str(ex):
                raise ExpiredIteratorException
            else:
                raise ex


class S3Service(AwsService):
    def __init__(self,
                 service_name,
                 aws_params=None,
                 profile=None,
                 **kwargs):
        """
        lambda service basic service.
        :param service_name: support the lambda service name to invoke,
                             it actually means a lambda function in aws.
        :param alias: you want to invoke the service alias version.
        :param aws_params: AWS secret config
        :param lambda_url: local test lambda url, if you define this url, it means
                           service only visit local lambda service.
        :param profile: The name of the profile to use for this
            session.  Note that the profile can only be set when
            the session is created.
        :param read_timeout: invoke lambda function read timeout.
        :param max_attempts: invoke lambda function max attempts.
        """
        super(S3Service, self).__init__(service_name, aws_params, profile, **kwargs)

    def push_records(self,  bucket, key, records):
        """
        put records to s3.
        :param bucket: s3 bucket
        :param key: s3 bucket key
        :param records: The data blob to put into the record
        """
        assert isinstance(records, list)
        return self.aws_client.put_object(
            bucket, key, to_byte(json.dumps(records))
        )
