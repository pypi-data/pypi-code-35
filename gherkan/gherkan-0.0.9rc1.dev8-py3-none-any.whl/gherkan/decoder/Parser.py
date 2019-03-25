# -*- coding: utf-8 -*-
import difflib
import re
from gherkan.containers.signal_scenario import SignalScenario
from gherkan.containers.signal_batch import SignalBatch
from gherkan.utils.dictionaryMapper import DictionaryMapper
from gherkan.utils.dicts import sectionDict
import gherkan.utils.gherkin_keywords as g
import gherkan.utils.constants as c
import os
import warnings


class Parser:
    def __init__(self):
        self.regex_flags = re.RegexFlag.IGNORECASE | re.RegexFlag.UNICODE
        self.sectionTypes = [g.GIVEN, g.WHEN, g.THEN]

        self.ROBOT_PROGRAMS_CZ = os.path.join(c.PROJECT_ROOT_DIR, "gherkan", "utils", "RobotPrograms_cz.json")
        self.ROBOT_PROGRAMS_EN = os.path.join(c.PROJECT_ROOT_DIR, "gherkan", "utils", "RobotPrograms_en.json")

        # active scenario for the current section
        self.scenario = None

        # path to file if the input is loaded from file
        self.filename = ""
        self.language = None

    # def findSimilar(self, word, possibilities, cutoff=0.6):
    #     """
    #     Finds similar words. For future use: can be used to correct typos.
    #     """
    #     result = []
    #     s = difflib.SequenceMatcher()
    #     s.set_seq2(word)
    #     for idx, x in enumerate(possibilities):
    #         s.set_seq1(x)
    #         if s.real_quick_ratio() >= cutoff and s.quick_ratio() >= cutoff and s.ratio() >= cutoff:
    #             result.append((s.ratio(), x, idx))
    #
    #     return [idx for score, x, idx in result]

    def generateDirectiveExtractor(self, directiveName: str):
        # Generates a regural expression for directive extraction
        return re.compile(r"#\s*{}\W+(?P<result>\w+)".format(directiveName), flags=self.regex_flags)

    def getTextAfterColon(self, text: str):
        # Returns regex match with text after colon or None if regex fails
        reTextAfterColon = re.compile(r".*:\s*(?P<result>.+)", flags=self.regex_flags)

        return reTextAfterColon.search(text)

    def getTextAfterWhitespace(self, text: str):
        # Returns regex match with text after whitespace or None if regex fails
        reTextAfterWhitespace = re.compile(r"^\s*\w+\s+(?P<result>.+)", flags=self.regex_flags)

        return reTextAfterWhitespace.search(text)

    def parseDirective(self, directiveName: str, line: str):
        # Parses directive on the current line
        # Directive == a "#" followed by a word followed by a colon and another word, e.g "# language: cs"
        reDirective = self.generateDirectiveExtractor(directiveName)
        directive = reDirective.search(line) or ""

        if not directive:
            warnings.warn("Directive {} not found!".format(directiveName))
            return ""

        return directive.group("result")

    def parseFeature(self, nlBatch: SignalBatch, lineNumber: int, textlines: list):
        # Parses the Feature section
        line = textlines[lineNumber]
        nextLine = textlines[lineNumber + 1]

        name = self.getTextAfterColon(line)

        if name:
            nlBatch.name = name.group("result")

        nlBatch.desc = nextLine

    def parseBackground(self, nlBatch: SignalBatch, lineNumber: int, textlines: list):
        # Parses the Background section
        nextLine = textlines[lineNumber + 1]
        cond = self.getTextAfterWhitespace(nextLine)

        if cond:
            nlBatch.context = self.parseStatement(cond.group("result"))
        else:
            raise Exception("Context parsing failed!")

    def finalizeScenario(self, nlBatch: SignalBatch):
        # Finalizes the section with scenario
        self.scenario.contextStatements.append(nlBatch.context)
        nlBatch.addScenario(self.scenario)

    def parseScenario(self, nlBatch: SignalBatch, lineNumber: int, textlines: list):
        # Parses the Scenario section
        if self.scenario:
            # finalize the previous scenario
            self.finalizeScenario(nlBatch)

        # start a new scenario
        self.scenario = SignalScenario()

        # extract the scenario name
        line = textlines[lineNumber]
        scenarioName = self.getTextAfterColon(line)

        if scenarioName:
            self.scenario.name = scenarioName.group("result")
        else:
            warnings.warn(
                "Missing name for a scenario on line {}. "
                "Using random name.\nLine content:\n{}".format(
                    lineNumber, line))


    def parseAnd(self, nlBatch, lineNumber, textlines):
        # TODO implement
        warnings.warn("Skipping And section, not implemented yet.")
        pass

    def parseScenarioSection(self, lineNumber: int, textlines: list, section: str):
        # Parses the Given / When / Then section inside the scenario section
        line = textlines[lineNumber]
        statement = self.getTextAfterWhitespace(line)
        tree = self.parseStatement(statement.group("result"))

        if section == g.GIVEN:
            self.scenario.givenStatements.append(tree)
        elif section == g.WHEN:
            self.scenario.whenStatements.append(tree)
        elif section == g.THEN:
            self.scenario.thenStatements.append(tree)
        else:
            warnings.warn(
                "Unknown section '{}' encountered on line {}: {}".format(section, lineNumber, line))

    def getSectionList(self, textlines: list):
        # dictionary with section keywords
        sectionDM = DictionaryMapper(sectionDict)
        sectionList = []

        for i, line in enumerate(textlines):
            words = re.findall(r"^\s*(\w+)", line)
            words = sectionDM.filter(words)

            # TODO rewrite filter to return only section names
            if words:
                sectionList.append((i, words[0][1]))

        return sectionList

    def parse(self, textlines: list):
        """
        Parses the given text

        Parameters
        ----------
        textlines : list
            The textual data to be parsed

        signalBatch: SignalBatch
            SignalBatch container to be filled with data and returned.

        Returns
        -------
        SignalBatch:
            The SignalBatch container object.

        """
        nlBatch = SignalBatch(filename=self.filename)

        # extract language directive
        # TODO rewrite to work for all directives in general
        # TODO exceptions
        nlBatch.language = self.parseDirective("language", textlines[0])
        self.language = nlBatch.language

        # retrieve the list of section with line numbers
        sectionList = self.getSectionList(textlines)

        # Iterate over section denominators and process text accordingly
        for lineNumber, section in sectionList:
            if section == g.FEATURE:
                self.parseFeature(nlBatch, lineNumber, textlines)

            elif section == g.BACKGROUND:
                self.parseBackground(nlBatch, lineNumber, textlines)

            elif section == g.SCENARIO:
                self.parseScenario(nlBatch, lineNumber, textlines)

            elif section == g.AND:
                self.parseAnd(nlBatch, lineNumber, textlines)

            elif section in self.sectionTypes and self.scenario is not None:
                self.parseScenarioSection(lineNumber, textlines, section)

        if self.scenario:
            self.finalizeScenario(nlBatch)

        return nlBatch

    def parseFile(self, inputFilePath: str):
        """
        Parameters
        ----------
        inputFilePath: str
            The full path, including filename, to the file containing the scenario batch
        """
        self.filename = os.path.basename(inputFilePath)

        with open(inputFilePath, "rt", encoding="utf-8") as file:
            lines = file.readlines()
            # remove empty lines and extra leading/trailing white space
            lines = [l.strip() for l in lines if len(l.strip()) > 0]

        return self.parse(lines)


    # virtual method, implemented in subclasses
    def parseStatement(self, statement: str):
        raise NotImplementedError()