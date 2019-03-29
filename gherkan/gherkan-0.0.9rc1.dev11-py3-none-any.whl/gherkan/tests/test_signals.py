import requests
import unittest
import re


class TestSignals(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.url = f"http://{self.__class__.host}:{self.__class__.port}/{{}}"
        self.signalFile = """
# language: en

Feature: Montrac
  Montrac
Background:
  Given lineOn

Scenario: given line is on
  Given lineOn
"""

    # @unittest.skip("TODO: skipped for debugging")
    def test_post_signal(self):
        resetResponse = requests.get(self.url.format("reset"))
        self.assertDictContainsSubset({"OK": True}, resetResponse.json())
        data = {'language': 'cs', 'scenarios': self.signalFile}
        response = requests.post(self.url.format("signals"), data=data)
        response = response.json()
        self.assertDictContainsSubset({"OK": True}, response)

    # @unittest.skip("TODO: skipped for debugging")
    def test_post_and_get_nl(self):
        resetResponse = requests.get(self.url.format("reset"))
        self.assertDictContainsSubset({"OK": True}, resetResponse.json())
        correctResponse = """
# language: en

Feature: Montrac
  Montrac
Background:
  Given line is on

Scenario: given line is on
  Given line is on
"""
        wsr = re.compile(u"(^\s+)|(\s+$)", flags=re.MULTILINE | re.UNICODE)
        data = {'language': 'cs', 'scenarios': self.signalFile}
        postResponse = requests.post(self.url.format("signals"), data=data)
        try:
            postResponse = postResponse.json()
        except Exception as exception:
            self.fail("An exception was raised whilel trying to convert response to JSON. This is most likely due to the fact that the response was of different type.\nThe exception: {}\nResponse text (if possible):\n{}".format(exception, postResponse.text))
        else:
            self.assertDictContainsSubset({"OK": True}, postResponse)

            response = requests.get(self.url.format("nltext"))
            self.assertMultiLineEqual(wsr.sub(u'', correctResponse), wsr.sub(
                u"", response.content.decode("utf-8")))


if __name__ == '__main__':
    unittest.TestCase.host = "localhost"
    unittest.TestCase.port = 5000
    unittest.main()