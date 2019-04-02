"""
Copyright (c) 2018, Toby Slight. All rights reserved.
ISC License (ISCL) - see LICENSE file for details.
"""
import os
import unicodedata

CHARS = ["\\", "/", "\"", ":", "<", ">", "^", "|", "*", "?"]
# http://www.unicode.org/reports/tr44/#GC_Values_Table
UCHARS = ["Lo", "So", "Cc"]  # Other_Letter, Other_Symbol, Control_Character


def replace_chars(name):
    """
    iterate over & delete invalid characters in name.
    """
    for char in name:
        if char in CHARS:
            name = name.replace(char, "")
        # https://stackoverflow.com/a/19016117
        if unicodedata.category(char) in UCHARS:
            name = name.replace(char, "")
        if name.endswith("."):
            name = name[:-1]  # remove last char
        name = name.strip()  # remove leading and trailing spaces
    return name


def is_invalid(name):
    """
    Checks if any of invalid chars are present in name of the node and returns
    true if they are.
    """
    # https://stackoverflow.com/a/5858943
    char = any(c in CHARS for c in name)
    uchar = any(unicodedata.category(c) in UCHARS for c in name)
    invalid = char or uchar
    return invalid


def get_paths(root, name):
    """
    If is_invalid returns true get a new name using replace_chars
    """
    oldpath = os.path.join(root, name)
    newpath = os.path.join(root, replace_chars(name))
    return (oldpath, newpath)
