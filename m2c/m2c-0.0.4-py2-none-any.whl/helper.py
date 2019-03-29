#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2018.11.28
 
import os

def assert_error(exp, msg, lineno, line):
    if exp:
        return
    err = 'line(%s): %s, error: %s' % (lineno, line, msg)
    raise Exception(err)

def writeCode(path, code):
    os.system('mkdir -p %s' % os.path.dirname(path))
    with open(path, 'wb') as f:
        f.write(code)

def appendCode(path, code):
    os.system('mkdir -p %s' % os.path.dirname(path))
    with open(path, 'ab') as f:
        f.write(code)

def getCodeFuncs(path):
    funcs = []
    for line in open(path, 'rb'):
        line = line.strip()
        if not line.startswith('func '):
            continue
        
        item, _ = line.split('(', 1)
        items = item.split()
        if len(items) != 2:
            print '无效的函数定义:%s' % line
            continue
        funcs.append(items[1])
    return funcs

def upperFirst(s):
    if len(s) in (0, 1):
        return s
    return s[0].upper() + s[1:]
