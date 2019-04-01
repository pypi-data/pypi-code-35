
import os
import sys
from .buche import *
from .repr import *
from .event import *
from .debug import *
from .repl import *


def _print_flush(x):
    print(x, flush=True)


def smart_breakpoint():
    if os.environ.get('BUCHE'):
        os.environ['PYTHONBREAKPOINT'] = 'buche.breakpoint'


H = hrepr.H
master = MasterBuche(hrepr, _print_flush)
buche = Buche(master, '/')
stdbuche = Buche(master, '/stdout')
reader = Reader(sys.stdin)
read = reader.read
repl = Repl(buche, reader)
breakpoint = BucheDb(repl).set_trace
