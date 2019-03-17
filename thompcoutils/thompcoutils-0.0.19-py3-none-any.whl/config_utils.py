import sys
from configparser import ConfigParser, NoOptionError, NoSectionError
from thompcoutils.log_utils import get_logger
import os


class ConfigManager:
    def __init__(self, file_name, title=None, create=False):
        self.file_name = file_name
        self.config = ConfigParser()
        self.config.optionxform = str
        self.create = create
        if not create:
            self.config.read(file_name)
        self.notes = []
        self.title = title

    @staticmethod
    def missing_entry(section, entry, file_name, default_value=None):
        logger = get_logger()
        logger.debug("starting")
        if default_value is None:
            log_fn = logger.critical
            message = "Required entry"
            default_value = ""
        else:
            log_fn = logger.debug
            message = "Entry"
            if default_value == "":
                default_value = "Ignoring."
            else:
                default_value = "Using default value of (" + str(default_value) + ")"
        log_fn(message + " \"" + entry + "\" in section [" + section + "] in file: " + file_name
               + " is malformed or missing.  " + str(default_value))
        if default_value == "":
            log_fn("Exiting now")
            sys.exit()

    @staticmethod
    def _insert_note(lines, line_number, note):
        if "\n" in note:
            message = note.split("\n")
        else:
            message = note
        if type(message) == str:
            lines.insert(line_number, "# " + message + ":\n")
        else:
            for l in message[:-1]:
                lines.insert(line_number, "# " + l + "\n")
                line_number += 1
            lines.insert(line_number, "# " + message[-1] + ":\n")

    def read_entry(self, section, entry, default_value, notes=None):
        value = default_value
        if self.create:
            # noinspection PyBroadException
            try:
                self.config.add_section(section)
            except Exception:
                pass
            if notes is not None:
                self.notes.append({"section": section,
                                   "entry": entry,
                                   "notes": notes})
            self.config.set(section, entry, str(default_value))
        else:
            try:
                if type(default_value) is str:
                    value = self.config.get(section, entry)
                elif type(default_value) is int:
                    value = self.config.getint(section, entry)
                elif type(default_value) is float:
                    value = self.config.getfloat(section, entry)
                elif type(default_value) is bool:
                    value = self.config.getboolean(section, entry)
                else:
                    print("type not handled for ()".format(default_value))
            except (NoSectionError, NoOptionError):
                ConfigManager.missing_entry(section, entry, self.file_name, default_value)
        return value

    def read_section(self, section, default_entries, notes=None):
        key_values = default_entries
        if self.create:
            # noinspection PyBroadException
            try:
                self.config.add_section(section)
            except Exception:
                pass
            for entry in default_entries:
                self.config.set(section, str(entry), str(default_entries[entry]))
            if notes is not None:
                self.notes.append({"section": section,
                                   "entry": None,
                                   "notes": notes})
        else:
            key_values = dict()
            for (key, val) in self.config.items(section):
                key_values[key] = val
        return key_values

    def write(self, out_file):
        if os.path.isfile(out_file):
            print("File {} exists!  You must remove it before running this".format(out_file))
            # sys.exit()
        f = open(out_file, "w")
        self.config.write(f)
        f.close()
        f = open(out_file)
        lines = f.readlines()
        f.close()
        if self.title is not None:
            ConfigManager._insert_note(lines, 0, self.title)
        for note in self.notes:
            in_section = False
            line_number = 0
            for line in lines:
                if "[" + note["section"] + "]" in line:
                    if note["entry"] is None:
                        ConfigManager._insert_note(lines, line_number, note["notes"])
                        break
                    else:
                        in_section = True
                elif line.startswith("[") and line.endswith("]"):
                    in_section = False
                if in_section:
                    if line.startswith(note["entry"]):
                        ConfigManager._insert_note(lines, line_number, note["notes"])
                        break
                line_number += 1
        f = open(out_file, "w")
        contents = "".join(lines)
        f.write(contents)
        f.close()
        print("Done writing {}".format(out_file))
        sys.exit()


def main():
    write = True  # set this to True to create the ini file
    cfg_mgr = ConfigManager("test.ini", "This is the title of the ini file\n"
                                        "You can have multiple lines if you use line breaks", write)
    first = cfg_mgr.read_entry("User 1", "first name", "Joe", "This is the first name")
    last = cfg_mgr.read_entry("User 1", "last name", "Brown", "This is the last name")
    age = cfg_mgr.read_entry("User 1", "age", 12)
    is_male = cfg_mgr.read_entry("User 1", "male", True)
    weight = cfg_mgr.read_entry("User 1", "weight", 23.5)
    section = cfg_mgr.read_section("user 2", {"first name": "Sally",
                                              "last name": "Jones",
                                              "age": 15,
                                              "is_male": False,
                                              "weight": 41.3},
                                   "You only get to add notes at the top of the section using this method")

    print(first)
    print(last)
    print(age)
    print(is_male)
    print(weight)
    print(section)

    if write:
        cfg_mgr.write("another.ini")


if __name__ == "__main__":
    main()
