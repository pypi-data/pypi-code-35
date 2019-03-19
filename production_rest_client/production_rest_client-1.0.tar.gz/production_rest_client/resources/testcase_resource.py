# coding=utf-8
# pylint: disable=import-error
import json
from resources.models.helper import rest_get_call
from resources.models.helper import rest_post_json_call
from resources.models.helper import rest_delete_call


class TestCaseResource(object):

    def __init__(self, host, port, session):
        self.host = host
        self.port = port
        self.session = session
        self.time_out = 120

    def list(self, filter_):
        """
        :param filter_: list filter
        :return: type: list, return test case list meet the filter
        """
        url_ = "http://{0}:{1}/tc/{2}".format(self.host, self.port, filter_)
        result = rest_get_call(url_, self.session, self.time_out)
        response_ = result.json()
        return response_["resource"]['data']

    def run(self, test_case, mode="sync"):
        """
        :param test_case: type string, test case name
        :param  mode: sync or async, run test case
        :return: type bool, return test case run result
        """
        data = {"tc": test_case, "mode":mode}
        url_ = "http://{0}:{1}/tc".format(self.host, self.port)
        result = rest_post_json_call(url_, self.session, json.dumps(data), self.time_out)
        response_ = result.json()
        return response_["resource"]

    def get_async_result(self, key):
        url_ = "http://{0}:{1}/tc/results/{2}".format(self.host, self.port, key)
        result = rest_get_call(url_, self.session, self.time_out)
        response_ = result.json()
        return response_["resource"]

    def stop_tests(self):
        url_ = "http://{0}:{1}/tc".format(self.host, self.port)
        result = rest_delete_call(url_, self.session, self.time_out)
        response_ = result.json()
        return response_["resource"]["result"]
