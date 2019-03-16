import uuid
from unittest import TestCase

from lambdabase.BaseHandler import BaseHandler, base_handler
from lambdabase.Request import Request
from lambdabase.Response import Response


class NoContentRequest(Request):
    def validate(self):
        return True


class OkContentRequest(Request):
    def validate(self):
        return True


class FailedValidationRequest(Request):
    def validate(self):
        return False


class ArgumentRequest(Request):
    @property
    def item(self):
        return self.data.get('item')

    @property
    def header_item(self):
        return self.headers.get('header_item')

    def validate(self):
        return True


class ArgumentResponse(Response):

    item = None
    header_item = None

    def __init__(self):
        super(ArgumentResponse, self).__init__({})
        self.code = 200

    def build(self):
        result = super(ArgumentResponse, self).build()
        result['item'] = self.item
        result['header_item'] = self.header_item
        return result


class NoContent(Response):

    def __init__(self):
        super(NoContent, self).__init__({})
        self.code = 204

    def build(self):
        return super(NoContent, self).build()


class OkContent(Response):

    def __init__(self):
        super(OkContent, self).__init__({})
        self.code = 200

    def build(self):
        return super(OkContent, self).build()


class Context(object):
    aws_request_id = str(uuid.uuid4())


class TestHandler(BaseHandler):
    NO_CONTENT_EVENT = 'NO_CONTENT_EVENT'
    OK_CONTENT_EVENT = "OK_CONTENT_EVENT"
    FAILED_VALIDATE_EVENT = "FAILED_VALIDATE_EVENT"
    ARGUMENT_EVENT = "ARGUMENT_EVENT"

    def __init__(self):
        super(TestHandler, self).__init__()
        self.register_event(self.NO_CONTENT_EVENT, NoContentRequest)
        self.register_event(self.OK_CONTENT_EVENT, OkContentRequest)
        self.register_event(self.FAILED_VALIDATE_EVENT, FailedValidationRequest)
        self.register_event(self.ARGUMENT_EVENT, ArgumentRequest)

    def execute(self, event):
        if isinstance(event, NoContentRequest):
            return NoContent()
        if isinstance(event, OkContentRequest):
            return OkContent()
        if isinstance(event, ArgumentRequest):
            response = ArgumentResponse()
            response.item = event.item
            response.header_item = event.header_item
            return response


test_handler = TestHandler()


def handler_no_content(event, context):
    return base_handler(event, context, TestHandler.NO_CONTENT_EVENT, test_handler)


def handler_ok_content(event, context):
    return base_handler(event, context, TestHandler.OK_CONTENT_EVENT, test_handler)


def handler_validate(event, context):
    return base_handler(event, context, TestHandler.FAILED_VALIDATE_EVENT, test_handler)


def handler_argument_request(event, context):
    return base_handler(event, context, TestHandler.ARGUMENT_EVENT, test_handler)


class BaseHandlerTests(TestCase):
    """
    Verify the base handler functions as expected
    """
    test_handler = TestHandler()

    def test_basic_invalid_event_missing_body(self):
        """
        Validate input with no body raises a bad request exception
        """
        event = {}
        context = Context()
        response = handler_no_content(event, context)
        self.assertTrue(response.get('statusCode') == 400)

    def test_simple_valid_no_content_event(self):
        """
        Validate that events are correctly mapped to the right type and can return no content
        """
        event = {"body": {}}
        context = Context()
        response = handler_no_content(event, context)
        self.assertTrue(response.get('statusCode') == 204)

    def test_simple_valid_ok_content_event(self):
        """
        Validate different events are mapped to the right type and can return a 200 response
        """
        event = {"body": {}}
        context = Context()
        response = handler_ok_content(event, context)
        self.assertTrue(response.get('statusCode') == 200)

    def test_cors_headers_are_correctly_set(self):
        """
        Assert that the CORS heards are returned from requests
        """
        event = {"body": {}}
        context = Context()
        response = handler_ok_content(event, context)

        headers = response.get('headers')
        self.assertTrue(response.get('statusCode') == 200)
        self.assertTrue('Access-Control-Allow-Credentials' in headers)
        self.assertTrue('Access-Control-Allow-Origin' in headers)

    def test_event_validation_fail_condition(self):
        """
        Test the failed validation results in 400 response
        """
        event = {'body': {}}
        context = Context()
        response = handler_validate(event, context)
        self.assertTrue(response.get('statusCode') == 400)

    def test_body_argument_mapping(self):
        """
        Test data in the request body maps into the event
        """
        event = {'body': {'item': 'value'}}
        context = Context()
        response = handler_argument_request(event, context)
        self.assertTrue(response.get('statusCode') == 200)
        self.assertTrue(response.get('item') == 'value')

    def test_header_argument_mapping(self):
        """
        Test data placed in the request header is mapped to an item
        """
        event = {'body': {}, 'headers': {'header_item': 'header_value'}}
        context = Context()
        response = handler_argument_request(event, context)
        self.assertTrue(response.get('statusCode') == 200)
        self.assertTrue(response.get('header_item') == 'header_value')

