#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-3-22'
"""
from .BaiduPost import BaiduPost
from gensim.models import FastText
model = FastText.load_fasttext_format('/home/yuanjie/desktop/Corpus/fast_text.model.bin')


