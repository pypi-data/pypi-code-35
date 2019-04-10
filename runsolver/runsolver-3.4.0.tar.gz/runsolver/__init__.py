#!/usr/bin/env python

import os
import sys
import subprocess


def run():
    runsolver = os.path.join(os.path.dirname(__file__), "runsolver", "runsolver")
    return subprocess.call([runsolver, *sys.argv[1:]])


if __name__ == "__main__":
    run()
