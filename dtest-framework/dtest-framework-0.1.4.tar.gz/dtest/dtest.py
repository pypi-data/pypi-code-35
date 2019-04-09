from .rmqhandler import RabbitMQHandler
from .results_schema import TestSuiteResultSchema, TestResultSchema

import warnings
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription
import time
import time
import json


class Dtest():
    def __init__(self, connectionConfig, suiteMetadata):
        self.rmqHandler = RabbitMQHandler(
            connectionConfig["host"], connectionConfig["exchange"], connectionConfig["exchange_type"], connectionConfig["username"], connectionConfig["password"])
        self.testSuite = TestSuiteResultSchema()
        self.testSuite.startTime = time.time()
        self.testSuite.description = suiteMetadata["description"]
        self.testSuite.topic = suiteMetadata["topic"]
        self.testSuite.ruleSet = suiteMetadata["ruleSet"]
        self.testSuite.dataSet = suiteMetadata["dataSet"]

    def publish(self):
        self.testSuite.testResults = self.convertListToVars(
            self.testSuite.testResultsList)
        self.testSuite.duration = time.time() - self.testSuite.startTime

        finalJSON = json.dumps(self.testSuite.__dict__)

        try:
            self.rmqHandler.connect()
            self.rmqHandler.publishResults(finalJSON)
            self.rmqHandler.closeConnection()
        except:
            print(
                "Error connecting and publishing to RabbitMQ @ " + self.rmqHandler.host + ":" + self.rmqHandler.port + " on exchange `" + self.rmqHandler.exchange + "`")

    def convertListToVars(self, l):
        newList = []
        for i in l:
            newList.append(vars(i))
        return newList

    """
    An adaptation of pyhamcrest 'assert_that' by Jon Reid
    __author__ = "Jon Reid"
    __copyright__ = "Copyright 2011 hamcrest.org"
    __license__ = "BSD, see hamcrest-License.txt"
    """

    def assert_that(self, arg1, arg2=None, arg3=''):
        """Asserts that actual value satisfies matcher. (Can also assert plain
        boolean condition.)

        :param actual: The object to evaluate as the actual value.
        :param matcher: The matcher to satisfy as the expected condition.
        :param reason: Optional explanation to include in failure description.

        ``assert_that`` passes the actual value to the matcher for evaluation. If
        the matcher is not satisfied, an exception is thrown describing the
        mismatch.

        ``assert_that`` is designed to integrate well with PyUnit and other unit
        testing frameworks. The exception raised for an unmet assertion is an
        :py:exc:`AssertionError`, which PyUnit reports as a test failure.

        With a different set of parameters, ``assert_that`` can also verify a
        boolean condition:

        .. function:: assert_that(assertion[, reason])

        :param assertion:  Boolean condition to verify.
        :param reason:  Optional explanation to include in failure description.

        This is equivalent to the :py:meth:`~unittest.TestCase.assertTrue` method
        of :py:class:`unittest.TestCase`, but offers greater flexibility in test
        writing by being a standalone function.

        """
        if isinstance(arg2, Matcher):
            return self._assert_match(actual=arg1, matcher=arg2, reason=arg3)
        else:
            if isinstance(arg1, Matcher):
                warnings.warn(
                    "arg1 should be boolean, but was {}".format(type(arg1)))
            self._assert_bool(assertion=arg1, reason=arg2)

    def _assert_match(self, actual, matcher, reason):
        results = TestResultSchema()
        results.description = reason
        results.startTime = time.time()

        if not matcher.matches(actual):
            results.duration = time.time() - results.startTime
            results.passed = False

            description = StringDescription()
            description.append_text('Expected: ')     \
                .append_description_of(matcher)
            results.expectedResult = description.out

            description = StringDescription()
            description.append_text('but: ')
            matcher.describe_mismatch(actual, description)
            results.actualResult = description.out
            self.testSuite.testResultsList.append(results)
            return False
        else:
            results.duration = time.time() - results.startTime
            results.passed = True

            description = StringDescription()
            description.append_text('Expected: ')     \
                .append_description_of(matcher)
            results.expectedResult = description.out
            self.testSuite.testResultsList.append(results)
            return True

    def _assert_bool(self, assertion, reason=None):
        if not assertion:
            if not reason:
                reason = 'Assertion failed'
            raise AssertionError(reason)


"""
    A test like test_dtest.py, but able to see print statements

if __name__ == "__main__":
    from hamcrest import *
    connectionConfig = {
        "host": "localhost",
        "username": "guest",
        "password": "guest",
        "exchange": "test.dtest",
        "exchange_type": "fanout"
    }
    metadata = {
        "description": "This is a test suite",
        "topic": "test.dtest",
        "ruleSet": "Testing some random things",
        "dataSet": "random_data_set_123912731.csv"
    }
    dt = Dtest(connectionConfig, metadata)

    dt.assert_that("adsasd", is_(instance_of(str)))
    dt.assert_that([0, 1], has_length(1))
    dt.finish()
"""
