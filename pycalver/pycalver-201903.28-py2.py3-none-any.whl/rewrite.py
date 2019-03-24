# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://gitlab.com/mbarkhau/pycalver
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""Rewrite files, updating occurences of version strings."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import io
import glob
import difflib
import logging
import typing as typ
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import pathlib2 as pl
str = getattr(builtins, 'unicode', str)
from . import parse
from . import config
from . import version
from . import patterns
log = logging.getLogger('pycalver.rewrite')


def detect_line_sep(content):
    """Parse line separator from content.

    >>> detect_line_sep('\\r\\n')
    '\\r\\n'
    >>> detect_line_sep('\\r')
    '\\r'
    >>> detect_line_sep('\\n')
    '\\n'
    >>> detect_line_sep('')
    '\\n'
    """
    if '\r\n' in content:
        return '\r\n'
    elif '\r' in content:
        return '\r'
    else:
        return '\n'


def rewrite_lines(pattern_strs, new_version, old_lines):
    """Replace occurances of pattern_strs in old_lines with new_version.

    >>> pattern_strs = ['__version__ = "{pycalver}"']
    >>> rewrite_lines(pattern_strs, "v201811.0123-beta", ['__version__ = "v201809.0002-beta"'])
    ['__version__ = "v201811.0123-beta"']

    >>> pattern_strs = ['__version__ = "{pep440_version}"']
    >>> rewrite_lines(pattern_strs, "v201811.0123-beta", ['__version__ = "201809.2b0"'])
    ['__version__ = "201811.123b0"']
    """
    new_version_nfo = version.parse_version_info(new_version)
    new_lines = old_lines[:]
    found_patterns = set()
    for m in parse.iter_matches(old_lines, pattern_strs):
        found_patterns.add(m.pattern)
        replacement = version.format_version(new_version_nfo, m.pattern)
        span_l, span_r = m.span
        new_line = m.line[:span_l] + replacement + m.line[span_r:]
        new_lines[m.lineno] = new_line
    non_matched_patterns = set(pattern_strs) - found_patterns
    if non_matched_patterns:
        for non_matched_pattern in non_matched_patterns:
            log.error("No match for pattern '{0}'".format(non_matched_pattern))
            compiled_pattern = patterns._compile_pattern(non_matched_pattern)
            log.error("Pattern compiles to regex '{0}'".format(
                compiled_pattern))
        raise ValueError('Invalid pattern(s)')
    else:
        return new_lines


RewrittenFileData = typ.NamedTuple('RewrittenFileData', [('path', str), (
    'line_sep', str), ('old_lines', typ.List[str]), ('new_lines', typ.List[
    str])])


def rfd_from_content(pattern_strs, new_version, content):
    """Rewrite pattern occurrences with version string.

    >>> pattern_strs = ['__version__ = "{pycalver}"']
    >>> content = '__version__ = "v201809.0001-alpha"'
    >>> rfd = rfd_from_content(pattern_strs, "v201809.0123", content)
    >>> rfd.new_lines
    ['__version__ = "v201809.0123"']
    """
    line_sep = detect_line_sep(content)
    old_lines = content.split(line_sep)
    new_lines = rewrite_lines(pattern_strs, new_version, old_lines)
    return RewrittenFileData('<path>', line_sep, old_lines, new_lines)


def _iter_file_paths(file_patterns):
    for globstr, pattern_strs in file_patterns.items():
        file_paths = glob.glob(globstr)
        if not any(file_paths):
            errmsg = "No files found for path/glob '{0}'".format(globstr)
            raise ValueError(errmsg)
        for file_path_str in file_paths:
            file_path = pl.Path(file_path_str)
            yield file_path, pattern_strs


def iter_rewritten(file_patterns, new_version):
    """Iterate over files with version string replaced.

    >>> file_patterns = {"src/pycalver/__init__.py": ['__version__ = "{pycalver}"']}
    >>> rewritten_datas = iter_rewritten(file_patterns, "v201809.0123")
    >>> rfd = list(rewritten_datas)[0]
    >>> assert rfd.new_lines == [
    ...     '# This file is part of the pycalver project',
    ...     '# https://gitlab.com/mbarkhau/pycalver',
    ...     '#',
    ...     '# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License',
    ...     '# SPDX-License-Identifier: MIT',
    ...     '""\"PyCalVer: CalVer for Python Packages.""\"',
    ...     '',
    ...     '__version__ = "v201809.0123"',
    ...     '',
    ... ]
    >>>
    """
    fh = None
    for file_path, pattern_strs in _iter_file_paths(file_patterns):
        with file_path.open(mode='rt', encoding='utf-8') as fh:
            content = fh.read()
        rfd = rfd_from_content(pattern_strs, new_version, content)
        yield rfd._replace(path=str(file_path))


def diff_lines(rfd):
    """Generate unified diff.

    >>> rfd = RewrittenFileData(
    ...    path      = "<path>",
    ...    line_sep  = "\\n",
    ...    old_lines = ["foo"],
    ...    new_lines = ["bar"],
    ... )
    >>> diff_lines(rfd)
    ['--- <path>', '+++ <path>', '@@ -1 +1 @@', '-foo', '+bar']
    """
    lines = difflib.unified_diff(a=rfd.old_lines, b=rfd.new_lines, lineterm
        ='', fromfile=rfd.path, tofile=rfd.path)
    return list(lines)


def diff(new_version, file_patterns):
    """Generate diffs of rewritten files.

    >>> file_patterns = {"src/pycalver/__init__.py": ['__version__ = "{pycalver}"']}
    >>> diff_str = diff("v201809.0123", file_patterns)
    >>> lines = diff_str.split("\\n")
    >>> lines[:2]
    ['--- src/pycalver/__init__.py', '+++ src/pycalver/__init__.py']
    >>> assert lines[6].startswith('-__version__ = "v2')
    >>> assert not lines[6].startswith('-__version__ = "v201809.0123"')
    >>> lines[7]
    '+__version__ = "v201809.0123"'
    """
    full_diff = ''
    fh = None
    for file_path, pattern_strs in sorted(_iter_file_paths(file_patterns)):
        with file_path.open(mode='rt', encoding='utf-8') as fh:
            content = fh.read()
        try:
            rfd = rfd_from_content(pattern_strs, new_version, content)
        except ValueError:
            errmsg = "No patterns matched for '{0}'".format(file_path)
            raise ValueError(errmsg)
        rfd = rfd._replace(path=str(file_path))
        lines = diff_lines(rfd)
        if len(lines) == 0:
            errmsg = "No patterns matched for '{0}'".format(file_path)
            raise ValueError(errmsg)
        full_diff += '\n'.join(lines) + '\n'
    full_diff = full_diff.rstrip('\n')
    return full_diff


def rewrite(new_version, file_patterns):
    """Rewrite project files, updating each with the new version."""
    fh = None
    for file_data in iter_rewritten(file_patterns, new_version):
        new_content = file_data.line_sep.join(file_data.new_lines)
        with io.open(file_data.path, mode='wt', encoding='utf-8') as fh:
            fh.write(new_content)
