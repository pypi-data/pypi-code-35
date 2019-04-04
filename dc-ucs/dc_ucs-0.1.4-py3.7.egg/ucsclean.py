#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : ucsclean.py
@Author: donggangcj
@Date  : 2019/4/1
@Desc  : 
'''
import click

from .userhelp import clean_user


@click.command()
@click.option('--user', prompt='请输入您的用户ID', help='需要清除数据的用户ID')
@click.option('--all_users', is_flag=True,
              help='删除数据库已存在的所有用户')
def clean_dce(user, all_users):
    """"清除DCE以及数据库工具"""
    if all_users:
        clean_user(None, True)
    clean_user(user)

# if __name__ == '__main__':
#     clean_dce()
