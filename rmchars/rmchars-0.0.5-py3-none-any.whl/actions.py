"""
Copyright (c) 2018, Toby Slight. All rights reserved.
ISC License (ISCL) - see LICENSE file for details.
"""
import os
from yorn import ask


def rename(oldpath, newpath):
    """
    Print and rename oldpath to newpath
    """
    print("RENAMING: {} to {}".format(oldpath, newpath))
    os.rename(oldpath, newpath)


def interactive(oldpath, newpath):
    """
    Ask before running rename_path function
    """
    question = "Would you like to rename " + \
        oldpath + " to " + newpath + " ? "
    if ask(question):
        rename(oldpath, newpath)


def dryrun(oldpath, newpath):
    """
    Print oldpath and newpath
    """
    print("TESTING: {} to {}".format(oldpath, newpath))
