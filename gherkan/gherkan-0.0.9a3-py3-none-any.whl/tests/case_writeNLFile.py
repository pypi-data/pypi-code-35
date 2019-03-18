
import os
import gherkan.utils.constants as c
from gherkan.flask_api.signal_to_nl import process

# Path to the text file with the signal batch

dir = os.path.join(c.DATA_DIR, 'output')
input_file = os.path.join(dir, 'case_R1NormalSequence2_signals.feature')

process(input_file)

output_file = os.path.join(dir, 'case_R1NormalSequence2.feature')

with open(output_file, "rt") as f:
    text = f.read()
    print(text)