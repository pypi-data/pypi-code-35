import unittest

from riot_api.api import _response_handler

class ResponseMock:

    def __init__ (self, status_code, headers=None):

        self.status_code = status_code
        self.headers = headers

class TestResponseHandler (unittest.TestCase):

    def test_handle_yields_successful_equals_true_when_status_code_is_200 (self):

        STATUS_CODE = 200
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertTrue(result["successful"])

    def test_handle_yields_response_object_when_status_code_is_200 (self):

        STATUS_CODE = 200
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertEqual(result["response"], RESPONSE)

    def test_handle_yields_successful_equals_false_when_status_code_is_400 (self):

        STATUS_CODE = 400
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_false_when_status_code_is_400 (self):

        STATUS_CODE = 400
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["retry"])

    def test_handle_yields_successful_equals_false_when_status_code_is_401 (self):

        STATUS_CODE = 401
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_false_when_status_code_is_401 (self):

        STATUS_CODE = 401
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["retry"])

    def test_handle_yields_successful_equals_false_when_status_code_is_403 (self):

        STATUS_CODE = 403
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_false_when_status_code_is_403 (self):

        STATUS_CODE = 403
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["retry"])

    def test_handle_yields_successful_equals_false_when_status_code_is_404 (self):

        STATUS_CODE = 404
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_true_when_status_code_is_404 (self):

        STATUS_CODE = 404
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertTrue(result["retry"])    

    def test_handle_yields_default_delay_when_status_code_is_404 (self):

        STATUS_CODE = 404
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertEqual(result["delay"], _response_handler._DEFAULT_DELAY_FOR_STATUS_CODE_404)

    def test_handle_yields_successful_equals_false_when_status_code_is_415 (self):

        STATUS_CODE = 415
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_false_when_status_code_is_415 (self):

        STATUS_CODE = 415
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["retry"])    

    def test_handle_yields_successful_equals_false_when_status_code_is_429 (self):

        STATUS_CODE = 429
        HEADERS = {
            "Retry-After": 0
        }
        RESPONSE = ResponseMock(STATUS_CODE, headers=HEADERS)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_true_when_status_code_is_429 (self):

        STATUS_CODE = 429
        HEADERS = {
            "Retry-After": 0
        }
        RESPONSE = ResponseMock(STATUS_CODE, headers=HEADERS)

        result = _response_handler.handle(RESPONSE)
        self.assertTrue(result["retry"])

    def test_handle_yields_retry_after_header_as_delay_when_status_code_is_429 (self):

        STATUS_CODE = 429
        HEADERS = {
            "Retry-After": 10
        }
        RESPONSE = ResponseMock(STATUS_CODE, headers=HEADERS)

        result = _response_handler.handle(RESPONSE)
        self.assertEqual(result["delay"], HEADERS["Retry-After"])

    def test_handle_yields_successful_equals_false_when_status_code_is_500 (self):

        STATUS_CODE = 500
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_true_when_status_code_is_500 (self):

        STATUS_CODE = 500
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertTrue(result["retry"])

    def test_handle_yields_default_delay_when_status_code_is_500 (self):

        STATUS_CODE = 500
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertEqual(result["delay"], _response_handler._DEFAULT_DELAY_FOR_STATUS_CODE_500)

    def test_handle_yields_successful_equals_false_when_status_code_is_502 (self):

        STATUS_CODE = 502
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_true_when_status_code_is_502 (self):

        STATUS_CODE = 502
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertTrue(result["retry"])

    def test_handle_yields_default_delay_when_status_code_is_502 (self):

        STATUS_CODE = 502
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertEqual(result["delay"], _response_handler._DEFAULT_DELAY_FOR_STATUS_CODE_502)

    def test_handle_yields_successful_equals_false_when_status_code_is_503 (self):

        STATUS_CODE = 503
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_true_when_status_code_is_503 (self):

        STATUS_CODE = 503
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertTrue(result["retry"])

    def test_handle_yields_default_delay_when_status_code_is_503 (self):

        STATUS_CODE = 503
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertEqual(result["delay"], _response_handler._DEFAULT_DELAY_FOR_STATUS_CODE_503)

    def test_handle_yields_successful_equals_false_when_status_code_is_504 (self):

        STATUS_CODE = 504
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertFalse(result["successful"])

    def test_handle_yields_retry_equals_true_when_status_code_is_504 (self):

        STATUS_CODE = 504
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertTrue(result["retry"])

    def test_handle_yields_default_delay_when_status_code_is_504 (self):

        STATUS_CODE = 504
        RESPONSE = ResponseMock(STATUS_CODE)

        result = _response_handler.handle(RESPONSE)
        self.assertEqual(result["delay"], _response_handler._DEFAULT_DELAY_FOR_STATUS_CODE_504)