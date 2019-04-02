#! /Users/xiaotian/anaconda3/bin/python3.6
# #coding:utf-8

import re

def argument(args, shortParaList, longParaList):

    # args 应该是一个列表

    try:
        # 形成正则表达式
        reg = r'-[' + shortParaList + ']'
        for p in longParaList:
            reg += r'|--' + p
        reg = '(?:' + reg + ')(?=\s|$)'
        args = ' '.join(args).split(' ')
        # 组合 args
        i = 0
        arg = ''
        for a in args:
            if re.search(reg, a):
                break
            else:
                arg += ' ' + a
                i += 1
        arg = arg[1:] # 去掉第一个空格
        
        # 组合后面的参数
        k = ''
        v = ''
        opts = {}
        for a in args[i:]:
            if re.search(reg, a):
                if k != '': # k 已经定义了
                    opts[k] = '' if v == '' else v[1:]
                k = a
                v = ''
            else:
                v += ' ' + a
        opts[k] = '' if v == '' else v[1:] # 最后一个参数
        args = arg

        return args, opts

    except:
        return None, None