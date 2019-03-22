#!/usr/bin/env python
import os
import re
from utils import *
from bs4 import BeautifulSoup
# https://pyscss.readthedocs.io/en/latest/python-api.html
from scss import Compiler

class WatchMySASS:
    def __init__(self, argDict):
        self.html = ''
        self.argDict = argDict
        self.paths = []
        self.rules = self.argDict["rules"]
        self.destructive = self.argDict["destructive"]
        self.uncompressed = self.argDict["uncompressed"]
        self.files = self.concatFilePaths(self.rules)
        self.main()

    # Loop through rules and concatenate into absolute paths
    def concatFilePaths(self, rules):
        temp = []
        for rule in rules:
            key = rule.keys()[0]
            # Concat and add to files
            if rule[key] != '*':
                abs = '/'.join([key, rule[key]])
                temp.append(abs)
            # Otherwise add path to paths
            else:
                self.paths.append(key)
        return temp

    # If file isn't a -compiled.html pass it to the program
    def checkAndCompile(self, file):
        iFile = os.path.split(file)[1]
        iFName = iFile.split('.')[0].split('-')[-1]
        if iFName != 'compiled':
            print('\nCompiling %s...' % file)
            self.parseStyleTags(file)

    # Main Function - Complile SCSS and write to file
    def parseStyleTags(self, filename):
        with open(filename, 'r') as iFile:
            cfile = filename
            soup = BeautifulSoup(iFile, 'html.parser')

            # Allow both type="text/scss" and lang="scss"
            langTags = soup.find_all('style', {'lang': 'scss'})
            typeTags = soup.find_all('style', {'type': 'text/scss'})
            tags = list(set(langTags + typeTags))

            print('%s Tag(s) Found.' % len(tags))

            for tag in tags:
                _tag = tag
                _scss = self.compileSCSS(tag)
                tag.clear()
                tag.append(_scss)
                tag = self.updateStyleAttributes(tag)
                self.html = re.sub(str(_tag), str(tag), str(soup))

                if self.destructive:
                    cfile = filename
                else:
                    cfile = self.compiledFileName(filename)

        quickWrite(cfile, self.html)
        print('%s Compiled Successfully!\n' % cfile)
        return self.html

    # Compile SCSS and return CSS
    def compileSCSS(self, tag, uncompressed=False):
        compiled = Compiler().compile_string(tag.text)
        if uncompressed == False:
            compiled = stripNewLines(compiled)
        return compiled

    # Update tag attributes -> style="text/css" lang="css"
    def updateStyleAttributes(self, tag):
        tag['lang'] = 'css'
        tag['type'] = 'text/css'
        return tag

    # Create new file name '<file>-compiled.html'
    def compiledFileName(self, file):
        iPath = os.path.split(file)[0]
        iFile = os.path.split(file)[1]
        return os.path.join(iPath, iFile.split('.')[0] + '-compiled.html')

    def main(self):
        # Allow multiple directories as arguments
        for i in self.paths:

            # Recursively grab all (non-compiled).html files from directory
            # and all subdirectories and add them to the list
            self.files = list(set(self.files + searchNestedDirectories(i, '*.html')))

        # Loop through files and compile
        for file in self.files:
            self.checkAndCompile(file)
