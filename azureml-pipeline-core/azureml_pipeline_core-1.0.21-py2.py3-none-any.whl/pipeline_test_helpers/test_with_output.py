# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import sys
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--output', type=str, help="output file path")
args = parser.parse_args()

print(os.environ)
print("Driver arguments = " + repr(sys.argv))
print("Python version = " + sys.version)

print(">>creating output")
if args.output is not None and args.output is not '':
    output_dir = args.output
else:
    output_dir = '.'
filename = output_dir + "/output_test.txt"

print("output path:", filename)

if output_dir != '.' and not os.path.exists(filename):
    os.makedirs(os.path.dirname(filename))

fo = open(filename, 'w+')

fo.write("sample output created by test script")

fo.close()
