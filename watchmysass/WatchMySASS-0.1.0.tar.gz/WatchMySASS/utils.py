import re
import os
import argparse
from glob import glob

def readFile(fName, printAfter = False):
    f = open(fName,'r')
    if f.mode == 'r':
        contents = f.read()
        if printAfter == True:
            print(contents)
        return contents
    else:
        print('File %s not found.' % fName)

def quickWrite(fName, string, printAfter = False):
    f = open(fName, 'w+') # w+ creates file if not found
    f.write(string)
    f.close()
    if printAfter == True:
        print(string)

def stripNewLines(str):
    stripped = re.sub('\s\s+', ' ', str)
    return stripped

# Recursively grab all specified file extensions from directory and all subdirectories
def searchNestedDirectories(_path, extensions):
    PATH = os.path.abspath(_path)
    matches = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], extensions))]
    return list(set(matches))

# Handle system arguments when the program is called
def handleArgs():
    temp = []
    rules = []

    # Get the directory to parse
    argParser = argparse.ArgumentParser()
    argParser.add_argument("relpath", type=str, metavar="path/to/compile", help="Path(s) or File(s) to compile", nargs="*")
    # store_true is counter-intuitive
    # this means store true IF present, default is false
    argParser.add_argument("-w", "--watch", help="Continuously watch directory(s)/file(s) for changes", action="store_true")
    argParser.add_argument("-u", "--uncompressed", help="Don't minify CSS output", action="store_true")
    argParser.add_argument("-d", "--destructive", help="Save changes to original file instead of *-compiled.html", action="store_true")
    args = argParser.parse_args()

    # Account for no arguments
    if len(args.relpath) == 0:
        temp.append(os.path.abspath('.'))
        rules.append({os.path.abspath('.'): '*'})

    else:
        for p in args.relpath:
            _path, _filename = os.path.split(os.path.abspath(p))

            # Save path to the list to watch
            if _path not in temp:
                temp.append(_path)

            # If file, save path/file to the rules
            if os.path.isfile(p):
                rules.append({_path: _filename})

            # Otherwise save * as the file for the path/file rule
            else:
                rules.append({_path: '*'})

    # Set the temp list of paths as args.relpath
    args.relpath = temp
    return (args, rules)
