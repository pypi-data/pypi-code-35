from .rmqhandler import RabbitMQHandler
from .results_schema import TestSuiteResultSchema, TestResultSchema
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

    # For version 0.1.2
    def expect(self, obj):
        return Expectation(obj)

    def assertTrue(self, condition, description=None):
        return self.assertCondition(condition, True, description)

    def assertFalse(self, condition, description=None):
        return self.assertCondition(condition, False, description)

    def assertCondition(self, condition, expected, description):
        testResults = TestResultSchema()

        testResults.startTime = time.time()
        if description is not None:
            testResults.description = description

        # Assert rule
        testResults.passed = condition == expected

        # Not right - change to actual and expected once
        # we figure out how to 'introspect' into an expression
        testResults.expectedResult = expected
        testResults.actualResult = condition

        # Closing metadata
        testResults.duration = time.time() - testResults.startTime

        self.testSuite.testResultsList.append(testResults)

        return True if condition else False

    def finish(self):
        self.testSuite.testResults = self.convertListToVars(
            self.testSuite.testResultsList)

        finalJSON = json.dumps(self.testSuite.__dict__)

        try:
            self.rmqHandler.connect()
            self.rmqHandler.publishResults(finalJSON)
            self.rmqHandler.closeConnection()
        except:
            print(
                f'Error connecting and publishing to RabbitMQ @ {self.rmqHandler.host}:{self.rmqHandler.port} on exchange `{self.rmqHandler.exchange}`')

    def convertListToVars(self, l):
        newList = []
        for i in l:
            newList.append(vars(i))
        return newList


# For version 0.1.2


class Expectation:
    def __init__(self, obj):
        self.object = obj
        pass

    def toBe(self, compareTo):
        return self.object is compareTo

    def toBeEqual(self, compareTo):
        return self.object == compareTo

    def toBeGreaterThan(self, compareTo):
        return self.object > compareTo

    def toBeLessThan(self, compareTo):
        return self.object < compareTo
