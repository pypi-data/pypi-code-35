"""
Copyright (c) 2018, Toby Slight. All rights reserved.
ISC License (ISCL) - see LICENSE file for details.
"""
import os

if os.name == 'nt':
    CHARS = ['/', '"', ':', '<', '>', '^', '|', '*', '?']
else:
    CHARS = ['\\', '"', ':', '<', '>', '^', '|', '*', '?']


def mknames(name):
    """
    Iterate over char array to to build names with invalid chars.
    """
    names = []
    for i in enumerate(CHARS):
        n, c = i
        newname = name + str(n)
        newname = c + " . " + "😇" + newname
        newname = newname + "😠" + " . " + c
        newname = " . " + newname + " . "
        names.append(newname)
    return names


def mknodes(path):
    """
    Use returned arrays from mknames to instantiate new filesystem nodes.
    """
    dirs = mknames("testdir")
    files = mknames("testfile")

    for d in dirs:
        dirpath = os.path.join(path, d)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
    for f in files:
        filepath = os.path.join(path, f)
        if not os.path.exists(filepath):
            open(filepath, 'a').close()


def create(path, count, limit):
    """
    Descend into directories to create children of specified depth.
    """
    mknodes(path)
    for root, dirs, files in os.walk(path):
        if limit < 5:  # creates depth level recursively in all directories....
            if count < limit:
                count = count + 1
                for d in dirs:
                    create(os.path.join(root, d), count, limit)
        # if more than 4, limit to one directory, as it will take too long...
        else:
            if count < limit:
                count = count + 1
                create(root, count, limit)
