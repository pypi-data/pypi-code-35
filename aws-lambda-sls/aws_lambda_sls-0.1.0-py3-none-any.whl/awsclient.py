"""
Simplified AWS client.
"""
import re
import time
from aws_lambda_sls.utils import get_content_type
from botocore.exceptions import ClientError
from botocore.vendored.requests import ConnectionError
from aws_lambda_sls.constants import MAX_LAMBDA_DEPLOYMENT_SIZE

_REMOTE_CALL_ERRORS = (
    ClientError,
    ConnectionError
)


class AWSClientError(Exception):
    pass


class ResourceDoesNotExistError(AWSClientError):
    pass


class LambdaClientError(AWSClientError):
    def __init__(self, original_error, context):
        self.original_error = original_error
        self.context = context
        super(LambdaClientError, self).__init__(str(original_error))


class DeploymentPackageTooLargeError(LambdaClientError):
    pass


class LambdaErrorContext(object):
    def __init__(self, function_name, client_method_name, deployment_size):
        self.function_name = function_name
        self.client_method_name = client_method_name
        self.deployment_size = deployment_size


class AWSClient(object):
    LAMBDA_CREATE_ATTEMPTS = 30
    DELAY_TIME = 5

    def __init__(self, session, sleep=time.sleep, **client_params):
        self._session = session
        self._sleep = sleep
        self._client_cache = {}
        self._client_params = client_params

    def lambda_function_exists(self, name):
        client = self._client("lambda")
        try:
            client.get_function(FunctionName=name)
            return True
        except client.exceptions.ResourceNotFoundException:
            return False

    def _create_vpc_config(self, security_group_ids, subnet_ids):
        vpc_config = {
            "SubnetIds": [],
            "SecurityGroupIds": [],
        }
        if security_group_ids is not None and subnet_ids is not None:
            vpc_config["SubnetIds"] = subnet_ids
            vpc_config["SecurityGroupIds"] = security_group_ids
        return vpc_config

    def create_function(self,
                        function_name,
                        role_arn,
                        s3_code,
                        runtime,
                        handler,
                        environment_variables=None,
                        tags=None,
                        timeout=None,
                        memory_size=None,
                        security_group_ids=None,
                        subnet_ids=None,
                        ):
        kwargs = {
            "FunctionName": function_name,
            "Runtime": runtime,
            "Code": s3_code,
            "Handler": handler,
            "Role": role_arn,
        }
        if tags is not None:
            kwargs["Tags"] = tags
        if timeout is not None:
            kwargs["Timeout"] = timeout
        if memory_size is not None:
            kwargs["MemorySize"] = memory_size
        if security_group_ids is not None and subnet_ids is not None:
            kwargs["VpcConfig"] = self._create_vpc_config(
                security_group_ids=security_group_ids,
                subnet_ids=subnet_ids,
            )
        return self._create_lambda_function(kwargs)

    def _create_lambda_function(self, api_args):
        try:
            return self._call_client_method_with_retries(
                self._client("lambda").create_function,
                api_args, max_attempts=self.LAMBDA_CREATE_ATTEMPTS,
            )["FunctionArn"]
        except _REMOTE_CALL_ERRORS as e:
            context = LambdaErrorContext(
                api_args["FunctionName"],
                "create_function", 0
            )
            raise self._get_lambda_code_deployment_error(e, context)
    
    def _get_lambda_code_deployment_error(self, error, context):
        error_cls = LambdaClientError
        if (isinstance(error, ConnectionError) and
                context.deployment_size > MAX_LAMBDA_DEPLOYMENT_SIZE):
            error_cls = DeploymentPackageTooLargeError
        elif isinstance(error, ClientError):
            code = error.response["Error"].get("Code", '')
            message = error.response["Error"].get("Message", '')
            if code == "RequestEntityTooLargeException":
                error_cls = DeploymentPackageTooLargeError
            elif code == "InvalidParameterValueException" and \
                    "Unzipped size must be smaller" in message:
                error_cls = DeploymentPackageTooLargeError
        return error_cls(error, context)

    def _is_iam_role_related_error(self, error):
        message = error.response["Error"].get("Message", '')
        if re.search("role.*cannot be assumed", message):
            return True
        if re.search("role.*does not have permissions", message):
            return True
        return False

    def delete_function(self, function_name):
        lambda_client = self._client("lambda")
        try:
            lambda_client.delete_function(FunctionName=function_name)
        except lambda_client.exceptions.ResourceNotFoundException:
            raise ResourceDoesNotExistError(function_name)

    def update_function(self,
                        function_name,
                        s3_code,
                        environment_variables=None,
                        runtime=None,
                        tags=None,
                        timeout=None,
                        memory_size=None,
                        role_arn=None,
                        subnet_ids=None,
                        security_group_ids=None,
                        ):
        return_value = self._update_function_code(
            function_name=function_name, s3_code=s3_code)
        self._update_function_config(
            environment_variables=environment_variables,
            runtime=runtime,
            timeout=timeout,
            memory_size=memory_size,
            role_arn=role_arn,
            subnet_ids=subnet_ids,
            security_group_ids=security_group_ids,
            function_name=function_name
        )
        if tags is not None:
            self._update_function_tags(return_value["FunctionArn"], tags)
        return return_value

    def _update_function_code(self, function_name, s3_code):
        lambda_client = self._client("lambda")
        try:
            return lambda_client.update_function_code(
                FunctionName=function_name,
                S3Bucket=s3_code["S3Bucket"],
                S3Key=s3_code["S3Key"]
            )
        except _REMOTE_CALL_ERRORS as e:
            context = LambdaErrorContext(
                function_name,
                "update_function_code", 0
            )
            raise self._get_lambda_code_deployment_error(e, context)

    def _update_function_config(self,
                                environment_variables,
                                runtime,
                                timeout,
                                memory_size,
                                role_arn,
                                subnet_ids,
                                security_group_ids,
                                function_name,
                                ):
        kwargs = {}
        if runtime is not None:
            kwargs["Runtime"] = runtime
        if timeout is not None:
            kwargs["Timeout"] = timeout
        if memory_size is not None:
            kwargs["MemorySize"] = memory_size
        if role_arn is not None:
            kwargs["Role"] = role_arn
        if security_group_ids is not None and subnet_ids is not None:
            kwargs["VpcConfig"] = self._create_vpc_config(
                subnet_ids=subnet_ids,
                security_group_ids=security_group_ids
            )
        if kwargs:
            kwargs["FunctionName"] = function_name
            lambda_client = self._client("lambda")
            self._call_client_method_with_retries(
                lambda_client.update_function_configuration, kwargs,
                max_attempts=self.LAMBDA_CREATE_ATTEMPTS
            )

    def _update_function_tags(self, function_arn, requested_tags):
        remote_tags = self._client("lambda").list_tags(
            Resource=function_arn)["Tags"]
        self._remove_unrequested_remote_tags(
            function_arn, requested_tags, remote_tags)
        self._add_missing_or_differing_value_requested_tags(
            function_arn, requested_tags, remote_tags)

    def _remove_unrequested_remote_tags(
            self, function_arn, requested_tags, remote_tags):
        tag_keys_to_remove = list(set(remote_tags) - set(requested_tags))
        if tag_keys_to_remove:
            self._client("lambda").untag_resource(
                Resource=function_arn, TagKeys=tag_keys_to_remove)

    def _add_missing_or_differing_value_requested_tags(
            self, function_arn, requested_tags, remote_tags):
        tags_to_add = {k: v for k, v in requested_tags.items()
                       if k not in remote_tags or v != remote_tags[k]}
        if tags_to_add:
            self._client("lambda").tag_resource(
                Resource=function_arn, Tags=tags_to_add)

    def _client(self, service_name):
        if service_name not in self._client_cache:
            self._client_cache[service_name] = self._session.client(
                service_name, **self._client_params)
        return self._client_cache[service_name]

    def _call_client_method_with_retries(
        self,
        method,
        kwargs,
        max_attempts,
        should_retry=None,
        delay_time=DELAY_TIME,
    ):
        client = self._client("lambda")
        attempts = 0
        if should_retry is None:
            should_retry = self._is_iam_role_related_error
        retryable_exceptions = (
            client.exceptions.InvalidParameterValueException,
            client.exceptions.ResourceInUseException,
        )
        while True:
            try:
                response = method(**kwargs)
            except retryable_exceptions as e:
                self._sleep(self.DELAY_TIME)
                attempts += 1
                if attempts >= max_attempts or \
                        not should_retry(e):
                    raise
                continue
            return response

    def put_object(self, bucket, key, body, content_type=None):
        s3 = self._client("s3")
        content_type = content_type or get_content_type(key)
        return s3.put_object(Bucket=bucket, Key=key, Body=body,
                             ContentType=content_type)

    def invoke(self, function_name, payload=None, client_context=None, alias=None):
        """
        invoke your self defined lambda function method.
        :param function_name: your invoke function name
        :param payload: invoke params, dict type
        :param client_context: client context data
        :param alias: function alias or version
        """
        invoke_params = {
            "InvocationType": "RequestResponse",
        }
        if payload:
            invoke_params["Payload"] = payload
        if client_context:
            invoke_params["ClientContext"] = client_context
        if alias:
            invoke_params["Qualifier"] = alias
        return self._client("lambda").invoke(FunctionName=function_name, **invoke_params)

    def kinesis_push_record(self, stream_name, data, partition_key=None):
        """
        Writes a single data record into an Amazon Kinesis data stream.
        :param stream_name: The name of the stream to put the data record into
        :param data: The data blob to put into the record
        :param partition_key: Determines which shard in the stream the data record is assigned to
        """
        return self._client("kinesis").put_record(
            StreamName=stream_name, Data=data,
            PartitionKey=partition_key
        )

    def kinesis_push_records(self, stream_name, records):
        """
        Writes a multi data record into an Amazon Kinesis data stream.
        :param stream_name: The name of the stream to put the data record into
        :param records: The data blob to put into the record list
        """
        return self._client("kinesis").put_records(
            StreamName=stream_name, Records=records
        )

    def kinesis_list_shards(self, stream_name):
        """
        Lists the shards in a stream.
        :param stream_name: The name of the stream
        """
        return self._client("kinesis").list_shards(StreamName=stream_name)

    def kinesis_get_shard_iterator(self, stream_name, shard_id, sequence_number=None):
        """
        Gets an Amazon Kinesis shard iterator.
        :param stream_name: The name of the stream
        :param shard_id: The stream shard id
        :param sequence_number: shard sequence number
        """
        if sequence_number:
            iterator_type, params = "AFTER_SEQUENCE_NUMBER", {
                "StartingSequenceNumber": sequence_number
            }
        else:
            iterator_type, params = "TRIM_HORIZON", {}
        return self._client("kinesis").get_shard_iterator(
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType=iterator_type, **params
        )

    def kinesis_get_records(self, shard_iterator, limit=10000):
        """
        Gets data records from a Kinesis data stream's shard.
        :param shard_iterator: The stream shard iterator
        :param limit: result limit
        """
        return self._client("kinesis").get_records(ShardIterator=shard_iterator, Limit=limit)
