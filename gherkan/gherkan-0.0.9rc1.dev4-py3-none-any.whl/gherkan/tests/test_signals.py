import requests
import unittest
import re


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

    # @unittest.skip("TODO: skipped for debugging")
    def test_post_signal(self):
        data = {'language': 'cs', 'scenarios': self.signalFile}
        response = requests.post(self.url.format("signals"), data=data)
        response = response.json()
        self.assertDictContainsSubset({"OK": True}, response)

    # @unittest.skip("TODO: skipped for debugging")
    def test_post_and_get_nl(self):
        requests.get(self.url.format("reset"))
        correctResponse = """
# language: cs

Feature: Robot R1
  Robot R1 má na starosti kompletaci skládání Chassi. Robot postupně zbírá kostičky potřebené ke kompletaci.
Background:
  Given ((robot R2 dá kostku 1 na podnos AND robot R1 zvedne všechny červené kostky) OR linka jest zapnutá)

Scenario: Normální běh linky - Robot R1 - Skládání Chassi - braní kostičky číslo 1
  When (stanice jest zamčená AND vozíček Xy jest ve stanici YZ)
  Then (robot R1 začne AND robot R1 zvedne všechny červené kostky)
Scenario: Normální běh linky - Robot R1 - Skládání Chassi - pokládání kostičky číslo 1
  When (robot R1 skončí AND robot R1 zvedne všechny červené kostky)
  Then robot R1 zvedne všechny zelené kostky
"""
        wsr = re.compile(u"(^\s+)|(\s+$)", flags=re.MULTILINE | re.UNICODE)
        data = {'language': 'cs', 'scenarios': self.signalFile}
        postResponse = requests.post(self.url.format("signals"), data=data)
        postResponse = postResponse.json()
        self.assertDictContainsSubset({"OK": True}, postResponse)

        response = requests.get(self.url.format("nltext"))
        self.assertMultiLineEqual(wsr.sub(u'', correctResponse), wsr.sub(u"", response.content.decode("utf-8")))

