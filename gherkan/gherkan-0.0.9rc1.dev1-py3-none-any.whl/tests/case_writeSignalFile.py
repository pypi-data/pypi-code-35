from gherkan.decoder.NLParser import NLParser
from gherkan.encoder.SignalFileWriter import SignalFileWriter
import importlib
import os

import gherkan.utils.constants as c

# Path to the text file with the signal batch
input_path = os.path.join(c.DATA_DIR, 'input')
output_path = os.path.join(c.DATA_DIR, 'output')
input_file = os.path.join(input_path, 'R1NormalSequenceE.feature')
output_file = os.path.join(output_path, 'R1NormalSequence_signals.feature')

nlFile = NLParser()
# Parse the entire file
nlBatch = nlFile.parseFile(input_file)

signalFileWriter = SignalFileWriter(nlBatch)
signalFileWriter.write(output_file)

