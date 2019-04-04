#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
# Author: yuyongpeng@hotmail.com
# Description:
#  

"""
import datetime
from oracle import tasks
from celery import chain

def test_celery():
    # a = tasks.test2.apply_async((2,), link=tasks.test.si(2))
    # print(a.get())
    tk = tasks.add.apply_async((2,2), link=tasks.add.s(3))
    print(tk.get())
    # res = chain(tasks.add.s(2,2), tasks.add.s(2))
    # print(res.get())




if __name__ == '__main__':
    # # 修改celery的配置
    # from oracle.tasks import app
    # app.conf.update(
    #     result_backend='redis://127.0.0.1:6379/1',
    #     broker_url='redis://127.0.0.1:6379/1',
    # )
    # test_celery()
    # # app.star()

    test_iv()