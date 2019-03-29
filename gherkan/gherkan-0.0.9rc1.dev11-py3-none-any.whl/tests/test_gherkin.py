from gherkin.parser import Parser
from gherkin.pickles.compiler import compile

from pprint import pprint as pp


# requires 'gherkin-official' package
parser = Parser()
input_file = "/windows/Soubory/Projekty/CIIRC/nl_instruction_processing/data/output/case_SignalParser_signals.feature"

with open(input_file, "rt", encoding="utf-8") as file:
    lines = file.read()

    gherkin_document = parser.parse(lines)
    pickles = compile(gherkin_document)

    pp(pickles)