import requests
import unittest


class TestNLText(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.url = f"http://{self.__class__.host}:{self.__class__.port}/{{}}"
        self.request = {
            "feature": "robot R1",
            "feature_desc": "lorem ipsum",
            "background": "given Line is On",
            "text_raw": "scenario As soon as shuttle XY is in the station ZX, then robot r1 picks "
                        "up cube one. scenario when robot r3 picks up cube one, robot r2 assembles the product.",
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

Feature: robot R1
    lorem ipsum
Background:
  Given LineOn == [empty]

Scenario: As soon as shuttle XY is in the station ZX, then robot r1 picks up cube one. 
  When shuttleXYAtStationZX == [empty]
  Then robotR1ProgramNumber == 1
Scenario: when robot r3 picks up cube one, robot r2 assembles the product.
  When robotR3ProgramNumber == 1
  Then robotR2ProgramNumber == 1
"""

        response = requests.post(self.url.format("nltext"), data=self.request)
        try:
            response = response.json()
        except Exception as exception:
            self.fail("An exception was raised whilel trying to convert response to JSON. This is most likely due to the fact that the response was of different type.\nThe exception: {}\nResponse text (if possible):\n{}".format(exception, response.text))
        else:
            self.assertDictContainsSubset({"errors": False}, response)

            response = requests.get(self.url.format("signals"))

            self.assertMultiLineEqual(
                correctResponse, response.content.decode())
