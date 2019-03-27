import os
import gherkan.utils.constants as c

from gherkan.flask_api.raw_text_to_signal import process

request = {
    "feature": "robot R4",
    "feature_desc": "Robot R4 je kolaborativní robot Kuka IIWA. Má za úkol finální kompletaci autíčka. Postupně mu jsou na jeho stanici XX přivezeny zkompletované součásti autíčka. Robotu je nejdříve přivezono chassi autíčka. Následuje body (korba) a jako poslední je přivezena kabina.",
    "background": "Pokud je linka v provozu",
    "text_raw": "scenario Pokud je sklad prázdný, když je vozíček XX ve stanici XY, Pak robot vyloží všechny kostičky 3x2. Scenario Když robot skončí vykládání kostiček 3x2  Pak robot vyloží všechny kostičky 4x2. Scenario Když robot dokončí vykládání kostiček 4x2, Pak robot vyloží všechny kostičky 6x2.",
    "language": "cs"
}


base_path = os.path.join(c.DATA_DIR, "output", "raw_out")

process(base_path, request)

nl_file_path = base_path + ".feature"
signal_file_path = base_path + "_signals.feature"

print("\n\n--- NL FILE ---")
with open(nl_file_path, "rt", encoding="utf-8") as f:
    text = f.read()
    print(text)

print("\n\n--- SIGNAL FILE ---")
with open(signal_file_path, "rt", encoding="utf-8") as f:
    text = f.read()
    print(text)