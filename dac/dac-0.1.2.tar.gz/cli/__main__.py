#!/usr/bin/env python

"""
dac - Documentation as Code

Usage:
  dac render <file> [--tpl=<tpl>] [--output=<output>]
  dac debug <file> [--props=<props>]
  
  dac (-v | --version)

Options:
  -s --silent           Reduce verbosity
  -h --help             Show this screen.
  -v --version          Show version.
  -f --file=<file>      The dac file to render.
  -o --output=<output>  The output path.
"""

from docopt import docopt
from .utils import *

def main():
    arguments = docopt(__doc__, version="0.1.0")
    c = Commander(arguments)
    c.run()

if __name__ == "__main__":
    main()