from gherkan.decoder.NLParser import NLParser
from gherkan.encoder.SignalFileWriter import SignalFileWriter
import importlib
import os

import gherkan.utils.constants as c

# Path to the text file with the signal batch
input_path = os.path.join(c.DATA_DIR, 'output')
output_path = os.path.join(c.DATA_DIR, 'output')
input_file = os.path.join(input_path, 'case_NLParser.feature')
output_file = os.path.join(output_path, 'case_NLParser_signals.feature')

nlFile = NLParser()
# Parse the entire file
nlBatch = nlFile.parseFile(input_file)

signalFileWriter = SignalFileWriter(nlBatch)
signalFileWriter.write(output_file)

with open(output_file, "rt", encoding="utf-8") as f:
    text = f.read()
    print(text)
