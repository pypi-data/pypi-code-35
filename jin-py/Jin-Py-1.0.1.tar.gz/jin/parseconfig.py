import sys
from makeconfig import CONFIG_PROPERTIES

class Parser():
    """Returns a configuration object for other parts of the toolchain"""

    def __init__(self):
        try:
            with open(".jinconfig", "r") as config:
                self.config = self.parse(config.readlines())
        except IOError:
            print(".jinconfig file doesn't exist in this directory!")
            return

    def parse(self, file):
        temp_config = {}

        for n, line in enumerate(file):
            if line.startswith("#"): continue

            for index, key in enumerate(CONFIG_PROPERTIES):
                cmd = CONFIG_PROPERTIES.get(key)
                if cmd in line:
                    if line.startswith(cmd + ":"):
                        cleaned = line.split(cmd + ":", 1)[1].strip(" \n\t")
                        cleanedList = cleaned.split(" ")
                        temp_config.update({key: cleanedList})
                    else:
                        print(f"Syntax error inside .jinconfig on line {n} -> {line}")
                        sys.exit(1)

        return temp_config
