from .rmqhandler import RabbitMQHandler
from .results_schema import TestSuiteResultSchema, TestResultSchema
import time
import json


class Dtest():
    def __init__(self, connectionConfig, metadata):
        self.rmqHandler = RabbitMQHandler(
            connectionConfig["host"], connectionConfig["exchange"], connectionConfig["exchange_type"])
        self.testMetadata = metadata

    def assertTrue(self, condition):
        return self.assertCondition(condition, True)

    def assertFalse(self, condition):
        return self.assertCondition(condition, False)

    def assertCondition(self, condition, expected):
        testResults = TestResultSchema()

        testResults.startTime = time.time()
        testResults.description = self.testMetadata["description"]
        testResults.topic = self.testMetadata["topic"]

        # Assert rule
        testResults.passed = condition == expected

        testResults.expectedResult = True
        testResults.actualResult = condition

        # Closing metadata
        testResults.duration = time.time() - testResults.startTime

        finalJSON = json.dumps(testResults.__dict__)

        self.rmqHandler.publishResults(finalJSON)
        self.rmqHandler.closeConnection()
        return True if condition else False

    def convertListToVars(self, l):
        newList = []
        for i in l:
            newList.append(vars(i))
        return newList
