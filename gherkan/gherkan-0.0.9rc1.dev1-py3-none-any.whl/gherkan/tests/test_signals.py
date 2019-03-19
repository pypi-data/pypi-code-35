import requests
import unittest


class TestSignals(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.url = f"http://{self.__class__.host}:{self.__class__.port}/{{}}"
        self.signalFile = """
# language: cs

Požadavek: Robot R1
Robot R1 má na starosti kompletaci skládání Chassi. Robot postupně zbírá kostičky potřebené ke kompletaci.
Kontext:
Pokud LineOn == 1 || (robotR1ProgramNumber == 1 && robotR2ProgramNumber == 1)

Scénář: Normální běh linky - Robot R1 - Skládání Chassi - braní kostičky číslo 1
Když ShuttleXyAtStationYZ == 1 && edge(StationLocked, 1)
Pak   robotR1ProgramNumber == 1 && edge(robotR1ProgramStart, 1)

Scénář: Normální běh linky - Robot R1 - Skládání Chassi - pokládání kostičky číslo 1
Když  robotR1ProgramNumber == 1 && edge(robotR1ProgramEnd, 1)
Pak   robotR1ProgramNumber == 2
"""

    def test_post_signal(self):
        data = {'language': 'en', 'scenarios': self.signalFile}
        response = requests.post(self.url.format("signals"), data=data)
        print(response.text)
        response = response.json()
        self.assertDictContainsSubset({"OK": True}, response)

    # @unittest.skip("TODO: fill in correctResponse")
    def test_post_and_get_nl(self):
        correctResponse = """
# language: cs

Feature: Robot R1
  Robot R1 má na starosti kompletaci skládání Chassi. Robot postupně zbírá kostičky potřebené ke kompletaci.
Background:
  Given ((robot R2 assembles product AND robot R1 picks up cube one) OR Line is On)

Scenario: Normální běh linky - Robot R1 - Skládání Chassi - braní kostičky číslo 1
  When (Station is Locked AND Shuttle Xy is in station YZ)
  Then (robot R1 starts program AND robot R1 picks up cube one)
Scenario: Normální běh linky - Robot R1 - Skládání Chassi - pokládání kostičky číslo 1
  When (robot R1 ends program AND robot R1 picks up cube one)
  Then robot R1 puts cube two on tray
"""

        data = {'language': 'en', 'scenarios': self.signalFile}
        postResponse = requests.post(self.url.format("signals"), data=data)
        print(postResponse.text)
        postResponse = postResponse.json()
        self.assertDictContainsSubset({"OK": True}, postResponse)

        response = requests.get(self.url.format("nltext"))
        self.assertMultiLineEqual(correctResponse, response.content.decode("utf-8"))

