#! /usr/bin/env python3

"""
Neulang: Executable org-formatted pseudocode embedded in Python.
Usage:
    neu [options] [<file>|(-c <command>)|-]  [(-d <areas>)] [(-o <org-path>)] [-m=<modules>]

-v, --version   Print version info.
-i              Open interpreter after executing command. [TODO]
-o, --org-path  Internal traversal path as list of regexes or indices, using sed format (works with <file>).
-m              List of modules to import, using bash format. [TODO]
-d, --debug     Enable debugging mode for areas (astir|resolver|pyexpr_r|regex_r|core|main|base|air_*|...).
"""


import traceback as tb
import pdb

import sys
import json
from os.path import exists, join, dirname

try:
    from docopt import docopt

except:
    # likely just installing
    pass

from .core import Neulang


__all__ = ("__meta__", "__version__", "run")
meta_file = join(dirname(__file__), "meta.json")
if not exists(meta_file):
    open(meta_file, "w").write("{}")
__meta__ = json.load(open(meta_file))
__author__ = __meta__.get("author", "skeledrew")
__version__ = __meta__.get("version", "0.1.0")


def _run():
    # catch assert errors

    try:
        run()

    except AssertionError as ae:
        tb.print_exc()
        pdb.post_mortem()
        sys.exit(1)
    return


def run():
    opt = docopt(__doc__)
    debug = opt.get("<areas>") if opt.get("--debug") else ""
    if opt.get("--debug") and not debug:
        debug = "main"
    if "main" in debug:
        pdb.set_trace()
    src_file = opt.get("<file>") or ""
    q_cmd = opt.get("<command>") if opt.get("-c") else None
    org_path = opt.get("<org-path>") if opt.get("--org-path") else ""
    org_path = (
        org_path.split(org_path[1])[1:]
        if org_path.startswith("s") and len(org_path) > 2
        else None
    )
    neulang = Neulang(debug)

    if not any(list(opt.values())):
        # nothing passed
        print(f"Neulang {__version__}")
        print('Type "air_quit" or "air_exit" to quit, ...\n')

        while True:
            # ultra-basic interpreter
            inp = input("* ")
            if inp.strip() in ["air_quit", "air_exit"]:
                break
            if not inp.startswith("* "):
                inp = f"* {inp}"
            neulang.loads(inp)
            neulang.eval()

    elif src_file:
        # source file
        neulang.org_path(org_path)
        neulang.load(src_file)
        neulang.eval()

    elif q_cmd:
        # quoted string command
        if not q_cmd.startswith("* "):
            q_cmd = f"* {q_cmd}"
        neulang.loads(q_cmd)
        neulang.eval()

    elif opt.get("--version", None):
        print(f"Neulang {__version__}")
    return


if __name__ == "__main__":
    run()
