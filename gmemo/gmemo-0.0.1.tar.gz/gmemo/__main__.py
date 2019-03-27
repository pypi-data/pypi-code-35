# -*- coding:utf-8 -*-
import sys

from .gmemo_ic import main as ic_main
from .gmemo_cl import main as cl_main

def main(argv=sys.argv):
    if len(argv) > 1:
        cl_main(argv=argv)
    else:
        ic_main()