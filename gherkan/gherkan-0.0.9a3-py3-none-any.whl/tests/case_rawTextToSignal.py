import os
import gherkan.utils.constants as c

from gherkan.flask_api.raw_text_to_signal import process

request = {
    "feature" : "robot R1",
    "feature_desc" : "lorem ipsum",
    "background" : "given Line is On",
    "text_raw" : "scenario As soon as shuttle XY is in the station ZX, then robot r1 picks "
                 "up cube one. scenario when robot r3 picks up cube one, robot r2 assembles the product.",
    "language" : "en"
}
base_path = os.path.join(c.DATA_DIR, "output", "raw_out")

process(base_path, request)

nl_file_path = base_path + ".feature"
signal_file_path = base_path + "_signals.feature"

print("\n\n--- NL FILE ---")
with open(nl_file_path, "rt") as f:
    text = f.read()
    print(text)

print("\n\n--- SIGNAL FILE ---")
with open(signal_file_path, "rt") as f:
    text = f.read()
    print(text)