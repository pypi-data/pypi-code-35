# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import sys
import os
import codecs
import fnmatch
import argparse


def count_words_in_file(file_path, wordcount_dict):
    print(">>counting words in file:", file_path)
    with codecs.open(file_path, "r", encoding="utf-8-sig") as f:
        contents = f.read()
        for word in contents.split():
            if word not in wordcount_dict:
                wordcount_dict[word] = 1
            else:
                wordcount_dict[word] += 1
        f.close()
    return wordcount_dict


parser = argparse.ArgumentParser()


parser.add_argument('--input', type=str, help="input file path")
parser.add_argument('--output', type=str, help="output file path")
parser.add_argument('--param', type=str)
args = parser.parse_args()

print(os.environ)
print("Hello, worldCount!")
print("Driver arguments = " + repr(sys.argv))
print("Python version = " + sys.version)

print("Environment variable: EXAMPLE_ENV_VAR value:", os.environ['EXAMPLE_ENV_VAR'])
print("Environment variable: num_iterations value:", os.environ['AML_PARAMETER_NUM_ITERATIONS'])

print("Param argument:", args.param)

print("pwd is: ")
print(os.popen("pwd").read())
print(os.popen("ls").read())

wordcount = {}

paths = os.listdir(args.input)

for path in paths:
    full_path = args.input + "/" + path
    if os.path.exists(full_path):
        if fnmatch.fnmatch(full_path, '*/file*') or fnmatch.fnmatch(full_path, '*.txt'):
            wordcount = count_words_in_file(full_path, wordcount)
        if os.path.isdir(full_path):
            files = os.listdir(full_path)
            for file in files:
                if fnmatch.fnmatch(file, '*/file*') or fnmatch.fnmatch(full_path, '*.txt'):
                    wordcount = count_words_in_file(full_path + "/" + file, wordcount)

print(">>word count results:")
print("word:\tcount:")
for word in wordcount.keys():
    print(word, "\t", wordcount[word])

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

fo.write("word:\tcount:\n")
for word in wordcount.keys():
    fo.write(word + "\t" + str(wordcount[word]) + "\n")

fo.close()
