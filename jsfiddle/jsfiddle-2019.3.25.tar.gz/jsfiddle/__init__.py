#!/usr/bin/env python
import jsfiddle.details
import github_name
import os
import public


def gitroot():
    path = os.getcwd()
    while path and len(path) > 1:
        if os.path.exists(os.path.join(path, ".git")):
            return path
        path = os.path.dirname(path)


@public.add
def github_tree():
    """return `github_tree` string. git remote required"""
    root = gitroot()
    if not root:
        return ""
    fullname = github_name.get()
    relpath = os.path.relpath(os.getcwd(), root)
    return os.path.join(fullname, relpath)


@public.add
def url():
    """return `https://jsfiddle.net/gh/get/library/pure/{github_tree}/` string"""
    _github_tree = github_tree()
    if not _github_tree:
        return ""
    return "https://jsfiddle.net/gh/get/library/pure/%s/" % _github_tree
