#!/usr/bin/env python

import sys
def signal_handler(sig, frame):
    sys.exit(0)

class GCPEXCEPTION(Exception): pass

