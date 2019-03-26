#! /usr/bin/env python

import re
import json
import sys
import argparse

from pandocfilters import toJSONFilter, get_value, Str, Para, Plain, OrderedList, Space

references = []

parser = argparse.ArgumentParser(description='Pandoc filter for simple citations.')
parser.add_argument('cfg')
args = parser.parse_args()

with open(args.cfg) as json_file:
    references = json.load(json_file)

def build_references():
    refs = []
    for r in references:
        refs.append(Para([Str("[" + r.get("citationId") + "] " + r.get("description"))]))

    return refs

def pandoc_simplecite(key, value, format, _):
    if key == 'Cite':
        citationId = value[0][0].get("citationId")
        m = re.search(r'ref:(\d)', citationId)
        if m:
            return Str("[" + m.group(1) + "]")

    if key == "Para":
        if len(value) > 4 and value[0].get("c") == "{" and value[2].get("c") == ":::refs" and value[4].get("c") == "}":
            return build_references()

def main():
    toJSONFilter(pandoc_simplecite)
    sys.stdout.flush()

if __name__ == "__main__":
    main()