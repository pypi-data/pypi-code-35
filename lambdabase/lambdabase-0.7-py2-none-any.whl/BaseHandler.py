import simplejson as json
import logging
from abc import ABCMeta, abstractmethod

from lambdabase.RequestContext import RequestContext
from lambdabase.Response import Response
from lambdabase.log.LogFactoryBase import LogFactoryBase as LogFactory
from lambdabase.LambdaException import BadRequestException, LambdaException


class BaseHandler(object):
    """
    Base class for all lambda handlers
    """
    __metaclass__ = ABCMeta

    KEY_BODY = 'body'
    KEY_PATH_PARAMETERS = 'pathParameters'
    KEY_QUERY_PARAMETERS = 'queryStringParameters'

    _config = {}
    _request = {}
    _event_map = {}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def handler(self, event, context):
        """
        The entry point for all calls into the lambda.
            - Parses the event and gets the request object
            - Sets the RequestContext object
            - Calls into the implemented execute methods
            - Builds and returns the response object
        :param event: Input event details
        :param context: The lambda context
        :return: a response object
        """
        try:
            request = self.pre_execute(event, context)
            response = self.execute(request)
        except LambdaException as ex:
            self.logger.error(LogFactory.base_005(ex))
            response = ex
        except BaseException as ex:
            self.logger.error(LogFactory.base_005(ex))
            response = LambdaException(ex.message, 500)

        return self.post_execute(response)

    # noinspection PyArgumentList
    def pre_execute(self, event, context):
        """
        Processes the incoming event and maps the body
        to an appropriate request object.
        :param event: The input lambda event
        :param context: The request context object
        :return: A parsed and validated request object
        """
        self.logger.info(LogFactory.base_001())

        event_type = event.get('event')
        if not event_type or event_type not in self._event_map:
            raise BadRequestException('Unknown event type [{}]'
                                      .format(event_type))

        request = self.build_request(self._event_map[event_type], event)
        self.validate(request)
        RequestContext.set(request, context)

        self.logger.info(LogFactory.base_002(event_type))
        return request

    @classmethod
    def build_request(cls, request_type, event):
        """
        Maps the input body to the appropriate request
        object based on the request type
        :param request_type: Indicates the event type
        :param event: the incoming event body
        :return: The constructed request object
        """
        body = event.get('body')
        headers = event.get('headers')
        claims = {}
        if 'requestContext' in event:
            authorizer = event.get('requestContext').get('authorizer')
            claims = authorizer.get('claims') if authorizer else {}
        request = request_type(body, headers, claims)
        return request

    @abstractmethod
    def execute(self, request):
        """
        Abstract base method for the actual lambda functionality
        :param request: The parsed and validated request obejct
        """
        pass

    # noinspection PyArgumentList
    def post_execute(self, response):
        """
        Complete the request and map to the appropriate
        response object and perform any global cleanup
        """
        self.logger.info(LogFactory.base_004(response.__class__.__name__))
        if not isinstance(response, Response):
            response = LambdaException("Lambdas should return a response object", 500)
        RequestContext.reset()
        return response.build()

    def register_event(self, event_key, request):
        """
        Register a request against the event key
        :param event_key: the event key
        :param request: the request object type
        """
        self.logger.info(LogFactory.base_003(event_key))
        self._event_map[event_key] = request

    @classmethod
    def validate(cls, request):
        """
        Validate that the request has valid parameters set
        :param request: The parsed request object
        :raise BadRequestException in the event of an error
        """
        if not request or not request.validate():
            raise BadRequestException('There was a a problem with the request')


# noinspection PyArgumentList
def base_handler(event, context, event_type, lambda_class):
    event['event'] = event_type

    if BaseHandler.KEY_BODY not in event:
        return BadRequestException('Input does not contain body element').build()

    if not isinstance(event[BaseHandler.KEY_BODY], dict):
        event[BaseHandler.KEY_BODY] = json.loads(event[BaseHandler.KEY_BODY]) if event[BaseHandler.KEY_BODY] else {}

    if BaseHandler.KEY_PATH_PARAMETERS in event and isinstance(event[BaseHandler.KEY_PATH_PARAMETERS], dict):
        event[BaseHandler.KEY_BODY].update(event[BaseHandler.KEY_PATH_PARAMETERS])

    if BaseHandler.KEY_QUERY_PARAMETERS in event and isinstance(event[BaseHandler.KEY_QUERY_PARAMETERS], dict):
        event[BaseHandler.KEY_BODY].update(event[BaseHandler.KEY_QUERY_PARAMETERS])

    return lambda_class.handler(event, context)







