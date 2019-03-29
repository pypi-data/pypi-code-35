import requests
import unittest

class TestNLText(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.url = f"http://{self.__class__.host}:{self.__class__.port}/{{}}"
        # self.request = {
        #     "feature": "robot R1",
        #     "feature_desc": "lorem ipsum",
        #     "background": "given Line is On",
        #     "text_raw": "scenario As soon as shuttle XY is in the station ZX, then robot r1 picks "
        #                 "up cube one. scenario when robot r3 picks up cube one, robot r2 assembles the product.",
        #     "language": "en"
        # }
        self.request = {
            "feature": "Montrac",
            "feature_desc": " Montrac",
            "background": "Given line is on",
            "text_raw": "scenario given line is on",
            "language": "en"
        }

    # @unittest.skip("TODO: skipped for debugging")
    def test_post_nltext(self):
        resetResponse = requests.get(self.url.format("reset"))
        self.assertDictContainsSubset({"OK": True}, resetResponse.json())
        correctResponse = {
            "info": "Processing done",
            "lines": [],
            "error_lines": [],
            "error_hints": [],
            "errors": False
        }

        response = requests.post(self.url.format(
            "nltext"), data=self.request).json()
        self.assertDictContainsSubset(correctResponse, response)

    # @unittest.skip("TODO: skipped for debugging")
    def test_post_and_get_signal(self):
        resetResponse = requests.get(self.url.format("reset"))
        self.assertDictContainsSubset({"OK": True}, resetResponse.json())
        correctResponse = """# language: en

Feature: Montrac
  Montrac
Background:
  Given lineon

Scenario: given line is on
  Given lineon
"""

        response = requests.post(self.url.format("nltext"), data=self.request)
        try:
            response = response.json()
        except Exception as exception:
            self.fail("An exception was raised while trying to convert response to JSON. This is most likely due to the fact that the response was of different type.\nThe exception: {}\nResponse text (if possible):\n{}".format(exception, response.text))
        else:
            self.assertDictContainsSubset({"errors": False}, response)

            response = requests.get(self.url.format("signals"))
            # correctResponseS = correctResponse.replace("\n", " ").split()
            # myresp = response.content.decode()
            # responseS = myresp.replace("\n", " ").split()
            # self.assertEqual(
            #     correctResponseS, responseS)

            self.compare_multiline(response.content.decode(), correctResponse)

    def compare_multiline(self, testee, teststr):
        if not isinstance(testee, str) or not isinstance(teststr, str):
            self.assertFalse("No strings given to compare!")
            return
        
        self.assertEqual(testee.replace("\n", " ").split(), teststr.replace("\n", " ").split())


        


if __name__ == '__main__':
    unittest.TestCase.host = "localhost"
    unittest.TestCase.port = 5000
    unittest.main()