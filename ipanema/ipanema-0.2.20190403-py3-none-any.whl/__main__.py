from __future__ import print_function
from ipanema import query_language
import sys

if len(sys.argv) > 1:
    print(repr(query_language(sys.argv[1])))
