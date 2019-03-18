#!/usr/bin/env python
import subprocess
import json
from typing import Mapping
import os
import fnmatch
import gzip
import bz2
import re
import sys
import os
def run_shell_command(cmd):
    exit_code = 0
    error_msg = ""
    try:
        out = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as err:
        exit_code = err.returncode
        error_msg = err.output
    ok = exit_code is 0
    try:
        decoded = out.decode("utf-8")
    except AttributeError:
        decoded = out
    return ok, decoded, exit_code, error_msg

def pp(obj: Mapping):
    s = json.dumps(obj, default=lambda x: str(x))
    cmd = f"echo '{s}' | python -m json.tool | pygmentize -l json -O style=paraiso-dark"
    success, output, exit_code, error_msg= run_shell_command(cmd)
    if success:
        print(output)
    else:
        print(error_msg)
    return success



def gen_find(filepat, top=None, pred=None, feeling_lucky=False, limit=999999):
    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    '''
    top = top if top is not None else os.environ['HOME']
    limit = 1 if feeling_lucky is True else limit if limit is not None else 9999999
    n = 0
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            n+=1
            fp = os.path.join(path, name)
            if pred is None:
              yield fp
            else:
                if pred(fp):
                    yield fp
            if n >= limit:
                break
        if n >= limit:
            break

import shlex
import subprocess

def gen_locate(patt, top=None, pred=None, feeling_lucky=False, max_wait=30, limit=9999999):

    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    '''
    top = top if top is not None else os.environ['HOME']
    limit = 1 if feeling_lucky is True else limit if limit is not None else 9999999
    n = 0
    pred = lambda x: True if pred is None else pred
    args = shlex.split(f"locate {patt} {top}")
    try:
        p = subprocess.check_output(args, timeout=max_wait, shell=True)
        for line in p.split(b'\n'):
            n += 1
            fp = line.decode("utf-8")
            if pred(fp):
              yield fp
            if n >= limit:
                break
    except subprocess.TimeoutExpired as e:
        print(f"Timed out: {e} (Max wait={max_wait})")
    except Exception as e:
        print(f"Got an unknown error: {e}")


def gen_filter(pred, filenames):
    for filename in filenames:
        if pred(filename):
            yield filename
            
def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration.
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line



if __name__ == '__main__':

    # Example 1
    lognames = gen_find('access-log*', 'www')
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    pylines = gen_grep('(?i)python', lines)
    for line in pylines:
        print(line)

    # Example 2
    lognames = gen_find('access-log*', 'www')
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    pylines = gen_grep('(?i)python', lines)
    bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
    bytes = (int(x) for x in bytecolumn if x != '-')
    print('Total', sum(bytes))
