import simplejson as json
import logging

import boto3

from lambdabase.RequestContext import RequestContext
from lambdabase.invokers import LogFactory
from lambdabase.invokers import Invoker


class LambdaInvoker(Invoker):
    """
    Invoker class for making lambda to lambda calls when running
    in an AWS environment using boto3 as the client
    """
    _client = None
    _context = RequestContext

    def __init__(self, function_name, request_type, response_type, async_event=False):
        super(LambdaInvoker, self).__init__(function_name, request_type, response_type)
        self.logger = logging.getLogger(LambdaInvoker.__class__.__name__)
        self.async_event = async_event

    # noinspection PyArgumentList
    def invoke(self, request):
        """
        Invoke the remote procedure
        :param request: the request data
        :return: the response object
        """
        data = {'body': request.data}
        data['body']['correlation_id'] = RequestContext.correlation_id
        self.logger.info(LogFactory.invoker_000(self.function_name, data))

        try:
            invocation_type = 'Event' if self.async_event else 'RequestResponse'
            response = self.client.invoke(FunctionName=self.function_name,
                                          Payload=json.dumps(data),
                                          InvocationType=invocation_type)

            if not self.async_event:
                response = json.loads(response['Payload'].read())
                result = json.loads(response['body'])
                self.logger.info(LogFactory.invoker_001(self.function_name, result))
                return self.response_type(result)
            
        except StandardError as ex:
            self.logger.error(LogFactory.invoker_002(self.function_name, ex))

        return None

    @property
    def client(self):
        if not self._client:
            self._client = boto3.client('lambda')
        return self._client
