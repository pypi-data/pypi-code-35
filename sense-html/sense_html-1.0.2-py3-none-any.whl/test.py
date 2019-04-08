#!/usr/bin/env python
# -*- coding: utf-8 -*-

#                                                           
# Copyright (C)2017 SenseDeal AI, Inc. All Rights Reserved  
#                                                           

"""                                                   
File: test.py
Author: lzl
E-mail: zll@sensedeal.ai
Last modified: 2019/4/8
Description:                                              
"""
from sense_html.text_etl import handle_text


def test_content():
    in_file = './demo.html'
    with open(in_file, 'r') as f:
        content = f.read()

    print(content)
    print('\n')
    res = handle_text(content)
    print(res)


def test_div():
    print(handle_text(
        """<div>在传出监管层将对分拆上市松绑的消息后，首家拟分拆上市的案例出炉。东港股份8日盘后公告称，控股子公司东港瑞云拟进行股份制改革，为了将申请登陆科创板公告称，控股子公司东港瑞云拟股份制改制并整体变更设立股份有限公司，更名为东港瑞云数据技术股份有限公司。股份制改制的目的为充分利用资本市场的新政策，在符合单独上市条件时，申请在国内a股单独上市融资，优先考虑在科创板申请上市，以拓展东港瑞云融资渠道，为未来档案项目的发展奠定良好的基础，推动该业务更好地发展。此外，通过股份制改制，进一步完善公司治理结构，扩大市场影响力，推进东港瑞云快速发展。</div>"""))
