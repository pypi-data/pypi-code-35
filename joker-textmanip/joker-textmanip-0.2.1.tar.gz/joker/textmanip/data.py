#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import functools

from joker.cast import cache_lookup
from joker.default import under_package_dir

import joker.textmanip
from joker.textmanip.tabular import nonblank_lines_of

# const cache
_const_cache = {}


def const_getter(func):
    return functools.wraps(func)(
        lambda: cache_lookup(_const_cache, func, func)
    )


def const_lookup(func):
    return functools.wraps(func)(
        lambda *args: cache_lookup(_const_cache, (func, args), func, *args)
    )


def _locate(name):
    return under_package_dir(joker.textmanip, 'asset', name)


@const_getter
def get_unicode_blocks():
    path = _locate('unicode_blocks.txt')
    results = []
    for line in nonblank_lines_of(path):
        head, tail, title = line.split(None, 2)
        head = int(head, base=0)
        tail = int(tail, base=0)
        results.append((head, tail, title))


def search_unicode_blocks(pattern):
    import re
    regex = re.compile(pattern)
    blocks = []
    for tup in get_unicode_blocks:
        if regex.search(tup[2]):
            blocks.append(tup)
    return blocks


def blocks_to_name_tuple_map(blocks=None):
    if blocks is None:
        blocks = get_unicode_blocks()
    return {tu[2]: tuple(tu[:2]) for tu in blocks}


@const_getter
def get_all_encodings():
    return list(nonblank_lines_of(_locate('encodings.txt')))


@const_lookup
def get_most_frequent_characters(lang='sc'):
    path = 'asset/mfc-{}.txt'.format(lang)
    path = under_package_dir(joker.textmanip, path)
    return ''.join(nonblank_lines_of(path))
