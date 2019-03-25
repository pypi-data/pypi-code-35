import os
import gherkan.utils.constants as c

from gherkan.flask_api.raw_text_to_signal import process

request = {
    "feature" : "robot R4",
    "feature_desc" : "Robot R4 je kolaborativní robot Kuka IIWA. Má za úkol finální kompletaci autíčka. Postupně mu jsou na jeho stanici XX přivezeny zkompletované součásti autíčka. Robotu je nejdříve přivezono chassi autíčka. Následuje body (korba) a jako poslední je přivezena kabina.",
    "background" : "given line is On",
    "text_raw" : "scenario Given the storage is empty when  shuttle xx is in station XY,  then robot unloads all cubes 3x2. Scenario when robot ended unloading all cubes 3x2 then robot unloads all cubes 4x2",
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