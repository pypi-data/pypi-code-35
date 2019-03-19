# coding=utf-8
# pylint: disable=wrong-import-position, relative-import
import sys
import os
import requests
sys.path.append(os.path.join(os.path.dirname(__file__)))
from resources.testsuite_resource import TestSuiteResource
from resources.testcase_resource import TestCaseResource
from resources.operation_resource import OperationResource

class RestClient(object):

    def __init__(self, host, port=5000):
        __session = requests.Session()
        self.test_suite = TestSuiteResource(host, port, __session)
        self.test_case = TestCaseResource(host, port, __session)
        self.operation = OperationResource(host, port, __session)

if __name__ == '__main__':
    RC = RestClient("172.29.130.138")
    # RC.test_case.run("test_fio_windows:TestFioWindows.test_seq_write", "async")
    # RC.test_case.run("test_fio_windows:TestFioWindows.test_seq_read", "async")
    # RC.test_case.stop_tests()
    # RC.test_suite.run("fio", "async")
    # ret = RC.test_suite.stop_tests()
