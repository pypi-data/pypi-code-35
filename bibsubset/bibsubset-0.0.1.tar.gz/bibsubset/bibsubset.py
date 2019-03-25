
import argparse
import re

import bibtexparser

bibtex_key_regex = re.compile(r"\b(\w+)\b")

def main():
    ap = argparse.ArgumentParser(
        description="Extract a subset of entries from bibtex libraries.")
    ap.add_argument("--library", "-l", action="append",
                    help="Library(ies) to take entries from.")
    ap.add_argument("--input", '-i', required=True, help="Input bib file.")
    ap.add_argument("--output", '-o', required=True, help="Output bib file.")
    ap.add_argument("--keys", '-k', action="append", help=
                    "File(s) containing bibtex key list on which to operate. "
                    "Non-alphanumeric symbols are ignored. Hint: you can "
                    "pass your tex or lyx file here and it will be "
                    "(stupidly) scanned for references.")
    ap.add_argument("--update", "-u", action='store_true',
                    help="Refresh existing entries.")
    ap.add_argument("--exclude-field", action="append", help=
                    "Field(s) to exclude, e.g., 'abstract'.")
    A = ap.parse_args()

    if not A.library:
        A.library = []

    if not A.exclude_field:
        A.exclude_field = []
    excluded_fields = set(s.lower() for s in A.exclude_field)

    def loadbib(filename):
        parser = bibtexparser.bparser.BibTexParser(
            common_strings=True,
            ignore_nonstandard_types=False)
        with open(filename, 'rt') as file:
            return bibtexparser.load(file, parser=parser)

    libraries = {filename: loadbib(filename) for filename in A.library}

    key_to_entry_dict = {}
    for filename, bib in libraries.items():
        for entry in bib.entries:
            for field in set(entry.keys()):
                if field.lower() in excluded_fields:
                    del entry[field]
            key_to_entry_dict.setdefault(
                entry["ID"], {
                    "filename": filename,
                    "entry": entry})

    key_to_operate_on = []
    key_to_operate_on_set = set()
    for keyfile in A.keys:
        with open(keyfile, 'rt') as file:
            for line in file:
                for word in bibtex_key_regex.findall(line):
                    if word not in key_to_entry_dict:
                        continue # not a bibtex key that we know of
                    if word not in key_to_operate_on_set:
                        key_to_operate_on_set.add(word)
                        key_to_operate_on.append(word)

    input_bib = loadbib(A.input)

    input_bib_entries_dict = input_bib.entries_dict

    for key in key_to_operate_on:
        d = key_to_entry_dict.get(key)
        if d is None:
            continue
        entry = d['entry']
        existing_entry = input_bib_entries_dict.get(key, None)
        if existing_entry is None:
            input_bib.entries.append(entry)
        else:
            if A.update:
                existing_entry.clear()
                existing_entry.update(entry)

    writer = bibtexparser.bwriter.BibTexWriter()
    writer.order_entries_by = None
    writer.contents = ['preambles', 'comments', 'entries']
    # writer.indent = '  '
    # writer.order_entries_by = ('ENTRYTYPE', 'author', 'year')
    bibtex_str = bibtexparser.dumps(input_bib, writer)
    with open(A.output, 'wt') as file:
        file.write(bibtex_str)


if __name__ == '__main__':
    main()


