import enum
import os
import sqlite3


class LocalizedNames:
    def __init__(self, localized_name: str, chapter_descriptor: str):
        self.localized_name = localized_name
        self.chapter_descriptor = chapter_descriptor


def __load_data():
    """Loads the basic set of data as dictionaries.

    This ensures that all lookups are lightning fast and we don't need to mess with SQLite thread safety
    """
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "db.sqlite"))

    cur = conn.cursor()
    cur.execute("SELECT osis_id, paratext_abbreviation FROM canonical_books")

    id_mappings = {row[0]: row[1] for row in cur}

    cur.execute("SELECT osis_id, language_code, localized_name, chapter_descriptor FROM localized_names")

    data_mappings = {}
    for row in cur:
        osis_id, language_code, localized_name, chapter_descriptor = row
        if osis_id not in data_mappings:
            data_mappings[osis_id] = {}

        data_mappings[osis_id][language_code] = LocalizedNames(localized_name, chapter_descriptor)

    conn.close()

    return id_mappings, data_mappings


def __fix_identifier(ident: str) -> str:
    """Fixes identifiers not starting with an integer by adding an _ prefix."""
    return ident if ident[0].isalpha() else f"_{ident}"


_id_to_paratext_mappings, _localized_name_mappings = __load_data()
_paratext_to_id_mappings = {value: key for key, value in _id_to_paratext_mappings.items()}


# Generate the enum programmatically
OSISBook = enum.Enum("OSISBook", [(__fix_identifier(key), key) for key in _id_to_paratext_mappings])


def __from_paratext(paratext: str) -> OSISBook:
    return OSISBook(_paratext_to_id_mappings[paratext])


@property
def __paratext_abbreviation(self: OSISBook) -> str:
    return _id_to_paratext_mappings[self.value]


def __localized_name(self: OSISBook, lang_code: str) -> str:
    result = _localized_name_mappings[self.value].get(lang_code)
    return result.localized_name if result else None


def __chapter_descriptor(self: OSISBook, lang_code: str) -> str:
    result = _localized_name_mappings[self.value].get(lang_code)
    return result.chapter_descriptor if result else None


OSISBook.from_paratext = staticmethod(__from_paratext)
OSISBook.paratext_abbreviation = __paratext_abbreviation
OSISBook.localized_name = __localized_name
OSISBook.chapter_descriptor = __chapter_descriptor
