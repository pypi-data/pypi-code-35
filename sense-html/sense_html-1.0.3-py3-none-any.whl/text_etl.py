#!/usr/bin/env python
# -*- coding: utf-8 -*-

#                                                           
# Copyright (C)2017 SenseDeal AI, Inc. All Rights Reserved  
#                                                           

"""                                                   
File: text_etl.py
Author: lzl
E-mail: zll@sensedeal.ai
Last modified: 2019/4/4
Description:                                              
"""

from lxml import etree
import re


def is_blank(text):
    """
    Determine the line is blank or not.
    If `True`, the line is blank.
    """
    if len(text.strip()) == 0:
        return True
    return False


def is_short_line(text, threshold):
    """
    Determine whether the line is shorter than threshold.
    If `True`, the line is shorter than threshold.
    """
    if len(text.strip()) <= int(threshold):
        return True
    return False


def has_end_punc(text):
    """
    Determine whether the line ends with certain punctuations.
    If `True`, the line ends with other characters.
    """
    end = text.strip()[-1]
    punc = ['：', ';', '。', '？', '！', '；', '”']
    if end not in punc:
        return True
    return False


def remove_tails(text):
    """
    Remove the unnecessary text with certain key words.
    If `True`, the line should be removed.
    """
    keywords = ['文章来源：', '责任编辑：', '责编', '原标题：', '注：', '仅供参考', '作者：',
                '来源：', '文章关键词：', '记者 ', '记者：', '本文', '文/', '编辑', '校对']
    for word in keywords:
        if word in text:
            return True
    return False


def remove_general(text):
    """
    Remove the unnecessary text in disclosure.
    If `True`, the line should be removed.
    """
    keywords = ['证券简称', '公告编号', '虚假记载', '重大遗漏', '【活动报名】',
                '免责声明', '点击量', '仅代表', '如有侵权', '采编', '证券之星', '查看更多']
    for word in keywords:
        if word in text:
            return True
    return False


def remove_src(text):
    """
    Remove the news source from the text, only context returned.
    """
    text = str(text).strip()
    keywords = ['讯：', '讯:', '讯 ', '讯，', '消息 ', '消息:', '消息：', '报道：', '报道:', '报道 ']
    for word in keywords:
        if text.find(word) != -1:
            index = text.index(word)
            text = text[index + len(word):]
            break

    idx = -1
    if text.startswith('('):
        idx = text.index(')')
    elif text.startswith('（'):
        idx = text.index('）')
    text = text[idx + 1:]

    idx = -1
    if '讯(' in text:
        idx = text.index(')')
    elif '讯（' in text:
        idx = text.index('）')
    text = text[idx + 1:]

    return text.strip()


# 处理两种格式的数据
def get_text(html):
    if '<p' in html:
        try:
            html = etree.HTML(html)
            ps = html.xpath("//p")
            text = ''
            for p in ps:
                line = ''
                for l in p.xpath("string(.)").split('\n'):
                    line += l.strip()
                if len(line) >= 1:
                    text += line
                    if line[-1] not in ['，', ',']:
                        text += '\n'
            return re.sub('<.*?>', '', text)
        except Exception as ex:
            pass
    html = re.sub('<.*?>', '', html)
    return html


# 文本处理
def handle_text(context, threshold=8):
    context = get_text(context)
    temp = []
    for line in context.split('\n'):
        if is_blank(line):
            continue
        if is_short_line(line, threshold):
            continue
        if has_end_punc(line):
            continue
        if remove_general(line):
            continue
        temp.append(line.strip())

    if not temp:
        return context

    head = temp[0]
    if len(temp) > 3:
        middle = temp[1: -3]
        tails = temp[-3:]
    else:
        middle = []
        tails = temp[1:]

    new_head = remove_src(head)
    new_tail = []
    for tail in tails:
        if remove_tails(tail):
            continue
        new_tail.append(tail)

    res = [new_head] + middle + new_tail
    return '\n'.join(res)
