
import os
import gherkan.utils.constants as c
from gherkan.flask_api.signal_to_nl import process

# Path to the text file with the signal batch

dir = os.path.join(c.DATA_DIR, 'output')
input_file = os.path.join(dir, 'case_SignalParser_signals.feature')

# saves automatically to file without the "_signals" suffix
process(input_file)

output_file = input_file.replace("_signals", "")

with open(output_file, "rt", encoding="utf-8") as f:
    text = f.read()
    print(text)
